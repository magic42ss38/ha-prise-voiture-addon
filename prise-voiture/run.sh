#!/command/with-contenv bashio

# Récupération des options de l'add-on
HA_BASE_URL=$(bashio::config 'ha_base_url')
HA_TOKEN=$(bashio::config 'ha_token')

export HA_BASE_URL
export HA_TOKEN

bashio::log.info "Starting Prise Voiture backend (FastAPI)"
bashio::log.info "HA_BASE_URL=${HA_BASE_URL}"

# Lancer l'API FastAPI via uvicorn
uvicorn app:app --host 0.0.0.0 --port 8000