"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
_sym_db = _symbol_database.Default()
DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x14substrait/type.proto\x12\tsubstrait"\x99$\n\x04Type\x12-\n\x04bool\x18\x01 \x01(\x0b2\x17.substrait.Type.BooleanH\x00R\x04bool\x12$\n\x02i8\x18\x02 \x01(\x0b2\x12.substrait.Type.I8H\x00R\x02i8\x12\'\n\x03i16\x18\x03 \x01(\x0b2\x13.substrait.Type.I16H\x00R\x03i16\x12\'\n\x03i32\x18\x05 \x01(\x0b2\x13.substrait.Type.I32H\x00R\x03i32\x12\'\n\x03i64\x18\x07 \x01(\x0b2\x13.substrait.Type.I64H\x00R\x03i64\x12*\n\x04fp32\x18\n \x01(\x0b2\x14.substrait.Type.FP32H\x00R\x04fp32\x12*\n\x04fp64\x18\x0b \x01(\x0b2\x14.substrait.Type.FP64H\x00R\x04fp64\x120\n\x06string\x18\x0c \x01(\x0b2\x16.substrait.Type.StringH\x00R\x06string\x120\n\x06binary\x18\r \x01(\x0b2\x16.substrait.Type.BinaryH\x00R\x06binary\x129\n\ttimestamp\x18\x0e \x01(\x0b2\x19.substrait.Type.TimestampH\x00R\ttimestamp\x12*\n\x04date\x18\x10 \x01(\x0b2\x14.substrait.Type.DateH\x00R\x04date\x12*\n\x04time\x18\x11 \x01(\x0b2\x14.substrait.Type.TimeH\x00R\x04time\x12C\n\rinterval_year\x18\x13 \x01(\x0b2\x1c.substrait.Type.IntervalYearH\x00R\x0cintervalYear\x12@\n\x0cinterval_day\x18\x14 \x01(\x0b2\x1b.substrait.Type.IntervalDayH\x00R\x0bintervalDay\x12@\n\x0ctimestamp_tz\x18\x1d \x01(\x0b2\x1b.substrait.Type.TimestampTZH\x00R\x0btimestampTz\x12*\n\x04uuid\x18  \x01(\x0b2\x14.substrait.Type.UUIDH\x00R\x04uuid\x12:\n\nfixed_char\x18\x15 \x01(\x0b2\x19.substrait.Type.FixedCharH\x00R\tfixedChar\x123\n\x07varchar\x18\x16 \x01(\x0b2\x17.substrait.Type.VarCharH\x00R\x07varchar\x12@\n\x0cfixed_binary\x18\x17 \x01(\x0b2\x1b.substrait.Type.FixedBinaryH\x00R\x0bfixedBinary\x123\n\x07decimal\x18\x18 \x01(\x0b2\x17.substrait.Type.DecimalH\x00R\x07decimal\x120\n\x06struct\x18\x19 \x01(\x0b2\x16.substrait.Type.StructH\x00R\x06struct\x12*\n\x04list\x18\x1b \x01(\x0b2\x14.substrait.Type.ListH\x00R\x04list\x12\'\n\x03map\x18\x1c \x01(\x0b2\x13.substrait.Type.MapH\x00R\x03map\x12?\n\x1buser_defined_type_reference\x18\x1f \x01(\rH\x00R\x18userDefinedTypeReference\x1a\x82\x01\n\x07Boolean\x128\n\x18type_variation_reference\x18\x01 \x01(\rR\x16typeVariationReference\x12=\n\x0bnullability\x18\x02 \x01(\x0e2\x1b.substrait.Type.NullabilityR\x0bnullability\x1a}\n\x02I8\x128\n\x18type_variation_reference\x18\x01 \x01(\rR\x16typeVariationReference\x12=\n\x0bnullability\x18\x02 \x01(\x0e2\x1b.substrait.Type.NullabilityR\x0bnullability\x1a~\n\x03I16\x128\n\x18type_variation_reference\x18\x01 \x01(\rR\x16typeVariationReference\x12=\n\x0bnullability\x18\x02 \x01(\x0e2\x1b.substrait.Type.NullabilityR\x0bnullability\x1a~\n\x03I32\x128\n\x18type_variation_reference\x18\x01 \x01(\rR\x16typeVariationReference\x12=\n\x0bnullability\x18\x02 \x01(\x0e2\x1b.substrait.Type.NullabilityR\x0bnullability\x1a~\n\x03I64\x128\n\x18type_variation_reference\x18\x01 \x01(\rR\x16typeVariationReference\x12=\n\x0bnullability\x18\x02 \x01(\x0e2\x1b.substrait.Type.NullabilityR\x0bnullability\x1a\x7f\n\x04FP32\x128\n\x18type_variation_reference\x18\x01 \x01(\rR\x16typeVariationReference\x12=\n\x0bnullability\x18\x02 \x01(\x0e2\x1b.substrait.Type.NullabilityR\x0bnullability\x1a\x7f\n\x04FP64\x128\n\x18type_variation_reference\x18\x01 \x01(\rR\x16typeVariationReference\x12=\n\x0bnullability\x18\x02 \x01(\x0e2\x1b.substrait.Type.NullabilityR\x0bnullability\x1a\x81\x01\n\x06String\x128\n\x18type_variation_reference\x18\x01 \x01(\rR\x16typeVariationReference\x12=\n\x0bnullability\x18\x02 \x01(\x0e2\x1b.substrait.Type.NullabilityR\x0bnullability\x1a\x81\x01\n\x06Binary\x128\n\x18type_variation_reference\x18\x01 \x01(\rR\x16typeVariationReference\x12=\n\x0bnullability\x18\x02 \x01(\x0e2\x1b.substrait.Type.NullabilityR\x0bnullability\x1a\x84\x01\n\tTimestamp\x128\n\x18type_variation_reference\x18\x01 \x01(\rR\x16typeVariationReference\x12=\n\x0bnullability\x18\x02 \x01(\x0e2\x1b.substrait.Type.NullabilityR\x0bnullability\x1a\x7f\n\x04Date\x128\n\x18type_variation_reference\x18\x01 \x01(\rR\x16typeVariationReference\x12=\n\x0bnullability\x18\x02 \x01(\x0e2\x1b.substrait.Type.NullabilityR\x0bnullability\x1a\x7f\n\x04Time\x128\n\x18type_variation_reference\x18\x01 \x01(\rR\x16typeVariationReference\x12=\n\x0bnullability\x18\x02 \x01(\x0e2\x1b.substrait.Type.NullabilityR\x0bnullability\x1a\x86\x01\n\x0bTimestampTZ\x128\n\x18type_variation_reference\x18\x01 \x01(\rR\x16typeVariationReference\x12=\n\x0bnullability\x18\x02 \x01(\x0e2\x1b.substrait.Type.NullabilityR\x0bnullability\x1a\x87\x01\n\x0cIntervalYear\x128\n\x18type_variation_reference\x18\x01 \x01(\rR\x16typeVariationReference\x12=\n\x0bnullability\x18\x02 \x01(\x0e2\x1b.substrait.Type.NullabilityR\x0bnullability\x1a\x86\x01\n\x0bIntervalDay\x128\n\x18type_variation_reference\x18\x01 \x01(\rR\x16typeVariationReference\x12=\n\x0bnullability\x18\x02 \x01(\x0e2\x1b.substrait.Type.NullabilityR\x0bnullability\x1a\x7f\n\x04UUID\x128\n\x18type_variation_reference\x18\x01 \x01(\rR\x16typeVariationReference\x12=\n\x0bnullability\x18\x02 \x01(\x0e2\x1b.substrait.Type.NullabilityR\x0bnullability\x1a\x9c\x01\n\tFixedChar\x12\x16\n\x06length\x18\x01 \x01(\x05R\x06length\x128\n\x18type_variation_reference\x18\x02 \x01(\rR\x16typeVariationReference\x12=\n\x0bnullability\x18\x03 \x01(\x0e2\x1b.substrait.Type.NullabilityR\x0bnullability\x1a\x9a\x01\n\x07VarChar\x12\x16\n\x06length\x18\x01 \x01(\x05R\x06length\x128\n\x18type_variation_reference\x18\x02 \x01(\rR\x16typeVariationReference\x12=\n\x0bnullability\x18\x03 \x01(\x0e2\x1b.substrait.Type.NullabilityR\x0bnullability\x1a\x9e\x01\n\x0bFixedBinary\x12\x16\n\x06length\x18\x01 \x01(\x05R\x06length\x128\n\x18type_variation_reference\x18\x02 \x01(\rR\x16typeVariationReference\x12=\n\x0bnullability\x18\x03 \x01(\x0e2\x1b.substrait.Type.NullabilityR\x0bnullability\x1a\xb6\x01\n\x07Decimal\x12\x14\n\x05scale\x18\x01 \x01(\x05R\x05scale\x12\x1c\n\tprecision\x18\x02 \x01(\x05R\tprecision\x128\n\x18type_variation_reference\x18\x03 \x01(\rR\x16typeVariationReference\x12=\n\x0bnullability\x18\x04 \x01(\x0e2\x1b.substrait.Type.NullabilityR\x0bnullability\x1a\xa8\x01\n\x06Struct\x12%\n\x05types\x18\x01 \x03(\x0b2\x0f.substrait.TypeR\x05types\x128\n\x18type_variation_reference\x18\x02 \x01(\rR\x16typeVariationReference\x12=\n\x0bnullability\x18\x03 \x01(\x0e2\x1b.substrait.Type.NullabilityR\x0bnullability\x1a\xa4\x01\n\x04List\x12#\n\x04type\x18\x01 \x01(\x0b2\x0f.substrait.TypeR\x04type\x128\n\x18type_variation_reference\x18\x02 \x01(\rR\x16typeVariationReference\x12=\n\x0bnullability\x18\x03 \x01(\x0e2\x1b.substrait.Type.NullabilityR\x0bnullability\x1a\xc8\x01\n\x03Map\x12!\n\x03key\x18\x01 \x01(\x0b2\x0f.substrait.TypeR\x03key\x12%\n\x05value\x18\x02 \x01(\x0b2\x0f.substrait.TypeR\x05value\x128\n\x18type_variation_reference\x18\x03 \x01(\rR\x16typeVariationReference\x12=\n\x0bnullability\x18\x04 \x01(\x0e2\x1b.substrait.Type.NullabilityR\x0bnullability"^\n\x0bNullability\x12\x1b\n\x17NULLABILITY_UNSPECIFIED\x10\x00\x12\x18\n\x14NULLABILITY_NULLABLE\x10\x01\x12\x18\n\x14NULLABILITY_REQUIRED\x10\x02B\x06\n\x04kind"S\n\x0bNamedStruct\x12\x14\n\x05names\x18\x01 \x03(\tR\x05names\x12.\n\x06struct\x18\x02 \x01(\x0b2\x16.substrait.Type.StructR\x06structB+\n\x12io.substrait.protoP\x01\xaa\x02\x12Substrait.Protobufb\x06proto3')
_TYPE = DESCRIPTOR.message_types_by_name['Type']
_TYPE_BOOLEAN = _TYPE.nested_types_by_name['Boolean']
_TYPE_I8 = _TYPE.nested_types_by_name['I8']
_TYPE_I16 = _TYPE.nested_types_by_name['I16']
_TYPE_I32 = _TYPE.nested_types_by_name['I32']
_TYPE_I64 = _TYPE.nested_types_by_name['I64']
_TYPE_FP32 = _TYPE.nested_types_by_name['FP32']
_TYPE_FP64 = _TYPE.nested_types_by_name['FP64']
_TYPE_STRING = _TYPE.nested_types_by_name['String']
_TYPE_BINARY = _TYPE.nested_types_by_name['Binary']
_TYPE_TIMESTAMP = _TYPE.nested_types_by_name['Timestamp']
_TYPE_DATE = _TYPE.nested_types_by_name['Date']
_TYPE_TIME = _TYPE.nested_types_by_name['Time']
_TYPE_TIMESTAMPTZ = _TYPE.nested_types_by_name['TimestampTZ']
_TYPE_INTERVALYEAR = _TYPE.nested_types_by_name['IntervalYear']
_TYPE_INTERVALDAY = _TYPE.nested_types_by_name['IntervalDay']
_TYPE_UUID = _TYPE.nested_types_by_name['UUID']
_TYPE_FIXEDCHAR = _TYPE.nested_types_by_name['FixedChar']
_TYPE_VARCHAR = _TYPE.nested_types_by_name['VarChar']
_TYPE_FIXEDBINARY = _TYPE.nested_types_by_name['FixedBinary']
_TYPE_DECIMAL = _TYPE.nested_types_by_name['Decimal']
_TYPE_STRUCT = _TYPE.nested_types_by_name['Struct']
_TYPE_LIST = _TYPE.nested_types_by_name['List']
_TYPE_MAP = _TYPE.nested_types_by_name['Map']
_NAMEDSTRUCT = DESCRIPTOR.message_types_by_name['NamedStruct']
_TYPE_NULLABILITY = _TYPE.enum_types_by_name['Nullability']
Type = _reflection.GeneratedProtocolMessageType('Type', (_message.Message,), {'Boolean': _reflection.GeneratedProtocolMessageType('Boolean', (_message.Message,), {'DESCRIPTOR': _TYPE_BOOLEAN, '__module__': 'substrait.type_pb2'}), 'I8': _reflection.GeneratedProtocolMessageType('I8', (_message.Message,), {'DESCRIPTOR': _TYPE_I8, '__module__': 'substrait.type_pb2'}), 'I16': _reflection.GeneratedProtocolMessageType('I16', (_message.Message,), {'DESCRIPTOR': _TYPE_I16, '__module__': 'substrait.type_pb2'}), 'I32': _reflection.GeneratedProtocolMessageType('I32', (_message.Message,), {'DESCRIPTOR': _TYPE_I32, '__module__': 'substrait.type_pb2'}), 'I64': _reflection.GeneratedProtocolMessageType('I64', (_message.Message,), {'DESCRIPTOR': _TYPE_I64, '__module__': 'substrait.type_pb2'}), 'FP32': _reflection.GeneratedProtocolMessageType('FP32', (_message.Message,), {'DESCRIPTOR': _TYPE_FP32, '__module__': 'substrait.type_pb2'}), 'FP64': _reflection.GeneratedProtocolMessageType('FP64', (_message.Message,), {'DESCRIPTOR': _TYPE_FP64, '__module__': 'substrait.type_pb2'}), 'String': _reflection.GeneratedProtocolMessageType('String', (_message.Message,), {'DESCRIPTOR': _TYPE_STRING, '__module__': 'substrait.type_pb2'}), 'Binary': _reflection.GeneratedProtocolMessageType('Binary', (_message.Message,), {'DESCRIPTOR': _TYPE_BINARY, '__module__': 'substrait.type_pb2'}), 'Timestamp': _reflection.GeneratedProtocolMessageType('Timestamp', (_message.Message,), {'DESCRIPTOR': _TYPE_TIMESTAMP, '__module__': 'substrait.type_pb2'}), 'Date': _reflection.GeneratedProtocolMessageType('Date', (_message.Message,), {'DESCRIPTOR': _TYPE_DATE, '__module__': 'substrait.type_pb2'}), 'Time': _reflection.GeneratedProtocolMessageType('Time', (_message.Message,), {'DESCRIPTOR': _TYPE_TIME, '__module__': 'substrait.type_pb2'}), 'TimestampTZ': _reflection.GeneratedProtocolMessageType('TimestampTZ', (_message.Message,), {'DESCRIPTOR': _TYPE_TIMESTAMPTZ, '__module__': 'substrait.type_pb2'}), 'IntervalYear': _reflection.GeneratedProtocolMessageType('IntervalYear', (_message.Message,), {'DESCRIPTOR': _TYPE_INTERVALYEAR, '__module__': 'substrait.type_pb2'}), 'IntervalDay': _reflection.GeneratedProtocolMessageType('IntervalDay', (_message.Message,), {'DESCRIPTOR': _TYPE_INTERVALDAY, '__module__': 'substrait.type_pb2'}), 'UUID': _reflection.GeneratedProtocolMessageType('UUID', (_message.Message,), {'DESCRIPTOR': _TYPE_UUID, '__module__': 'substrait.type_pb2'}), 'FixedChar': _reflection.GeneratedProtocolMessageType('FixedChar', (_message.Message,), {'DESCRIPTOR': _TYPE_FIXEDCHAR, '__module__': 'substrait.type_pb2'}), 'VarChar': _reflection.GeneratedProtocolMessageType('VarChar', (_message.Message,), {'DESCRIPTOR': _TYPE_VARCHAR, '__module__': 'substrait.type_pb2'}), 'FixedBinary': _reflection.GeneratedProtocolMessageType('FixedBinary', (_message.Message,), {'DESCRIPTOR': _TYPE_FIXEDBINARY, '__module__': 'substrait.type_pb2'}), 'Decimal': _reflection.GeneratedProtocolMessageType('Decimal', (_message.Message,), {'DESCRIPTOR': _TYPE_DECIMAL, '__module__': 'substrait.type_pb2'}), 'Struct': _reflection.GeneratedProtocolMessageType('Struct', (_message.Message,), {'DESCRIPTOR': _TYPE_STRUCT, '__module__': 'substrait.type_pb2'}), 'List': _reflection.GeneratedProtocolMessageType('List', (_message.Message,), {'DESCRIPTOR': _TYPE_LIST, '__module__': 'substrait.type_pb2'}), 'Map': _reflection.GeneratedProtocolMessageType('Map', (_message.Message,), {'DESCRIPTOR': _TYPE_MAP, '__module__': 'substrait.type_pb2'}), 'DESCRIPTOR': _TYPE, '__module__': 'substrait.type_pb2'})
_sym_db.RegisterMessage(Type)
_sym_db.RegisterMessage(Type.Boolean)
_sym_db.RegisterMessage(Type.I8)
_sym_db.RegisterMessage(Type.I16)
_sym_db.RegisterMessage(Type.I32)
_sym_db.RegisterMessage(Type.I64)
_sym_db.RegisterMessage(Type.FP32)
_sym_db.RegisterMessage(Type.FP64)
_sym_db.RegisterMessage(Type.String)
_sym_db.RegisterMessage(Type.Binary)
_sym_db.RegisterMessage(Type.Timestamp)
_sym_db.RegisterMessage(Type.Date)
_sym_db.RegisterMessage(Type.Time)
_sym_db.RegisterMessage(Type.TimestampTZ)
_sym_db.RegisterMessage(Type.IntervalYear)
_sym_db.RegisterMessage(Type.IntervalDay)
_sym_db.RegisterMessage(Type.UUID)
_sym_db.RegisterMessage(Type.FixedChar)
_sym_db.RegisterMessage(Type.VarChar)
_sym_db.RegisterMessage(Type.FixedBinary)
_sym_db.RegisterMessage(Type.Decimal)
_sym_db.RegisterMessage(Type.Struct)
_sym_db.RegisterMessage(Type.List)
_sym_db.RegisterMessage(Type.Map)
NamedStruct = _reflection.GeneratedProtocolMessageType('NamedStruct', (_message.Message,), {'DESCRIPTOR': _NAMEDSTRUCT, '__module__': 'substrait.type_pb2'})
_sym_db.RegisterMessage(NamedStruct)
if _descriptor._USE_C_DESCRIPTORS == False:
    DESCRIPTOR._options = None
    DESCRIPTOR._serialized_options = b'\n\x12io.substrait.protoP\x01\xaa\x02\x12Substrait.Protobuf'
    _TYPE._serialized_start = 36
    _TYPE._serialized_end = 4669
    _TYPE_BOOLEAN._serialized_start = 1265
    _TYPE_BOOLEAN._serialized_end = 1395
    _TYPE_I8._serialized_start = 1397
    _TYPE_I8._serialized_end = 1522
    _TYPE_I16._serialized_start = 1524
    _TYPE_I16._serialized_end = 1650
    _TYPE_I32._serialized_start = 1652
    _TYPE_I32._serialized_end = 1778
    _TYPE_I64._serialized_start = 1780
    _TYPE_I64._serialized_end = 1906
    _TYPE_FP32._serialized_start = 1908
    _TYPE_FP32._serialized_end = 2035
    _TYPE_FP64._serialized_start = 2037
    _TYPE_FP64._serialized_end = 2164
    _TYPE_STRING._serialized_start = 2167
    _TYPE_STRING._serialized_end = 2296
    _TYPE_BINARY._serialized_start = 2299
    _TYPE_BINARY._serialized_end = 2428
    _TYPE_TIMESTAMP._serialized_start = 2431
    _TYPE_TIMESTAMP._serialized_end = 2563
    _TYPE_DATE._serialized_start = 2565
    _TYPE_DATE._serialized_end = 2692
    _TYPE_TIME._serialized_start = 2694
    _TYPE_TIME._serialized_end = 2821
    _TYPE_TIMESTAMPTZ._serialized_start = 2824
    _TYPE_TIMESTAMPTZ._serialized_end = 2958
    _TYPE_INTERVALYEAR._serialized_start = 2961
    _TYPE_INTERVALYEAR._serialized_end = 3096
    _TYPE_INTERVALDAY._serialized_start = 3099
    _TYPE_INTERVALDAY._serialized_end = 3233
    _TYPE_UUID._serialized_start = 3235
    _TYPE_UUID._serialized_end = 3362
    _TYPE_FIXEDCHAR._serialized_start = 3365
    _TYPE_FIXEDCHAR._serialized_end = 3521
    _TYPE_VARCHAR._serialized_start = 3524
    _TYPE_VARCHAR._serialized_end = 3678
    _TYPE_FIXEDBINARY._serialized_start = 3681
    _TYPE_FIXEDBINARY._serialized_end = 3839
    _TYPE_DECIMAL._serialized_start = 3842
    _TYPE_DECIMAL._serialized_end = 4024
    _TYPE_STRUCT._serialized_start = 4027
    _TYPE_STRUCT._serialized_end = 4195
    _TYPE_LIST._serialized_start = 4198
    _TYPE_LIST._serialized_end = 4362
    _TYPE_MAP._serialized_start = 4365
    _TYPE_MAP._serialized_end = 4565
    _TYPE_NULLABILITY._serialized_start = 4567
    _TYPE_NULLABILITY._serialized_end = 4661
    _NAMEDSTRUCT._serialized_start = 4671
    _NAMEDSTRUCT._serialized_end = 4754