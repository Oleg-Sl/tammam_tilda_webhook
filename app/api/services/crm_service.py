import json
import logging
import requests
from typing import Dict
from pprint import pprint

from app.api.models.crm import LeadCreationFields


logger = logging.getLogger(__name__)


class CrmService:
    def __init__(self, base_url: str):
        self.base_url = base_url
    
    async def crete_lead(self, lead_data: LeadCreationFields) -> Dict:
        payload_data = self._prepare_lead_payload(lead_data)
        headers = {
            'Content-Type': 'application/json',
        }

        try:
            response = requests.post(
                f'{self.base_url}/crm.lead.add',
                headers=headers,
                data=json.dumps(payload_data),
            )
            result = response.json()
            return result
        except Exception as e:
            logging.error(f"Error creating lead: {e}. Payload: {payload_data}")
            raise

    def _prepare_lead_payload(self, lead_data: LeadCreationFields) -> Dict:
        return {
            "fields": {
				"TITLE": lead_data.title,
                "NAME": lead_data.name,
                "PHONE": [
					{ "VALUE": phone.value, "VALUE_TYPE": phone.value_type }
                    for phone in lead_data.phone
				],
                "UF_CRM_1769831136": lead_data.modules_data,
                "OPPORTUNITY": lead_data.opportunity,
                "ASSIGNED_BY_ID": 351
            },
			# "params": {
			# 	"REGISTER_SONET_EVENT": "Y",
			# }
        }
