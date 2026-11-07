


# ── mock 数据 ──────────────────────────────────────────
def make_mock_industry():
    return {
        "summary": {
            "total_products": 12847,
            "total_monthly_sales": 523140,
            "total_monthly_revenue": 18472930.5,
            "brand_count": 312,
        },
        "payload": {
            "price_tier": {
                "rows": [
                    {
                        "item_label": "$0-25",
                        "product_count": 3200,
                        "monthly_sales": 120000,
                        "monthly_revenue": 2100000.0,
                        "avg_rating": 4.32,
                        "sales_share_pct": 22.9,
                        "revenue_share_pct": 11.4,
                    },
                    {
                        "item_label": "$25-50",
                        "product_count": 4100,
                        "monthly_sales": 180000,
                        "monthly_revenue": 6300000.0,
                        "avg_rating": 4.51,
                        "sales_share_pct": 34.4,
                        "revenue_share_pct": 34.1,
                    },
                ]
            },
            "brand_tier": {
                "rows": [
                    {
                        "item_label": "Brand A",
                        "product_count": 45,
                        "monthly_sales": 85000,
                        "monthly_revenue": 3200000.0,
                        "avg_rating": 4.7,
                        "sales_share_pct": 16.2,
                        "revenue_share_pct": 17.3,
                    },
                ]
            },
            "listing_month": {
                "rows": [
                    {
                        "item_label": "2024-01",
                        "product_count": 320,
                        "monthly_sales": None,
                        "monthly_revenue": None,
                        "avg_rating": None,
                        "sales_share_pct": None,
                        "revenue_share_pct": None,
                    },
                ]
            },
        },
    }


def test_industry_template_renders(jinja_env):
    industry = make_mock_industry()

    template = jinja_env.get_template("industry.jinja2")
    html = template.render(
        industry=industry,
        # ✅ mock url_for
        url_for=lambda name, **kwargs: {
            "industry": "/industry",
        }.get(name, "/"),
        # 如果 base.jinja2 里还用了 request
        request=None,
    )

    assert "行业分析" in html

    # ── 基本断言 ──────────────────────────────────────
    assert "行业分析" in html
    assert "12,847" in html  # total_products 格式化
    assert "价格带分布" in html
    assert "$0-25" in html
    assert "Brand A" in html
    assert "2024-01" in html

    # ── 关键字段不丢失 ─────────────────────────────────
    assert "chart_type" in html or "price_tier" in html

    # ── JS payload 注入成功 ───────────────────────────
    assert "window.PAYLOAD" in html
    assert "price_tier" in html

    print("✅ template rendered, length =", len(html))
