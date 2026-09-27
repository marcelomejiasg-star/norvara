"""Norvara — brief de semáforo para una reunión.

No dibuja un tablero. Lee definiciones de KPI y tablas, controla si el
dato está definido, completo y al día, y escribe output/brief.md.

Uso (desde la raíz del repo):

    python3 src/brief.py
    python3 src/brief.py --hoy 2026-09-27
    python3 src/brief.py --stdout
"""

from __future__ import annotations

import argparse
import csv
import sys
from dataclasses import dataclass
from datetime import date, datetime
from pathlib import Path
from typing import Callable

# Fecha anclada del ejemplo. Así el README y el brief no se pudren
# cuando pasa un día. Se puede sobreescribir con --hoy.
HOY_EJEMPLO = date(2026, 9, 27)
RAIZ = Path(__file__).resolve().parent.parent

USAR = "usar"
REVISAR = "revisar"
NO_USAR = "no_usar"

SEMAFORO = {
    USAR: "VERDE — se puede usar",
    REVISAR: "AMARILLO — revisar",
    NO_USAR: "ROJO — no usar en la reunión",
}

LECTURA = {
    USAR: "dato usable en la reunión",
    REVISAR: "hay un problema de calidad; no presentar sin revisar",
    NO_USAR: "dato no apto para afirmar nada en la reunión",
}


@dataclass(frozen=True)
class Regla:
    kpi: str
    pregunta: str
    como_se_calcula: str
    dueno: str
    fuente: str
    usable_si: str


@dataclass(frozen=True)
class Resultado:
    regla: Regla
    estado: str
    valor: float | int
    valor_texto: str
    ultima: date | None
    nota: str


