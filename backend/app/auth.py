"""Simple password-based admin authentication."""
import hashlib
import os

from fastapi import Depends, HTTPException, Request


ADMIN_PASSWORD = os.environ.get("ADMIN_PASSWORD", "admin123")


def _hash_password(pw: str) -> str:
    return hashlib.sha256(pw.encode()).hexdigest()


async def verify_admin(request: Request) -> None:
    auth = request.headers.get("Authorization", "")
    if not auth.startswith("Bearer "):
        raise HTTPException(401, "Missing authorization")
    token = auth[7:]
    if token != _hash_password(ADMIN_PASSWORD):
        raise HTTPException(403, "Invalid password")


class AdminAuth:
    """Dependency for admin routes."""

    async def __call__(self, request: Request) -> None:
        await verify_admin(request)


admin_auth = AdminAuth()
