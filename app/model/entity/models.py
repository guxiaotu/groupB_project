import datetime as dt
from decimal import Decimal

from sqlmodel import SQLModel, Field


class IndustryChartData(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)

    # -------- 维度 --------
    chart_type: str = Field(description="分组维度")
    item_key: str = Field(description="业务唯一键")
    item_label: str = Field(description="展示标签")

    sort_order: int = Field(default=0, description="排序与数量")
    sample_count: int = Field(default=0, description="该分组样本量")

    product_count: int | None = Field(default=None, description="该分组产品数")
    cumulative_product_count: int | None = Field(default=None, description="累计产品数")

    valid_sales_count: int | None = Field(default=None, description="有有效销量数据的产品数")
    monthly_sales: int | None = Field(default=None, description="月销量合计")
    avg_monthly_sales: Decimal | None = Field(default=None)
    sales_rank: int | None = Field(default=None, description="销量排名")
    sales_cumulative_share_pct: Decimal | None = Field(default=None, description="销量累计占比 %")

    valid_revenue_count: int | None = Field(default=None, description="有有效销售额数据的产品数")
    monthly_revenue: Decimal | None = Field(default=None)
    revenue_rank: int | None = Field(default=None, description="销售额排名")
    revenue_cumulative_share_pct: Decimal | None = Field(default=None, description="销售额累计占比 %")

    valid_rating_count: int | None = Field(default=None, description="有有效评分数据的产品数")
    avg_rating: Decimal | None = Field(default=None, description="平均评分 0~5")
    rating_score_pct: Decimal | None = Field(default=None, description="评分达标占比 %")

    sales_share_pct: Decimal | None = Field(default=None, description="销量占比 %")
    revenue_share_pct: Decimal | None = Field(default=None, description="销售额占比 %")
    avg_sales_share_pct: Decimal | None = Field(default=None, description="单品均销量占比 %")

    sample_share_pct: Decimal | None = Field(default=None, description="样本占比 %")

    snapshot_at: dt.datetime = Field(default_factory=lambda: dt.datetime.now(dt.timezone.utc),
                                     description="数据快照时间，同快照+同维度+同业务键唯一")
