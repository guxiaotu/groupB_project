from pathlib import Path

from fastapi import APIRouter
from starlette.templating import Jinja2Templates

router = APIRouter()

BASE_DIR = Path(__file__).resolve().parent.parent.parent.parent

# 模板
templates = Jinja2Templates(directory=BASE_DIR / "templates")
