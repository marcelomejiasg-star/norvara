"""Norvara v1 — arma un brief con semaforo.

Lee las reglas (metrics/kpis.csv) y las tablas (data/).
Escribe output/brief.md.

Correr desde la carpeta norvara:
    python3 src/brief.py
"""

from datetime import datetime, date
from pathlib import Path
import csv

HOY = date(2026, 9, 27)
RAIZ = Path(__file__).resolve().parent.parent


def leer_csv(ruta):
    with open(ruta, newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def parse_fecha(texto):
    texto = (texto or "").strip()
    if not texto:
        return None
    return datetime.strptime(texto, "%Y-%m-%d").date()


def dias_desde(fecha):
    if fecha is None:
        return None
    return (HOY - fecha).days


def semaforo(estado):
    if estado == "usar":
        return "VERDE — se puede usar"
    if estado == "revisar":
        return "AMARILLO — revisar"
    return "ROJO — no usar en reunion"


def chequear_ingresos(filas):
    fechas = [parse_fecha(f["fecha"]) for f in filas]
    ultima = max(fechas)
    total = sum(float(f["monto_neto"]) for f in filas)
    antiguedad = dias_desde(ultima)
    if antiguedad is None or antiguedad > 2:
        return "revisar", total, ultima, f"la fuente tiene {antiguedad} dias (regla: menos de 2)"
    return "usar", total, ultima, f"ultima venta hace {antiguedad} dia(s)"


def chequear_clientes(filas):
    vacios = [f["cliente_id"] for f in filas if not (f.get("ultima_compra") or "").strip()]
    activos = 0
    for f in filas:
        d = parse_fecha(f.get("ultima_compra"))
        if d and dias_desde(d) <= 90:
            activos += 1
    if vacios:
        return "revisar", activos, None, f"hay fechas vacias ({', '.join(vacios)})"
    return "usar", activos, None, "no hay fechas vacias"


def chequear_menciones(filas):
    fechas = [parse_fecha(f["fecha"]) for f in filas]
    ultima = max(fechas)
    n = len(filas)
    antiguedad = dias_desde(ultima)
    if antiguedad is None or antiguedad > 3:
        return "no_usar", n, ultima, f"ultima mencion hace {antiguedad} dias (regla: maximo 3)"
    return "usar", n, ultima, f"ultima mencion hace {antiguedad} dia(s)"


def main():
    kpis = leer_csv(RAIZ / "metrics" / "kpis.csv")
    ventas = leer_csv(RAIZ / "data" / "ventas.csv")
    clientes = leer_csv(RAIZ / "data" / "clientes.csv")
    menciones = leer_csv(RAIZ / "data" / "menciones.csv")

    resultados = {}
    for fila in kpis:
        nombre = fila["kpi"]
        if nombre == "ingresos":
            resultados[nombre] = (*chequear_ingresos(ventas), fila)
        elif nombre == "clientes_activos":
            resultados[nombre] = (*chequear_clientes(clientes), fila)
        elif nombre == "menciones":
            resultados[nombre] = (*chequear_menciones(menciones), fila)

    lineas = [
        "# Brief Norvara",
        "",
        f"Fecha del brief: {HOY.isoformat()}",
        "Marca de practica: ejemplo.",
        "",
        "Esto no es un dashboard. Es que numeros se pueden llevar a una reunion.",
        "",
    ]

    for nombre, (estado, valor, ultima, nota, regla) in resultados.items():
        lineas.append(f"## {nombre}")
        lineas.append(f"- Pregunta: {regla['pregunta']}")
        lineas.append(f"- Como se calcula: {regla['como_se_calcula']}")
        lineas.append(f"- Dueno: {regla['dueno']}")
        lineas.append(f"- Valor: {valor}")
        if ultima:
            lineas.append(f"- Ultimo dato: {ultima.isoformat()}")
        lineas.append(f"- Semaforo: {semaforo(estado)}")
        lineas.append(f"- Por que: {nota}")
        lineas.append("")

    lineas.append("## Lectura rapida")
    lineas.append("- Ingresos: dato reciente. Se puede usar el neto.")
    lineas.append("- Clientes activos: hay una fila sin fecha. Revisar antes de presentar.")
    lineas.append("- Menciones: dato viejo. No decir 'esta semana' en una reunion.")
    lineas.append("")

    salida = RAIZ / "output" / "brief.md"
    salida.write_text("\n".join(lineas), encoding="utf-8")
    print("Listo. Brief escrito en output/brief.md")


if __name__ == "__main__":
    main()
