import os
import asyncio
from hashlib import sha1
from typing import Awaitable, Optional, Any, TypeVar


def get_random_id():
    return sha1(os.urandom(24)).hexdigest()[:16]


T = TypeVar("T")


async def wait_for(fut: Awaitable[T], timeout: Optional[float] = 5, **kwargs: Any) -> T:
    try:
        return await asyncio.wait_for(fut, timeout=timeout, **kwargs)
    except asyncio.TimeoutError:
        raise Exception("Operation timed out")
