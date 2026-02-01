import re
import pathlib
import logging
from typing import Dict, Any
from logging.handlers import RotatingFileHandler
from fastapi import APIRouter, Request, Depends, Query, Form, Body, Header
from pydantic import BaseModel

from app.api.dependencies import get_tilda_webhook_handler
from app.api.handlers.tilda_handler import TildaWebhookHandler


router = APIRouter(
    prefix="/api/v1",
    tags=["Api"],
)


log_path = pathlib.Path('logs')
log_path.mkdir(parents=True, exist_ok=True)

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

file_handler = RotatingFileHandler(
    filename="logs/app.log",
    maxBytes=10*1024*1024,
    backupCount=5,
    encoding='utf-8'
)

formatter = logging.Formatter("%(asctime)s %(levelname)s %(message)s")
file_handler.setFormatter(formatter)

logger.addHandler(file_handler)


@router.post("/webhook/tilda")
async def event_bot(
    request: Request,
    body: Dict[str, Any] = Body(...),
    handler: TildaWebhookHandler = Depends(get_tilda_webhook_handler)
    ):

    logger.info(f"Headers: {dict(request.headers)}")
    logger.info(f'Qury params: {dict(request.query_params)}')
    logger.info(f'Body: {body}')

    try:
        response = await handler.handle_webhook(body)
        logger.info(f"Webhook response: {response}")
        return response
    except Exception as e:
        logger.error(f"Error processing webhook: {e}")
 

# @router.post("/webhook/tilda")
# async def event_bot(
#     request: Request,
#     body: Dict[str, Any] = Body(...),
#     ):

#     headers = dict(request.headers)
#     logger.info(f"Headers: {headers}")

#     query_params = dict(request.query_params)
#     logger.info(f'Qury params: {query_params}')

#     form_data = TildaFormData(**body)
#     logger.info(f'Parsed form data: {form_data}')

#     data = parse_body(body)
#     logger.info(f'Parsed modules data: {data}')
#     result = create_lead(
#         name=form_data.name,
#         phone=form_data.phone,
#         calc=form_data.calc,
#         formid=form_data.formid,
#         modules_data=', '.join([f'{key} ({value})' for key, value in data.items()])
#     )
#     logger.info(f'Lead creation result: {result}')
    
#     return {'status': 'received'}
