import sqlite3
import pandas as pd

DB_PATH = r"C:projects\final\flask_events_app\flask_events_app\app.db"


def execute_query(query: str, db_path: str) -> pd.DataFrame:
    with sqlite3.connect(db_path) as connect:
        return pd.read_sql(query, connect)


_sql = "select id, text from event"
_description_df = execute_query(_sql, DB_PATH)
assert "text" in _description_df.columns


def get_data_from_db_by_search(search_request: str) -> dict:
    _filter_df = lambda row: search_request.lower() in row['text'].lower()
    description_df = _description_df[_description_df.apply(_filter_df, axis=1)]
    ids_you_are_looking_for = list(map(str, description_df['id']))
    ids_str = ",".join(ids_you_are_looking_for)
    sql_for_search = f"select * from event where id in ({ ids_str })"
    result_of_query = execute_query(sql_for_search, DB_PATH)
    all_search_results = result_of_query.values.tolist()
    return all_search_results
