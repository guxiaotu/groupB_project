from pathlib import Path

import pandas as pd


def load_industry(path: Path) -> dict:
    """按 chart_type 分组，输出可直接喂给 ECharts 的 JSON 结构"""
    df = pd.read_csv(path)
    payload: dict[str, dict] = {}
    for ctype, g in df.groupby("chart_type"):
        g = g.sort_values("sort_order").reset_index(drop=True)
        payload[ctype] = {
            "labels": g["item_label"].astype(str).tolist(),
            "rows": g.to_dict("records"),
        }
    total_products = int(df["product_count"].sum())
    total_sales = int(df["monthly_sales"].sum())
    total_revenue = round(float(df["monthly_revenue"].sum()), 2)
    return {
        "payload": payload,
        "summary": {
            "total_products": total_products,
            "total_monthly_sales": total_sales,
            "total_monthly_revenue": total_revenue,
            "brand_count": int((df["chart_type"] == "brand_concentration").sum()),
        },
    }


def load_review(path: Path) -> dict:
    """按 analysis_type 分组：negative / positive / motivation"""
    df = pd.read_csv(path)
    payload: dict[str, dict] = {}
    for atype, g in df.groupby("analysis_type"):
        g = g.sort_values("sort_order").reset_index(drop=True)
        payload[atype] = {
            "labels": g["topic_name"].astype(str).tolist(),
            "rows": g.to_dict("records"),
        }
    # 三类样本总量
    samples = (
        df.drop_duplicates("analysis_type")
        .set_index("analysis_type")["sample_count"]
        .to_dict()
    )

    return {
        "payload": payload,
        "summary": {
            "negative_total": int(
                df[df.analysis_type == "negative"]["matched_reviews"].sum()
            ),
            "positive_total": int(
                df[df.analysis_type == "positive"]["matched_reviews"].sum()
            ),
            "motivation_total": int(
                df[df.analysis_type == "motivation"]["matched_reviews"].sum()
            ),
            "sample_negative": int(samples.get("negative", 0)),
            "sample_positive": int(samples.get("positive", 0)),
            "sample_motivation": int(samples.get("motivation", 0)),
        },
    }
