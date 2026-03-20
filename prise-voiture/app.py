import os
import httpx
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

HA_BASE_URL = os.getenv("HA_BASE_URL", "http://homeassistant.local:8123")
HA_TOKEN = os.getenv("HA_TOKEN")

if not HA_TOKEN:
    raise RuntimeError("HA_TOKEN environment variable must be set")

# Entités Home Assistant pour ta prise voiture
SWITCH_ENTITY_ID = "switch.prise_voiture"
POWER_ENTITY_ID = "sensor.prise_voiture_puissance_2"
ENERGY_ENTITY_ID = "sensor.prise_voiture_energy"

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # tu pourras restreindre si besoin
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class StateResponse(BaseModel):
    is_on: bool
    power: float | None = None
    energy: float | None = None


def ha_headers() -> dict:
    return {
        "Authorization": f"Bearer {HA_TOKEN}",
        "Content-Type": "application/json",
    }


async def get_entity_state(client: httpx.AsyncClient, entity_id: str) -> dict:
    url = f"{HA_BASE_URL}/api/states/{entity_id}"
    resp = await client.get(url, headers=ha_headers(), timeout=10)
    if resp.status_code != 200:
        raise HTTPException(
            status_code=502,
            detail=f"Erreur HA states pour {entity_id}: {resp.text}",
        )
    return resp.json()


async def call_service(
    client: httpx.AsyncClient, domain: str, service: str, data: dict
) -> None:
    url = f"{HA_BASE_URL}/api/services/{domain}/{service}"
    resp = await client.post(url, headers=ha_headers(), json=data, timeout=10)
    if resp.status_code not in (200, 201):
        raise HTTPException(
            status_code=502,
            detail=f"Erreur HA service {domain}.{service}: {resp.text}",
        )


async def read_complete_state(client: httpx.AsyncClient) -> StateResponse:
    switch_state = await get_entity_state(client, SWITCH_ENTITY_ID)
    power_state = await get_entity_state(client, POWER_ENTITY_ID)
    energy_state = await get_entity_state(client, ENERGY_ENTITY_ID)

    is_on = switch_state["state"] == "on"

    def parse_float(entity: dict) -> float | None:
        try:
            return float(entity["state"])
        except (ValueError, TypeError):
            return None

    power = parse_float(power_state)
    energy = parse_float(energy_state)

    return StateResponse(is_on=is_on, power=power, energy=energy)


@app.get("/state", response_model=StateResponse)
async def get_state():
    async with httpx.AsyncClient() as client:
        return await read_complete_state(client)


@app.post("/on", response_model=StateResponse)
async def turn_on():
    async with httpx.AsyncClient() as client:
        await call_service(
            client,
            domain="switch",
            service="turn_on",
            data={"entity_id": SWITCH_ENTITY_ID},
        )
        return await read_complete_state(client)


@app.post("/off", response_model=StateResponse)
async def turn_off():
    async with httpx.AsyncClient() as client:
        await call_service(
            client,
            domain="switch",
            service="turn_off",
            data={"entity_id": SWITCH_ENTITY_ID},
        )
        return await read_complete_state(client)