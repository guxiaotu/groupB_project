from pathlib import Path

import pandas as pd

from app.model.view.industry import Industry
from app.model.view.review import Review


def load_industry(path: Path) -> Industry:
    """按 chart_type 分组，输出可直接喂给 ECharts 的 JSON 结构"""
    df = pd.read_csv(path)
    payload: dict[str, dict] = {}
    for ctype, g in df.groupby("chart_type"):
        g = g.sort_values("sort_order").reset_index(drop=True)
        payload[ctype] = {
            "labels": g["item_label"].astype(str).tolist(),
            "rows": g.to_dict("records"),
        }

    return Industry(
        payload=payload,
        summary=Industry.Summary(
            total_products=df["product_count"].sum(),
            total_monthly_sales=df["monthly_sales"].sum(),
            total_monthly_revenue=df["monthly_revenue"].sum(),
            brand_count=(df["chart_type"] == "brand_concentration").sum(),
        ))


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

    return Review(
        payload=payload,
        summary=Review.Summary(
            negative_total=df[df.analysis_type == "negative"]["matched_reviews"].sum(),
            positive_total=df[df.analysis_type == "positive"]["matched_reviews"].sum(),
            motivation_total=df[df.analysis_type == "motivation"]["matched_reviews"].sum(),
            sample_negative=samples.get("negative", 0),
            sample_positive=samples.get("positive", 0),
            sample_motivation=samples.get("motivation", 0)
        ))
