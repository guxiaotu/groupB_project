# 亚马逊评论数据可视化平台
## （一）使用docker-compose方式部署
1. compose-env环境，只部署silo和PostgreSQL
2. compose-prod环境，包括Web项目

## （二） 所有部署脚本都在script下，并同时提供windows和linux
1. deploy-prod，包括web、silo和PostgreSQL
2. deploy-env，只包括silo和PostgreSQL
3. destroy为销毁清理脚本