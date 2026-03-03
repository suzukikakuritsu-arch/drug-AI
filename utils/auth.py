# utils/auth.py
from fastapi import Depends, HTTPException
from pydantic import BaseModel

# 簡易ユーザーモデル
class User(BaseModel):
    id: int
    username: str

# ダミーユーザー認証
def get_current_user():
    # テスト用: 常にユーザーID 1
    return User(id=1, username="test_user")
