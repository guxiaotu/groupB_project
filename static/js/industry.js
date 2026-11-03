/* 行业分析页图表逻辑 —— 读取 window.PAYLOAD（由 Jinja2 注入） */
(function () {
  'use strict';
  var D = window.PAYLOAD || {};
  var charts = [];

  function reg(dom, opt) { var c = echarts.init(dom); c.setOption(opt); charts.push(c); return c; }
  var LAB = { textStyle: { color: '#6b7280' } };

  /* ---------- 价格带：产品数/月销量 + 月销售额 + 平均评分 ---------- */
  (function () {
    var d = D.price_distribution, lb = d.labels;
    var pc = d.rows.map(function (r) { return r.product_count; });
    var ms = d.rows.map(function (r) { return r.monthly_sales; });
    var mr = d.rows.map(function (r) { return r.monthly_revenue; });
    var ar = d.rows.map(function (r) { return r.avg_rating; });
    var cat = { type: 'category', data: lb, axisLabel: { color: '#475569', rotate: 30 } };

    reg(document.getElementById('price_sales'), {
      // title: { text: '价格带 · 产品数 / 月销量', left: 'center', textStyle: { fontSize: 14, fontWeight: 600 } },
      tooltip: { trigger: 'axis' }, legend: LAB, grid: { top: 56, left: 60, right: 20, bottom: 40 },
      xAxis: cat,
      yAxis: [
        { type: 'value', name: '产品数', axisLine: { lineStyle: { color: '#cbd5e1' } } },
        { type: 'value', name: '月销量', axisLine: { lineStyle: { color: '#cbd5e1' } } }
      ],
      series: [
        { name: '产品数', type: 'bar', data: pc, itemStyle: { color: '#93c5fd', borderRadius: [4, 4, 0, 0] } },
        { name: '月销量', type: 'line', yAxisIndex: 1, data: ms, smooth: true, itemStyle: { color: '#2563eb' }, lineStyle: { width: 3 } }
      ]
    });

    reg(document.getElementById('price_revenue'), {
      title: { text: '价格带 · 月销售额', left: 'center', textStyle: { fontSize: 14, fontWeight: 600 } },
      tooltip: { trigger: 'axis', valueFormatter: function (v) { return '$' + Number(v).toLocaleString(); } },
      grid: { top: 56, left: 72, right: 20, bottom: 40 },
      xAxis: cat,
      yAxis: { type: 'value', axisLine: { lineStyle: { color: '#cbd5e1' } }, axisLabel: { formatter: function (v) { return '$' + (v / 1e6).toFixed(1) + 'M'; } } },
      series: [{
        type: 'bar', data: mr, itemStyle: { color: '#34d399', borderRadius: [4, 4, 0, 0] },
        label: { show: true, position: 'top', formatter: function (p) { return (p.value / 1e6).toFixed(1) + 'M'; }, fontSize: 11, color: '#059669' }
      }]
    });

    reg(document.getElementById('price_rating'), {
      title: { text: '价格带 · 平均评分分布', left: 'center', textStyle: { fontSize: 14, fontWeight: 600 } },
      tooltip: { trigger: 'axis' }, grid: { top: 56, left: 56, right: 20, bottom: 40 },
      xAxis: cat,
      yAxis: { type: 'value', min: 4, max: 4.7, axisLine: { lineStyle: { color: '#cbd5e1' } } },
      series: [{
        type: 'line', data: ar, smooth: true,
        areaStyle: { color: 'rgba(236,72,153,.18)' }, itemStyle: { color: '#ec4899' }, lineStyle: { width: 3 },
        label: { show: true, formatter: function (p) { return p.value.toFixed(2); }, fontSize: 11, color: '#db2777' }
      }]
    });
  })();

  /* ---------- 品牌集中度：Pareto 曲线 + TOP15 横向条形 ---------- */
  (function () {
    var d = D.brand_concentration, lb = d.labels;
    var rev = d.rows.map(function (r) { return r.monthly_revenue; });
    var cum = d.rows.map(function (r) { return r.revenue_cumulative_share_pct; });
    var ms = d.rows.map(function (r) { return r.monthly_sales; });

    reg(document.getElementById('brand_pareto'), {
      // title: { text: '品牌销售额 Pareto 曲线', left: 'center', textStyle: { fontSize: 14, fontWeight: 600 } },
      tooltip: { trigger: 'axis' }, legend: LAB, grid: { top: 56, left: 70, right: 60, bottom: 40 },
      xAxis: { type: 'category', data: lb, axisLabel: { color: '#475569', interval: 4, rotate: 40 } },
      yAxis: [
        { type: 'value', name: '销售额($)', axisLine: { lineStyle: { color: '#cbd5e1' } }, axisLabel: { formatter: function (v) { return '$' + (v / 1e6).toFixed(1) + 'M'; } } },
        { type: 'value', name: '累计占比(%)', max: 100, axisLine: { lineStyle: { color: '#cbd5e1' } } }
      ],
      series: [
        { name: '销售额', type: 'bar', data: rev, itemStyle: { color: '#a5b4fc', borderRadius: [3, 3, 0, 0] } },
        { name: '累计占比', type: 'line', yAxisIndex: 1, data: cum, smooth: true, itemStyle: { color: '#dc2626' }, lineStyle: { width: 2.5 } }
      ]
    });

    var top = d.rows.slice(0, 15).slice().reverse();
    reg(document.getElementById('brand_top'), {
      // title: { text: 'TOP15 品牌 · 销量与销售额', left: 'center', textStyle: { fontSize: 14, fontWeight: 600 } },
      tooltip: { trigger: 'axis' }, legend: LAB, grid: { top: 56, left: 100, right: 70, bottom: 20 },
      xAxis: [
        { type: 'value', axisLine: { lineStyle: { color: '#cbd5e1' } } },
        { type: 'value', axisLine: { lineStyle: { color: '#cbd5e1' } }, axisLabel: { formatter: function (v) { return '$' + (v / 1e6).toFixed(1) + 'M'; } } }
      ],
      yAxis: { type: 'category', data: top.map(function (r) { return r.item_label; }), axisLabel: { color: '#475569' } },
      series: [
        { name: '月销量', type: 'bar', data: top.map(function (r) { return r.monthly_sales; }), itemStyle: { color: '#60a5fa', borderRadius: [0, 4, 4, 0] } },
        { name: '月销售额', type: 'bar', xAxisIndex: 1, data: top.map(function (r) { return r.monthly_revenue; }), itemStyle: { color: '#f59e0b', borderRadius: [0, 4, 4, 0] } }
      ]
    });
  })();

  /* ---------- 上架时间分布 ---------- */
  (function () {
    var d = D.listing_distribution, lb = d.labels;
    var cnt = d.rows.map(function (r) { return r.product_count; });
    var cum = d.rows.map(function (r) { return r.cumulative_product_count; });

    reg(document.getElementById('listing'), {
      // title: { text: '产品上架数量随月份变化', left: 'center', textStyle: { fontSize: 14, fontWeight: 600 } },
      tooltip: { trigger: 'axis' }, legend: LAB, grid: { top: 56, left: 60, right: 60, bottom: 44 },
      xAxis: { type: 'category', data: lb, axisLabel: { color: '#475569', interval: 11, rotate: 40 } },
      yAxis: [
        { type: 'value', name: '当月上架', axisLine: { lineStyle: { color: '#cbd5e1' } } },
        { type: 'value', name: '累计产品', axisLine: { lineStyle: { color: '#cbd5e1' } } }
      ],
      series: [
        { name: '当月上架', type: 'bar', data: cnt, itemStyle: { color: '#22d3ee', borderRadius: [3, 3, 0, 0] } },
        { name: '累计产品', type: 'line', yAxisIndex: 1, data: cum, smooth: true, itemStyle: { color: '#7c3aed' }, lineStyle: { width: 3 }, areaStyle: { color: 'rgba(124,58,237,.08)' } }
      ]
    });
  })();

  window.addEventListener('resize', function () {
    charts.forEach(function (c) { c.resize(); });
  });
})();
