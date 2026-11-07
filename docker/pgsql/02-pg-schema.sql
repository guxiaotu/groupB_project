DROP TABLE IF EXISTS industry_chart_data;
CREATE TABLE industry_chart_data
(
    -- -------- 维度 --------
    chart_type                   VARCHAR(64)  NOT NULL,
    item_key                     VARCHAR(128) NOT NULL,
    item_label                   VARCHAR(256) NOT NULL,

    -- -------- 排序与数量（三类分组都有值）--------
    sort_order                   INTEGER      NOT NULL,
    sample_count                 INTEGER,

    -- -------- 数量口径 --------
    product_count                INTEGER,
    cumulative_product_count     INTEGER,

    -- -------- 销量口径（price / brand）--------
    valid_sales_count            INTEGER,
    monthly_sales                BIGINT,
    avg_monthly_sales            NUMERIC(12, 2),
    sales_rank                   INTEGER,
    sales_cumulative_share_pct   NUMERIC(9, 6),

    -- -------- 销售额口径（price / brand）--------
    valid_revenue_count          INTEGER,
    monthly_revenue              NUMERIC(18, 2),
    revenue_rank                 INTEGER,
    revenue_cumulative_share_pct NUMERIC(9, 6),

    -- -------- 评分口径（仅 price）--------
    valid_rating_count           INTEGER,
    avg_rating                   NUMERIC(5, 4),
    rating_score_pct             NUMERIC(9, 6),

    -- -------- 占比口径（price / brand）--------
    sales_share_pct              NUMERIC(9, 6),
    revenue_share_pct            NUMERIC(9, 6),
    avg_sales_share_pct          NUMERIC(9, 6),
    sample_share_pct             NUMERIC(9, 6)
) USING columnar;

-- ===== 列注释 =====
COMMENT ON COLUMN industry_chart_data.chart_type IS '分组维度';
COMMENT ON COLUMN industry_chart_data.item_key IS '业务唯一键';
COMMENT ON COLUMN industry_chart_data.item_label IS '展示标签';
COMMENT ON COLUMN industry_chart_data.sort_order IS '排序与数量';
COMMENT ON COLUMN industry_chart_data.sample_count IS '该分组样本量';
COMMENT ON COLUMN industry_chart_data.product_count IS '该分组产品数';
COMMENT ON COLUMN industry_chart_data.cumulative_product_count IS '累计产品数';
COMMENT ON COLUMN industry_chart_data.valid_sales_count IS '有有效销量数据的产品数';
COMMENT ON COLUMN industry_chart_data.monthly_sales IS '月销量合计';
COMMENT ON COLUMN industry_chart_data.avg_monthly_sales IS '平均月销量';
COMMENT ON COLUMN industry_chart_data.sales_rank IS '销量排名';
COMMENT ON COLUMN industry_chart_data.sales_cumulative_share_pct IS '销量累计占比%';
COMMENT ON COLUMN industry_chart_data.valid_revenue_count IS '有有效销售额数据的产品数';
COMMENT ON COLUMN industry_chart_data.monthly_revenue IS '月销售额合计';
COMMENT ON COLUMN industry_chart_data.revenue_rank IS '销售额排名';
COMMENT ON COLUMN industry_chart_data.revenue_cumulative_share_pct IS '销售额累计占比%';
COMMENT ON COLUMN industry_chart_data.valid_rating_count IS '有有效评分数据的产品数';
COMMENT ON COLUMN industry_chart_data.avg_rating IS '平均评分 0~5';
COMMENT ON COLUMN industry_chart_data.rating_score_pct IS '评分达标占比%';
COMMENT ON COLUMN industry_chart_data.sales_share_pct IS '销量占比%';
COMMENT ON COLUMN industry_chart_data.revenue_share_pct IS '销售额占比%';
COMMENT ON COLUMN industry_chart_data.avg_sales_share_pct IS '单品均销量占比%';
COMMENT ON COLUMN industry_chart_data.sample_share_pct IS '该分组样本总量占比%';

DROP TABLE IF EXISTS review_chart_data;
CREATE TABLE review_chart_data
(
    analysis_type   VARCHAR(32)  NOT NULL,
    topic_id        VARCHAR(64)  NOT NULL,
    topic_name      VARCHAR(200) NOT NULL,
    sort_order      INTEGER      NOT NULL,
    matched_reviews INTEGER,
    sample_count    INTEGER,
    share_pct       NUMERIC(9, 6),
    reason          VARCHAR(200)
) USING columnar;

-- ===== 列注释 =====
COMMENT ON COLUMN review_chart_data.analysis_type IS '分组大类：negative / motivation / positive';
COMMENT ON COLUMN review_chart_data.topic_id IS '业务唯一键，如 negative_4';
COMMENT ON COLUMN review_chart_data.topic_name IS '展示标签，如 做工与耐用性';
COMMENT ON COLUMN review_chart_data.sort_order IS '排序';
COMMENT ON COLUMN review_chart_data.matched_reviews IS '命中评论数';
COMMENT ON COLUMN review_chart_data.sample_count IS '该分组样本总量';
COMMENT ON COLUMN review_chart_data.share_pct IS '占比%';
COMMENT ON COLUMN review_chart_data.reason IS '原因描述';