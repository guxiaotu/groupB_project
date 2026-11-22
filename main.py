import uvicorn
from typing import Annotated

from fastapi import Depends, FastAPI, Request
from starlette.responses import HTMLResponse
from starlette.staticfiles import StaticFiles

from app.api import templates
from app.api.routers import router as api_router
from app.config import BASE_DIR
from app.view import get_industry, get_review

app = FastAPI(title="智能商品统计分析系统")

# 全局挂载静态文件
app.mount("/static", StaticFiles(directory=BASE_DIR / "static"), name="static")

# 注册路由
app.include_router(api_router)


@app.get(path="/", response_class=HTMLResponse, name="index")
async def index(
    request: Request,
    industry_view: Annotated[dict, Depends(get_industry)],
    review_view: Annotated[dict, Depends(get_review)],
):
    """入口首页：两张 CSV 的核心指标 + 双入口卡片"""

    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={"industry": industry_view, "review": review_view},
    )


if __name__ == "__main__":
    # 开启 reload=True 热重载时，第一个参数必须传 "文件名:实例名" 字符串
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
