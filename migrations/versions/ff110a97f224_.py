"""empty message

Revision ID: ff110a97f224
Revises: be3e5d52aa3d
Create Date: 2025-01-31 00:22:48.460732

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'ff110a97f224'
down_revision = 'be3e5d52aa3d'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('favorites', schema=None) as batch_op:
        batch_op.add_column(sa.Column('planet_id', sa.Integer(), nullable=True))
        batch_op.add_column(sa.Column('people_id', sa.Integer(), nullable=True))
        batch_op.create_foreign_key(None, 'planets', ['planet_id'], ['id'])
        batch_op.create_foreign_key(None, 'people', ['people_id'], ['id'])
        batch_op.drop_column('favorite_type')
        batch_op.drop_column('favorite_id')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('favorites', schema=None) as batch_op:
        batch_op.add_column(sa.Column('favorite_id', sa.INTEGER(), autoincrement=False, nullable=False))
        batch_op.add_column(sa.Column('favorite_type', sa.VARCHAR(length=20), autoincrement=False, nullable=False))
        batch_op.drop_constraint(None, type_='foreignkey')
        batch_op.drop_constraint(None, type_='foreignkey')
        batch_op.drop_column('people_id')
        batch_op.drop_column('planet_id')

    # ### end Alembic commands ###
