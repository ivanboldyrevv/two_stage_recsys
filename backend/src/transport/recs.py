from fastapi import APIRouter


recs = APIRouter()


@recs.get("/recs")
def get_recommendation():
    pass
