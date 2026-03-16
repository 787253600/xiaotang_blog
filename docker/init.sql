-- PostgreSQL 初始化脚本
-- 在 Docker 首次启动时执行

-- 尝试创建 zhparser 中文分词扩展（需要镜像预装，失败则静默跳过）
DO $$
BEGIN
    CREATE EXTENSION IF NOT EXISTS zhparser;
    CREATE TEXT SEARCH CONFIGURATION zhparser (PARSER = zhparser);
    ALTER TEXT SEARCH CONFIGURATION zhparser ADD MAPPING FOR n,v,a,i,e,l WITH simple;
    RAISE NOTICE 'zhparser 中文分词扩展已启用';
EXCEPTION WHEN OTHERS THEN
    RAISE NOTICE 'zhparser 不可用，将使用 simple 分词配置';
END;
$$;

-- 搜索向量自动更新触发器（Alembic 迁移会创建表，此触发器在表存在后生效）
-- 实际触发器通过 Alembic 迁移脚本创建
