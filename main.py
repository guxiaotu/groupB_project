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

# csv文件存到 app.state（放在 lifespan 里），一次在加载数据到内存中
csv_dir = BASE_DIR / "data/csv"
app.state.industry = load_industry(csv_dir / "industry_chart_data.csv")
app.state.review = load_review(csv_dir / "review_chart_data.csv")


@app.get(path="/", response_class=HTMLResponse, name="index")
def index(request: Request):
    """入口首页：两张 CSV 的核心指标 + 双入口卡片"""

    return templates.TemplateResponse(
        request=request,
        name="index.jinja2",
        context={
            "industry": request.app.state.industry,
            "review": request.app.state.review,
        },
    )
