from pathlib import Path

from fastapi import Request, APIRouter
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from app.data_mining.read_csv import load_industry, load_review

router = APIRouter()

BASE_DIR = Path(__file__).resolve().parent.parent.parent

# 模板
templates = Jinja2Templates(directory=BASE_DIR / "templates")


@router.get("/industry", response_class=HTMLResponse, name="industry")
def industry(request: Request):
    """行业分析页：价格带 / 品牌集中度 / 上架时间分布"""
    return templates.TemplateResponse(
        request,
        "industry.jinja2",
        {
            "industry": load_industry(Path(BASE_DIR / "data/csv/industry_chart_data.csv")),
        },
    )


@router.get("/review", response_class=HTMLResponse, name="review")
def review(request: Request):
    """评论分析页：负面 / 正面 / 购买动机主题"""
    return templates.TemplateResponse(
        request,
        "review.jinja2",
        {"review": load_review(Path(BASE_DIR / "data/csv/review_chart_data.csv"))},
    )
