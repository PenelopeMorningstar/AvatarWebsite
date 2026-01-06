from flask import g, current_app
import os
import psycopg2.pool


def init_db_pool():
    current_app.db_pool = psycopg2.pool.SimpleConnectionPool(
        1, 10, dsn=os.getenv("CONNECTION_STRING")
    )


def get_db():
    db = getattr(g, "_database", None)
    if db is None:
        g._database = current_app.db_pool.getconn()
    return g._database


def close_connection(exception):
    db = getattr(g, "_database", None)
    if db is not None:
        current_app.db_pool.putconn(db)


def init_db():
    init_db_pool()
    db = get_db()
    cursor = db.cursor()
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS records (
            id              serial primary key,
            time            timestamp not null,
            robot_id        smallint not null,
            robot_state     smallint not null,
            line            smallint not null,
            motor_left      smallint not null,
            motor_right     smallint not null,
            ultra_front     smallint not null,
            ultra_right     smallint,
            grip            smallint not null,
            gyro_z          real,
            heading         real
        );
    """
    )
    db.commit()


def insert_record(values):
    db = get_db()
    cursor = db.cursor()
    cursor.execute(
        """INSERT INTO records (time,
        robot_id, robot_state, line, motor_left, motor_right,
        ultra_front, ultra_right, grip, gyro_z, heading)
        VALUES (CURRENT_TIMESTAMP,  %s, %s, %s, %s, %s,  %s, %s, %s, %s, %s)
        """,
        values,
    )
    db.commit()
    return cursor.rowcount == 1


def get_latest_record():
    db = get_db()
    cursor = db.cursor()
    cursor.execute("SELECT * FROM records ORDER BY id DESC LIMIT 1")
    return cursor.fetchone()
