from fastapi import APIRouter, HTTPException,Depends
from app.models.user_model import User, CreateUser, LoginUser,UpdateUser
from app.services.user_service import (
    create_user_service,
    login_user_service,
    get_users_service,
    get_user_by_id_service,
    update_user_service,
    delete_user_service,
)
from app.utils.auth import get_bearer_token
router = APIRouter()


# @router.post("/", response_model=User)
# async def create_user(user: User):
#     return await create_user_service(user)

@router.post("/auth/register")
async def create_user(user: CreateUser):

   
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




@router.put("/update")
async def update_user(
    user: UpdateUser,  # Replace UpdateUser with your schema class
    token: str = Depends(get_bearer_token)
):
    """
    Updates a user's details after validating the JWT token.
    """
    # Print or use the extracted token
    print(f"Token received: {token}")
    
    # Mock implementation for now
    return {"message": "User updated successfully.", "token": token}


@router.delete("/{user_id}")
async def delete_user(user_id: int):
    success = await delete_user_service(user_id)
    if not success:
        raise HTTPException(status_code=400, detail="User delete failed")
    return {"message": "User deleted successfully"}
