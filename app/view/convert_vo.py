from collections import defaultdict
from decimal import Decimal
from typing import Any

from app.model.entity import IndustryChartData, ReviewChartData
from app.model.view import Industry, Review
from app.service import query_data


def _to_json_compatible(obj: Any) -> Decimal:
    """
    Decimal序列化
    """
    if isinstance(obj, Decimal):
        return float(obj)
    if isinstance(obj, dict):
        return {k: _to_json_compatible(v) for k, v in obj.items()}
    if isinstance(obj, list):
        return [_to_json_compatible(v) for v in obj]
    return obj


async def get_review() -> Review:
    """
    按 analysis_type 分组：negative / positive / motivation
    """
    payload: dict[str, dict] = {}

    # 聚合用
    negative_total: int = 0
    positive_total: int = 0
    motivation_total: int = 0

    # sample_count 按 analysis_type 去重后取（等价于 drop_duplicates）
    sample_map: dict[str, int] = {}

    industry_list: list[ReviewChartData] = await query_data(ReviewChartData)

    # 按 analysis_type 分组
    grouped: dict[str, list[ReviewChartData]] = defaultdict(list)
    for item in industry_list:
        grouped[item.analysis_type].append(item)

    for atype, items in grouped.items():
        # 按 sort_order 排序
        items = sorted(items, key=lambda x: x.sort_order)

        labels: list[str] = []
        rows: list[dict] = []

        seen_sample = False

        for item in items:
            labels.append(item.topic_name)

            # 转 dict + Decimal → float
            rows.append(_to_json_compatible(item.model_dump()))

            # matched_reviews 聚合
            if item.matched_reviews is not None:
                if atype == "negative":
                    negative_total += item.matched_reviews
                elif atype == "positive":
                    positive_total += item.matched_reviews
                elif atype == "motivation":
                    motivation_total += item.matched_reviews

            # sample_count 只取一次（等价于 drop_duplicates("analysis_type")）
            if not seen_sample and item.sample_count is not None:
                sample_map[atype] = item.sample_count
                seen_sample = True

        payload[atype] = {
            "labels": labels,
            "rows": rows,
        }

    return Review(
        payload=payload,
        summary=Review.Summary(
            negative_total=negative_total,
            positive_total=positive_total,
            motivation_total=motivation_total,
            sample_negative=sample_map.get("negative", 0),
            sample_positive=sample_map.get("positive", 0),
            sample_motivation=sample_map.get("motivation", 0),
        ),
    )


async def get_industry() -> Industry:
    """
    按 chart_type 分组，输出可直接喂给 ECharts 的 JSON 结构
    """

    payload: dict[str, dict] = {}
    brand_count: int = 0
    total_products: int = 0
    total_monthly_sales: int = 0
    total_monthly_revenue: Decimal = Decimal()

    review_list: list[IndustryChartData] = await query_data(IndustryChartData)

    # 按 chart_type 分组
    grouped: dict[str, list[IndustryChartData]] = defaultdict(list)
    for item in review_list:
        grouped[item.chart_type].append(item)

    for chart_type, items in grouped.items():
        # 按 sort_order 排序（等价于 pandas sort_values）
        items = sorted(items, key=lambda x: x.sort_order)

        if chart_type == "brand_concentration":
            brand_count += len(items)

        labels: list[str] = []
        rows: list[dict] = []

        for item in items:
            labels.append(item.item_label)

            # 将 SQLModel 对象转为 dict（等价于 df.to_dict("records")）
            rows.append(_to_json_compatible(item.model_dump()))

            # summary 聚合（只统计一次，避免重复计算）
            if item.product_count is not None:
                total_products += item.product_count

            if item.monthly_sales is not None:
                total_monthly_sales += item.monthly_sales

            if item.monthly_revenue is not None:
                total_monthly_revenue += item.monthly_revenue

        payload[chart_type] = {
            "labels": labels,
            "rows": rows,
        }

    return Industry(
        payload=payload,
        summary=Industry.Summary(
            total_products=total_products,
            total_monthly_sales=float(total_monthly_sales),
            total_monthly_revenue=float(total_monthly_revenue),
            brand_count=brand_count,
        ),
    )
