from typing import Optional

from pydantic import BaseModel


class HireStatisticsSchema(BaseModel):
    minimum_days_to_hire: float
    average_days_to_hire: float
    maximum_days_to_hire: float
    job_postings_number: int
    country_code: Optional[str]
    standard_job_id: str

    class Config:
        orm_mode = True
