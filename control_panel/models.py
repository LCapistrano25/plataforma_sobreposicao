from django.db import models

from django.db import models

class FileManagement(models.Model):
    phytoecology_zip_file = models.FileField(
        upload_to='documents/',
        verbose_name="Documentos Fitoecologia",
        help_text="Arquivo ZIP contendo dados da Área de Fitoecologia."
    )

    environmental_protection_zip_file = models.FileField(
        upload_to='documents/',
        verbose_name="Documentos Proteção Ambiental",
        help_text="Arquivo ZIP contendo dados da Área de Proteção Ambiental."
    )

    zoning_zip_file = models.FileField(
        upload_to='documents/',
        verbose_name="Documentos Zoneamento",
        help_text="Arquivo ZIP contendo dados da Área de Zoneamento."
    )

    sicar_zip_file = models.FileField(
        upload_to='documents/',
        verbose_name="Documentos SICAR",
        help_text="Arquivo ZIP contendo dados da Área SICAR."
    )

    class Meta:
        db_table = 'tb_gerenciamento_arquivos'
        verbose_name = "Gerenciamento de Arquivos"
        verbose_name_plural = "Gerenciamento de Arquivos"

    def __str__(self):
        return f"Gerenciamento de Arquivos"
        
