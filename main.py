from pathlib import Path

from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles

from app.api.routers import router, templates, BASE_DIR
from app.data_mining.read_csv import load_industry, load_review

app = FastAPI(title="行业与评论数据可视化平台", version="1.0.0")

# 全局挂载静态文件
app.mount("/static", StaticFiles(directory=BASE_DIR / "static"), name="static")

# 注册路由
app.include_router(router)


@app.get("/", response_class=HTMLResponse, name="index")
def index(request: Request):
    """入口首页：两张 CSV 的核心指标 + 双入口卡片"""

    industry = load_industry(Path(BASE_DIR / "data/csv/industry_chart_data.csv"))
    review = load_review(Path(BASE_DIR / "data/csv/review_chart_data.csv"))
    return templates.TemplateResponse(
        request,
        "index.jinja2",
        {
            "industry": industry,
            "review": review,
        },
    )
