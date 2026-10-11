CREATE TABLE IF NOT EXISTS industry_chart_data
(
    id                           BIGINT UNSIGNED PRIMARY KEY AUTO_INCREMENT,

    -- -------- 维度 --------
    chart_type                   VARCHAR(64)  NOT NULL,
    item_key                     VARCHAR(128) NOT NULL,
    item_label                   VARCHAR(256) NOT NULL,

    -- -------- 排序与数量（三类分组都有值）--------
    sort_order                   INTEGER      NOT NULL DEFAULT 0,
    sample_count                 INTEGER      NOT NULL DEFAULT 0,

    -- -------- 数量口径 --------
    product_count                INTEGER,       -- price / listing
    cumulative_product_count     INTEGER,       -- listing

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
    sample_share_pct             DECIMAL(9, 6), -- listing

    -- -------- 快照 --------
    snapshot_at                  TIMESTAMP    NOT NULL DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT uq_industry_snapshot_dim_key
        UNIQUE (snapshot_at, chart_type, item_key)
) ENGINE = InnoDB
  DEFAULT CHARSET = utf8mb4
  COLLATE = utf8mb4_0900_ai_ci;

-- 对齐原项目 main.py 的读取路径：按 chart_type 分组、按 sort_order 排序
CREATE INDEX idx_industry_chart_type_order ON industry_chart_data (chart_type, sort_order);
CREATE INDEX idx_industry_snapshot_at ON industry_chart_data (snapshot_at);
CREATE INDEX idx_industry_item_key ON industry_chart_data (item_key);


CREATE TABLE review_chart_data
(
    id              BIGINT UNSIGNED PRIMARY KEY AUTO_INCREMENT,
    analysis_type   VARCHAR(32)  NOT NULL,
    topic_id        VARCHAR(64)  NOT NULL,
    topic_name      VARCHAR(200) NOT NULL,
    sort_order      INTEGER      NOT NULL DEFAULT 0,
    matched_reviews INTEGER      NOT NULL,
    sample_count    INTEGER      NOT NULL,
    share_pct       DECIMAL(9, 6),
    reason          VARCHAR(200) NOT NULL,
    snapshot_at     TIMESTAMP    NOT NULL,
    UNIQUE (snapshot_at, analysis_type, topic_id)
) ENGINE = InnoDB
  DEFAULT CHARSET = utf8mb4
  COLLATE = utf8mb4_0900_ai_ci;

CREATE INDEX ix_review_analysis_type ON review_chart_data (analysis_type);
CREATE INDEX ix_review_topic_id ON review_chart_data (topic_id);
CREATE INDEX ix_review_snapshot_at ON review_chart_data (snapshot_at);