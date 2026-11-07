@echo off
echo =================构建 groupB 项目镜像==========================
docker compose -f docker/compose-prod.yaml up -d --build --force-recreate --no-deps web

echo =============直接启用单机环境，.env默认配置文件在docker下=============
docker compose -f docker/compose-prod.yaml up -d