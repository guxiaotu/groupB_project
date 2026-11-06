from contextlib import asynccontextmanager

from fastapi import FastAPI, Request
from starlette.responses import HTMLResponse
from starlette.staticfiles import StaticFiles

from app.api import templates
from app.api.routers import router as api_router
from app.config import BASE_DIR
from app.view import get_industry, get_review


@asynccontextmanager
async def lifespan(app: FastAPI):
    app.state.industry_view = await get_industry()
    app.state.review_view = await get_review()
    yield


application = FastAPI(title="智能商品统计分析系统", lifespan=lifespan)

# 全局挂载静态文件
application.mount("/static", StaticFiles(directory=BASE_DIR / "static"), name="static")

# 注册路由
application.include_router(api_router)


# 模板
@application.get(path="/", response_class=HTMLResponse, name="index")
async def index(request: Request):
    """入口首页：两张 CSV 的核心指标 + 双入口卡片"""

    return templates.TemplateResponse(
        request=request,
        name="index.jinja2",
        context={
            "industry": request.app.state.industry_view,
            "review": request.app.state.review_view,
        },
    )