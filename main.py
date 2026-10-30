"""Inicializa analytics.db y demuestra el mapeo ORM estilo SQLAlchemy 2.0."""

from sqlalchemy import create_engine, func, inspect, select
from sqlalchemy.orm import Session

from models import Base, Dataset, ModelExperiment


def main() -> None:
    # Se crea una base SQLite real (persistente) en el directorio actual.
    engine = create_engine("sqlite:///analytics.db")

    try:
        # Registra las tablas declaradas sin borrarlas si ya existen.
        Base.metadata.create_all(engine)
        nombres = set(inspect(engine).get_table_names())
        assert {"datasets", "model_experiments"}.issubset(nombres)
        print("TABLAS CREADAS / VERIFICADAS: datasets, model_experiments")

        # Instanciación de los objetos pedidos en el ejercicio.
        # Valores ficticios: no representan resultados de un entrenamiento real.
        dataset_ejemplo = Dataset(
            name="Ventas de prueba",
            source_url="https://example.com/datasets/ventas_demo.csv",
            num_rows=1500,
        )
        experimento_ejemplo = ModelExperiment(
            algorithm_name="RandomForest (demostración)",
            accuracy=0.87,
            is_deployed=False,
        )
        print("OBJETOS ORM INSTANCIADOS:")
        print(f"  Dataset: {dataset_ejemplo.name} | filas: {dataset_ejemplo.num_rows}")
        print(
            f"  ModelExperiment: {experimento_ejemplo.algorithm_name} | "
            f"accuracy: {experimento_ejemplo.accuracy:.2f} | "
            f"desplegado: {experimento_ejemplo.is_deployed}"
        )

        # Paso extra opcional: guardar y leer datos con una Session moderna.
        # Evita duplicar los ejemplos al ejecutar main.py más de una vez.
        with Session(engine) as session:
            existe_dataset = session.scalar(
                select(Dataset.id).where(Dataset.name == dataset_ejemplo.name).limit(1)
            )
            existe_experimento = session.scalar(
                select(ModelExperiment.id)
                .where(ModelExperiment.algorithm_name == experimento_ejemplo.algorithm_name)
                .limit(1)
            )
            if existe_dataset is None:
                session.add(dataset_ejemplo)
            if existe_experimento is None:
                session.add(experimento_ejemplo)
            session.commit()

            cantidad_datasets = session.scalar(select(func.count()).select_from(Dataset))
            cantidad_experimentos = session.scalar(
                select(func.count()).select_from(ModelExperiment)
            )
            print(f"DATOS PERSISTIDOS: {cantidad_datasets} datasets y {cantidad_experimentos} experimentos")

        print("ARCHIVO GENERADO: analytics.db")
        print("VALIDACIONES FINALES: OK")
    finally:
        engine.dispose()


if __name__ == "__main__":
    main()
