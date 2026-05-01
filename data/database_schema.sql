"""
数据库Schema定义
PostgreSQL表结构SQL

创建时间：2026-05-01 19:45
"""

-- ============================================
-- 用户表（users）⭐⭐⭐⭐⭐
-- ============================================

CREATE TABLE users (
    user_id VARCHAR(50) PRIMARY KEY,
    username VARCHAR(100) NOT NULL,
    email VARCHAR(100),
    phone VARCHAR(20),
    age INTEGER,
    gender VARCHAR(10),
    health_status TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- ============================================
-- 健康记录表（health_records）⭐⭐⭐⭐⭐
-- ============================================

CREATE TABLE health_records (
    record_id VARCHAR(50) PRIMARY KEY,
    user_id VARCHAR(50) REFERENCES users(user_id),
    device_id VARCHAR(50),
    data_type VARCHAR(50),
    data_value JSONB,
    data_time TIMESTAMP,
    data_verified BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 创建索引
CREATE INDEX idx_health_records_user_id ON health_records(user_id);
CREATE INDEX idx_health_records_data_time ON health_records(data_time);

-- ============================================
-- 预警历史表（warning_history）⭐⭐⭐⭐⭐
-- ============================================

CREATE TABLE warning_history (
    warning_id VARCHAR(50) PRIMARY KEY,
    user_id VARCHAR(50) REFERENCES users(user_id),
    warning_level VARCHAR(10),
    warning_type VARCHAR(100),
    explanation TEXT,
    suggestion JSONB,
    validation_status VARCHAR(20),
    validation_score FLOAT,
    warning_time TIMESTAMP,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 创建索引
CREATE INDEX idx_warning_history_user_id ON warning_history(user_id);
CREATE INDEX idx_warning_history_warning_level ON warning_history(warning_level);
CREATE INDEX idx_warning_history_warning_time ON warning_history(warning_time);

-- ============================================
-- 设备表（devices）
-- ============================================

CREATE TABLE devices (
    device_id VARCHAR(50) PRIMARY KEY,
    user_id VARCHAR(50) REFERENCES users(user_id),
    device_type VARCHAR(50),
    device_name VARCHAR(100),
    connect_status VARCHAR(20),
    last_data_time TIMESTAMP,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- ============================================
-- 推送历史表（notification_history）⭐⭐⭐⭐⭐
-- ============================================

CREATE TABLE notification_history (
    notification_id VARCHAR(50) PRIMARY KEY,
    warning_id VARCHAR(50) REFERENCES warning_history(warning_id),
    user_id VARCHAR(50) REFERENCES users(user_id),
    channel VARCHAR(20),
    status VARCHAR(20),
    send_time TIMESTAMP,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- ============================================
-- 时序数据优化（使用TimescaleDB）⭐⭐⭐⭐⭐
-- ============================================

-- 如果安装TimescaleDB扩展
-- CREATE EXTENSION IF NOT EXISTS timescaledb;

-- 将health_records转换为超表（时序表）
-- SELECT create_hypertable('health_records', 'data_time');

-- 将warning_history转换为超表
-- SELECT create_hypertable('warning_history', 'warning_time');