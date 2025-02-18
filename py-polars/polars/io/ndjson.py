from __future__ import annotations

from typing import TYPE_CHECKING

import polars._reexport as pl
from polars.datatypes import N_INFER_DEFAULT
from polars.utils.deprecation import deprecate_renamed_parameter

if TYPE_CHECKING:
    from io import IOBase
    from pathlib import Path

    from polars import DataFrame, LazyFrame
    from polars.type_aliases import SchemaDefinition


def read_ndjson(
    source: str | Path | IOBase | bytes,
    *,
    schema: SchemaDefinition | None = None,
    schema_overrides: SchemaDefinition | None = None,
    ignore_errors: bool = False,
) -> DataFrame:
    """
    Read into a DataFrame from a newline delimited JSON file.

    Parameters
    ----------
    source
        Path to a file or a file-like object (by file-like object, we refer to objects
        that have a `read()` method, such as a file handler (e.g. via builtin `open`
        function) or `BytesIO`).
    schema : Sequence of str, (str,DataType) pairs, or a {str:DataType,} dict
        The DataFrame schema may be declared in several ways:

        * As a dict of {name:type} pairs; if type is None, it will be auto-inferred.
        * As a list of column names; in this case types are automatically inferred.
        * As a list of (name,type) pairs; this is equivalent to the dictionary form.

        If you supply a list of column names that does not match the names in the
        underlying data, the names given here will overwrite them. The number
        of names given in the schema should match the underlying data dimensions.
    schema_overrides : dict, default None
        Support type specification or override of one or more columns; note that
        any dtypes inferred from the schema param will be overridden.
    ignore_errors
        Return `Null` if parsing fails because of schema mismatches.
    """
    return pl.DataFrame._read_ndjson(
        source,
        schema=schema,
        schema_overrides=schema_overrides,
        ignore_errors=ignore_errors,
    )


@deprecate_renamed_parameter("row_count_name", "row_index_name", version="0.20.4")
@deprecate_renamed_parameter("row_count_offset", "row_index_offset", version="0.20.4")
def scan_ndjson(
    source: str | Path | list[str] | list[Path],
    *,
    schema: SchemaDefinition | None = None,
    infer_schema_length: int | None = N_INFER_DEFAULT,
    batch_size: int | None = 1024,
    n_rows: int | None = None,
    low_memory: bool = False,
    rechunk: bool = False,
    row_index_name: str | None = None,
    row_index_offset: int = 0,
    ignore_errors: bool = False,
) -> LazyFrame:
    """
    Lazily read from a newline delimited JSON file or multiple files via glob patterns.

    This allows the query optimizer to push down predicates and projections to the scan
    level, thereby potentially reducing memory overhead.

    Parameters
    ----------
    source
        Path to a file.
    schema : Sequence of str, (str,DataType) pairs, or a {str:DataType,} dict
        The DataFrame schema may be declared in several ways:

        * As a dict of {name:type} pairs; if type is None, it will be auto-inferred.
        * As a list of column names; in this case types are automatically inferred.
        * As a list of (name,type) pairs; this is equivalent to the dictionary form.

        If you supply a list of column names that does not match the names in the
        underlying data, the names given here will overwrite them. The number
        of names given in the schema should match the underlying data dimensions.
    infer_schema_length
        The maximum number of rows to scan for schema inference.
        If set to `None`, the full data may be scanned *(this is slow)*.
    batch_size
        Number of rows to read in each batch.
    n_rows
        Stop reading from JSON file after reading `n_rows`.
    low_memory
        Reduce memory pressure at the expense of performance.
    rechunk
        Reallocate to contiguous memory when all chunks/ files are parsed.
    row_index_name
        If not None, this will insert a row index column with give name into the
        DataFrame
    row_index_offset
        Offset to start the row index column (only use if the name is set)
    ignore_errors
        Return `Null` if parsing fails because of schema mismatches.
    """
    return pl.LazyFrame._scan_ndjson(
        source,
        infer_schema_length=infer_schema_length,
        schema=schema,
        batch_size=batch_size,
        n_rows=n_rows,
        low_memory=low_memory,
        rechunk=rechunk,
        row_index_name=row_index_name,
        row_index_offset=row_index_offset,
        ignore_errors=ignore_errors,
    )
