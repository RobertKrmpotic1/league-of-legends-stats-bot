from datetime import datetime
from loguru import logger
import sqlite3
import pandas as pd
from sqlalchemy import create_engine

db_uri = "sqlite:///database.db"
engine = create_engine(db_uri)


def write_to_database(df: pd.DataFrame, db_name: str = "Users", if_exists="replace"):
    """Writes a dataframe to a table in the database. Can choose what to do when the table already exists"""
    df.to_sql(name=db_name, con=engine, index=False, if_exists=if_exists)


def read_database(query: str) -> pd.DataFrame:
    """Reads a query and returns a dataframe"""
    con = sqlite3.connect("database.db")
    df = pd.read_sql_query(query, con)
    return df


def execute_query(query: str):

    with sqlite3.connect("database.db") as con:
        con.execute(query)
