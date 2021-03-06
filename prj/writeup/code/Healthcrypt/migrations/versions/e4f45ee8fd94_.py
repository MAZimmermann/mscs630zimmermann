"""empty message

Revision ID: e4f45ee8fd94
Revises: 
Create Date: 2020-05-06 19:13:39.369496

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'e4f45ee8fd94'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('physician',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('key', sa.LargeBinary(), nullable=True),
    sa.Column('fname', sa.LargeBinary(), nullable=True),
    sa.Column('lname', sa.LargeBinary(), nullable=True),
    sa.Column('username', sa.String(length=256), nullable=True),
    sa.Column('userpwd', sa.String(length=256), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_physician_username'), 'physician', ['username'], unique=True)
    op.create_table('record',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('phys_id', sa.Integer(), nullable=True),
    sa.Column('date_created', sa.DateTime(), nullable=True),
    sa.Column('date_last_modified', sa.DateTime(), nullable=True),
    sa.Column('patfname', sa.LargeBinary(), nullable=True),
    sa.Column('patlname', sa.LargeBinary(), nullable=True),
    sa.Column('patdob', sa.LargeBinary(), nullable=True),
    sa.Column('patdiag', sa.LargeBinary(), nullable=True),
    sa.ForeignKeyConstraint(['phys_id'], ['physician.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_record_date_created'), 'record', ['date_created'], unique=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_record_date_created'), table_name='record')
    op.drop_table('record')
    op.drop_index(op.f('ix_physician_username'), table_name='physician')
    op.drop_table('physician')
    # ### end Alembic commands ###
