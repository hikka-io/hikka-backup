"""Initial migration

Revision ID: 3da5f06f5a16
Revises: 
Create Date: 2024-06-15 00:59:03.566146

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '3da5f06f5a16'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('service_images',
    sa.Column('downloaded', sa.Boolean(), nullable=False),
    sa.Column('path', sa.String(), nullable=False),
    sa.Column('updated', sa.DateTime(), nullable=False),
    sa.Column('created', sa.DateTime(), nullable=False),
    sa.Column('id', sa.Uuid(), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('path')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('service_images')
    # ### end Alembic commands ###
