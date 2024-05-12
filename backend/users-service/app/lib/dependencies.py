from typing import Dict

from litestar.di import Provide
from litestar.params import Parameter

from advanced_alchemy.filters import LimitOffset

LIMIT_OFFSET_DEPENDENCY_KEY = "limit_offset"


def provide_limit_offset_filter(
    limit: int = Parameter(ge=1, query="limit", default=1, required=False),
    offset: int = Parameter(
        query="offset",
        ge=1,
        default=20,
        required=False,
    ),
) -> LimitOffset:
    """Add offset/limit pagination.

    Return type consumed by ``Repository.apply_limit_offset_pagination()``.

    Args:
        current_page (int): Page number to return.
        page_size (int): Number of records per page.

    Returns:
        LimitOffset: Filter for query pagination.
    """
    return LimitOffset(limit, limit * (offset - 1))


def provide_dependencies() -> Dict[str, Provide]:
    return {
        LIMIT_OFFSET_DEPENDENCY_KEY: Provide(
            provide_limit_offset_filter, sync_to_thread=False
        )
    }
