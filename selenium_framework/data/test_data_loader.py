import json
import yaml
import pandas as pd
from typing import Any, Dict, List, Union
from pathlib import Path

class TestDataLoader:
    """Chargeur intelligent de données de test"""
    
    @staticmethod
    def load_from_json(file_path: Union[str, Path]) -> Any:
        """Charge des données depuis un fichier JSON"""
        with open(file_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    
    @staticmethod
    def load_from_yaml(file_path: Union[str, Path]) -> Any:
        """Charge des données depuis un fichier YAML"""
        with open(file_path, 'r', encoding='utf-8') as f:
            return yaml.safe_load(f)
    
    @staticmethod
    def load_from_excel(file_path: Union[str, Path], sheet_name: str = None) -> List[Dict]:
        """Charge des données depuis un fichier Excel"""
        if sheet_name:
            df = pd.read_excel(file_path, sheet_name=sheet_name)
        else:
            df = pd.read_excel(file_path)
        
        return df.to_dict('records')
    
    @staticmethod
    def load_test_scenarios(scenario_type: str) -> List[Dict]:
        """Charge des scénarios de test par type"""
        scenarios_dir = Path(__file__).parent / 'test_scenarios'
        
        # Priorité: YAML > JSON > Excel
        for ext in ['yaml', 'yml', 'json', 'xlsx']:
            file_path = scenarios_dir / f"{scenario_type}_scenarios.{ext}"
            if file_path.exists():
                if ext in ['yaml', 'yml']:
                    return TestDataLoader.load_from_yaml(file_path)
                elif ext == 'json':
                    return TestDataLoader.load_from_json(file_path)
                elif ext == 'xlsx':
                    return TestDataLoader.load_from_excel(file_path)
        
        raise FileNotFoundError(f"Aucun fichier de scénarios trouvé pour {scenario_type}")
