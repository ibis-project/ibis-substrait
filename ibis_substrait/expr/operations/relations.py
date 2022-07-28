import typing
import urllib.parse

import ibis.expr.operations.relations as rel
import ibis.expr.rules as rlz
from ibis.common.grounds import Annotable, Comparable
from ibis.common.validators import validator


@validator  # type: ignore[misc]
def valid_uri(arg: str, **kwargs: typing.Dict[typing.Any, typing.Any]) -> str:
    arg = rlz.instance_of(str, arg)
    uri = urllib.parse.urlparse(arg)
    if not uri.scheme:
        raise ValueError(f"Missing URI scheme in '{arg}'")
    return arg


class FileFormat(Annotable, Comparable):
    """
    Base class representing the format of files in a LocalFiles.
    """

    def __equals__(self, other: typing.Any) -> bool:
        if type(other) is not type(self):
            raise TypeError(
                f"invalid equality comparison between DataType and {type(other)}"
            )
        return super().__cached_equals__(other)


class ParquetReadOptions(FileFormat):
    """
    Files of Parquet format.
    """


class ArrowReadOptions(FileFormat):
    """
    Files of Arrow IPC format.
    """


class OrcReadOptions(FileFormat):
    """
    Files of ORC format.
    """


class FileOrFiles(Annotable, Comparable):
    """
    Base class representing some files in a LocalFiles.
    """

    file_format = rlz.instance_of(FileFormat)

    def __equals__(self, other: typing.Any) -> bool:
        if type(other) is not type(self):
            raise TypeError(
                f"invalid equality comparison between DataType and {type(other)}"
            )
        return super().__cached_equals__(other)


class UriPath(FileOrFiles):
    """A single file or directory."""

    uri_path = valid_uri


class UriPathGlob(FileOrFiles):
    """A glob."""

    uri_path_glob = valid_uri


class UriFile(FileOrFiles):
    """A single file."""

    uri_file = valid_uri


class UriFolder(FileOrFiles):
    """A single directory."""

    uri_folder = valid_uri


class LocalFilesTable(rel.UnboundTable):
    """
    A table backed by files on a filesystem.

    Translates to a ReadRel of LocalFiles.
    """

    items = rlz.tuple_of(rlz.instance_of(FileOrFiles))
