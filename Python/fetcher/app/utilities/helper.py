from functools import wraps
from typing import Optional
import httpx
from fastapi import HTTPException

from app.utilities.log import DebugError


def handle_exceptions(func):
    @wraps(func)
    async def wrapper(*args, **kwargs):
        try:
            return await func(*args, **kwargs)
        except ValueError as value_error:
            raise HTTPException(status_code=404, detail=str(value_error))
        except HTTPException as http_error:
            raise http_error
        except Exception as error:
            DebugError(f"Error in {func.__name__}: {error}")
            raise HTTPException(status_code=500, detail="Internal server error")

    return wrapper




async def call_api(
                   method: str,
                   endpoint: str,
                   json_data: Optional[dict] = None,
                   params: Optional[dict] = None,
                   headers: Optional[dict] = None,
                   timeout: float = 10.0
                   ):
    full_url = f"{endpoint.lstrip('/')}"
    try:
        async with httpx.AsyncClient() as client:
            response = await client.request(
                url=full_url,
                method=method.upper(),
                json=json_data,
                params=params,
                headers=headers,
                timeout=timeout
            )
            response.raise_for_status()
            return response.json()
    except httpx.HTTPStatusError as e:
        DebugError(f"HTTP status error occurred: {e} - {full_url}")
        raise ValueError(f"HTTP error occurred: {e}")
    except httpx.RequestError as e:
        DebugError(f"Network error occurred: {e} - {full_url}")
        raise ValueError(f"Network error occurred: {e}")
    except ValueError as e:
        DebugError(f"Invalid JSON response: {e} - {full_url}")
        raise ValueError(f"Invalid JSON response: {e}")
    except Exception as e:
        DebugError(f"Unexpected error occurred: {e} - {full_url}")
        raise ValueError(f"Unexpected error: {e}")


