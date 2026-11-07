from typing import Annotated

from fastapi import Depends, FastAPI, Request
from starlette.responses import HTMLResponse
from starlette.staticfiles import StaticFiles

from app.api import load_dashboard_data, templates
from app.api.routers import router as api_router
from app.config import BASE_DIR
from app.model.view import DashboardData

app = FastAPI(title="智能商品统计分析系统")

# 全局挂载静态文件
app.mount("/static", StaticFiles(directory=BASE_DIR / "static"), name="static")

# 注册路由
app.include_router(api_router)


@app.get(path="/", response_class=HTMLResponse, name="index")
async def index(
    request: Request,
    dashboard_data: Annotated[DashboardData, Depends(load_dashboard_data)],
):
    """入口首页：两张 CSV 的核心指标 + 双入口卡片"""

    return templates.TemplateResponse(
        request=request,
        name="index.jinja2",
        context={"industry": dashboard_data.industry, "review": dashboard_data.review},
    )
