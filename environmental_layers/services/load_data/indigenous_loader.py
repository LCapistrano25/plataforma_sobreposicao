from typing import Dict, List, Any
from environmental_layers.models import IndigenousArea


class IndigenousLoader:
    
    @staticmethod
    def load() -> List[Dict[str, Any]]:
        indigenous_areas = IndigenousArea.objects.all()
        indigenous_data = []
        
        for indigenous in indigenous_areas:
            indigenous_data.append({
                'wkt': indigenous.geometry,
                'NOME_AREA': indigenous.indigenous_name
            })
        
        return indigenous_data
