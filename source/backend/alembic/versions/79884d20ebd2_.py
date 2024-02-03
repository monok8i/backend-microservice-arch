"""empty message

Revision ID: 79884d20ebd2
Revises: db6a8deecc37
Create Date: 2024-02-03 11:09:32.655752

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "79884d20ebd2"
down_revision: Union[str, None] = "db6a8deecc37"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
