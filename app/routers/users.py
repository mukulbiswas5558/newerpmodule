from fastapi import APIRouter, HTTPException
from app.models.user_model import User, CreateUser, LoginUser
from app.services.user_service import (
    create_user_service,
    login_user_service,
    get_users_service,
    get_user_by_id_service,
    update_user_service,
    delete_user_service,
)

router = APIRouter()


# @router.post("/", response_model=User)
# async def create_user(user: User):
#     return await create_user_service(user)

@router.post("/auth/register")
async def create_user(user: CreateUser):

    user.hash_password()
    # Pass the user to the service to save
    return await create_user_service(user)
@router.post("/auth/login")
async def login_user(user: LoginUser):
    return await login_user_service(user)

@router.get("/", response_model=list[User])
async def get_users():
    return await get_users_service()


@router.get("/{user_id}", response_model=User)
async def get_user(user_id: int):
    user = await get_user_by_id_service(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@router.put("/{user_id}", response_model=User)
async def update_user(user_id: int, user: User):
    updated_user = await update_user_service(user_id, user)
    if not updated_user:
        raise HTTPException(status_code=400, detail="User update failed")
    return updated_user


@router.delete("/{user_id}")
async def delete_user(user_id: int):
    success = await delete_user_service(user_id)
    if not success:
        raise HTTPException(status_code=400, detail="User delete failed")
    return {"message": "User deleted successfully"}
