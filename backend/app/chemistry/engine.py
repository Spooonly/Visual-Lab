import json
from pathlib import Path
from typing import Dict, Any, List

DATA_DIR = Path(__file__).parent / "data"


def _load_json(filename: str):
    return json.loads((DATA_DIR / filename).read_text(encoding="utf-8"))


PRECIP_RULES = _load_json("precip_rules.json")


def simulate_mix(reagent_ids: List[str]) -> Dict[str, Any]:
    # simple MVP: match exactly 2 reagents, order-insensitive
    if len(reagent_ids) != 2:
        return {
            "status": "no_result",
            "message_ru": "Пока поддерживается смешивание ровно двух растворов."
        }

    a, b = sorted(reagent_ids)

    for rule in PRECIP_RULES:
        r1, r2 = sorted(rule["reactants"])
        if [a, b] == [r1, r2]:
            return {
                "status": "ok",
                "products": rule["products"],
                "observation_ru": rule["observation_ru"],
                "equation": rule["equation"],
                "net_ionic": rule["net_ionic"],
            }

    return {
        "status": "no_reaction",
        "products": [],
        "observation_ru": "В видимых условиях реакции не наблюдается.",
        "equation": None,
        "net_ionic": None,
    }