import httpx
from fastapi import HTTPException
from app.core.config import settings
from app.utils import messages

class IntegrationService:
    @staticmethod
    async def get_user_info(user_id: int, token: str) -> dict:
        async with httpx.AsyncClient() as client:
            try:
                response = await client.get(
                    f"{settings.USER_SERVICE_URL}/api/v1/users/user/{user_id}",
                    headers={"Authorization": f"Bearer {token}"}
                )
                if response.status_code == 200:
                    json_resp = response.json()
                    return json_resp.get("data", json_resp)
                elif response.status_code == 404:
                    raise HTTPException(status_code=404, detail=messages.USER_NOT_FOUND)
                elif response.status_code == 403:
                    raise HTTPException(status_code=403, detail=messages.UNAUTHORIZED_FETCH)
                else:
                    raise HTTPException(status_code=response.status_code, detail=messages.SERVICE_ERROR)
            except httpx.RequestError as exc:
                raise HTTPException(status_code=503, detail=messages.SERVICE_UNAVAILABLE.format(service="User Service", exc=exc))

    @staticmethod
    async def get_doctor_info(doctor_id: int, token: str) -> dict:
        async with httpx.AsyncClient() as client:
            try:
                response = await client.get(
                    f"{settings.DOCTOR_SERVICE_URL}/api/v1/doctors/doctor/{doctor_id}",
                    headers={"Authorization": f"Bearer {token}"}
                )
                if response.status_code == 200:
                    json_resp = response.json()
                    return json_resp.get("data", json_resp)
                elif response.status_code == 404:
                    raise HTTPException(status_code=404, detail=messages.DOCTOR_NOT_FOUND)
                elif response.status_code == 403:
                    raise HTTPException(status_code=403, detail=messages.UNAUTHORIZED_FETCH)
                else:
                    raise HTTPException(status_code=response.status_code, detail=messages.SERVICE_ERROR)
            except httpx.RequestError as exc:
                raise HTTPException(status_code=503, detail=messages.SERVICE_UNAVAILABLE.format(service="Doctor Service", exc=exc))
