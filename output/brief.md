# Brief Norvara

Fecha del brief: 2026-09-27
Marca de practica: ejemplo.

Esto no es un dashboard. Es que numeros se pueden llevar a una reunion.

## ingresos
- Pregunta: Cuanto vendimos este mes?
- Como se calcula: suma de monto_neto
- Dueno: finanzas
- Valor: 206612.0
- Ultimo dato: 2026-09-25
- Semaforo: VERDE — se puede usar
- Por que: ultima venta hace 2 dia(s)

## clientes_activos
- Pregunta: Quien compro en los ultimos 90 dias?
- Como se calcula: contar clientes con compra reciente
- Dueno: comercial
- Valor: 2
- Semaforo: AMARILLO — revisar
- Por que: hay fechas vacias (C004)

## menciones
- Pregunta: De que se habla de la marca?
- Como se calcula: contar filas de menciones
- Dueno: marca
- Valor: 3
- Ultimo dato: 2026-09-15
- Semaforo: ROJO — no usar en reunion
- Por que: ultima mencion hace 12 dias (regla: maximo 3)

## Lectura rapida
- Ingresos: dato reciente. Se puede usar el neto.
- Clientes activos: hay una fila sin fecha. Revisar antes de presentar.
- Menciones: dato viejo. No decir 'esta semana' en una reunion.
