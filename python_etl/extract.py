import pandas as pd
import requests
from typing import Dict, Any, Iterator


def extract_csv(path: str, **kwargs) -> pd.DataFrame:
    df = pd.read_csv(path, **kwargs)
    return df


def extract_csv_chunked(path: str, chunksize: int = 10000, **kwargs) -> Iterator[pd.DataFrame]:
    # pandas.read_csv with chunksize returns TextFileReader which yields DataFrames
    return pd.read_csv(path, chunksize=chunksize, **kwargs)


def extract_http_json(url: str, params: Dict[str, Any] = None, json_path: str = None, **kwargs) -> pd.DataFrame:
    resp = requests.get(url, params=params, timeout=30)
    resp.raise_for_status()
    payload = resp.json()
    if json_path:
        for part in json_path.split('.'):
            payload = payload.get(part, {})
    if isinstance(payload, list):
        return pd.DataFrame(payload)
    elif isinstance(payload, dict):
        return pd.DataFrame([payload])
    else:
        raise ValueError("Unsupported JSON payload shape for conversion to DataFrame")


def extract(source: Dict[str, Any]):
    kind = source.get("type")
    if kind == "csv":
        if source.get("chunked", False):
            return extract_csv_chunked(source["path"], chunksize=source.get("chunksize", 10000), **source.get("params", {}))
        return extract_csv(source["path"], **source.get("params", {}))
    elif kind == "http_json":
        return extract_http_json(source["url"], params=source.get("params"), json_path=source.get("json_path"))
    else:
        raise ValueError(f"Unknown source type: {kind}")
