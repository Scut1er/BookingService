import pytest
from httpx import AsyncClient


@pytest.mark.parametrize("location, date_from, date_to, status_code",
                         [("Cosmos Collection Altay Resort", "2023-07-11", "2023-07-10", 400),
                          ("Cosmos Collection Altay Resort", "2023-07-11", "2023-08-20", 400),
                          ("Cosmos Collection Altay Resort", "2023-07-11", "2023-08-05", 200)
                          ])
async def test_get_hotels(location, date_from, date_to, status_code, authenticated_ac: AsyncClient):
    response = await authenticated_ac.get("/hotels", params={
        "location": location,
        "date_from": date_from,
        "date_to": date_to
    })
    assert response.status_code == status_code