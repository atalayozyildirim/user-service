from fastapi import APIRouter
from controller.UserController import get_user_username, add_user_controller, update_user_controller,delete_user_controller
from db.Model.UserModel import UserModel

router  = APIRouter()


@router.get("/users/{username}")
async def read_user(username: str):
    try:
       return await get_user_username(username)
    except Exception as e:
        return {"message": "Server error", "error": str(e)}
@router.post("/user/add")
async def add_user(user: UserModel):
    try:
        return await add_user_controller(user)
    except Exception as e:
        return {"message": "Server error", "error": str(e)}

@router.put("/user/update")
async def update_user(user: UserModel):
    try:
        return await update_user_controller(user)
    except Exception as e:
        return {"message": "Server error", "error": str(e)}

@router.delete("/user/delete")
async def delete_user(username: str):
    try:
        return await delete_user_controller(username)
    except Exception as e:
        return {"message": "Server error", "error": str(e)}
