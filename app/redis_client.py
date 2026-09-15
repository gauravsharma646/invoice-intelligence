import os
import redis
from dotenv import load_dotenv

load_dotenv()

REDIS_URL = os.getenv(
    "REDIS_URL",
    "redis://localhost:6379/0"
)

redis_client = redis.Redis.from_url(
    REDIS_URL,
    decode_responses=True
)


def check_invoice_processed(invoice_number: str):
    key = f"invoice:processed:{invoice_number}"
    return redis_client.get(key)


def mark_invoice_processed(invoice_number: str, status: str):
    key = f"invoice:processed:{invoice_number}"

    redis_client.set(
        key,
        status,
        ex=3600
    )