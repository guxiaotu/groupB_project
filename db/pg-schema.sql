CREATE TABLE industry_chart_data
(
    -- -------- 主键：PG 17 官方推荐 IDENTITY --------
    id                           BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,

    -- -------- 维度 --------
    chart_type
                                 VARCHAR(64)  NOT NULL,
    item_key                     VARCHAR(128) NOT NULL,
    item_label                   VARCHAR(256) NOT NULL,

    -- -------- 排序与数量（三类分组都有值）--------
    sort_order                   INTEGER      NOT NULL DEFAULT 0,
    sample_count                 INTEGER      NOT NULL DEFAULT 0,

    -- -------- 数量口径 --------
    product_count                INTEGER,
    cumulative_product_count     INTEGER,

    -- -------- 销量口径（price / brand）--------
    valid_sales_count            INTEGER,
    monthly_sales                BIGINT,
    avg_monthly_sales            DECIMAL(12, 2),
    sales_rank                   INTEGER,
    sales_cumulative_share_pct   DECIMAL(9, 6),

    -- -------- 销售额口径（price / brand）--------
    valid_revenue_count          INTEGER,
    monthly_revenue              DECIMAL(18, 2),
    revenue_rank                 INTEGER,
    revenue_cumulative_share_pct DECIMAL(9, 6),

    -- -------- 评分口径（仅 price）--------
    valid_rating_count           INTEGER,
    avg_rating                   DECIMAL(5, 4),
    rating_score_pct             DECIMAL(9, 6),

    -- -------- 占比口径（price / brand）--------
    sales_share_pct              DECIMAL(9, 6),
    revenue_share_pct            DECIMAL(9, 6),
    avg_sales_share_pct          DECIMAL(9, 6),
    sample_share_pct             DECIMAL(9, 6),

    -- -------- 快照：带时区，PG 最佳实践 --------
    snapshot_at                  TIMESTAMPTZ  NOT NULL DEFAULT NOW
                                                               (
                                                               ),
    CONSTRAINT uq_industry_snapshot_dim_key
        UNIQUE (snapshot_at, chart_type, item_key)

) PARTITION BY RANGE(snapshot_at);

-- 对齐 main.py 读取路径：按 chart_type 分组、按 sort_order 排序
CREATE INDEX IF NOT EXISTS idx_industry_chart_type_order
    ON industry_chart_data (chart_type, sort_order);

CREATE INDEX IF NOT EXISTS idx_industry_item_key
    ON industry_chart_data (item_key);

-- snapshot_at 已作为分区键，分区内局部索引由 PG 自动维护，
-- 这里不再单独建全局索引，避免大表冗余开销。

CREATE TABLE review_chart_data
(
    id              BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    analysis_type   VARCHAR(32)  NOT NULL,
    topic_id        VARCHAR(64)  NOT NULL,
    topic_name      VARCHAR(200) NOT NULL,
    sort_order      INTEGER      NOT NULL DEFAULT 0,
    matched_reviews INTEGER      NOT NULL,
    sample_count    INTEGER      NOT NULL,
    share_pct       DECIMAL(9, 6),
    reason          VARCHAR(200) NOT NULL,
    snapshot_at     TIMESTAMPTZ  NOT NULL DEFAULT NOW(),
    UNIQUE (snapshot_at, analysis_type, topic_id)
);

CREATE INDEX IF NOT EXISTS ix_review_analysis_type
    ON review_chart_data (analysis_type);

CREATE INDEX IF NOT EXISTS ix_review_topic_id
    ON review_chart_data (topic_id);

-- snapshot_at 上的等值/范围过滤由 UNIQUE 约束的索引覆盖，无需再建单列索引