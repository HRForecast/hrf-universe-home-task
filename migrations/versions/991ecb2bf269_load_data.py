"""Load data

Revision ID: 991ecb2bf269
Revises: 21f6a5adb97e
Create Date: 2023-03-13 10:06:42.751105

"""
import os

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '991ecb2bf269'
down_revision = '21f6a5adb97e'
branch_labels = None
depends_on = None


def upgrade() -> None:
    dir_name = os.path.dirname(__file__)

    file_name = os.path.join(dir_name, '/tmp/data/standard_job_family.csv')
    op.execute(f"COPY public.standard_job_family FROM '{file_name}' WITH CSV;", execution_options=None)

    file_name = os.path.join(dir_name, '/tmp/data/standard_job.csv')
    op.execute(f"COPY public.standard_job FROM '{file_name}' WITH CSV;", execution_options=None)


def downgrade() -> None:
    op.execute("DELETE FROM public.standard_job")
    op.execute("DELETE FROM public.standard_job_family")
