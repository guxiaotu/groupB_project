from typing import Annotated

from fastapi import APIRouter, Depends, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from app.api import load_dashboard_data
from app.config import BASE_DIR
from app.model.view import DashboardData
from app.service import save_csv

router = APIRouter()

# 模板
templates = Jinja2Templates(directory=BASE_DIR / "templates")


@router.get(path="/industry", response_class=HTMLResponse, name="industry")
async def industry(
    request: Request,
    dashboard_data: Annotated[DashboardData, Depends(load_dashboard_data)],
):
    """行业分析页：价格带 / 品牌集中度 / 上架时间分布"""
    return templates.TemplateResponse(
        request=request,
        name="industry.jinja2",
        context={"industry": dashboard_data.industry},
    )


@router.get(path="/review", response_class=HTMLResponse, name="review")
async def review(
    request: Request,
    dashboard_data: Annotated[DashboardData, Depends(load_dashboard_data)],
):
    """评论分析页：负面 / 正面 / 购买动机主题"""
    return templates.TemplateResponse(
        request=request,
        name="review.jinja2",
        context={"review": dashboard_data.review},
    )


@router.get(path="/api/webhook/{file_name}")
async def db_update(file_name: str):
    await save_csv(file_name)
