from app.database import db
from app.models.user_model import User, CreateUser, LoginUser
from app.utils.auth import create_access_token, pwd_context
from datetime import datetime


# User service function for creating a user
async def create_user_service(user: CreateUser):
    # Check if the username already exists in the database
    query_check = "SELECT id FROM users WHERE username = $1"
    existing_user = await db.fetch_one(query_check, user.username)

    # If the username exists, raise an exception
    if existing_user:
       
       return {"message": "Username already exists. Please login."}

    # Hash the password using the method in CreateUser model
    user.hash_password()

    # Insert the new user into the database
    query = """
    INSERT INTO users (name, username, password, role) 
    VALUES ($1, $2, $3, $4) 
    RETURNING id, name, username, role;
    """
    result = await db.fetch_one(query, user.name, user.username, user.password, user.role)

    # Create the access token after successful registration
    user_data = {
        "username": user.username,
        "role": user.role
    }

    # Create a token with an expiry time of 30 minutes
  
    access_token = create_access_token(data=user_data)

    return {"user": dict(result), "access_token": access_token}

async def login_user_service(user: LoginUser):
    # Fetch the user from the database
    query = "SELECT id, username, password, role FROM users WHERE username = $1"
    db_user = await db.fetch_one(query, user.username)

    if not db_user:
        return {"message": "Invalid username or password"}

    # Verify the password
    if not pwd_context.verify(user.password, db_user['password']):

        return {"message": "Invalid username or password"}

    # Prepare JWT payload
    user_data = {
        "username": db_user['username'],
        "role": db_user['role']
    }
    access_token = create_access_token(data=user_data)

    # Return user information and token
    return {
        "user": {
            "id": db_user['id'],
            "username": db_user['username'],
            "role": db_user['role']
        },
        "access_token": access_token
    }

async def get_users_service():
    query = "SELECT id, name, username, role, status, created_at, updated_at FROM users;"
    users = await db.fetch(query)
    return [dict(user) for user in users]


async def get_user_by_id_service(user_id: int):
    query = "SELECT id, name, username, role, status, created_at, updated_at FROM users WHERE id = $1;"
    user = await db.fetch_one(query, user_id)
    return dict(user) if user else None


async def update_user_service(user_id: int, user: User):
    # Ensure that the updated_at field is set to the current time when updating
    current_time = datetime.utcnow()
    
    query = """
    UPDATE users 
    SET name = $1, username = $2, password = $3, role = $4, status = $5, updated_at = $6 
    WHERE id = $7 
    RETURNING id, name, username, role, status, created_at, updated_at;
    """
    result = await db.fetch_one(query, user.name, user.username, user.password, user.role, user.status, current_time, user_id)
    return dict(result) if result else None


async def delete_user_service(user_id: int):
    query = "DELETE FROM users WHERE id = $1;"
    result = await db.execute(query, user_id)
    return result == "DELETE 1"
