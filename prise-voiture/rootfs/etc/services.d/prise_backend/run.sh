#!/usr/bin/with-contenv bashio

HA_BASE_URL=$(bashio::config 'ha_base_url')
HA_TOKEN=$(bashio::config 'ha_token')

export HA_BASE_URL
export HA_TOKEN

bashio::log.info "Starting Prise Voiture backend (FastAPI)"
bashio::log.info "HA_BASE_URL=${HA_BASE_URL}"

exec uvicorn app:app --host 0.0.0.0 --port 8000