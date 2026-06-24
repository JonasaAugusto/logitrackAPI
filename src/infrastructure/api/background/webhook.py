import asyncio

from src.infrastructure.config.logging import get_logger

logger = get_logger(__name__)

WEBHOOK_URL = "https://webhook.example.com/logitrack/events"


async def dispatch_delivery_webhook(tracking_code: str, status: str, event_type: str = "delivery.created") -> None:
    logger.info("webhook_dispatch_started", tracking_code=tracking_code, event_type=event_type, url=WEBHOOK_URL)
    try:
        await asyncio.sleep(1)
        logger.info("webhook_dispatch_success", tracking_code=tracking_code, event_type=event_type)
    except Exception as e:
        logger.error("webhook_dispatch_failed", tracking_code=tracking_code, error=str(e))
