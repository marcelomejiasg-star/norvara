"""Puerta de ingesta. Abre un archivo y dice qué encontró.

No opina del KPI. No escribe el brief. Solo mira.

Uso, desde la carpeta norvara:

    python3 src/ingesta.py data/pedidos.csv
"""

from __future__ import annotations

import csv
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
    print(informe(abrir_csv(Path(sys.argv[1]))))


if __name__ == "__main__":
    main()
