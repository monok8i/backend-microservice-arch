"""empty message

Revision ID: db6a8deecc37
Revises: 2d585e9ebc97
Create Date: 2024-02-03 10:48:48.889951

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "db6a8deecc37"
down_revision: Union[str, None] = "2d585e9ebc97"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
