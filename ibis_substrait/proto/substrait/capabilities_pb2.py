"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
_sym_db = _symbol_database.Default()
DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x1csubstrait/capabilities.proto\x12\tsubstrait"\xec\x02\n\x0cCapabilities\x12-\n\x12substrait_versions\x18\x01 \x03(\tR\x11substraitVersions\x12?\n\x1cadvanced_extension_type_urls\x18\x02 \x03(\tR\x19advancedExtensionTypeUrls\x12T\n\x11simple_extensions\x18\x03 \x03(\x0b2\'.substrait.Capabilities.SimpleExtensionR\x10simpleExtensions\x1a\x95\x01\n\x0fSimpleExtension\x12\x10\n\x03uri\x18\x01 \x01(\tR\x03uri\x12#\n\rfunction_keys\x18\x02 \x03(\tR\x0cfunctionKeys\x12\x1b\n\ttype_keys\x18\x03 \x03(\tR\x08typeKeys\x12.\n\x13type_variation_keys\x18\x04 \x03(\tR\x11typeVariationKeysB+\n\x12io.substrait.protoP\x01\xaa\x02\x12Substrait.Protobufb\x06proto3')
_CAPABILITIES = DESCRIPTOR.message_types_by_name['Capabilities']
_CAPABILITIES_SIMPLEEXTENSION = _CAPABILITIES.nested_types_by_name['SimpleExtension']
Capabilities = _reflection.GeneratedProtocolMessageType('Capabilities', (_message.Message,), {'SimpleExtension': _reflection.GeneratedProtocolMessageType('SimpleExtension', (_message.Message,), {'DESCRIPTOR': _CAPABILITIES_SIMPLEEXTENSION, '__module__': 'substrait.capabilities_pb2'}), 'DESCRIPTOR': _CAPABILITIES, '__module__': 'substrait.capabilities_pb2'})
_sym_db.RegisterMessage(Capabilities)
_sym_db.RegisterMessage(Capabilities.SimpleExtension)
if _descriptor._USE_C_DESCRIPTORS == False:
    DESCRIPTOR._options = None
    DESCRIPTOR._serialized_options = b'\n\x12io.substrait.protoP\x01\xaa\x02\x12Substrait.Protobuf'
    _CAPABILITIES._serialized_start = 44
    _CAPABILITIES._serialized_end = 408
    _CAPABILITIES_SIMPLEEXTENSION._serialized_start = 259
    _CAPABILITIES_SIMPLEEXTENSION._serialized_end = 408