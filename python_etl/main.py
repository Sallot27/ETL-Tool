import click
import logging
from .config import load_config
from .extract import extract
from .transform import transform
from .load import load
from .schema import validate_df
import sys
import pandas as pd

logger = logging.getLogger("python_etl")
handler = logging.StreamHandler(sys.stdout)
formatter = logging.Formatter("%(asctime)s %(levelname)s %(message)s")
handler.setFormatter(formatter)
logger.addHandler(handler)

@click.group()
def cli():
    pass

@cli.command()
@click.option("--config", "-c", required=True, type=click.Path(exists=True), help="Path to YAML config")
@click.option("--log-level", default="INFO", help="Logging level")
@click.option("--fail-on-validate/--no-fail-on-validate", default=True, help="Fail on schema validation errors")
def run(config, log_level, fail_on_validate):
    logger.setLevel(getattr(logging, log_level.upper(), logging.INFO))
    cfg = load_config(config)
    logger.info("Starting extraction")
    src = cfg.source
    data_iter = extract(src)

    # load schema if present
    schema_cfg = cfg.schema or None

    def process_df(df: pd.DataFrame):
        logger.info("Extracted %d rows", len(df))
        logger.info("Starting transformation")
        df2 = transform(df, cfg.transform or {})
        logger.info("Transformed to %d rows / %d columns", len(df2), len(df2.columns))
        # validate
        if schema_cfg:
            try:
                validate_df(df2, schema_cfg, strict=fail_on_validate)
                logger.info("Schema validation passed")
            except Exception as e:
                logger.exception("Schema validation failed")
                if fail_on_validate:
                    raise
        logger.info("Starting load")
        res = load(df2, cfg.target)
        logger.info("Load result: %s", res)

    # If data_iter is an iterator (chunks), iterate; else process single DF
    if hasattr(data_iter, "__iter__") and not isinstance(data_iter, pd.DataFrame):
        for chunk in data_iter:
            process_df(chunk)
    else:
        process_df(data_iter)

if __name__ == "__main__":
    cli()
