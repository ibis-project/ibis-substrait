"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
_sym_db = _symbol_database.Default()
from .substrait.ibis import algebra_pb2 as substrait_dot_ibis_dot_algebra__pb2
DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x14extension_rels.proto\x12\x13arrow.substrait_ext\x1a\x1csubstrait/ibis/algebra.proto"\xd4\x01\n\x0bAsOfJoinRel\x12@\n\x04keys\x18\x01 \x03(\x0b2,.arrow.substrait_ext.AsOfJoinRel.AsOfJoinKeyR\x04keys\x12\x1c\n\ttolerance\x18\x02 \x01(\x03R\ttolerance\x1ae\n\x0bAsOfJoinKey\x12*\n\x02on\x18\x01 \x01(\x0b2\x1a.substrait.ibis.ExpressionR\x02on\x12*\n\x02by\x18\x02 \x03(\x0b2\x1a.substrait.ibis.ExpressionR\x02byBK\n\x12io.arrow.substraitP\x01Z!github.com/apache/arrow/substrait\xaa\x02\x0fArrow.Substraitb\x06proto3')
_ASOFJOINREL = DESCRIPTOR.message_types_by_name['AsOfJoinRel']
_ASOFJOINREL_ASOFJOINKEY = _ASOFJOINREL.nested_types_by_name['AsOfJoinKey']
AsOfJoinRel = _reflection.GeneratedProtocolMessageType('AsOfJoinRel', (_message.Message,), {'AsOfJoinKey': _reflection.GeneratedProtocolMessageType('AsOfJoinKey', (_message.Message,), {'DESCRIPTOR': _ASOFJOINREL_ASOFJOINKEY, '__module__': 'extension_rels_pb2'}), 'DESCRIPTOR': _ASOFJOINREL, '__module__': 'extension_rels_pb2'})
_sym_db.RegisterMessage(AsOfJoinRel)
_sym_db.RegisterMessage(AsOfJoinRel.AsOfJoinKey)
if _descriptor._USE_C_DESCRIPTORS == False:
    DESCRIPTOR._options = None
    DESCRIPTOR._serialized_options = b'\n\x12io.arrow.substraitP\x01Z!github.com/apache/arrow/substrait\xaa\x02\x0fArrow.Substrait'
    _ASOFJOINREL._serialized_start = 76
    _ASOFJOINREL._serialized_end = 288
    _ASOFJOINREL_ASOFJOINKEY._serialized_start = 187
    _ASOFJOINREL_ASOFJOINKEY._serialized_end = 288