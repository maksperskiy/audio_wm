"""empty message

Revision ID: b9f5bc743004
Revises: 
Create Date: 2023-04-17 11:02:32.074317

"""
import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision = "b9f5bc743004"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "params_history",
        sa.Column("step_number", sa.Integer(), nullable=False),
        sa.Column("label", sa.String(length=255), nullable=False),
        sa.Column("experiment_number", sa.Integer(), nullable=False),
        sa.Column("param_number", sa.Integer(), nullable=True),
        sa.Column("freq_bottom", sa.Integer(), nullable=False),
        sa.Column("freq_top", sa.Integer(), nullable=False),
        sa.Column("duration", sa.Integer(), nullable=False),
        sa.Column("freq_bottom_grad", sa.Numeric(), nullable=True),
        sa.Column("freq_top_grad", sa.Numeric(), nullable=True),
        sa.Column("duration_grad", sa.Numeric(), nullable=True),
        sa.Column("freq_bottom_step", sa.Integer(), nullable=False),
        sa.Column("freq_top_step", sa.Integer(), nullable=False),
        sa.Column("duration_step", sa.Integer(), nullable=False),
        sa.Column("expert_score", sa.Numeric(), nullable=True),
        sa.Column("sound_noise_ratio", sa.Numeric(), nullable=True),
        sa.Column("success_ratio", sa.Numeric(), nullable=True),
        sa.Column(
            "created_at", sa.DateTime(), server_default=sa.text("now()"), nullable=True
        ),
        sa.PrimaryKeyConstraint("label", "experiment_number", "step_number"),
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table("params_history")
    # ### end Alembic commands ###