def leer_csv(ruta: Path) -> list[dict[str, str]]:
    if not ruta.exists():
        raise FileNotFoundError(f"no está el archivo: {ruta}")
    with ruta.open(newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def parse_fecha(texto: str | None) -> date | None:
    texto = (texto or "").strip()
    if not texto:
        return None
    return datetime.strptime(texto, "%Y-%m-%d").date()


def dias_desde(hoy: date, fecha: date | None) -> int | None:
    if fecha is None:
        return None
    return (hoy - fecha).days


def formatear_entero(n: int) -> str:
    return f"{n:,}".replace(",", ".")


def formatear_monto(n: float) -> str:
    entero = int(round(n))
    return f"${formatear_entero(entero)}"


def chequear_ingresos(filas: list[dict[str, str]], hoy: date) -> tuple[str, float, date | None, str]:
    if not filas:
        return REVISAR, 0.0, None, "la tabla de ventas está vacía"
    fechas = [parse_fecha(f.get("fecha")) for f in filas]
    validas = [d for d in fechas if d is not None]
    if not validas:
        return REVISAR, 0.0, None, "ninguna fila de ventas tiene fecha"
    ultima = max(validas)
    total = sum(float(f["monto_neto"]) for f in filas)
    antiguedad = dias_desde(hoy, ultima)
    if antiguedad is None or antiguedad > 2:
        return (
            REVISAR,
            total,
            ultima,
            f"la fuente tiene {antiguedad} día(s) (regla: 2 días o menos)",
        )
    return USAR, total, ultima, f"última venta hace {antiguedad} día(s)"


def chequear_clientes(filas: list[dict[str, str]], hoy: date) -> tuple[str, int, date | None, str]:
    if not filas:
        return REVISAR, 0, None, "la tabla de clientes está vacía"
    vacios = [f.get("cliente_id", "?") for f in filas if not (f.get("ultima_compra") or "").strip()]
    activos = 0
    for f in filas:
        d = parse_fecha(f.get("ultima_compra"))
        if d and dias_desde(hoy, d) is not None and dias_desde(hoy, d) <= 90:
            activos += 1
    if vacios:
        return REVISAR, activos, None, f"hay fechas vacías ({', '.join(vacios)})"
    return USAR, activos, None, "no hay fechas vacías"


def chequear_menciones(filas: list[dict[str, str]], hoy: date) -> tuple[str, int, date | None, str]:
    if not filas:
        return NO_USAR, 0, None, "la tabla de menciones está vacía"
    fechas = [parse_fecha(f.get("fecha")) for f in filas]
    validas = [d for d in fechas if d is not None]
    if not validas:
        return NO_USAR, len(filas), None, "ninguna mención tiene fecha"
    ultima = max(validas)
    n = len(filas)
    antiguedad = dias_desde(hoy, ultima)
    if antiguedad is None or antiguedad > 3:
        return (
            NO_USAR,
            n,
            ultima,
            f"última mención hace {antiguedad} día(s) (regla: máximo 3)",
        )
    return USAR, n, ultima, f"última mención hace {antiguedad} día(s)"


CHEQUEOS: dict[str, Callable[[list[dict[str, str]], date], tuple[str, float | int, date | None, str]]] = {
    "ingresos": chequear_ingresos,
    "clientes_activos": chequear_clientes,
    "menciones": chequear_menciones,
}


def cargar_reglas(ruta: Path) -> list[Regla]:
    filas = leer_csv(ruta)
    reglas = []
    for f in filas:
        reglas.append(
            Regla(
                kpi=f["kpi"].strip(),
                pregunta=f["pregunta"].strip(),
                como_se_calcula=f["como_se_calcula"].strip(),
                dueno=f["dueno"].strip(),
                fuente=f.get("fuente", "").strip(),
                usable_si=f["usable_si"].strip(),
            )
        )
    return reglas


def evaluar(reglas: list[Regla], hoy: date, raiz: Path = RAIZ) -> list[Resultado]:
    resultados: list[Resultado] = []
    for regla in reglas:
        chequeo = CHEQUEOS.get(regla.kpi)
        if chequeo is None:
            resultados.append(
                Resultado(
                    regla=regla,
                    estado=REVISAR,
                    valor=0,
                    valor_texto="—",
                    ultima=None,
                    nota=f"no hay chequeo implementado para '{regla.kpi}'",
                )
            )
            continue
        fuente = raiz / regla.fuente if regla.fuente else None
        filas = leer_csv(fuente) if fuente else []
        estado, valor, ultima, nota = chequeo(filas, hoy)
        if regla.kpi == "ingresos":
            valor_texto = formatear_monto(float(valor))
        else:
            valor_texto = formatear_entero(int(valor))
        resultados.append(
            Resultado(
                regla=regla,
                estado=estado,
                valor=valor,
                valor_texto=valor_texto,
                ultima=ultima,
                nota=nota,
            )
        )
    return resultados


def render_brief(resultados: list[Resultado], hoy: date, marca: str = "ejemplo") -> str:
    lineas = [
        "# Brief Norvara",
        "",
        f"Fecha del brief: {hoy.isoformat()}",
        f"Marca de práctica: {marca}.",
        "",
        "Esto no es un dashboard. Es qué números se pueden llevar a una reunión.",
        "",
        "## Semáforo",
        "",
        "| KPI | Valor | Semáforo | Por qué |",
        "| --- | ---: | --- | --- |",
    ]
    for r in resultados:
        lineas.append(
            f"| {r.regla.kpi} | {r.valor_texto} | {SEMAFORO[r.estado]} | {r.nota} |"
        )

    lineas.append("")
    lineas.append("## Detalle")
    lineas.append("")

    for r in resultados:
        lineas.append(f"### {r.regla.kpi}")
        lineas.append(f"- Pregunta: {r.regla.pregunta}")
        lineas.append(f"- Cómo se calcula: {r.regla.como_se_calcula}")
        lineas.append(f"- Dueño: {r.regla.dueno}")
        if r.regla.fuente:
            lineas.append(f"- Fuente: `{r.regla.fuente}`")
        lineas.append(f"- Usable si: {r.regla.usable_si}")
        lineas.append(f"- Valor: {r.valor_texto}")
        if r.ultima:
            lineas.append(f"- Último dato: {r.ultima.isoformat()}")
        lineas.append(f"- Semáforo: {SEMAFORO[r.estado]}")
        lineas.append(f"- Por qué: {r.nota}")
        lineas.append("")

    lineas.append("## Lectura rápida")
    for r in resultados:
        lineas.append(f"- {r.regla.kpi}: {LECTURA[r.estado]}. {r.nota}.")
    lineas.append("")
    return "\n".join(lineas)


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Genera el brief de semáforo de Norvara.")
    parser.add_argument(
        "--hoy",
        default=HOY_EJEMPLO.isoformat(),
        help=f"fecha del brief (YYYY-MM-DD). Por defecto el ejemplo: {HOY_EJEMPLO.isoformat()}",
    )
    parser.add_argument(
        "--marca",
        default="ejemplo",
        help="nombre de la marca que aparece en el brief",
    )
    parser.add_argument(
        "--stdout",
        action="store_true",
        help="imprimir el brief en stdout además de escribirlo",
    )
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    hoy = parse_fecha(args.hoy)
    if hoy is None:
        print("fecha --hoy inválida; usar YYYY-MM-DD", file=sys.stderr)
        return 2

    reglas = cargar_reglas(RAIZ / "metrics" / "kpis.csv")
    resultados = evaluar(reglas, hoy, RAIZ)
    texto = render_brief(resultados, hoy, marca=args.marca)

    salida = RAIZ / "output" / "brief.md"
    salida.parent.mkdir(parents=True, exist_ok=True)
    salida.write_text(texto, encoding="utf-8")
    print(f"Listo. Brief escrito en {salida.relative_to(RAIZ)}")
    if args.stdout:
        print()
        print(texto)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
