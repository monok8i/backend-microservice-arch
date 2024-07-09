from typing import Annotated

from advanced_alchemy.filters import FilterTypes
from advanced_alchemy.service import OffsetPagination
from litestar import delete, get, patch, post, put
from litestar.controller import Controller
from litestar.di import Provide
from litestar.params import Body, Dependency, Parameter

from app.database.models import User
from app.domain.dependencies import current_user, provide_users_service
from app.domain.guards import super_user_guard
from app.domain.schemas import (
    PydanticUser,
    PydanticUserCreate,
    PydanticUserUpdate,
    UserOutputDTO,
)
from app.domain.services import UserService


class UserController(Controller):
    dependencies = {"service": Provide(provide_users_service)}
    quards = [super_user_guard]
    signature_namespace = {"UserService": UserService}
    path = "/users"
    return_dto = UserOutputDTO
    tags = ["users"]

    @get("/me", dependencies={"user": Provide(current_user)})
    async def get_me(self, user: User) -> User:
        return user

    @get("/{user_id:int}", cache=True)
    async def get_user(
        self,
        service: UserService,
        user_id: Annotated[
            int,
            Parameter(
                title="User ID",
                description="Get user with specific identifier",
                required=True,
            ),
        ],
    ) -> User:
        return await service.get(user_id=user_id)

    @post("/")
    async def create_user(
        self,
        service: UserService,
        *,
        data: Annotated[
            PydanticUserCreate,
            Body(
                title="Create user data",
                description="Data for creating new user in system",
            ),
        ],
    ) -> User:
        return await service.create(data=data)

    @get("/", return_dto=None, cache=False)
    async def get_users(
        self,
        service: UserService,
        filters: Annotated[list[FilterTypes], Dependency(skip_validation=True)],
    ) -> OffsetPagination[PydanticUser]:
        return await service.get_users(*filters)

    @patch("/{user_id:int}")
    async def patch_user(
        self,
        service: UserService,
        user_id: Annotated[
            int,
            Parameter(title="User ID", description="Get user with specific identifier"),
        ],
        data: Annotated[
            PydanticUserUpdate,
            Body(
                title="User Update data",
                description="Data for partitialy updating user in system",
            ),
        ],
    ) -> User:
        return await service.update(user_id=user_id, data=data)

    @put("/{user_id:int}")
    async def put_user(
        self,
        service: UserService,
        user_id: Annotated[
            int,
            Parameter(title="User ID", description="Get user with specific identifier"),
        ],
        data: Annotated[
            PydanticUserUpdate,
            Body(
                title="User Update data",
                description="Data for completely updating user in system",
            ),
        ],
    ) -> User:
        return await service.update(user_id=user_id, data=data)

    @delete("/{user_id:int}")
    async def delete_user(
        self,
        service: UserService,
        user_id: Annotated[
            int,
            Parameter(title="User ID", description="Get user with specific identifier"),
        ],
    ) -> None:
        _ = await service.delete(user_id)
