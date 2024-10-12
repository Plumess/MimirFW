# ==============================
# 使用 Redis-Stack 官方镜像
# Stack 是功能增强的版本
# ==============================
ARG REDIS_VERSION
FROM redis/redis-stack:${REDIS_VERSION}

# 维护者信息
LABEL maintainer="Plumess"

# Redis 默认端口
EXPOSE 6379
# 如果需要 RedisInsight，暴露端口 8001
EXPOSE 8001