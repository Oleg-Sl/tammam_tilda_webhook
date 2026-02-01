import logging
from typing import Dict, Any

from app.api.services.body_parser import BodyParser
from app.api.services.crm_service import CrmService
from app.api.models.crm import LeadCreationFields, Phone
from app.api.models.webhook_response import WebhookResponse


logger = logging.getLogger(__name__)


class TildaWebhookHandler:
    def __init__(self, body_parser: BodyParser, bitrix_service: CrmService):
        self.body_parser = body_parser
        self.bitrix_service = bitrix_service

    async def handle_webhook(self, raw_data: Dict[str, Any]) -> WebhookResponse:
        form_data = self.body_parser.extract_form_data(raw_data)
        
        modules = self.body_parser.parse_modules_data(raw_data)

        modules_data = self.body_parser.format_modules_data(modules)

        lead_data = LeadCreationFields(
            title=f"Запрос с сайта! Сборка комбинации. ({form_data.formid})",
            name=form_data.name,
            phone=[Phone(value=form_data.phone)],
            modules_data=modules_data,
            opportunity=form_data.calc
        )

        result = await self.bitrix_service.crete_lead(lead_data)
        logging.info('Lead creation result: %s', result)

        lead_id = result.get('result')
            
        return WebhookResponse(
            status="success" if lead_id else "failure",
            message=str(lead_id)
        )
