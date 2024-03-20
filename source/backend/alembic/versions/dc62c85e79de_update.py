"""Update

Revision ID: dc62c85e79de
Revises: 0075ce25d406
Create Date: 2024-03-16 00:02:43.541145

"""
from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = "dc62c85e79de"
down_revision: Union[str, None] = "0075ce25d406"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column(
        "userprofiles", "user_id", existing_type=sa.INTEGER(), nullable=True
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column(
        "userprofiles", "user_id", existing_type=sa.INTEGER(), nullable=False
    )
    # ### end Alembic commands ###