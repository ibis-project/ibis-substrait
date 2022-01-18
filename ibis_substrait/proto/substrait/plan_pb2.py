"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
_sym_db = _symbol_database.Default()
from ..substrait import relations_pb2 as substrait_dot_relations__pb2
from ..substrait.extensions import extensions_pb2 as substrait_dot_extensions_dot_extensions__pb2
DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x14substrait/plan.proto\x12\tsubstrait\x1a\x19substrait/relations.proto\x1a%substrait/extensions/extensions.proto"c\n\x07PlanRel\x12"\n\x03rel\x18\x01 \x01(\x0b2\x0e.substrait.RelH\x00R\x03rel\x12(\n\x04root\x18\x02 \x01(\x0b2\x12.substrait.RelRootH\x00R\x04rootB\n\n\x08rel_type"\xe3\x02\n\x04Plan\x12O\n\x0eextension_uris\x18\x01 \x03(\x0b2(.substrait.extensions.SimpleExtensionURIR\rextensionUris\x12P\n\nextensions\x18\x02 \x03(\x0b20.substrait.extensions.SimpleExtensionDeclarationR\nextensions\x120\n\trelations\x18\x03 \x03(\x0b2\x12.substrait.PlanRelR\trelations\x12X\n\x13advanced_extensions\x18\x04 \x01(\x0b2\'.substrait.extensions.AdvancedExtensionR\x12advancedExtensions\x12,\n\x12expected_type_urls\x18\x05 \x03(\tR\x10expectedTypeUrlsB+\n\x12io.substrait.protoP\x01\xaa\x02\x12Substrait.Protobufb\x06proto3')
_PLANREL = DESCRIPTOR.message_types_by_name['PlanRel']
_PLAN = DESCRIPTOR.message_types_by_name['Plan']
PlanRel = _reflection.GeneratedProtocolMessageType('PlanRel', (_message.Message,), {'DESCRIPTOR': _PLANREL, '__module__': 'substrait.plan_pb2'})
_sym_db.RegisterMessage(PlanRel)
Plan = _reflection.GeneratedProtocolMessageType('Plan', (_message.Message,), {'DESCRIPTOR': _PLAN, '__module__': 'substrait.plan_pb2'})
_sym_db.RegisterMessage(Plan)
if _descriptor._USE_C_DESCRIPTORS == False:
    DESCRIPTOR._options = None
    DESCRIPTOR._serialized_options = b'\n\x12io.substrait.protoP\x01\xaa\x02\x12Substrait.Protobuf'
    _PLANREL._serialized_start = 101
    _PLANREL._serialized_end = 200
    _PLAN._serialized_start = 203
    _PLAN._serialized_end = 558