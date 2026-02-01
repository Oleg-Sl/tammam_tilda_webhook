from fastapi import Depends

from app.api.services.crm_service import CrmService
from app.api.services.body_parser import BodyParser
from app.api.handlers.tilda_handler import TildaWebhookHandler
from app.config import settings


def get_crm_service() -> CrmService:
    return CrmService(settings.webhook)


def get_body_parser() -> BodyParser:
    return BodyParser()


def get_tilda_webhook_handler(
        parser: BodyParser = Depends(get_body_parser),
        crm: CrmService = Depends(get_crm_service)
):
    return TildaWebhookHandler(parser, crm)
