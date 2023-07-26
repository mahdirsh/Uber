"""empty message

Revision ID: c592178a89b5
Revises: ee690f8ff54a
Create Date: 2023-07-24 19:25:24.077026

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'c592178a89b5'
down_revision = 'ee690f8ff54a'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('trips', schema=None) as batch_op:
        batch_op.add_column(sa.Column('description', sa.String(), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('trips', schema=None) as batch_op:
        batch_op.drop_column('description')

    # ### end Alembic commands ###