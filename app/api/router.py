import pathlib
import logging
from logging.handlers import RotatingFileHandler
from fastapi import APIRouter, Request, Query, Form, Body, Header


router = APIRouter(
    prefix="/api/v1",
    tags=["Api"],
)


log_path = pathlib.Path('logs')
log_path.mkdir(parents=True, exist_ok=True)

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

file_handler = RotatingFileHandler(
    filename="logs/tilda_webhook.log",
    maxBytes=10*1024*1024,
    backupCount=5,
    encoding='utf-8'
)

formatter = logging.Formatter("%(asctime)s %(levelname)s %(message)s")
file_handler.setFormatter(formatter)

logger.addHandler(file_handler)


@router.post("/webhook/tilda")
async def event_bot(request: Request):
    headers = dict(request.headers)
    logger.info(f"Headers: {headers}")

    query_params = dict(request.query_params)
    logger.info(f'Qury params: {query_params}')

    content_type = request.headers.get('content-type', '')
    logger.info(f"Content-Type: {content_type}")
    
    try:
        body = await request.json()
    except Exception:
        body = await request.body()
    logger.info(f'Body: {body}')
    
    return {'status': 'received'}
