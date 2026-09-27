"""Pruebas del semáforo con los datos de práctica (hoy = 2026-09-27)."""

import sys
import unittest
from datetime import date
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(RAIZ / "src"))

from brief import (  # noqa: E402
    HOY_EJEMPLO,
    NO_USAR,
    REVISAR,
    USAR,
    cargar_reglas,
    evaluar,
    render_brief,
)


class TestDatosDePractica(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.hoy = HOY_EJEMPLO
        cls.reglas = cargar_reglas(RAIZ / "metrics" / "kpis.csv")
        cls.resultados = {r.regla.kpi: r for r in evaluar(cls.reglas, cls.hoy, RAIZ)}

    def test_hay_tres_kpis(self):
        self.assertEqual(set(self.resultados), {"ingresos", "clientes_activos", "menciones"})

    def test_ingresos_verde(self):
        r = self.resultados["ingresos"]
        self.assertEqual(r.estado, USAR)
        self.assertEqual(r.valor, 206612.0)
        self.assertEqual(r.valor_texto, "$206.612")
        self.assertEqual(r.ultima, date(2026, 9, 25))

    def test_clientes_amarillo_por_fecha_vacia(self):
        r = self.resultados["clientes_activos"]
        self.assertEqual(r.estado, REVISAR)
        self.assertEqual(r.valor, 2)
        self.assertIn("C004", r.nota)

    def test_menciones_rojo_por_dato_viejo(self):
        r = self.resultados["menciones"]
        self.assertEqual(r.estado, NO_USAR)
        self.assertEqual(r.valor, 3)
        self.assertEqual(r.ultima, date(2026, 9, 15))
        self.assertIn("12", r.nota)

    def test_brief_incluye_tabla_y_lectura(self):
        texto = render_brief(list(self.resultados.values()), self.hoy)
        self.assertIn("# Brief Norvara", texto)
        self.assertIn("| KPI |", texto)
        self.assertIn("## Lectura rápida", texto)
        self.assertIn("VERDE", texto)
        self.assertIn("AMARILLO", texto)
        self.assertIn("ROJO", texto)


if __name__ == "__main__":
    unittest.main()
