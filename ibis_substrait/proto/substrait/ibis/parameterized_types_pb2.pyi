"""
@generated by mypy-protobuf.  Do not edit manually!
isort:skip_file
SPDX-License-Identifier: Apache-2.0"""
import builtins
import collections.abc
import google.protobuf.descriptor
import google.protobuf.internal.containers
import google.protobuf.message
from ... import substrait
import sys
if sys.version_info >= (3, 8):
    import typing as typing_extensions
else:
    import typing_extensions
DESCRIPTOR: google.protobuf.descriptor.FileDescriptor

class ParameterizedType(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    class TypeParameter(google.protobuf.message.Message):
        DESCRIPTOR: google.protobuf.descriptor.Descriptor
        NAME_FIELD_NUMBER: builtins.int
        BOUNDS_FIELD_NUMBER: builtins.int
        name: builtins.str

        @property
        def bounds(self) -> google.protobuf.internal.containers.RepeatedCompositeFieldContainer[global___ParameterizedType]:
            ...

        def __init__(self, *, name: builtins.str=..., bounds: collections.abc.Iterable[global___ParameterizedType] | None=...) -> None:
            ...

        def ClearField(self, field_name: typing_extensions.Literal['bounds', b'bounds', 'name', b'name']) -> None:
            ...

    class IntegerParameter(google.protobuf.message.Message):
        DESCRIPTOR: google.protobuf.descriptor.Descriptor
        NAME_FIELD_NUMBER: builtins.int
        RANGE_START_INCLUSIVE_FIELD_NUMBER: builtins.int
        RANGE_END_EXCLUSIVE_FIELD_NUMBER: builtins.int
        name: builtins.str

        @property
        def range_start_inclusive(self) -> global___ParameterizedType.NullableInteger:
            ...

        @property
        def range_end_exclusive(self) -> global___ParameterizedType.NullableInteger:
            ...

        def __init__(self, *, name: builtins.str=..., range_start_inclusive: global___ParameterizedType.NullableInteger | None=..., range_end_exclusive: global___ParameterizedType.NullableInteger | None=...) -> None:
            ...

        def HasField(self, field_name: typing_extensions.Literal['range_end_exclusive', b'range_end_exclusive', 'range_start_inclusive', b'range_start_inclusive']) -> builtins.bool:
            ...

        def ClearField(self, field_name: typing_extensions.Literal['name', b'name', 'range_end_exclusive', b'range_end_exclusive', 'range_start_inclusive', b'range_start_inclusive']) -> None:
            ...

    class NullableInteger(google.protobuf.message.Message):
        DESCRIPTOR: google.protobuf.descriptor.Descriptor
        VALUE_FIELD_NUMBER: builtins.int
        value: builtins.int

        def __init__(self, *, value: builtins.int=...) -> None:
            ...

        def ClearField(self, field_name: typing_extensions.Literal['value', b'value']) -> None:
            ...

    class ParameterizedFixedChar(google.protobuf.message.Message):
        DESCRIPTOR: google.protobuf.descriptor.Descriptor
        LENGTH_FIELD_NUMBER: builtins.int
        VARIATION_POINTER_FIELD_NUMBER: builtins.int
        NULLABILITY_FIELD_NUMBER: builtins.int

        @property
        def length(self) -> global___ParameterizedType.IntegerOption:
            ...
        variation_pointer: builtins.int
        nullability: substrait.ibis.type_pb2.Type.Nullability.ValueType

        def __init__(self, *, length: global___ParameterizedType.IntegerOption | None=..., variation_pointer: builtins.int=..., nullability: substrait.ibis.type_pb2.Type.Nullability.ValueType=...) -> None:
            ...

        def HasField(self, field_name: typing_extensions.Literal['length', b'length']) -> builtins.bool:
            ...

        def ClearField(self, field_name: typing_extensions.Literal['length', b'length', 'nullability', b'nullability', 'variation_pointer', b'variation_pointer']) -> None:
            ...

    class ParameterizedVarChar(google.protobuf.message.Message):
        DESCRIPTOR: google.protobuf.descriptor.Descriptor
        LENGTH_FIELD_NUMBER: builtins.int
        VARIATION_POINTER_FIELD_NUMBER: builtins.int
        NULLABILITY_FIELD_NUMBER: builtins.int

        @property
        def length(self) -> global___ParameterizedType.IntegerOption:
            ...
        variation_pointer: builtins.int
        nullability: substrait.ibis.type_pb2.Type.Nullability.ValueType

        def __init__(self, *, length: global___ParameterizedType.IntegerOption | None=..., variation_pointer: builtins.int=..., nullability: substrait.ibis.type_pb2.Type.Nullability.ValueType=...) -> None:
            ...

        def HasField(self, field_name: typing_extensions.Literal['length', b'length']) -> builtins.bool:
            ...

        def ClearField(self, field_name: typing_extensions.Literal['length', b'length', 'nullability', b'nullability', 'variation_pointer', b'variation_pointer']) -> None:
            ...

    class ParameterizedFixedBinary(google.protobuf.message.Message):
        DESCRIPTOR: google.protobuf.descriptor.Descriptor
        LENGTH_FIELD_NUMBER: builtins.int
        VARIATION_POINTER_FIELD_NUMBER: builtins.int
        NULLABILITY_FIELD_NUMBER: builtins.int

        @property
        def length(self) -> global___ParameterizedType.IntegerOption:
            ...
        variation_pointer: builtins.int
        nullability: substrait.ibis.type_pb2.Type.Nullability.ValueType

        def __init__(self, *, length: global___ParameterizedType.IntegerOption | None=..., variation_pointer: builtins.int=..., nullability: substrait.ibis.type_pb2.Type.Nullability.ValueType=...) -> None:
            ...

        def HasField(self, field_name: typing_extensions.Literal['length', b'length']) -> builtins.bool:
            ...

        def ClearField(self, field_name: typing_extensions.Literal['length', b'length', 'nullability', b'nullability', 'variation_pointer', b'variation_pointer']) -> None:
            ...

    class ParameterizedDecimal(google.protobuf.message.Message):
        DESCRIPTOR: google.protobuf.descriptor.Descriptor
        SCALE_FIELD_NUMBER: builtins.int
        PRECISION_FIELD_NUMBER: builtins.int
        VARIATION_POINTER_FIELD_NUMBER: builtins.int
        NULLABILITY_FIELD_NUMBER: builtins.int

        @property
        def scale(self) -> global___ParameterizedType.IntegerOption:
            ...

        @property
        def precision(self) -> global___ParameterizedType.IntegerOption:
            ...
        variation_pointer: builtins.int
        nullability: substrait.ibis.type_pb2.Type.Nullability.ValueType

        def __init__(self, *, scale: global___ParameterizedType.IntegerOption | None=..., precision: global___ParameterizedType.IntegerOption | None=..., variation_pointer: builtins.int=..., nullability: substrait.ibis.type_pb2.Type.Nullability.ValueType=...) -> None:
            ...

        def HasField(self, field_name: typing_extensions.Literal['precision', b'precision', 'scale', b'scale']) -> builtins.bool:
            ...

        def ClearField(self, field_name: typing_extensions.Literal['nullability', b'nullability', 'precision', b'precision', 'scale', b'scale', 'variation_pointer', b'variation_pointer']) -> None:
            ...

    class ParameterizedStruct(google.protobuf.message.Message):
        DESCRIPTOR: google.protobuf.descriptor.Descriptor
        TYPES_FIELD_NUMBER: builtins.int
        VARIATION_POINTER_FIELD_NUMBER: builtins.int
        NULLABILITY_FIELD_NUMBER: builtins.int

        @property
        def types(self) -> google.protobuf.internal.containers.RepeatedCompositeFieldContainer[global___ParameterizedType]:
            ...
        variation_pointer: builtins.int
        nullability: substrait.ibis.type_pb2.Type.Nullability.ValueType

        def __init__(self, *, types: collections.abc.Iterable[global___ParameterizedType] | None=..., variation_pointer: builtins.int=..., nullability: substrait.ibis.type_pb2.Type.Nullability.ValueType=...) -> None:
            ...

        def ClearField(self, field_name: typing_extensions.Literal['nullability', b'nullability', 'types', b'types', 'variation_pointer', b'variation_pointer']) -> None:
            ...

    class ParameterizedNamedStruct(google.protobuf.message.Message):
        DESCRIPTOR: google.protobuf.descriptor.Descriptor
        NAMES_FIELD_NUMBER: builtins.int
        STRUCT_FIELD_NUMBER: builtins.int

        @property
        def names(self) -> google.protobuf.internal.containers.RepeatedScalarFieldContainer[builtins.str]:
            """list of names in dfs order"""

        @property
        def struct(self) -> global___ParameterizedType.ParameterizedStruct:
            ...

        def __init__(self, *, names: collections.abc.Iterable[builtins.str] | None=..., struct: global___ParameterizedType.ParameterizedStruct | None=...) -> None:
            ...

        def HasField(self, field_name: typing_extensions.Literal['struct', b'struct']) -> builtins.bool:
            ...

        def ClearField(self, field_name: typing_extensions.Literal['names', b'names', 'struct', b'struct']) -> None:
            ...

    class ParameterizedList(google.protobuf.message.Message):
        DESCRIPTOR: google.protobuf.descriptor.Descriptor
        TYPE_FIELD_NUMBER: builtins.int
        VARIATION_POINTER_FIELD_NUMBER: builtins.int
        NULLABILITY_FIELD_NUMBER: builtins.int

        @property
        def type(self) -> global___ParameterizedType:
            ...
        variation_pointer: builtins.int
        nullability: substrait.ibis.type_pb2.Type.Nullability.ValueType

        def __init__(self, *, type: global___ParameterizedType | None=..., variation_pointer: builtins.int=..., nullability: substrait.ibis.type_pb2.Type.Nullability.ValueType=...) -> None:
            ...

        def HasField(self, field_name: typing_extensions.Literal['type', b'type']) -> builtins.bool:
            ...

        def ClearField(self, field_name: typing_extensions.Literal['nullability', b'nullability', 'type', b'type', 'variation_pointer', b'variation_pointer']) -> None:
            ...

    class ParameterizedMap(google.protobuf.message.Message):
        DESCRIPTOR: google.protobuf.descriptor.Descriptor
        KEY_FIELD_NUMBER: builtins.int
        VALUE_FIELD_NUMBER: builtins.int
        VARIATION_POINTER_FIELD_NUMBER: builtins.int
        NULLABILITY_FIELD_NUMBER: builtins.int

        @property
        def key(self) -> global___ParameterizedType:
            ...

        @property
        def value(self) -> global___ParameterizedType:
            ...
        variation_pointer: builtins.int
        nullability: substrait.ibis.type_pb2.Type.Nullability.ValueType

        def __init__(self, *, key: global___ParameterizedType | None=..., value: global___ParameterizedType | None=..., variation_pointer: builtins.int=..., nullability: substrait.ibis.type_pb2.Type.Nullability.ValueType=...) -> None:
            ...

        def HasField(self, field_name: typing_extensions.Literal['key', b'key', 'value', b'value']) -> builtins.bool:
            ...

        def ClearField(self, field_name: typing_extensions.Literal['key', b'key', 'nullability', b'nullability', 'value', b'value', 'variation_pointer', b'variation_pointer']) -> None:
            ...

    class ParameterizedUserDefined(google.protobuf.message.Message):
        DESCRIPTOR: google.protobuf.descriptor.Descriptor
        TYPE_POINTER_FIELD_NUMBER: builtins.int
        VARIATION_POINTER_FIELD_NUMBER: builtins.int
        NULLABILITY_FIELD_NUMBER: builtins.int
        type_pointer: builtins.int
        variation_pointer: builtins.int
        nullability: substrait.ibis.type_pb2.Type.Nullability.ValueType

        def __init__(self, *, type_pointer: builtins.int=..., variation_pointer: builtins.int=..., nullability: substrait.ibis.type_pb2.Type.Nullability.ValueType=...) -> None:
            ...

        def ClearField(self, field_name: typing_extensions.Literal['nullability', b'nullability', 'type_pointer', b'type_pointer', 'variation_pointer', b'variation_pointer']) -> None:
            ...

    class IntegerOption(google.protobuf.message.Message):
        DESCRIPTOR: google.protobuf.descriptor.Descriptor
        LITERAL_FIELD_NUMBER: builtins.int
        PARAMETER_FIELD_NUMBER: builtins.int
        literal: builtins.int

        @property
        def parameter(self) -> global___ParameterizedType.IntegerParameter:
            ...

        def __init__(self, *, literal: builtins.int=..., parameter: global___ParameterizedType.IntegerParameter | None=...) -> None:
            ...

        def HasField(self, field_name: typing_extensions.Literal['integer_type', b'integer_type', 'literal', b'literal', 'parameter', b'parameter']) -> builtins.bool:
            ...

        def ClearField(self, field_name: typing_extensions.Literal['integer_type', b'integer_type', 'literal', b'literal', 'parameter', b'parameter']) -> None:
            ...

        def WhichOneof(self, oneof_group: typing_extensions.Literal['integer_type', b'integer_type']) -> typing_extensions.Literal['literal', 'parameter'] | None:
            ...
    BOOL_FIELD_NUMBER: builtins.int
    I8_FIELD_NUMBER: builtins.int
    I16_FIELD_NUMBER: builtins.int
    I32_FIELD_NUMBER: builtins.int
    I64_FIELD_NUMBER: builtins.int
    FP32_FIELD_NUMBER: builtins.int
    FP64_FIELD_NUMBER: builtins.int
    STRING_FIELD_NUMBER: builtins.int
    BINARY_FIELD_NUMBER: builtins.int
    TIMESTAMP_FIELD_NUMBER: builtins.int
    DATE_FIELD_NUMBER: builtins.int
    TIME_FIELD_NUMBER: builtins.int
    INTERVAL_YEAR_FIELD_NUMBER: builtins.int
    INTERVAL_DAY_FIELD_NUMBER: builtins.int
    TIMESTAMP_TZ_FIELD_NUMBER: builtins.int
    UUID_FIELD_NUMBER: builtins.int
    FIXED_CHAR_FIELD_NUMBER: builtins.int
    VARCHAR_FIELD_NUMBER: builtins.int
    FIXED_BINARY_FIELD_NUMBER: builtins.int
    DECIMAL_FIELD_NUMBER: builtins.int
    STRUCT_FIELD_NUMBER: builtins.int
    LIST_FIELD_NUMBER: builtins.int
    MAP_FIELD_NUMBER: builtins.int
    USER_DEFINED_FIELD_NUMBER: builtins.int
    USER_DEFINED_POINTER_FIELD_NUMBER: builtins.int
    TYPE_PARAMETER_FIELD_NUMBER: builtins.int

    @property
    def bool(self) -> substrait.ibis.type_pb2.Type.Boolean:
        ...

    @property
    def i8(self) -> substrait.ibis.type_pb2.Type.I8:
        ...

    @property
    def i16(self) -> substrait.ibis.type_pb2.Type.I16:
        ...

    @property
    def i32(self) -> substrait.ibis.type_pb2.Type.I32:
        ...

    @property
    def i64(self) -> substrait.ibis.type_pb2.Type.I64:
        ...

    @property
    def fp32(self) -> substrait.ibis.type_pb2.Type.FP32:
        ...

    @property
    def fp64(self) -> substrait.ibis.type_pb2.Type.FP64:
        ...

    @property
    def string(self) -> substrait.ibis.type_pb2.Type.String:
        ...

    @property
    def binary(self) -> substrait.ibis.type_pb2.Type.Binary:
        ...

    @property
    def timestamp(self) -> substrait.ibis.type_pb2.Type.Timestamp:
        ...

    @property
    def date(self) -> substrait.ibis.type_pb2.Type.Date:
        ...

    @property
    def time(self) -> substrait.ibis.type_pb2.Type.Time:
        ...

    @property
    def interval_year(self) -> substrait.ibis.type_pb2.Type.IntervalYear:
        ...

    @property
    def interval_day(self) -> substrait.ibis.type_pb2.Type.IntervalDay:
        ...

    @property
    def timestamp_tz(self) -> substrait.ibis.type_pb2.Type.TimestampTZ:
        ...

    @property
    def uuid(self) -> substrait.ibis.type_pb2.Type.UUID:
        ...

    @property
    def fixed_char(self) -> global___ParameterizedType.ParameterizedFixedChar:
        ...

    @property
    def varchar(self) -> global___ParameterizedType.ParameterizedVarChar:
        ...

    @property
    def fixed_binary(self) -> global___ParameterizedType.ParameterizedFixedBinary:
        ...

    @property
    def decimal(self) -> global___ParameterizedType.ParameterizedDecimal:
        ...

    @property
    def struct(self) -> global___ParameterizedType.ParameterizedStruct:
        ...

    @property
    def list(self) -> global___ParameterizedType.ParameterizedList:
        ...

    @property
    def map(self) -> global___ParameterizedType.ParameterizedMap:
        ...

    @property
    def user_defined(self) -> global___ParameterizedType.ParameterizedUserDefined:
        ...
    user_defined_pointer: builtins.int
    'Deprecated in favor of user_defined, which allows nullability and\n    variations to be specified. If user_defined_pointer is encountered,\n    treat it as being non-nullable and having the default variation.\n    '

    @property
    def type_parameter(self) -> global___ParameterizedType.TypeParameter:
        ...

    def __init__(self, *, bool: substrait.ibis.type_pb2.Type.Boolean | None=..., i8: substrait.ibis.type_pb2.Type.I8 | None=..., i16: substrait.ibis.type_pb2.Type.I16 | None=..., i32: substrait.ibis.type_pb2.Type.I32 | None=..., i64: substrait.ibis.type_pb2.Type.I64 | None=..., fp32: substrait.ibis.type_pb2.Type.FP32 | None=..., fp64: substrait.ibis.type_pb2.Type.FP64 | None=..., string: substrait.ibis.type_pb2.Type.String | None=..., binary: substrait.ibis.type_pb2.Type.Binary | None=..., timestamp: substrait.ibis.type_pb2.Type.Timestamp | None=..., date: substrait.ibis.type_pb2.Type.Date | None=..., time: substrait.ibis.type_pb2.Type.Time | None=..., interval_year: substrait.ibis.type_pb2.Type.IntervalYear | None=..., interval_day: substrait.ibis.type_pb2.Type.IntervalDay | None=..., timestamp_tz: substrait.ibis.type_pb2.Type.TimestampTZ | None=..., uuid: substrait.ibis.type_pb2.Type.UUID | None=..., fixed_char: global___ParameterizedType.ParameterizedFixedChar | None=..., varchar: global___ParameterizedType.ParameterizedVarChar | None=..., fixed_binary: global___ParameterizedType.ParameterizedFixedBinary | None=..., decimal: global___ParameterizedType.ParameterizedDecimal | None=..., struct: global___ParameterizedType.ParameterizedStruct | None=..., list: global___ParameterizedType.ParameterizedList | None=..., map: global___ParameterizedType.ParameterizedMap | None=..., user_defined: global___ParameterizedType.ParameterizedUserDefined | None=..., user_defined_pointer: builtins.int=..., type_parameter: global___ParameterizedType.TypeParameter | None=...) -> None:
        ...

    def HasField(self, field_name: typing_extensions.Literal['binary', b'binary', 'bool', b'bool', 'date', b'date', 'decimal', b'decimal', 'fixed_binary', b'fixed_binary', 'fixed_char', b'fixed_char', 'fp32', b'fp32', 'fp64', b'fp64', 'i16', b'i16', 'i32', b'i32', 'i64', b'i64', 'i8', b'i8', 'interval_day', b'interval_day', 'interval_year', b'interval_year', 'kind', b'kind', 'list', b'list', 'map', b'map', 'string', b'string', 'struct', b'struct', 'time', b'time', 'timestamp', b'timestamp', 'timestamp_tz', b'timestamp_tz', 'type_parameter', b'type_parameter', 'user_defined', b'user_defined', 'user_defined_pointer', b'user_defined_pointer', 'uuid', b'uuid', 'varchar', b'varchar']) -> builtins.bool:
        ...

    def ClearField(self, field_name: typing_extensions.Literal['binary', b'binary', 'bool', b'bool', 'date', b'date', 'decimal', b'decimal', 'fixed_binary', b'fixed_binary', 'fixed_char', b'fixed_char', 'fp32', b'fp32', 'fp64', b'fp64', 'i16', b'i16', 'i32', b'i32', 'i64', b'i64', 'i8', b'i8', 'interval_day', b'interval_day', 'interval_year', b'interval_year', 'kind', b'kind', 'list', b'list', 'map', b'map', 'string', b'string', 'struct', b'struct', 'time', b'time', 'timestamp', b'timestamp', 'timestamp_tz', b'timestamp_tz', 'type_parameter', b'type_parameter', 'user_defined', b'user_defined', 'user_defined_pointer', b'user_defined_pointer', 'uuid', b'uuid', 'varchar', b'varchar']) -> None:
        ...

    def WhichOneof(self, oneof_group: typing_extensions.Literal['kind', b'kind']) -> typing_extensions.Literal['bool', 'i8', 'i16', 'i32', 'i64', 'fp32', 'fp64', 'string', 'binary', 'timestamp', 'date', 'time', 'interval_year', 'interval_day', 'timestamp_tz', 'uuid', 'fixed_char', 'varchar', 'fixed_binary', 'decimal', 'struct', 'list', 'map', 'user_defined', 'user_defined_pointer', 'type_parameter'] | None:
        ...
global___ParameterizedType = ParameterizedType