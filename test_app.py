import tempfile
import unittest
from pathlib import Path
from app import GestorTareas, OrdenPorPrioridad, FabricaTareas

class Pruebas(unittest.TestCase):
    def test_fabrica_valida(self):
        with self.assertRaises(ValueError):
            FabricaTareas.crear(1, '', 'alta')
    def test_crear_persistir_y_completar(self):
        with tempfile.TemporaryDirectory() as carpeta:
            ruta = Path(carpeta) / 'tareas.json'
            gestor = GestorTareas(ruta)
            gestor.agregar('Revisar codigo', 'baja')
            gestor.agregar('Corregir error', 'alta')
            self.assertEqual(gestor.listar(OrdenPorPrioridad())[0].titulo, 'Corregir error')
            gestor.completar(1)
            self.assertTrue(GestorTareas(ruta).tareas[0].completada)

if __name__ == '__main__':
    unittest.main()
