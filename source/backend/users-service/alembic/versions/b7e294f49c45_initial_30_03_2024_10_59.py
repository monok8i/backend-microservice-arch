"""Initial 30-03-2024 10:59

Revision ID: b7e294f49c45
Revises: 00f7ec19705c
Create Date: 2024-03-31 10:59:52.687385

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'b7e294f49c45'
down_revision: Union[str, None] = '00f7ec19705c'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
