from fastapi import APIRouter, Body, Depends, Request

from app.middlewares import JWTBearer
from app.repositories import supabase
from app.schemas import Report, ReportInsert

router = APIRouter(prefix="/reports", tags=["Reports"])


@router.post("/new", dependencies=[Depends(JWTBearer())])
def create_report(request: Request, report: ReportInsert = Body(...)):
    res = supabase.table("reports").insert(json=report.model_dump()).execute()

    report_inserted = Report(**res.data[0])

    return {"data": report_inserted, "count": 1}