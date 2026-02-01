import re
from typing import List, Dict, Any
from app.api.models.tilda import TildaFormData


class BodyParser:
    @staticmethod
    def extract_form_data(raw_data: Dict[str, Any]) -> TildaFormData:
        return TildaFormData(**raw_data)
    
    @staticmethod
    def parse_modules_data(raw_data: Dict[str, Any]) -> Dict[str, str]:
        count_of_modules_keys = BodyParser._find_count_of_modules_keys(raw_data)

        name_of_modules_keys = []
        for module_count_key in count_of_modules_keys:
            postfix = module_count_key[1:]
            for key in raw_data.keys():
                if key != module_count_key and re.match(f'^[a-zA-Z]+{postfix}$', key):
                    name_of_modules_keys.append(key)
        
        return {
            raw_data[name_of_modules_key]: raw_data[count_of_modules_key]
            for name_of_modules_key, count_of_modules_key in zip(name_of_modules_keys, count_of_modules_keys)
        }
    
    def format_modules_data(self, modules: Dict[str, str]) -> str:
        return ', '.join([f'{key} ({value})' for key, value in modules.items()])

    @staticmethod
    def _find_count_of_modules_keys(raw_data: Dict[str, Any]) -> List[str]:
        return [
            key for key in raw_data.keys()
            if re.match(r'^t\d+', key)
        ]
