"""Mapping API routes."""
from fastapi import APIRouter, Query

from .mapping import get_mapping, KEY_OFFSETS

router = APIRouter(prefix="/api/mapping", tags=["mapping"])


@router.get("/{key}")
async def get_hole_mapping(
    key: str,
    tuning: str = Query("paddy", pattern="^(paddy|standard)$"),
):
    if key not in KEY_OFFSETS:
        from fastapi import HTTPException
        raise HTTPException(400, f"Unsupported key: {key}. Supported: {list(KEY_OFFSETS.keys())}")
    return {
        "key": key,
        "tuning": tuning,
        "holes": get_mapping(key, tuning),
    }


@router.get("")
async def list_keys():
    return {"keys": list(KEY_OFFSETS.keys()), "tunings": ["paddy", "standard"]}
