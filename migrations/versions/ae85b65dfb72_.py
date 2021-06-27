"""empty message

Revision ID: ae85b65dfb72
Revises: 4a1b7d57f99e
Create Date: 2021-06-23 18:25:45.238611

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = 'ae85b65dfb72'
down_revision = '4a1b7d57f99e'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_foreign_key(None, 'exam', 'course', ['course_id'], ['id'])
    op.create_foreign_key(None, 'exam', 'clazz', ['clazz_id'], ['id'])
    op.create_foreign_key(None, 'exam', 'user', ['user_id'], ['id'])
    op.create_foreign_key(None, 'result', 'exam', ['exam_id'], ['id'])
    op.create_foreign_key(None, 'student_score', 'exam', ['exam_id'], ['id'])
    op.drop_column('user', 'isdelete')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('user', sa.Column('isdelete', mysql.TINYINT(display_width=1), autoincrement=False, nullable=True))
    op.drop_constraint(None, 'student_score', type_='foreignkey')
    op.drop_constraint(None, 'result', type_='foreignkey')
    op.drop_constraint(None, 'exam', type_='foreignkey')
    op.drop_constraint(None, 'exam', type_='foreignkey')
    op.drop_constraint(None, 'exam', type_='foreignkey')
    # ### end Alembic commands ###