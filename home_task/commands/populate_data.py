"""
CLI script that populates HireStatistic table
to run command use: python -m home_task.commands.populate_data --jobs_threshold=5 from root directory
"""

import argparse
import uuid

from sqlalchemy import select, func, distinct
from sqlalchemy.orm import Query

from home_task.db import get_session
from home_task.models import JobPosting, HireStatistic


def populate_statistic(jobs_threshold: int = 5) -> None:
    statistic_data = []
    country_codes_query = select([distinct(JobPosting.country_code)])
    job_ids_query = select([distinct(JobPosting.standard_job_id)])
    session = get_session()

    with session.begin():
        country_codes_result = session.execute(country_codes_query)
        job_ids_result = session.execute(job_ids_query)

        country_codes = [row[0] for row in country_codes_result]
        job_ids = [row[0] for row in job_ids_result]

        for job_id in job_ids:
            for country_code in country_codes:
                job_posting_query = prepare_filtered_job_posting_query(country_code, job_id, jobs_threshold)
                result = session.execute(job_posting_query)
                row = result.fetchone()
                if row:
                    data = {
                        **row._asdict(),
                        "standard_job_id": job_id,
                        "country_code": country_code,
                        "id": str(uuid.uuid4())
                    }
                    statistic_data.append(HireStatistic(**data))

            session.query(HireStatistic).delete()
            session.add_all(statistic_data)


def prepare_filtered_job_posting_query(country_code: str, job_id: str, jobs_threshold: int) -> Query:
    subquery = select([
        JobPosting.days_to_hire,
        func.ntile(10).over(order_by=JobPosting.days_to_hire).label('percentile')
    ]).where(
        JobPosting.days_to_hire != None,
        JobPosting.standard_job_id == job_id
    )

    if country_code is not None:
        subquery = subquery.where(
            JobPosting.country_code == country_code,
        )

    subquery = subquery.subquery()

    query = select([
        func.min(subquery.c.days_to_hire).label("minimum_days_to_hire"),
        func.avg(subquery.c.days_to_hire).label("average_days_to_hire"),
        func.max(subquery.c.days_to_hire).label("maximum_days_to_hire"),
        func.count(subquery.c.days_to_hire).label("job_postings_number"),

    ]).where(
        (subquery.c.percentile >= 2) & (subquery.c.percentile <= 9)
    ).having(
        func.count(subquery.c.days_to_hire) > jobs_threshold
    )
    return query


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='CLI script that populates HireStatistic table')
    parser.add_argument('--jobs_threshold', type=int, nargs='+',
                        help="to determine threshold for job_posting table jobs, is amount of jobs"
                             " less than [jobs_threshold], script won't include these jobs into statistic")
    args = parser.parse_args()
    threshold = args.jobs_threshold.pop(0) if args.jobs_threshold else 5
    populate_statistic(threshold)
