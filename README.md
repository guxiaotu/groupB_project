# 亚马逊评论数据可视化平台
##（一）使用docker-compose方式部署
1. compose-env环境，只部署silo和PostgreSQL
2. compose-prod环境，包括Web项目

##（二） 所有部署脚本都在script下，并同时提供windows和linux
1. deploy-prod，包括web、silo和PostgreSQL
2. deploy-env，只包括silo和PostgreSQL
3. destroy为销毁清理脚本

## (三) csv文件格式
1. 固定文件格式，如industry_chart_data_2026-09-24_22-00-00.csv（时间精确到毫秒）
2. 两张数据文件，文件名为industry_chart_data_2026-09-24_22-00-00.csv和review_chart_data_2026-09-23_22-00-00.csv