from app.database import db
from app.models.user_model import User
from datetime import datetime


async def create_user_service(user: User):
    # Ensure that the current time is used for created_at and updated_at
    current_time = datetime.utcnow()
    
    query = """
    INSERT INTO users (name, username, password, role, status, created_at, updated_at) 
    VALUES ($1, $2, $3, $4, $5, $6, $6) 
    RETURNING id, name, username, role, status, created_at, updated_at;
    """
    result = await db.fetch_one(query, user.name, user.username, user.password, user.role, user.status, current_time)
    return dict(result)


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
