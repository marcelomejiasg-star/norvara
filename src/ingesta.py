"""Puerta de ingesta. Abre un archivo y dice qué encontró.

No opina del KPI. No escribe el brief. Solo mira.

Uso, desde la carpeta norvara:

    python3 src/ingesta.py data/pedidos.csv
    python3 src/ingesta.py data/pedidos.json
"""

from __future__ import annotations

import csv
import json
from pathlib import Path


def abrir_csv(ruta: Path) -> dict:
    """Lee un CSV y devuelve el inventario, no el semáforo.

    Prueba coma y punto y coma. Un Excel en español suele guardar
    el CSV con punto y coma. Si no se puede leer, no inventa filas.
    """
    if not ruta.exists():
        return {
            "ok": False,
            "archivo": ruta.name,
            "nota": "no está el archivo",
            "filas": 0,
            "columnas": [],
        }

    texto = ruta.read_text(encoding="utf-8")
    if not texto.strip():
        return {
            "ok": False,
            "archivo": ruta.name,
            "nota": "el archivo está vacío",
            "filas": 0,
            "columnas": [],
        }

    separador = ";" if texto.splitlines()[0].count(";") > texto.splitlines()[0].count(",") else ","
    with ruta.open(newline="", encoding="utf-8") as f:
        lector = csv.DictReader(f, delimiter=separador)
        filas = list(lector)
        columnas = list(lector.fieldnames or [])

    return {
        "ok": True,
        "archivo": ruta.name,
        "nota": "se pudo leer",
        "filas": len(filas),
        "columnas": columnas,
        "separador": "punto y coma" if separador == ";" else "coma",
    }


def abrir_excel(ruta: Path) -> dict:
    """Lee la primera hoja de un Excel. Misma salida que el CSV."""
    if not ruta.exists():
        return {
            "ok": False,
            "archivo": ruta.name,
            "nota": "no está el archivo",
            "filas": 0,
            "columnas": [],
        }
    import pandas as pd

    tabla = pd.read_excel(ruta)
    return {
        "ok": True,
        "archivo": ruta.name,
        "nota": "se pudo leer",
        "filas": len(tabla),
        "columnas": [str(c) for c in tabla.columns],
    }


def abrir_json(ruta: Path) -> dict:
    """Lee un JSON de lista de objetos y lo aplana a columnas.

    Un JSON no es una tabla. Si es una lista de objetos, cada objeto
    es una fila y las claves son las columnas. Si no tiene esa forma,
    no se inventan filas.
    """
    if not ruta.exists():
        return {
            "ok": False,
            "archivo": ruta.name,
            "nota": "no está el archivo",
            "filas": 0,
            "columnas": [],
        }
    datos = json.loads(ruta.read_text(encoding="utf-8"))
    if not isinstance(datos, list) or not datos or not isinstance(datos[0], dict):
        return {
            "ok": False,
            "archivo": ruta.name,
            "nota": "no es una lista de objetos",
            "filas": 0,
            "columnas": [],
        }
    columnas = list(datos[0].keys())
    return {
        "ok": True,
        "archivo": ruta.name,
        "nota": "se pudo leer",
        "filas": len(datos),
        "columnas": columnas,
    }


def abrir(ruta: Path) -> dict:
    sufijo = ruta.suffix.lower()
    if sufijo in {".xlsx", ".xls"}:
        return abrir_excel(ruta)
    if sufijo == ".json":
        return abrir_json(ruta)
    return abrir_csv(ruta)


def informe(resultado: dict) -> str:
    columnas = ", ".join(resultado["columnas"]) if resultado["columnas"] else "ninguna"
    return (
        f"archivo: {resultado['archivo']}\n"
        f"estado: {resultado['nota']}\n"
        f"filas: {resultado['filas']}\n"
        f"columnas: {columnas}"
    )


def main() -> None:
    import sys

    if len(sys.argv) != 2:
        print("pasá la ruta del archivo. ejemplo: python3 src/ingesta.py data/pedidos.csv")
        sys.exit(1)
    print(informe(abrir(Path(sys.argv[1]))))


if __name__ == "__main__":
    main()
