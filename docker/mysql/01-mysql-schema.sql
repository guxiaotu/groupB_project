-- 设置客户端连接使用的编码格式
SET NAMES utf8mb4 COLLATE utf8mb4_0900_ai_ci;

CREATE TABLE IF NOT EXISTS industry_chart_data
(
    id                           BIGINT UNSIGNED PRIMARY KEY AUTO_INCREMENT COMMENT '自增主键',

    -- -------- 维度 --------
    chart_type                   VARCHAR(64)  NOT NULL COMMENT '分组维度',
    item_key                     VARCHAR(128) NOT NULL COMMENT '业务唯一键',
    item_label                   VARCHAR(256) NOT NULL COMMENT '展示标签',

    -- -------- 排序与数量（三类分组都有值）--------
    sort_order                   INTEGER COMMENT '排序与数量',
    sample_count                 INTEGER COMMENT '该分组样本量',

    -- -------- 数量口径 --------
    product_count                INTEGER COMMENT '该分组产品数（price/listing）',
    cumulative_product_count     INTEGER COMMENT '累计产品数（listing）',

    -- -------- 销量口径（price / brand）--------
    valid_sales_count            INTEGER COMMENT '有有效销量数据的产品数',
    monthly_sales                BIGINT COMMENT '月销量合计',
    avg_monthly_sales            NUMERIC(12, 2) COMMENT '平均月销量',
    sales_rank                   INTEGER COMMENT '销量排名',
    sales_cumulative_share_pct   NUMERIC(9, 2) COMMENT '销量累计占比%',

    -- -------- 销售额口径（price / brand）--------
    valid_revenue_count          INTEGER COMMENT '有有效销售额数据的产品数',
    monthly_revenue              NUMERIC(18, 2) COMMENT '月销售额合计',
    revenue_rank                 INTEGER COMMENT '销售额排名',
    revenue_cumulative_share_pct NUMERIC(9, 2) COMMENT '销售额累计占比%',

    -- -------- 评分口径（仅 price）--------
    valid_rating_count           INTEGER COMMENT '有有效评分数据的产品数',
    avg_rating                   NUMERIC(5, 4) COMMENT '平均评分 0~5',
    rating_score_pct             NUMERIC(9, 2) COMMENT '评分达标占比%',

    -- -------- 占比口径（price / brand）--------
    sales_share_pct              NUMERIC(9, 2) COMMENT '销量占比%',
    revenue_share_pct            NUMERIC(9, 2) COMMENT '销售额占比%',
    avg_sales_share_pct          NUMERIC(9, 2) COMMENT '单品均销量占比%',
    sample_share_pct             NUMERIC(9, 6) COMMENT '该分组样本总量占比%'

) ENGINE = InnoDB
  DEFAULT CHARSET = utf8mb4
  COLLATE = utf8mb4_0900_ai_ci COMMENT = '行业图表快照数据';

CREATE TABLE IF NOT EXISTS review_chart_data
(
    id              BIGINT UNSIGNED PRIMARY KEY AUTO_INCREMENT COMMENT '自增主键',
    analysis_type   VARCHAR(32)  NOT NULL COMMENT '分组大类：negative / motivation / positive',
    topic_id        VARCHAR(64)  NOT NULL COMMENT '业务唯一键，如 negative_4',
    topic_name      VARCHAR(200) NOT NULL COMMENT '展示标签，如 做工与耐用性',
    sort_order      INTEGER      NOT NULL COMMENT '排序',
    matched_reviews INTEGER COMMENT '命中评论数',
    sample_count    INTEGER COMMENT '该分组样本总量',
    share_pct       NUMERIC(9, 6) COMMENT '占比%',
    reason          VARCHAR(200) COMMENT '原因描述'

) ENGINE = InnoDB
  DEFAULT CHARSET = utf8mb4
  COLLATE = utf8mb4_0900_ai_ci COMMENT = '评论图表分析数据';