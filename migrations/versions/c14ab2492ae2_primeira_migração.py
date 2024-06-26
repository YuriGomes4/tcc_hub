"""Primeira migração

Revision ID: c14ab2492ae2
Revises: 
Create Date: 2023-10-25 02:57:41.579305

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'c14ab2492ae2'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('area_residencia',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('data_criacao', sa.DateTime(), nullable=True),
    sa.Column('data_alteracao', sa.DateTime(), nullable=True),
    sa.Column('id_residencia', sa.Integer(), nullable=True),
    sa.Column('nome', sa.String(length=100), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('dispositivo',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('data_criacao', sa.DateTime(), nullable=True),
    sa.Column('data_alteracao', sa.DateTime(), nullable=True),
    sa.Column('id_residencia', sa.Integer(), nullable=True),
    sa.Column('id_area_residencia', sa.Integer(), nullable=True),
    sa.Column('nome', sa.String(length=100), nullable=True),
    sa.Column('codigo', sa.String(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('log_exec',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('data_criacao', sa.DateTime(), nullable=True),
    sa.Column('data_alteracao', sa.DateTime(), nullable=True),
    sa.Column('id_residencia', sa.Integer(), nullable=True),
    sa.Column('id_area_residencia', sa.Integer(), nullable=True),
    sa.Column('id_dispositivo', sa.Integer(), nullable=True),
    sa.Column('acao', sa.String(), nullable=True),
    sa.Column('status', sa.String(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('residencia',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('data_criacao', sa.DateTime(), nullable=True),
    sa.Column('data_alteracao', sa.DateTime(), nullable=True),
    sa.Column('id_usuario', sa.Integer(), nullable=True),
    sa.Column('nome', sa.String(length=100), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('usuario',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('data_criacao', sa.DateTime(), nullable=True),
    sa.Column('data_alteracao', sa.DateTime(), nullable=True),
    sa.Column('id_publico', sa.String(length=50), nullable=True),
    sa.Column('nome', sa.String(length=100), nullable=True),
    sa.Column('email', sa.String(length=70), nullable=True),
    sa.Column('senha', sa.String(length=80), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('email'),
    sa.UniqueConstraint('id_publico')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('usuario')
    op.drop_table('residencia')
    op.drop_table('log_exec')
    op.drop_table('dispositivo')
    op.drop_table('area_residencia')
    # ### end Alembic commands ###
