import pytest
from httpx import AsyncClient


@pytest.mark.parametrize("room_id, date_from, date_to, status_code",
                         [("1", "2023-07-11", "2023-07-10", 400),
                          ("1", "2023-07-11", "2023-08-20", 400),
                          ("1", "2023-07-11", "2023-08-05", 200)
                          ])
async def test_add_booking(room_id, date_from, date_to, status_code, authenticated_ac: AsyncClient):
    response = await authenticated_ac.post("/booking", json={
        "room_id": room_id,
        "date_from": date_from,
        "date_to": date_to
    })
    assert response.status_code == status_code