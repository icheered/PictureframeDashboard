
from fastapi import APIRouter, status

router = APIRouter()

@router.get("/")
def get_state() -> int:
    print("Getting monitor state")
    return 1

@router.post("/")
def post_state(state: int) -> int:
    print(f"Setting monitor state: {state}")
    return state

