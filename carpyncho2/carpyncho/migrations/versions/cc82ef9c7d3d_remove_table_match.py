"""remove table match

Revision ID: cc82ef9c7d3d
Revises: a69f8ae5fb9c
Create Date: 2016-09-26 14:46:14.368375

"""

# revision identifiers, used by Alembic.
revision = 'cc82ef9c7d3d'
down_revision = 'a69f8ae5fb9c'
branch_labels = None
depends_on = None

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('Match')
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.create_table('Match',
    sa.Column('id', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.Column('master_src_id', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.Column('pawprint_src_id', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.Column('ra_avg', postgresql.DOUBLE_PRECISION(precision=53), autoincrement=False, nullable=True),
    sa.Column('dec_avg', postgresql.DOUBLE_PRECISION(precision=53), autoincrement=False, nullable=True),
    sa.Column('ra_std', postgresql.DOUBLE_PRECISION(precision=53), autoincrement=False, nullable=True),
    sa.Column('dec_std', postgresql.DOUBLE_PRECISION(precision=53), autoincrement=False, nullable=True),
    sa.Column('ra_range', postgresql.DOUBLE_PRECISION(precision=53), autoincrement=False, nullable=True),
    sa.Column('dec_range', postgresql.DOUBLE_PRECISION(precision=53), autoincrement=False, nullable=True),
    sa.Column('euc', postgresql.DOUBLE_PRECISION(precision=53), autoincrement=False, nullable=True),
    sa.Column('tile_id', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.ForeignKeyConstraint(['master_src_id'], [u'MasterSource.id'], name=u'Match_master_src_id_fkey'),
    sa.ForeignKeyConstraint(['pawprint_src_id'], [u'PawprintSource.id'], name=u'Match_pawprint_src_id_fkey'),
    sa.ForeignKeyConstraint(['tile_id'], [u'Tile.id'], name=u'Match_tile_id_fkey'),
    sa.PrimaryKeyConstraint('id', name=u'Match_pkey'),
    sa.UniqueConstraint('pawprint_src_id', 'master_src_id', 'tile_id', name=u'_match_uc')
    )
    ### end Alembic commands ###
