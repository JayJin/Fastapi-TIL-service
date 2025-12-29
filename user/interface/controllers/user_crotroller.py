from typing import Annotated
from fastapi import APIRouter, Depends
from pydantic import BaseModel, EmailStr, Field

from user.application.user_service import UserService
from dependency_injector.wiring import inject, Provide
from containers import Container


router = APIRouter(prefix="/users")

class CreateUserBody(BaseModel):
    name: str = Field(min_length=2, max_length=32)
    email: EmailStr= Field(max_length=64)
    password: str = Field(min_length=8, max_length=32)

class UpdateUser(BaseModel):
    name: str | None = None
    password: str | None = None

@router.post("", status_code=201)
@inject
def create_user(
    user: CreateUserBody,
    user_service: UserService = Depends(Provide[Container.user_service]),       # 의존성 주입
    # user_service: UserService = Depends(Provide["user_service"]),
    # user_service: Annotated[UserService, Depends(UserService)]
    ):
    created_user = user_service.create_user(
        name=user.name,
        email=user.email,
        password=user.password
    )
    return created_user


@router.put("/{user_id}")
@inject
def update_user(
    user_id: str,
    user: UpdateUser,
    user_service: UserService = Depends(Provide[Container.user_service]),
    ):
    user = user_service.update_user(
        user_id=user_id,
        name=user.name,
        password=user.password
    )
    return user

@router.get("")
@inject
def get_users(
    page: int = 1,
    items_per_page: int = 10,
    user_service: UserService = Depends(Provide[Container.user_service]),
    ):
    total_count, users = user_service.get_users(page, items_per_page)
    return {
        "total_count": total_count, 
        "page": page,
        "users": users,
}
    
@router.delete("", status_code=204)
@inject
def delete_user(
    user_id: str,
    user_service: UserService = Depends(Provide[Container.user_service]),
    ):
    # 다른 유저를 삭제할 수 없도록 토큰에서 유저 아이디를 구한다.
    user_service.delete_user(user_id)