-- Ensure TimescaleDB extension is available
CREATE EXTENSION IF NOT EXISTS timescaledb;

-- Raw sensor readings hypertable
CREATE TABLE IF NOT EXISTS sensor_readings (
    id              BIGSERIAL,
    sensor_id       TEXT        NOT NULL,
    sensor_type     TEXT        NOT NULL,
    value           DOUBLE PRECISION NOT NULL,
    observed_at     TIMESTAMPTZ NOT NULL,
    metadata        JSONB,
    raw_payload     JSONB       NOT NULL,
    PRIMARY KEY (id, observed_at)
);

SELECT create_hypertable('sensor_readings', 'observed_at', if_not_exists => TRUE);

CREATE INDEX IF NOT EXISTS idx_sensor_readings_sensor_time
    ON sensor_readings (sensor_id, observed_at DESC);

CREATE INDEX IF NOT EXISTS idx_sensor_readings_type_time
    ON sensor_readings (sensor_type, observed_at DESC);

CREATE INDEX IF NOT EXISTS idx_sensor_readings_observed_at
    ON sensor_readings (observed_at DESC);

-- Weather station data hypertable
CREATE TABLE IF NOT EXISTS weather_readings (
    id              BIGSERIAL,
    station_id      TEXT        NOT NULL,
    metric          TEXT        NOT NULL,
    value           DOUBLE PRECISION,
    units           TEXT,
    observed_at     TIMESTAMPTZ NOT NULL,
    metadata        JSONB,
    raw_payload     JSONB       NOT NULL,
    PRIMARY KEY (id, observed_at)
);

SELECT create_hypertable('weather_readings', 'observed_at', if_not_exists => TRUE);

CREATE INDEX IF NOT EXISTS idx_weather_station_time
    ON weather_readings (station_id, observed_at DESC);

CREATE INDEX IF NOT EXISTS idx_weather_metric_time
    ON weather_readings (metric, observed_at DESC);

CREATE INDEX IF NOT EXISTS idx_weather_observed_at
    ON weather_readings (observed_at DESC);
