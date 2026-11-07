from typing import Annotated

from fastapi import APIRouter, Depends, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from app.config import BASE_DIR
from app.service import save_csv
from app.view import get_industry, get_review

router = APIRouter()

# 模板
templates = Jinja2Templates(directory=BASE_DIR / "templates")


@router.get(path="/industry", response_class=HTMLResponse, name="industry")
async def industry(
    request: Request, industry_view: Annotated[dict, Depends(get_industry)]
):
    """行业分析页：价格带 / 品牌集中度 / 上架时间分布"""
    return templates.TemplateResponse(
        request=request,
        name="industry.jinja2",
        context={"industry": industry_view},
    )


@router.get(path="/review", response_class=HTMLResponse, name="review")
async def review(request: Request, review_view: Annotated[dict, Depends(get_review)]):
    """评论分析页：负面 / 正面 / 购买动机主题"""
    return templates.TemplateResponse(
        request=request,
        name="review.jinja2",
        context={"review": review_view},
    )


@router.get(path="/api/webhook/{file_name}")
async def db_update(file_name: str):
    await save_csv(file_name)
