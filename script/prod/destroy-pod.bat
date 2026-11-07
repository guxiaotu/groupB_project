@echo off
echo "=================删除清理所有容器和volume=========================="
docker compose -f docker/compose-prod.yaml down -v