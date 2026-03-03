# utils/auth.py
from pydantic import BaseModel

class User(BaseModel):
    id: int
    username: str

def get_current_user():
    # GitHubだけで使う場合、常にテストユーザー
    return User(id=1, username="test_user")
