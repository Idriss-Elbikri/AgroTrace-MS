from __future__ import annotations

import io
from datetime import datetime
from pathlib import Path
from typing import Annotated

from fastapi import APIRouter, Depends, File, Form, UploadFile, status
from sqlalchemy.ext.asyncio import AsyncSession

from ..config import get_settings
from ..db import get_session
from ..schemas import (
    ImageTilingRequest,
    JobCreateResponse,
    JobStatus,
    MinioObjectRef,
)
from ..services import imagery as imagery_service
from ..storage import get_client

router = APIRouter(prefix='/imagery', tags=['imagery'])


@router.post('/upload', status_code=status.HTTP_202_ACCEPTED)
async def upload_imagery(
    parcel_id: Annotated[str, Form(description="Parcel ID")],
    mission_id: Annotated[str, Form(description="Mission ID")],
    file: Annotated[UploadFile, File(description="Image file to upload")],
    tile_size: Annotated[int, Form(description="Tile size in pixels")] = 512,
    overlap: Annotated[int, Form(description="Overlap between tiles in pixels")] = 64,
    target_crs: Annotated[str, Form(description="Target CRS")] = "EPSG:4326",
    session: AsyncSession = Depends(get_session),
):
    """
    Upload a UAV image and automatically trigger tiling.

    Returns upload info and tiling job ID.
    """
    settings = get_settings()
    minio_client = get_client()

    filename = Path(file.filename or 'uav-image.tif').name
    object_name = f"{parcel_id}/{mission_id}/raw/{filename}"

    # Read file content
    content = await file.read()

    # Upload to MinIO
    minio_client.put_object(
        settings.minio_raw_bucket,
        object_name,
        io.BytesIO(content),
        length=len(content),
        content_type=file.content_type or 'image/tiff',
    )

    # Automatically trigger tiling
    tiling_request = ImageTilingRequest(
        source=MinioObjectRef(bucket=settings.minio_raw_bucket, object_name=object_name),
        parcel_id=parcel_id,
        mission_id=mission_id,
        tile_size=tile_size,
        overlap=overlap,
        target_crs=target_crs,
    )

    job_id = await imagery_service.create_tile_job(tiling_request, session)
    await session.commit()

    return {
        "message": "Image uploaded successfully",
        "upload": {
            "bucket": settings.minio_raw_bucket,
            "object_name": object_name,
            "size_bytes": len(content),
            "content_type": file.content_type,
        },
        "tiling_job_id": job_id,
        "tiling_status": "Tiling job created and processing automatically",
    }


@router.post('/tile', status_code=status.HTTP_202_ACCEPTED)
async def tile_existing_imagery(
    request: ImageTilingRequest,
    session: AsyncSession = Depends(get_session),
):
    """
    Create a job to tile an existing UAV image into smaller patches.

    This endpoint is automatically called after image upload,
    but can also be used manually for existing images.
    """
    job_id = await imagery_service.create_tile_job(request, session)
    await session.commit()

    return {
        "job_id": job_id,
        "status": "Tiling job created",
        "target_bucket": "uav-tiles",
    }


@router.get("/tiles/{parcel_id}/{mission_id}", response_model=list)
async def get_tiles(
    parcel_id: str,
    mission_id: str,
    session: AsyncSession = Depends(get_session),
):
    """List all tiles for a given parcel and mission."""
    tiles = await imagery_service.list_tiles(parcel_id, mission_id, session)
    return tiles
