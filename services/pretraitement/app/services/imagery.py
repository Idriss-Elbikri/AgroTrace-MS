from __future__ import annotations

import io
import logging
from datetime import datetime, timezone
from uuid import uuid4

import numpy as np
import rasterio
from rasterio.windows import Window
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from ..db import get_session
from ..models import PreprocessJob, UavTileMetadata
from ..schemas import JobStatus
from ..storage import get_client
from ..config import get_settings

logger = logging.getLogger(__name__)


async def create_tile_job(req, session: AsyncSession) -> str:
    """Create a tiling job and trigger processing."""
    job_id = f"job_{datetime.utcnow().strftime('%Y%m%dT%H%M%SZ')}_{uuid4().hex[:8]}"
    job = PreprocessJob(
        id=job_id,
        job_type="tile_uav_image",
        status=JobStatus.pending.value,
        payload={
            "source": req.source.model_dump(),
            "parcel_id": req.parcel_id,
            "mission_id": req.mission_id,
            "tile_size": req.tile_size,
            "overlap": req.overlap,
            "target_crs": req.target_crs,
        },
    )
    session.add(job)

    # Note: metadata creation removed - will be created after tiling completes
    await session.flush()

    # Start tiling asynchronously
    import asyncio
    asyncio.create_task(_process_tiling(job_id, req))

    return job_id


async def _process_tiling(job_id: str, req):
    """Process the actual tiling operation."""
    async for session in get_session():
        try:
            # Update job status to processing
            stmt = select(PreprocessJob).where(PreprocessJob.id == job_id)
            result = await session.execute(stmt)
            job = result.scalar_one()
            job.status = JobStatus.processing.value
            await session.commit()

            logger.info(f"Starting tiling job {job_id}")

            # Get MinIO client and settings
            settings = get_settings()
            minio_client = get_client()

            # Download source image
            logger.info(
                f"Downloading source image: {req.source.bucket}/{req.source.object_name}"
            )
            response = minio_client.get_object(
                req.source.bucket, req.source.object_name
            )
            image_bytes = response.read()
            response.close()
            response.release_conn()

            # Process with rasterio
            tiles_created = []
            with rasterio.open(io.BytesIO(image_bytes)) as src:
                width = src.width
                height = src.height
                bands = src.count
                transform = src.transform
                crs = src.crs

                logger.info(
                    f"Image properties: {width}x{height}, {bands} bands, CRS: {crs}"
                )

                # Calculate stride (step size considering overlap)
                stride = req.tile_size - req.overlap

                # Generate tiles
                tile_count = 0
                for i in range(0, height, stride):
                    for j in range(0, width, stride):
                        # Calculate window size
                        window_height = min(req.tile_size, height - i)
                        window_width = min(req.tile_size, width - j)

                        if window_height < req.tile_size // 2 or window_width < req.tile_size // 2:
                            continue  # Skip small edge tiles

                        # Read window
                        window = Window(j, i, window_width, window_height)
                        tile_data = src.read(window=window)

                        # Calculate tile bounds
                        tile_transform = src.window_transform(window)

                        # Create tile filename
                        tile_name = f"{req.mission_id}_tile_{tile_count:04d}.tif"
                        tile_path = f"{req.parcel_id}/{req.mission_id}/{tile_name}"

                        # Write tile to bytes
                        tile_bytes = io.BytesIO()
                        with rasterio.open(
                            tile_bytes,
                            "w",
                            driver="GTiff",
                            height=window_height,
                            width=window_width,
                            count=bands,
                            dtype=tile_data.dtype,
                            crs=crs,
                            transform=tile_transform,
                            compress="lzw",
                        ) as dst:
                            dst.write(tile_data)

                        # Upload tile to MinIO
                        tile_bytes.seek(0)
                        minio_client.put_object(
                            settings.minio_tiles_bucket,
                            tile_path,
                            tile_bytes,
                            length=tile_bytes.getbuffer().nbytes,
                            content_type="image/tiff",
                        )

                        tiles_created.append(
                            {
                                "tile_id": tile_count,
                                "path": tile_path,
                                "bounds": {
                                    "col_off": j,
                                    "row_off": i,
                                    "width": window_width,
                                    "height": window_height,
                                },
                            }
                        )

                        tile_count += 1
                        if tile_count % 10 == 0:
                            logger.info(f"Created {tile_count} tiles so far...")

            logger.info(f"Total tiles created: {tile_count}")

            # Create UavTileMetadata record for each tile
            for tile_info in tiles_created:
                tile_meta = UavTileMetadata(
                    job_id=job_id,
                    parcel_id=req.parcel_id,
                    mission_id=req.mission_id,
                    tile_path=tile_info["path"],
                    bounds=tile_info["bounds"],
                    crs=str(crs),
                    resolution=None,
                    meta={
                        "tile_id": tile_info["tile_id"],
                        "original_size": {"width": width, "height": height},
                        "tile_size": req.tile_size,
                        "overlap": req.overlap,
                    },
                )
                session.add(tile_meta)

            # Update job status to completed
            job.status = JobStatus.completed.value
            job.result = {
                "tiles_created": tile_count,
                "target_bucket": settings.minio_tiles_bucket,
                "tiles_sample": tiles_created[:5],  # Store first 5 for reference
                "original_size": {"width": width, "height": height},
                "crs": str(crs),
            }

            await session.commit()
            logger.info(f"Tiling job {job_id} completed: {tile_count} tiles created")

        except Exception as e:
            logger.error(f"Tiling job {job_id} failed: {e}", exc_info=True)
            # Update job status to failed
            stmt = select(PreprocessJob).where(PreprocessJob.id == job_id)
            result = await session.execute(stmt)
            job = result.scalar_one()
            job.status = JobStatus.failed.value
            job.error = {"message": str(e), "type": type(e).__name__}
            await session.commit()
        finally:
            await session.close()
            break


async def list_tiles(parcel_id: str, mission_id: str, session: AsyncSession) -> list:
    """List all tiles for a given parcel and mission."""
    stmt = (
        select(UavTileMetadata)
        .where(UavTileMetadata.parcel_id == parcel_id)
        .where(UavTileMetadata.mission_id == mission_id)
    )
    result = await session.execute(stmt)
    metadata = result.scalar_one_or_none()

    if not metadata or not metadata.meta:
        return []

    return metadata.meta.get("tiles", [])
