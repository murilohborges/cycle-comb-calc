import json
from sqlmodel import Session, select
from .create import create_db_and_tables
from .models import Substance, CorrelationSpecificHeat
from .engine import engine


def populate_database_tables():
    with open("database/default_substances.json", "r", encoding="utf-8") as f:
        data = json.load(f)

    with Session(engine) as session:
        """Creating substance and fill the params of correlation"""
        for item in data:
            existing = session.exec(
                select(Substance).where(Substance.name == item["name"])
            ).first()

            if existing:
                print(f"Substance '{item['name']}' already exists. Skipping.")
                continue

            substance = Substance(
                name=item["name"],
                molar_mass=item["molar_mass"],
                lower_calorific_value=item["lower_calorific_value"],
                is_default=item["is_default"]
            )
            session.add(substance)
            session.commit()

            corr = CorrelationSpecificHeat(
                substance_id=substance.id,
                param_A=item["param_A"],
                param_B=item["param_B"],
                param_C=item["param_C"],
                param_D=item["param_D"],
                is_default=item["is_default"]
            )
            session.add(corr)

        session.commit()
        print("Finished populating database.")


if __name__ == "__main__":
    create_db_and_tables()
    populate_database_tables()
