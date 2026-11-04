import polars as pl

from app.model import Industry, Review


async def query_review() -> Review:
    """按 analysis_type 分组：negative / positive / motivation"""
    df = pl.read_csv("")
    payload: dict[str, dict] = {}
    for (atype,), g in df.group_by("analysis_type"):
        g = g.sort("sort_order")
        payload[atype] = {
            "labels": g["topic_name"].cast(pl.String).to_list(),
            "rows": g.to_dicts(),
        }

    # 修正：使用 dict(zip(...)) 生成 {'negative': 10, 'positive': 20, ...}
    unique_df = df.unique(subset="analysis_type")
    samples = dict(zip(unique_df["analysis_type"], unique_df["sample_count"]))

    # 1. 一次性聚合计算三类 matched_reviews 总和
    totals = df.select(
        [
            pl.col("matched_reviews")
            .filter(pl.col("analysis_type") == "negative")
            .sum()
            .fill_null(0)
            .alias("negative"),
            pl.col("matched_reviews")
            .filter(pl.col("analysis_type") == "positive")
            .sum()
            .fill_null(0)
            .alias("positive"),
            pl.col("matched_reviews")
            .filter(pl.col("analysis_type") == "motivation")
            .sum()
            .fill_null(0)
            .alias("motivation"),
        ]
    ).to_dicts()[0]

    # 2. 构建返回对象
    return(
        Review(
            payload=payload,
            summary=Review.Summary(
                negative_total=totals["negative"],
                positive_total=totals["positive"],
                motivation_total=totals["motivation"],
                sample_negative=samples.get("negative", 0),
                sample_positive=samples.get("positive", 0),
                sample_motivation=samples.get("motivation", 0),
            ),
        )
    )


async def query_industry() -> Industry:
    pass
