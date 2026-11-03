from fastapi import FastAPI, Request
from starlette.responses import HTMLResponse
from starlette.staticfiles import StaticFiles

from app.api.routers import BASE_DIR, templates
from app.api.routers import router as api_router
from app.view.query_data import query_industry, query_review

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
            "industry": await query_industry(),
            "review": await query_review(),
        },
    )
