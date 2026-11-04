from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from app.config import BASE_DIR
from app.model import IndustryChartData, ReviewChartData
from app.service import query_data

router = APIRouter()

# 模板
templates = Jinja2Templates(directory=BASE_DIR / "templates")


@router.get(path="/industry", response_class=HTMLResponse, name="industry")
async def industry(request: Request):
    """行业分析页：价格带 / 品牌集中度 / 上架时间分布"""
    return templates.TemplateResponse(
        request=request,
        name="industry.jinja2",
        context={"industry": await query_data(IndustryChartData)},
    )


@router.get(path="/review", response_class=HTMLResponse, name="review")
async def review(request: Request):
    """评论分析页：负面 / 正面 / 购买动机主题"""
    return templates.TemplateResponse(
        request=request,
        name="review.jinja2",
        context={"review": await query_data(ReviewChartData)},
    )
