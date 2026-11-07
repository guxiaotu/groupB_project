#!/usr/bin/env bash
echo "=============部署生产环境，包括silo和Postgresql============="
docker compose -f docker/compose-env.yaml up -d