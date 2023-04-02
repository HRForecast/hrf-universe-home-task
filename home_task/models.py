from _decimal import Decimal
from dataclasses import dataclass
from typing import Optional

from sqlalchemy import (
    Column,
    Integer,
    String,
    Table,
    DECIMAL,
)
from sqlalchemy.orm import registry

mapper_registry = registry()


class Model:
    pass


@mapper_registry.mapped
@dataclass
class StandardJobFamily(Model):
    __table__ = Table(
        "standard_job_family",
        mapper_registry.metadata,
        Column("id", String, nullable=False, primary_key=True),
        Column("name", String, nullable=False),
        schema="public",
    )

    id: str
    name: str


@mapper_registry.mapped
@dataclass
class StandardJob(Model):
    __table__ = Table(
        "standard_job",
        mapper_registry.metadata,
        Column("id", String, nullable=False, primary_key=True),
        Column("name", String, nullable=False),
        Column("standard_job_family_id", String, nullable=False),
        schema="public",
    )

    id: str
    name: str
    standard_job_family_id: str


@mapper_registry.mapped
@dataclass
class JobPosting(Model):
    __table__ = Table(
        "job_posting",
        mapper_registry.metadata,
        Column("id", String, nullable=False, primary_key=True),
        Column("title", String, nullable=False),
        Column("standard_job_id", String, nullable=False),
        Column("country_code", String, nullable=True),
        Column("days_to_hire", Integer, nullable=True),
        schema="public",
    )

    id: str
    title: str
    standard_job_id: str
    country_code: Optional[str] = None
    days_to_hire: Optional[int] = None


@mapper_registry.mapped
@dataclass
class HireStatistic(Model):
    __table__ = Table(
        "hire_statistic",
        mapper_registry.metadata,
        Column("id", String, nullable=False, primary_key=True),
        Column("minimum_days_to_hire", DECIMAL, nullable=False),
        Column("average_days_to_hire", DECIMAL, nullable=False),
        Column("maximum_days_to_hire", DECIMAL, nullable=False),
        Column("job_postings_number", Integer, nullable=False),
        Column("standard_job_id", String, nullable=False),
        Column("country_code", String, nullable=True),
        schema="public",
    )

    id: str
    minimum_days_to_hire: Decimal
    average_days_to_hire: Decimal
    maximum_days_to_hire: Decimal
    job_postings_number: int
    standard_job_id: str
    country_code: Optional[str] = None
