This is a task to check your skills in Python and SQL.
It is a simplified version of a real task in our project.

Create a public fork of this repository and send us a link to your fork when you are done.

# Task

We have millions of job postings crawled from the internet and want to calculate some statistics about days to hire.

Job posting structure:

```python
@dataclass
class JobPosting:
    id: str
    title: str
    standard_job_id: str
    country_code: Optional[str] = None
    days_to_hire: Optional[int] = None
```

- `standard_job_id` -- all job postings are assigned to a standard job. It is a job title normalized to a common form,
  e.g. "Software Engineer" and "Software Developer" are both assigned to "Software Engineer".
- `country_code` -- country code in ISO 3166-1 alpha-2 format. 
  It can be `None` if we can't determine the country.
- `days_to_hire` -- a number of days between posting date and hire date. 
  It can be `None` if a job posting is not hired yet.

## 1. Create a table in the database to store "days to hire" statistics. 

- Statistics should be per country(also global for the world) and per standard job.
- It should contain average, minimum, and maximum days to hire.
- Also, it should contain a number of job postings used to calculate the average. 
We use this value to measure statistics quality. If the number of job postings is small, values can be inaccurate.

You can add SQLAlchemy model to `home_task.models` module and generate a migration with:

    alembic revision --autogenerate -m "<description>"

## 2. Write a CLI script to calculate "days to hire" statistics and store it in a created table.

`days_to_hire` can contain potentially invalid values, because it is quite difficult to gather this information.
For example, 1 day in most cases means that job posting was closed and reopened without real hiring.
Large values can be caused by incorrect parsing of dates. 
So we want to cut lowest and highest percentiles of `days_to_hire` before calculating average.

- Minimum days to hire is 10 percentile.
- Maximum days to hire is 90 percentile.
- Average days to hire is an average of **remaining values after cutting 10 and 90 percentiles**.
- Number of job postings is a number of rows used to calculate an average.
- Do not save resulted row if a number of job postings is less than 5. 
  Allow passing this threshold as a parameter.
- For each country and standard job create a separate row in a table.
- Also, create a row for world per standard job. 
  Job postings with `country_code` equal to `NULL` should be included in this calculation.
- Overwrite existing rows in the table. We need only the latest statistics.

## 3. Create REST API with one endpoint to get "days to hire" statistics.

- Endpoint should accept `standard_job_id` and `country_code` as request parameters.
- If `country_code` is not specified, return statistics for the world.

Response example:

    {
        "standard_job_id": "5affc1b4-1d9f-4dec-b404-876f3d9977a0",
        "country_code": "DE",
        "min_days": 11.0,
        "avg_days": 50.5,
        "max_days": 80.9,
        "job_postings_number": 100,
    }

# Some information to consider

- Use FastAPI for REST API.
- It is not necessary to use ORM. You can use raw SQL queries. 
  Connection to the database is available in `home_task.db` module.
- In a real environment code can fail at any moment with some probability. The database should not be corrupted.
- In a real database we have millions of rows, so you can't load all of them into memory at once.
- In a real environment new job postings are continuously added to the database. 
  For simplicity, you can assume that data is frozen and will not change during script execution.

# Installation

Install packages with poetry:

    python3 -m venv venv
    . venv/bin/activate
    pip install poetry
    POETRY_VIRTUALENVS_CREATE=false poetry install

Create database:

    docker-compose up -d
    docker cp migrations/data/ hrf_universe_postgres:/tmp
    alembic upgrade head
