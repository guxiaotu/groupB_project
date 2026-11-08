from typing import Annotated
from urllib.parse import unquote

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


@router.post(path="/webhook", description="silo更新csv文件")
async def db_update(request: Request):
    payload = await request.json()

    # 取 object key
    records = payload.get("Records", [])
    if not records:
        return {"error": "no records"}

    rec = records[0]
    raw_key = rec["s3"]["object"]["key"]

    # URL 解码
    object_key = unquote(raw_key)

    # 取完整文件名（不去掉后缀）
    file_name = object_key.rsplit("/", 1)[-1]
    await save_csv(file_name)
    return {"status": "ok"}