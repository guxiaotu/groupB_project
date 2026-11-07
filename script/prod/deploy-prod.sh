#!/usr/bin/env bash
echo "=================构建groupB项目镜像（强制重建，利用缓存）=========================="
docker compose -f docker/compose-prod.yaml up -d --build --force-recreate --no-deps web

echo "=============直接启用单机环境，.env默认配置文件在docker下============="
docker compose -f docker/compose-prod.yaml up -d