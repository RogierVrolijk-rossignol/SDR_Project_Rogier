from oopsql import OopSqlClass
import csv


def main():
    db = connect_clean()
    insert_csv_data(db)

    survival_by_embarked(db)
    survival_by_sex(db)
    survival_by_age_group(db)

    update_passenger_survival(db)

    db._conn.close()


def connect_clean():
    db = OopSqlClass("titanic.db")

    db._cursor.execute("DELETE FROM tickets")
    db._conn.commit()

    return db


def insert_csv_data(db):
    with open("titanic.csv", newline="", encoding="utf-8") as file:
        reader = csv.DictReader(file)

        insert_query = """
        INSERT INTO tickets
        (
            PassengerId, Survived, Pclass, Name, Sex, Age,
            SibSp, Parch, Ticket, Fare, Cabin, Embarked
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """

        for row in reader:
            db._cursor.execute(
                insert_query,
                (
                    int(row["PassengerId"]),
                    int(row["Survived"]),
                    int(row["Pclass"]),
                    row["Name"],
                    row["Sex"],
                    float(row["Age"]) if row["Age"] != "" else None,
                    int(row["SibSp"]),
                    int(row["Parch"]),
                    row["Ticket"],
                    float(row["Fare"]),
                    row["Cabin"],
                    row["Embarked"],
                )
            )

    db._conn.commit()


def survival_by_embarked(db):
    query_station = """
    SELECT Embarked, COUNT(*) AS total, SUM(Survived) AS survived
    FROM tickets
    WHERE Embarked != ''
    GROUP BY Embarked
    """

    db._cursor.execute(query_station)
    results = db._cursor.fetchall()

    print("\nSurvival rate by embarkment station:")

    for row in results:
        station = row["Embarked"]
        total = row["total"]
        survived = row["survived"]
        survival_rate = survived / total * 100

        print(f"Station {station}: {survived}/{total} survived = {survival_rate:.2f}%")


def survival_by_sex(db):
    query_sex = """
    SELECT Sex, COUNT(*) AS total, SUM(Survived) AS survived
    FROM tickets
    GROUP BY Sex
    """

    db._cursor.execute(query_sex)
    results = db._cursor.fetchall()

    print("\nSurvival rate by sex:")

    for row in results:
        sex = row["Sex"]
        total = row["total"]
        survived = row["survived"]
        survival_rate = survived / total * 100

        print(f"{sex}: {survived}/{total} survived = {survival_rate:.2f}%")


def survival_by_age_group(db):
    query_age = """
    SELECT
        CASE
            WHEN Age < 30 THEN 'Young'
            WHEN Age >= 30 AND Age <= 50 THEN 'Middle'
            WHEN Age > 50 THEN 'Old'
        END AS age_group,
        COUNT(*) AS total,
        SUM(Survived) AS survived
    FROM tickets
    WHERE Age IS NOT NULL
    GROUP BY age_group
    """

    db._cursor.execute(query_age)
    results = db._cursor.fetchall()

    print("\nSurvival rate by age group:")

    for row in results:
        age_group = row["age_group"]
        total = row["total"]
        survived = row["survived"]
        survival_rate = survived / total * 100

        print(f"{age_group}: {survived}/{total} survived = {survival_rate:.2f}%")


def update_passenger_survival(db):
    passenger_id = int(input("\nGive passenger ID: "))

    select_query = """
    SELECT *
    FROM tickets
    WHERE PassengerId = ?
    """

    db._cursor.execute(select_query, (passenger_id,))
    record = db._cursor.fetchone()

    print("\nCurrent passenger data:")
    print(record)

    new_survival = int(input("Did this passenger survive? 1 = yes, 0 = no: "))

    update_query = """
    UPDATE tickets
    SET Survived = ?
    WHERE PassengerId = ?
    """

    db._cursor.execute(update_query, (new_survival, passenger_id))
    db._conn.commit()

    db._cursor.execute(select_query, (passenger_id,))
    new_record = db._cursor.fetchone()

    print("\nUpdated passenger data:")
    print(new_record)


if __name__ == "__main__":
    main()