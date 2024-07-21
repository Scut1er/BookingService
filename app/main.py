from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from app.bookings.router import router as router_bookings
from app.users.router import router_auth as router_auth
from app.users.router import router_users as router_users
from app.hotels.router import router as router_hotels
from app.hotels.rooms.router import router as router_rooms
from app.pages.router import router as router_pages
from app.images.router import router as router_images

app = FastAPI(title="Hotel Booking Service",)

app.mount("/static", StaticFiles(directory="app/static"), "static")

app.include_router(router_auth)
app.include_router(router_users)
app.include_router(router_bookings)
router_hotels.include_router(router_rooms)
app.include_router(router_hotels)
app.include_router(router_pages)
app.include_router(router_images)
