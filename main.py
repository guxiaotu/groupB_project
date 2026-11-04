from fastapi import FastAPI, Request
from starlette.responses import HTMLResponse
from starlette.staticfiles import StaticFiles

from app.config import BASE_DIR
from app.api import templates
from app.api.routers import router as api_router
from app.model import IndustryChartData, ReviewChartData
from app.service import query_data

app = FastAPI(title="智能商品统计分析系统")

# 全局挂载静态文件
app.mount("/static", StaticFiles(directory=BASE_DIR / "static"), name="static")

# 注册路由
app.include_router(api_router)


# 模板
@app.get(path="/", response_class=HTMLResponse, name="index")
async def index(request: Request):
    """入口首页：两张 CSV 的核心指标 + 双入口卡片"""

    return templates.TemplateResponse(
        request=request,
        name="index.jinja2",
        context={
            "industry": await query_data(IndustryChartData),
            "review": await query_data(ReviewChartData),
        },
    )
