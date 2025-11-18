from kernel.service.geometry_overlap_service import OverlapChecker
from typing import Any, Dict, List, Tuple, Optional
from kernel.utils import base_result, calculate_safe_overlap


class IndigenousProcess:
    def __init__(self, verifier: OverlapChecker):
        """Inicializa com o verificador de sobreposição."""
        self.verifier = verifier

    def process(
        self,
        polygon_wkt: str,
        indigenous_data: List[Dict[str, Any]],
        base_name: str,
    ) -> Dict[str, Any]:
        """Processa lista de áreas de proteção ambiental e retorna estrutura padronizada para UI."""
        if not indigenous_data:
            return base_result(base_name, [], 0)

        found_areas: List[Dict[str, Any]] = []
        not_evaluated_count = 0

        for item in indigenous_data:
            multi_wkt = item.get("wkt")
            indigenous_name = item.get("NOME_AREA")
            try:
                item_result, not_eval_inc = self._process_indigenous_item(
                    polygon_wkt, multi_wkt, indigenous_name, base_name
                )
                not_evaluated_count += not_eval_inc
                if item_result is not None:
                    found_areas.append(item_result)
            except Exception:
                not_evaluated_count += 1
                continue

        return base_result(base_name, found_areas, not_evaluated_count)

    def _process_indigenous_item(
        self,
        polygon_wkt: str,
        multi_wkt: str,
        indigenous_name: str,
        base_name: str,
    ) -> Tuple[Optional[Dict[str, Any]], int]:
        """Processa um item de área de proteção ambiental e decide inclusão."""
        overlap_hectares = calculate_safe_overlap(
            self.verifier, polygon_wkt, multi_wkt
        )

        if overlap_hectares is None:
            return None, 1
        if overlap_hectares <= 0:
            return None, 0

        return (
            self._build_result_item(indigenous_name, overlap_hectares),
            0,
        )

    def _build_result_item(self, indigenous_name: str, overlap_hectares: float) -> Dict[str, Any]:
        """Monta o dicionário do item de resultado para a UI (mantém string esperada)."""
        return {
            "area": overlap_hectares,
            "item_info": f"Áreas de Proteção Ambiental: {indigenous_name}",
        }