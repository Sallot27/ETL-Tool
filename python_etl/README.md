# Python ETL (pandera + chunked CSV)

This folder contains the Python ETL engine core for Sallot27/ETL-Tool. PR 1 adds pandera-based schema validation and chunked CSV extraction.

Quick use:

1. Install deps: pip install -e .
2. Run pipeline: python -m python_etl.main run --config config/config.yaml

Config supports `source.chunked: true` and `source.chunksize: <int>` to enable chunked processing.
