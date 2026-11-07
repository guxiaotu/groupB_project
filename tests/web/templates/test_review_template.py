# tests/test_review_template.py


# ── mock 数据 ──────────────────────────────────────────
def make_mock_review():
    return {
        "summary": {
            "sample_negative": 1240,
            "negative_total": 3820,
            "sample_positive": 2150,
            "positive_total": 5600,
            "sample_motivation": 980,
            "motivation_total": 2100,
        },
        "payload": {
            "negative": {
                "labels": ["质量差", "发货慢", "客服态度差", "包装破损", "尺寸不符"],
                "rows": [
                    {
                        "topic_name": "质量差",
                        "reason": "多用户反馈使用一周后产品出现裂纹，材质明显低于预期",
                    },
                    {
                        "topic_name": "发货慢",
                        "reason": "下单后平均 5 天才发货，远超同类竞品 2 天水平",
                    },
                    {
                        "topic_name": "客服态度差",
                        "reason": "售后响应超过 48 小时，且回复模板化无实质解决方案",
                    },
                ],
            },
            "positive": {
                "labels": ["性价比高", "外观好看", "物流快", "功能齐全", "包装精美"],
                "rows": [
                    {
                        "topic_name": "性价比高",
                        "reason": "同价位中功能最全，用户反复提及物超所值",
                    },
                    {
                        "topic_name": "外观好看",
                        "reason": "设计简洁，适合摆放在办公桌，多次被拍照晒单",
                    },
                    {
                        "topic_name": "物流快",
                        "reason": "次日达覆盖区域广，用户明确表达惊喜",
                    },
                ],
            },
            "motivation": {
                "labels": ["送礼", "自用办公", "替代旧款", "朋友推荐", "凑单"],
                "rows": [
                    {
                        "topic_name": "送礼",
                        "reason": "包装体面，价格适中，是节假日送礼高频选择",
                    },
                    {
                        "topic_name": "自用办公",
                        "reason": "满足日常办公需求，便携性是被提及最多的关键词",
                    },
                    {
                        "topic_name": "朋友推荐",
                        "reason": "口碑传播占比高，多个用户提到是同事/朋友安利",
                    },
                ],
            },
        },
    }


# ── 测试 1：基本渲染不炸 ───────────────────────────────
def test_review_template_renders(jinja_env, template_context):
    template_context["review"] = make_mock_review()

    template = jinja_env.get_template("review.jinja2")
    html = template.render(**template_context)

    # 页面标题
    assert "评论分析" in html
    assert "数据可视化平台" in html

    # KPI 数字
    assert "1,240" in html
    assert "2,150" in html
    assert "980" in html

    # 主题名
    assert "质量差" in html
    assert "性价比高" in html
    assert "送礼" in html

    # JS payload
    assert "window.REVIEW" in html
    assert "negative" in html

    # 图表容器
    assert 'id="neg"' in html
    assert 'id="pos"' in html
    assert 'id="mot"' in html
    assert 'id="all"' in html

    print("✅ review template rendered, length =", len(html))


# ── 测试 2：payload 为空 ──────────────────────────────
def test_review_empty_payload(jinja_env, template_context):
    review = make_mock_review()
    # payload 结构保留，只清空 rows
    review["payload"]["negative"]["rows"] = []
    review["payload"]["positive"]["rows"] = []
    review["payload"]["motivation"]["rows"] = []
    review["summary"] = {
        "sample_negative": 0,
        "negative_total": 0,
        "sample_positive": 0,
        "positive_total": 0,
        "sample_motivation": 0,
        "motivation_total": 0,
    }

    template_context["review"] = review
    html = jinja_env.get_template("review.jinja2").render(**template_context)

    assert "评论分析" in html


# ── 测试 3：rows 为空列表 ─────────────────────────────
def test_review_empty_rows(jinja_env, template_context):
    review = make_mock_review()
    review["payload"]["negative"]["rows"] = []
    review["payload"]["positive"]["rows"] = []
    review["payload"]["motivation"]["rows"] = []

    template_context["review"] = review
    html = jinja_env.get_template("review.jinja2").render(**template_context)

    assert "负面主题" in html
    assert "正面主题" in html
    assert "购买动机" in html
    # reason-list 应该是空的
    assert html.count('class="reason"') == 0


# ── 测试 4：XSS 安全（tojson 转义） ──────────────────
def test_review_payload_xss_safe(jinja_env, template_context):
    review = make_mock_review()
    review["payload"]["negative"]["rows"].append(
        {
            "topic_name": "<script>alert('xss')</script>",
            "reason": "<img src=x onerror=alert(1)>",
        }
    )

    template_context["review"] = review
    html = jinja_env.get_template("review.jinja2").render(**template_context)

    # tojson 应该转义
    assert "<script>alert" not in html
    assert "\\u003c" in html or "&lt;" in html


# ── 测试 5：labels 长度动态渲染 ────────────────────────
def test_review_labels_length_dynamic(jinja_env, template_context):
    """验证 TOP N 标题里的数字跟着 labels 长度走"""
    review = make_mock_review()
    # 只有 2 个 label
    review["payload"]["negative"]["labels"] = ["质量差", "发货慢"]

    template_context["review"] = review
    html = jinja_env.get_template("review.jinja2").render(**template_context)

    assert "负面主题 TOP2" in html


# ── 测试 6：summary 数字格式化（大数） ─────────────────
def test_review_large_numbers(jinja_env, template_context):
    review = make_mock_review()
    review["summary"]["sample_negative"] = 1_000_000
    review["summary"]["sample_positive"] = 5_000_000

    template_context["review"] = review
    html = jinja_env.get_template("review.jinja2").render(**template_context)

    assert "1,000,000" in html
    assert "5,000,000" in html
