# 亚马逊评论数据可视化平台
  本系统采用`uv+python3.14+fastapi+silo+citus`开发，数据库采用逻辑列模式存储。
  所有环境变量均配置在`.env`中。原始数据文件为`csv`，上传到`silo`对象存储`data/csv`下，通过配置`silio`的`webhook`事件，
自动读取数据保存到`citus`（无主键，逻辑列模式），查询数据采用`SQLModel`的ORM框架。<br>
项目地址：https://github.com/guxiaotu/groupB_project.git，
默认分支release（异步模式），开发分支为async（异步模式）和sync（同步模式）<br>
项目演示：https://groupb-project-3a82e1f0.fastapicloud.dev/
## （一）代码本地运行

1. 推荐使用`uv`工具，可以一键部署`python`环境第三方依赖，
   命令
   ```python
   uv sync
   uv run fastapi dev # 开发模式
   # 或者直接运行main.py
   uv run main.py # 也提供了main入口
   ```
3. 也可以使用pip方式
   - linux
   ```python
   python3 -m venv .venv && source .venv/bin/activate
   python3 -m pip install -r requirements.txt
   python main.py
   ```
   - Windows
   ```python
   python3 -m venv .venv && .venv\Scripts\activate
   python3 -m pip install -r requirements.txt
   python main.py
   ```

## （二）使用`docker-compose`方式部署
1. `compose-env`环境，只部署`silo`和`citus`
2. `compose-prod`环境，包括Web项目

## （三）所有部署脚本都在script下，并同时提供`Windows`和`Linux`
1. deploy-prod，包括`web`、`silo`和`citus`
2. deploy-env，只包括`silo`和`citus`
3. destroy为销毁清理脚本

## （四）csv文件格式
1. 固定文件格式，如industry_chart_data_2026-09-24_22-00-00.csv（时间精确到毫秒）
2. 两张数据文件，文件名为industry_chart_data_2026-09-24_22-00-00.csv和review_chart_data_2026-09-23_22-00-00.csv
