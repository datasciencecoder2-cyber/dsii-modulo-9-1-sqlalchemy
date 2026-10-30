"""Pruebas sin dependencia de red ni modificaciones a la BD del usuario."""

import sqlite3
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

from sqlalchemy import Boolean, Float, Integer, String, create_engine, inspect, select
from sqlalchemy.orm import Session

# Permite ejecutar: py -m unittest discover -s tests -v
PROYECTO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROYECTO))

from models import Base, Dataset, ModelExperiment  # noqa: E402


class TestSQLAlchemy20(unittest.TestCase):
    def setUp(self):
        self.engine = create_engine("sqlite+pysqlite:///:memory:")
        Base.metadata.create_all(self.engine)

    def tearDown(self):
        self.engine.dispose()

    def test_01_base_declarativa_20(self):
        from sqlalchemy.orm import DeclarativeBase
        self.assertTrue(issubclass(Base, DeclarativeBase))

    def test_02_tablas_y_nombres(self):
        self.assertEqual(set(inspect(self.engine).get_table_names()), {"datasets", "model_experiments"})

    def test_03_dataset_campos_y_pk(self):
        columnas = {c["name"]: c for c in inspect(self.engine).get_columns("datasets")}
        self.assertEqual(set(columnas), {"id", "name", "source_url", "num_rows"})
        self.assertEqual([c["name"] for c in columnas.values() if c["primary_key"]], ["id"])

    def test_04_experimento_campos_y_pk(self):
        columnas = {c["name"]: c for c in inspect(self.engine).get_columns("model_experiments")}
        self.assertEqual(set(columnas), {"id", "algorithm_name", "accuracy", "is_deployed"})
        self.assertEqual([c["name"] for c in columnas.values() if c["primary_key"]], ["id"])

    def test_05_tipos_de_columnas(self):
        self.assertIsInstance(Dataset.__table__.c.name.type, String)
        self.assertIsInstance(Dataset.__table__.c.num_rows.type, Integer)
        self.assertIsInstance(ModelExperiment.__table__.c.accuracy.type, Float)
        self.assertIsInstance(ModelExperiment.__table__.c.is_deployed.type, Boolean)

    def test_06_mapped_typed(self):
        from sqlalchemy.orm import Mapped
        self.assertTrue(all("Mapped" in str(field) for field in (
            Dataset.__annotations__["id"],
            Dataset.__annotations__["name"],
            Dataset.__annotations__["num_rows"],
            ModelExperiment.__annotations__["accuracy"],
            ModelExperiment.__annotations__["is_deployed"],
        )))

    def test_07_instancia_de_ambos_modelos(self):
        dato = Dataset(name="Muestra", source_url="https://example.com", num_rows=12)
        exp = ModelExperiment(algorithm_name="Prueba", accuracy=0.7, is_deployed=False)
        self.assertEqual(dato.num_rows, 12)
        self.assertFalse(exp.is_deployed)

    def test_08_persistencia_y_lectura_de_ambos(self):
        with Session(self.engine) as session:
            session.add_all([
                Dataset(name="Muestra", source_url="https://example.com", num_rows=12),
                ModelExperiment(algorithm_name="Prueba", accuracy=0.7, is_deployed=False),
            ])
            session.commit()
            self.assertEqual(len(session.scalars(select(Dataset)).all()), 1)
            self.assertEqual(len(session.scalars(select(ModelExperiment)).all()), 1)

    def test_09_restriccion_filas_no_negativas(self):
        from sqlalchemy.exc import IntegrityError
        with Session(self.engine) as session:
            session.add(Dataset(name="Incorrecto", source_url="https://example.com", num_rows=-3))
            with self.assertRaises(IntegrityError):
                session.commit()
            session.rollback()

    def test_10_restriccion_accuracy_0_a_1(self):
        from sqlalchemy.exc import IntegrityError
        with Session(self.engine) as session:
            session.add(ModelExperiment(algorithm_name="Incorrecto", accuracy=1.3, is_deployed=False))
            with self.assertRaises(IntegrityError):
                session.commit()
            session.rollback()

    def test_11_main_crea_db_fisica_y_ejemplos_idempotentes(self):
        with tempfile.TemporaryDirectory() as carpeta:
            for _ in range(2):
                ejecucion = subprocess.run(
                    [sys.executable, str(PROYECTO / "main.py")],
                    cwd=carpeta, capture_output=True, text=True, check=True,
                )
                self.assertIn("VALIDACIONES FINALES: OK", ejecucion.stdout)
            db = Path(carpeta) / "analytics.db"
            self.assertTrue(db.is_file())
            with sqlite3.connect(db) as conexion:
                self.assertEqual(conexion.execute("SELECT COUNT(*) FROM datasets").fetchone()[0], 1)
                self.assertEqual(conexion.execute("SELECT COUNT(*) FROM model_experiments").fetchone()[0], 1)

    def test_12_create_all_es_idempotente(self):
        Base.metadata.create_all(self.engine)
        self.assertEqual(len(inspect(self.engine).get_table_names()), 2)


if __name__ == "__main__":
    unittest.main()
