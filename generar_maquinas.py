import json
from pathlib import Path
from copy import deepcopy

BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data"

ARCHIVO_ORIGEN_VALLADOLID = DATA_DIR / "espirales.json"
ARCHIVO_SALIDA_VALLADOLID = DATA_DIR / "espirales_valladolid.json"
ARCHIVO_SALIDA_ZAMORA = DATA_DIR / "espirales_zamora.json"
ARCHIVO_SALIDA_MAQUINAS = DATA_DIR / "maquinas.json"

ESPIRALES_ORDEN = [
    "A11","A12","A13","A14","A15","A16",
    "A21","A22","A23","A24","A25","A26",
    "A31","A32","A33","A34","A35","A36",
    "A41","A42","A43","A44","A45","A46",
    "A51","A52","A53","A54","A55","A56",
    "A61","A62","A63","A64","A65","A66"
]

COMBINACIONES = [
    {
        "ids": ["A65", "A66"],
        "label": "A66"
    }
]

def cargar_json(ruta):
    with open(ruta, "r", encoding="utf-8") as f:
        return json.load(f)

def guardar_json(ruta, datos):
    ruta.parent.mkdir(parents=True, exist_ok=True)
    with open(ruta, "w", encoding="utf-8") as f:
        json.dump(datos, f, ensure_ascii=False, indent=2)

def crear_plantilla_vacia(espirales_orden):
    plantilla = {}
    for espiral in espirales_orden:
        plantilla[espiral] = {
            "coleccion": "",
            "cartas": []
        }
    return plantilla

def normalizar_espirales(espirales_existentes, espirales_orden):
    resultado = crear_plantilla_vacia(espirales_orden)

    for espiral, datos in espirales_existentes.items():
        if espiral not in resultado:
            resultado[espiral] = {
                "coleccion": datos.get("coleccion", ""),
                "cartas": datos.get("cartas", [])
            }
        else:
            resultado[espiral]["coleccion"] = datos.get("coleccion", "")
            resultado[espiral]["cartas"] = datos.get("cartas", [])

    return resultado

def construir_maquinas(valladolid, zamora):
    return {
        "valladolid": {
            "nombre": "Valladolid",
            "titulo": "CC Vallsur",
            "espiralesOrden": ESPIRALES_ORDEN,
            "combinaciones": deepcopy(COMBINACIONES),
            "espirales": valladolid
        },
        "zamora": {
            "nombre": "Zamora",
            "titulo": "Zamora",
            "espiralesOrden": ESPIRALES_ORDEN,
            "espirales": zamora
        }
    }

def main():
    if not ARCHIVO_ORIGEN_VALLADOLID.exists():
        raise FileNotFoundError(
            f"No se encontró el archivo origen: {ARCHIVO_ORIGEN_VALLADOLID}"
        )

    espirales_valladolid_original = cargar_json(ARCHIVO_ORIGEN_VALLADOLID)
    espirales_valladolid = normalizar_espirales(
        espirales_valladolid_original,
        ESPIRALES_ORDEN
    )

    espirales_zamora = crear_plantilla_vacia(ESPIRALES_ORDEN)

    maquinas = construir_maquinas(espirales_valladolid, espirales_zamora)

    guardar_json(ARCHIVO_SALIDA_VALLADOLID, espirales_valladolid)
    guardar_json(ARCHIVO_SALIDA_ZAMORA, espirales_zamora)
    guardar_json(ARCHIVO_SALIDA_MAQUINAS, maquinas)

    print(f"Generado: {ARCHIVO_SALIDA_VALLADOLID}")
    print(f"Generado: {ARCHIVO_SALIDA_ZAMORA}")
    print(f"Generado: {ARCHIVO_SALIDA_MAQUINAS}")

if __name__ == "__main__":
    main()