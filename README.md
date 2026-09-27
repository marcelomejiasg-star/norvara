# Norvara

Brief automatico: que numeros de una marca o de un negocio se pueden llevar a una reunion y cuales no.

No es un dashboard. Lee definiciones de KPI, controla si el dato esta fresco y completo, y escribe un semaforo:
- usar (verde)
- revisar (amarillo)
- no usar (rojo)

## Que hay aca

- `metrics/kpis.csv` — que significa cada numero
- `data/` — tablas de ejemplo (con trampas a proposito)
- `src/brief.py` — el script
- `output/brief.md` — el brief generado

## Como correrlo

Desde esta carpeta:

```bash
python3 src/brief.py
```

Sale `output/brief.md`.

Datos de practica (septiembre 2026):

- Ingresos: usar (verde) — dato reciente, monto neto
- Clientes activos: revisar (amarillo) — una fecha vacia
- Menciones: no usar (rojo) — ultima fila con 12 dias

## Stack de esta version

Python 3, CSV, Git. A proposito, sin panel ni servidor.

## Autor

Proyecto de Norvara (inteligencia de marca con dato usable).
