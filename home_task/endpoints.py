import logging
from typing import Optional

from fastapi import (
    APIRouter,
    Depends,
)
from sqlalchemy.orm import Session
from starlette.responses import JSONResponse

from home_task.dao import HireStatisticDAO
from home_task.db import get_session
from home_task.schemas import HireStatisticsSchema

router = APIRouter()
logger = logging.getLogger(__name__)


@router.get("/get-hired-days", status_code=200, response_model=HireStatisticsSchema,
            description="Get hire days statistic")
async def get_hired_days(standard_job_id: str, country_code: Optional[str] = None, db: Session = Depends(get_session)):
    dao = HireStatisticDAO(standard_job_id, db, country_code)
    schema = HireStatisticsSchema.from_orm(dao.get_statistic()[0])
    return JSONResponse(status_code=200, content=schema.dict())
