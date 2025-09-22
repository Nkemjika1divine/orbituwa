from dotenv import load_dotenv
from fastapi import APIRouter, HTTPException, Request, BackgroundTasks, Depends
from fastapi.responses import JSONResponse
from schema.placeschema import PlaceExpected
from utils.errors import Not_Found, Unauthorized, Forbidden, Bad_Request


load_dotenv()


place_router = APIRouter()


@place_router.get("/places")
async def get_all_places():
    """Get all places on the DB"""
    from db.reload import storage

    places = storage.all("Place")
    if places:
        return places
    return Not_Found(detail="No places in the DB")


@place_router.post("/create_place")
async def create_place(place_input: PlaceExpected):
    from utils.utils import get_place_by_email
    from models.place import Place
    from db.reload import storage

    """Create a new place"""
    if get_place_by_email(place_input.email):
        raise Bad_Request(
            detail="This email is already registered to another organization"
        )

    place = Place(
        email=place_input.email,
        password=place_input.password,
        name=place_input.name,
        address=place_input.address,
        description=place_input.description,
    )
    storage.new(place)
    storage.save()
    return place
