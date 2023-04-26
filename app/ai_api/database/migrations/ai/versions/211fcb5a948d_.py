"""empty message

Revision ID: 211fcb5a948d
Revises: 
Create Date: 2023-04-20 14:59:32.639860

"""
import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision = "211fcb5a948d"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "params",
        sa.Column("label", sa.String(length=255), nullable=False),
        sa.Column("freq_bottom", sa.Integer(), nullable=False),
        sa.Column("freq_top", sa.Integer(), nullable=False),
        sa.Column("duration", sa.Integer(), nullable=False),
        sa.Column(
            "created_at", sa.DateTime(), server_default=sa.text("now()"), nullable=True
        ),
        sa.PrimaryKeyConstraint("label"),
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table("params")
    # ### end Alembic commands ###