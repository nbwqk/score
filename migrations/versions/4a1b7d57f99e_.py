"""empty message

Revision ID: 4a1b7d57f99e
Revises: 0e27a5b4a8e2
Create Date: 2021-06-23 17:46:24.867214

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '4a1b7d57f99e'
down_revision = '0e27a5b4a8e2'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_foreign_key(None, 'exam', 'clazz', ['clazz_id'], ['id'])
    op.create_foreign_key(None, 'exam', 'course', ['course_id'], ['id'])
    op.create_foreign_key(None, 'exam', 'user', ['user_id'], ['id'])
    op.create_foreign_key(None, 'result', 'exam', ['exam_id'], ['id'])
    op.create_foreign_key(None, 'student_score', 'exam', ['exam_id'], ['id'])
    op.add_column('user', sa.Column('isadmin', sa.Boolean(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('user', 'isadmin')
    op.drop_constraint(None, 'student_score', type_='foreignkey')
    op.drop_constraint(None, 'result', type_='foreignkey')
    op.drop_constraint(None, 'exam', type_='foreignkey')
    op.drop_constraint(None, 'exam', type_='foreignkey')
    op.drop_constraint(None, 'exam', type_='foreignkey')
    # ### end Alembic commands ###
