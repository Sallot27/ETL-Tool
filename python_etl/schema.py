import pandera as pa
from pandera import Column, DataFrameSchema, Check
from typing import Optional

# Example schema for a 'people' dataset
people_schema = DataFrameSchema(
    {
        "name": Column(pa.String, nullable=False, checks=Check.str_length(min_value=1)),
        "age": Column(pa.Int, nullable=True),
        "old_name": Column(pa.String, nullable=True),
        "address": Column(pa.String, nullable=True),
        "salary": Column(pa.Float, nullable=True),
    },
    coerce=True,
)

# Utility function to validate a DataFrame with a schema (or schema object)
def validate_df(df, schema=None, strict=True):
    """Validate a pandas DataFrame with a pandera schema.

    Args:
        df: pandas.DataFrame
        schema: either a pandera DataFrameSchema or a dict with name mapping to schema key
        strict: if True, raise errors on validation failures. If False, return False on failure.
    Returns:
        True if validation passes (or schema is None). Raises pandera errors if strict=True.
    """
    if schema is None:
        return True
    try:
        # if schema is a string key mapping, support that later; for now, accept DataFrameSchema
        schema.validate(df, lazy=not strict)
        return True
    except Exception:
        if strict:
            raise
        return False
