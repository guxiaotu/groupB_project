/* 评论分析页图表逻辑 —— 读取 window.REVIEW（由 Jinja2 注入） */
(function () {
  'use strict';
  var D = window.REVIEW || {};
  var charts = [];
  function reg(dom, opt) { var c = echarts.init(dom); c.setOption(opt); charts.push(c); return c; }
  var LAB = { textStyle: { color: '#6b7280' } };

  /* 单类主题横向条形图 */
  function bar(id, rows, color) {
    var rev = rows.slice().reverse();
    reg(document.getElementById(id), {
      tooltip: {
        trigger: 'axis', axisPointer: { type: 'shadow' },
        formatter: function (p) {
          var r = rev[p[0].dataIndex];
          return '<b>' + r.topic_name + '</b><br>匹配评论：' + r.matched_reviews +
            '<br>样本量：' + r.sample_count + '<br>占比：' + r.share_pct.toFixed(1) + '%';
        }
      },
      grid: { top: 10, left: 110, right: 60, bottom: 10 },
      xAxis: { type: 'value', axisLine: { lineStyle: { color: '#cbd5e1' } }, axisLabel: { formatter: '{value} 条' } },
      yAxis: { type: 'category', data: rev.map(function (r) { return r.topic_name; }), axisLabel: { color: '#374151' } },
      series: [{
        type: 'bar',
        data: rev.map(function (r) { return r.matched_reviews; }),
        itemStyle: { color: color, borderRadius: [0, 6, 6, 0] },
        label: {
          show: true, position: 'right', fontSize: 12, color: '#374151',
          formatter: function (p) { var r = rev[p.dataIndex]; return r.matched_reviews + ' 条 (' + r.share_pct.toFixed(1) + '%)'; }
        }
      }]
    });
  }

  bar('neg', D.negative.rows, '#f87171');
  bar('pos', D.positive.rows, '#34d399');
  bar('mot', D.motivation.rows, '#38bdf8');

  /* 三类主题占比对照 */
  (function () {
    var groups = [
      { key: 'negative', name: '负面主题', color: '#f87171' },
      { key: 'positive', name: '正面主题', color: '#34d399' },
      { key: 'motivation', name: '购买动机', color: '#38bdf8' }
    ];
    var cats = [];
    groups.forEach(function (g) { D[g.key].rows.forEach(function (r) { if (cats.indexOf(r.topic_name) === -1) cats.push(r.topic_name); }); });
    var series = groups.map(function (g) {
      return {
        name: g.name, type: 'bar',
        itemStyle: { color: g.color, borderRadius: [4, 4, 0, 0] },
        data: cats.map(function (c) {
          var found = D[g.key].rows.filter(function (r) { return r.topic_name === c; });
          return found.length ? found[0].share_pct : 0;
        })
      };
    });
    reg(document.getElementById('all'), {
      tooltip: { trigger: 'axis', valueFormatter: function (v) { return v ? v.toFixed(1) + '%' : '-'; } },
      legend: LAB, grid: { top: 40, left: 60, right: 24, bottom: 10 },
      xAxis: { type: 'value', max: 30, axisLine: { lineStyle: { color: '#cbd5e1' } }, axisLabel: { formatter: '{value}%' } },
      yAxis: { type: 'category', data: cats, axisLabel: { color: '#374151' } },
      series: series
    });
  })();

  window.addEventListener('resize', function () { charts.forEach(function (c) { c.resize(); }); });
})();
