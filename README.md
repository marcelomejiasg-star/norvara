# Norvara

Brief automático: qué números de una marca o de un negocio se pueden llevar a una reunión, y cuáles no.

No es un dashboard. Lee definiciones de KPI, controla si el dato está fresco y completo, y escribe un semáforo:

- **usar** (verde)
- **revisar** (amarillo)
- **no usar** (rojo)

Un recruiter puede abrir `output/brief.md`. Un cliente entiende la pregunta: *¿esto se puede decir en la reunión?*

## Por qué existe

Los tableros muestran el número. Casi nunca muestran si el número está definido, completo y al día. Norvara separa esas dos cosas: primero la aptitud del dato, después —si aplica— el valor.

Los datos de práctica tienen trampas a propósito. El script las encuentra.

## Cómo correrlo

Desde la raíz del repo, sin dependencias:

```bash
python3 src/brief.py
```

Sale `output/brief.md`. La fecha del ejemplo está anclada en `2026-09-27` para que el brief no se pudra al día siguiente. Se puede cambiar:

```bash
python3 src/brief.py --hoy 2026-09-27 --stdout
python3 -m unittest discover -s tests -v
```

## Qué hay acá

| Ruta | Para qué |
| --- | --- |
| `metrics/kpis.csv` | qué significa cada número, quién es dueño y cuándo es usable |
| `data/` | tablas de ejemplo (con trampas) |
| `src/brief.py` | el script: chequea y escribe el brief |
| `tests/test_brief.py` | las tres trampas tienen que seguir saliendo igual |
| `output/brief.md` | lo que se lleva a la reunión |

## Datos de práctica (27 de septiembre de 2026)

| KPI | Semáforo | Por qué |
| --- | --- | --- |
| Ingresos | verde — usar | última venta el 25/09; monto neto $206.612 |
| Clientes activos | amarillo — revisar | C004 no tiene fecha |
| Menciones | rojo — no usar | última fila con 12 días; no se puede decir “esta semana” |

Tres modos de fallo distintos: frescura, completitud, frescura que ya no admite el claim.

## Criterio del semáforo

- **Verde:** la regla de `usable_si` se cumple. El número se puede decir.
- **Amarillo:** el cálculo se puede hacer, pero hay un hueco (fila vacía, fuente al límite). Hay que revisar antes de presentar.
- **Rojo:** el dato no sostiene la frase que alguien querría decir en la reunión.

Cada KPI tiene dueño (`finanzas`, `comercial`, `marca`). Si el semáforo no es verde, el dueño es quien tiene que responder.

## Stack de esta versión

Python 3, CSV, Git. A propósito: sin panel, sin servidor, sin librerías externas.

## Autor

Proyecto de Norvara — inteligencia de marca con dato usable.
