from typing import Optional

from sqlalchemy import select
from sqlalchemy.orm import Session

from home_task.models import HireStatistic


class HireStatisticDAO:
    def __init__(self, standard_job_id: str, session: Session, country_code: str = None):
        self.job_id: str = standard_job_id
        self.country_code: Optional[str] = country_code
        self.session: Session = session

    def get_statistic(self):
        query = select([HireStatistic]).where(HireStatistic.standard_job_id == self.job_id)
        if self.country_code is not None:
            query = query.where(
                HireStatistic.country_code == self.country_code,
            )
        result = self.session.execute(query)
        return result.fetchone()
