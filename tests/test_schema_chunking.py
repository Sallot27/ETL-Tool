import pandas as pd
import tempfile
import os
from python_etl.extract import extract_csv_chunked
from python_etl.schema import people_schema, validate_df


def test_chunked_csv(tmp_path):
    data = "name,age,old_name,address,salary\nAlice,30,engineer,addr1,60000\nBob,17,student,addr2,0\nCharlie,40,manager,addr3,90000\n"
    p = tmp_path / "sample.csv"
    p.write_text(data)

    # chunksize 2 -> should produce 2 chunks (2 rows, then 1 row)
    it = extract_csv_chunked(str(p), chunksize=2)
    chunks = list(it)
    assert len(chunks) == 2
    assert chunks[0].iloc[0]["name"].strip() == "Alice"


def test_schema_validation_passes():
    df = pd.DataFrame({
        "name": ["Alice", "Bob"],
        "age": [30, 25],
        "old_name": ["x", "y"],
        "address": ["a", "b"],
        "salary": [1000.0, 2000.0],
    })
    assert validate_df(df, people_schema) is True
