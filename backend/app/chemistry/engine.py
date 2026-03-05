import json
from pathlib import Path
from typing import Dict, Any, List, Tuple

DATA_DIR = Path(__file__).parent / "data"

def _load_json(filename: str):
    return json.loads((DATA_DIR / filename).read_text(encoding="utf-8"))

IONS = _load_json("ions.json")
INSOLUBLE = _load_json("insoluble.json")
ION_DISPLAY = _load_json("ion_display.json")

def _pretty_ion(ion: str) -> str:
    return ION_DISPLAY.get(ion, ion)

def _get_ions(reagent_id: str) -> List[str]:
    entry = IONS.get(reagent_id)
    if not entry:
        return []
    ions = []
    for it in entry["ions"]:
        ions.extend([it["ion"]] * int(it["n"]))
    return ions

def _find_precipitate(ions_a: List[str], ions_b: List[str]) -> Dict[str, Any] | None:
    cations = [x for x in ions_a + ions_b if "+" in x]
    anions = [x for x in ions_a + ions_b if "-" in x]

    # try all cation/anion pairs
    for cat in cations:
        for an in anions:
            for rule in INSOLUBLE:
                if rule["cation"] == cat and rule["anion"] == an:
                    return rule
    return None

def simulate_mix(reagent_ids: List[str]) -> Dict[str, Any]:
    if len(reagent_ids) != 2:
        return {"status": "no_result", "message_ru": "Пока поддерживается смешивание ровно двух растворов."}

    a, b = reagent_ids[0], reagent_ids[1]
    ions_a = _get_ions(a)
    ions_b = _get_ions(b)

    if not ions_a or not ions_b:
        return {"status": "no_result", "message_ru": "Неизвестный реагент или нет данных по диссоциации."}

    precip = _find_precipitate(ions_a, ions_b)
    if precip:
        solid = precip["solid"]
        color = precip["color_ru"]
        return {
            "status": "ok",
            "products": [f"{solid}(s)"],
            "observation_ru": f"Образуется {color} осадок {solid}.",
            "equation": None,
            "net_ionic": f"{_pretty_ion(precip['cation'])} + {_pretty_ion(precip['anion'])} -> {solid}(s)",
            "visual": {
                "type": "precipitate",
                "solid": solid,
                "color": "white" if color == "белый" else ("blue" if color == "голубой" else "gray")
            }
        }

    return {
        "status": "no_reaction",
        "products": [],
        "observation_ru": "В видимых условиях реакции не наблюдается.",
        "equation": None,
        "net_ionic": None,
        "visual": {"type": "none"}
    }