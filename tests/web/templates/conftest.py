from pathlib import Path

import pytest
from jinja2 import Environment, FileSystemLoader, select_autoescape


@pytest.fixture
def jinja_env():
    templates_dir = Path(__file__).parent.parent.parent.parent / "templates"
    return Environment(
        loader=FileSystemLoader(templates_dir),
        autoescape=select_autoescape(["html", "jinja2"]),
    )


# ── 公共 mock 上下文（url_for / request） ──────────────
@pytest.fixture
def template_context():
    return {
        "url_for": lambda name, **kw: {
            "index": "/",
            "industry": "/industry",
            "review": "/review",
        }.get(name, "/"),
        "request": None,
    }
