import geopandas as gpd
import hashlib
import json
import numpy as np
from concurrent.futures import ThreadPoolExecutor, as_completed

from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth.models import User
from django.db import connection

from car_system.models import SicarRecord


class Command(BaseCommand):
    help = "Insere registros SICAR com processamento paralelo e hash única por linha."

    def add_arguments(self, parser):
        parser.add_argument(
            "--threads",
            type=int,
            default=4,
            help="Número de threads para processamento paralelo."
        )

    def get_user(self):
        user = User.objects.first()
        if not user:
            raise CommandError("Nenhum usuário encontrado.")
        return user

    # =============================================================
    # Função executada em cada thread (processa 1 partição do DF)
    # =============================================================
    def process_partition(self, partition_df, user):
        results = []

        for _, row in partition_df.iterrows():
            formatted = self.format_data(row, user)
            formatted["hash_id"] = self.generate_hash(formatted)

            try:
                obj, created = SicarRecord.objects.get_or_create(
                    hash_id=formatted["hash_id"],
                    defaults={
                        "car_number": formatted["car_number"],
                        "status": formatted["status"],
                        "geometry": formatted["geometry"],
                        "created_by": formatted["created_by"],
                        "source": formatted["source"]
                    }
                )

                if created:
                    print(f"[CRIADO] CAR: {obj.car_number}")
                else:
                    print(f"[JÁ EXISTIA] CAR: {obj.car_number}")
                
                results.append(obj.car_number)

            except Exception as e:
                print(f"[ERRO THREAD] {e}")

        # Fecha conexão após uso
        connection.close()
        return results

    # =============================================================
    # Execução principal
    # =============================================================
    def handle(self, *args, **options):
        print("Iniciando leitura e processamento paralelo...")

        num_threads = options["threads"]
        user = self.get_user()

        archive_path = r"documents\AREA_IMOVEL.zip"
        df = gpd.read_file(archive_path, encoding="utf-8")

        print(f"Total de linhas encontradas: {len(df)}")

        # Particionar o DataFrame
        partitions = np.array_split(df, num_threads)

        all_results = []

        with ThreadPoolExecutor(max_workers=num_threads) as executor:
            futures = [
                executor.submit(self.process_partition, part, user)
                for part in partitions
            ]

            for future in as_completed(futures):
                all_results.extend(future.result())

        print("Registros inseridos:")
        for r in all_results:
            print(" →", r)

        print("Processamento concluído com sucesso.")

    # =============================================================
    # Funções auxiliares
    # =============================================================
    @staticmethod
    def format_data(row, user):
        return {
            "car_number": row.get("cod_imovel"),
            "status": row.get("ind_status"),
            "geometry": str(row.get("geometry")),
            "created_by": user,
            "source": "Base Sicar"
        }

    @staticmethod
    def generate_hash(data: dict) -> str:
        json_str = json.dumps(data, sort_keys=True, default=str)
        return hashlib.sha256(json_str.encode("utf-8")).hexdigest()
