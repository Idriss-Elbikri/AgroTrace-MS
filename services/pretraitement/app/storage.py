from __future__ import annotations

import asyncio
import io
import logging
from typing import Optional

from minio import Minio

from .config import Settings, get_settings

logger = logging.getLogger(__name__)


_client: Minio | None = None


def get_client(settings: Optional[Settings] = None) -> Minio:
    global _client
    settings = settings or get_settings()
    if _client is None:
        _client = Minio(
            settings.minio_endpoint,
            access_key=settings.minio_access_key,
            secret_key=settings.minio_secret_key,
            secure=settings.minio_secure,
        )
    return _client


async def ensure_bucket(client: Minio, bucket_name: str) -> None:
    exists = await asyncio.to_thread(client.bucket_exists, bucket_name)
    if not exists:
        logger.info("Creating MinIO bucket %s", bucket_name)
        await asyncio.to_thread(client.make_bucket, bucket_name)


async def upload_bytes(
    client: Minio,
    bucket: str,
    object_name: str,
    data: bytes,
    content_type: str,
) -> None:
    stream = io.BytesIO(data)
    length = len(data)
    await asyncio.to_thread(
        client.put_object,
        bucket,
        object_name,
        stream,
        length,
        content_type=content_type,
    )


async def ensure_default_buckets(settings: Settings) -> None:
    client = get_client(settings)
    await ensure_bucket(client, settings.minio_raw_bucket)
    await ensure_bucket(client, settings.minio_tiles_bucket)
