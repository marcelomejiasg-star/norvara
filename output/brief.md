# Brief Norvara

Fecha del brief: 2026-09-27
Marca de práctica: ejemplo.

Esto no es un dashboard. Es qué números se pueden llevar a una reunión.

## Semáforo

| KPI | Valor | Semáforo | Por qué |
| --- | ---: | --- | --- |
| ingresos | $206.612 | VERDE — se puede usar | última venta hace 2 día(s) |
| clientes_activos | 2 | AMARILLO — revisar | hay fechas vacías (C004) |
| menciones | 3 | ROJO — no usar en la reunión | última mención hace 12 día(s) (regla: máximo 3) |

## Detalle

### ingresos
- Pregunta: ¿Cuánto vendimos este mes?
- Cómo se calcula: suma de monto_neto
- Dueño: finanzas
- Fuente: `data/ventas.csv`
- Usable si: la última fila tiene 2 días o menos
- Valor: $206.612
- Último dato: 2026-09-25
- Semáforo: VERDE — se puede usar
- Por qué: última venta hace 2 día(s)

### clientes_activos
- Pregunta: ¿Quién compró en los últimos 90 días?
- Cómo se calcula: contar clientes con compra reciente
- Dueño: comercial
- Fuente: `data/clientes.csv`
- Usable si: no hay filas con fecha vacía
- Valor: 2
- Semáforo: AMARILLO — revisar
- Por qué: hay fechas vacías (C004)

### menciones
- Pregunta: ¿De qué se habla de la marca?
- Cómo se calcula: contar filas de menciones
- Dueño: marca
- Fuente: `data/menciones.csv`
- Usable si: la última mención tiene 3 días o menos
- Valor: 3
- Último dato: 2026-09-15
- Semáforo: ROJO — no usar en la reunión
- Por qué: última mención hace 12 día(s) (regla: máximo 3)

## Lectura rápida
- ingresos: dato usable en la reunión. última venta hace 2 día(s).
- clientes_activos: hay un problema de calidad; no presentar sin revisar. hay fechas vacías (C004).
- menciones: dato no apto para afirmar nada en la reunión. última mención hace 12 día(s) (regla: máximo 3).
