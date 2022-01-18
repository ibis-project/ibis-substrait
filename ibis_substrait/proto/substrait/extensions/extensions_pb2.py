"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
_sym_db = _symbol_database.Default()
from google.protobuf import any_pb2 as google_dot_protobuf_dot_any__pb2
DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n%substrait/extensions/extensions.proto\x12\x14substrait.extensions\x1a\x19google/protobuf/any.proto"X\n\x12SimpleExtensionURI\x120\n\x14extension_uri_anchor\x18\x01 \x01(\rR\x12extensionUriAnchor\x12\x10\n\x03uri\x18\x02 \x01(\tR\x03uri"\xb4\x06\n\x1aSimpleExtensionDeclaration\x12g\n\x0eextension_type\x18\x01 \x01(\x0b2>.substrait.extensions.SimpleExtensionDeclaration.ExtensionTypeH\x00R\rextensionType\x12\x83\x01\n\x18extension_type_variation\x18\x02 \x01(\x0b2G.substrait.extensions.SimpleExtensionDeclaration.ExtensionTypeVariationH\x00R\x16extensionTypeVariation\x12s\n\x12extension_function\x18\x03 \x01(\x0b2B.substrait.extensions.SimpleExtensionDeclaration.ExtensionFunctionH\x00R\x11extensionFunction\x1a|\n\rExtensionType\x126\n\x17extension_uri_reference\x18\x01 \x01(\rR\x15extensionUriReference\x12\x1f\n\x0btype_anchor\x18\x02 \x01(\rR\ntypeAnchor\x12\x12\n\x04name\x18\x03 \x01(\tR\x04name\x1a\x98\x01\n\x16ExtensionTypeVariation\x126\n\x17extension_uri_reference\x18\x01 \x01(\rR\x15extensionUriReference\x122\n\x15type_variation_anchor\x18\x02 \x01(\rR\x13typeVariationAnchor\x12\x12\n\x04name\x18\x03 \x01(\tR\x04name\x1a\x88\x01\n\x11ExtensionFunction\x126\n\x17extension_uri_reference\x18\x01 \x01(\rR\x15extensionUriReference\x12\'\n\x0ffunction_anchor\x18\x02 \x01(\rR\x0efunctionAnchor\x12\x12\n\x04name\x18\x03 \x01(\tR\x04nameB\x0e\n\x0cmapping_type"\x85\x01\n\x11AdvancedExtension\x128\n\x0coptimization\x18\x01 \x01(\x0b2\x14.google.protobuf.AnyR\x0coptimization\x126\n\x0benhancement\x18\x02 \x01(\x0b2\x14.google.protobuf.AnyR\x0benhancementB+\n\x12io.substrait.protoP\x01\xaa\x02\x12Substrait.Protobufb\x06proto3')
_SIMPLEEXTENSIONURI = DESCRIPTOR.message_types_by_name['SimpleExtensionURI']
_SIMPLEEXTENSIONDECLARATION = DESCRIPTOR.message_types_by_name['SimpleExtensionDeclaration']
_SIMPLEEXTENSIONDECLARATION_EXTENSIONTYPE = _SIMPLEEXTENSIONDECLARATION.nested_types_by_name['ExtensionType']
_SIMPLEEXTENSIONDECLARATION_EXTENSIONTYPEVARIATION = _SIMPLEEXTENSIONDECLARATION.nested_types_by_name['ExtensionTypeVariation']
_SIMPLEEXTENSIONDECLARATION_EXTENSIONFUNCTION = _SIMPLEEXTENSIONDECLARATION.nested_types_by_name['ExtensionFunction']
_ADVANCEDEXTENSION = DESCRIPTOR.message_types_by_name['AdvancedExtension']
SimpleExtensionURI = _reflection.GeneratedProtocolMessageType('SimpleExtensionURI', (_message.Message,), {'DESCRIPTOR': _SIMPLEEXTENSIONURI, '__module__': 'substrait.extensions.extensions_pb2'})
_sym_db.RegisterMessage(SimpleExtensionURI)
SimpleExtensionDeclaration = _reflection.GeneratedProtocolMessageType('SimpleExtensionDeclaration', (_message.Message,), {'ExtensionType': _reflection.GeneratedProtocolMessageType('ExtensionType', (_message.Message,), {'DESCRIPTOR': _SIMPLEEXTENSIONDECLARATION_EXTENSIONTYPE, '__module__': 'substrait.extensions.extensions_pb2'}), 'ExtensionTypeVariation': _reflection.GeneratedProtocolMessageType('ExtensionTypeVariation', (_message.Message,), {'DESCRIPTOR': _SIMPLEEXTENSIONDECLARATION_EXTENSIONTYPEVARIATION, '__module__': 'substrait.extensions.extensions_pb2'}), 'ExtensionFunction': _reflection.GeneratedProtocolMessageType('ExtensionFunction', (_message.Message,), {'DESCRIPTOR': _SIMPLEEXTENSIONDECLARATION_EXTENSIONFUNCTION, '__module__': 'substrait.extensions.extensions_pb2'}), 'DESCRIPTOR': _SIMPLEEXTENSIONDECLARATION, '__module__': 'substrait.extensions.extensions_pb2'})
_sym_db.RegisterMessage(SimpleExtensionDeclaration)
_sym_db.RegisterMessage(SimpleExtensionDeclaration.ExtensionType)
_sym_db.RegisterMessage(SimpleExtensionDeclaration.ExtensionTypeVariation)
_sym_db.RegisterMessage(SimpleExtensionDeclaration.ExtensionFunction)
AdvancedExtension = _reflection.GeneratedProtocolMessageType('AdvancedExtension', (_message.Message,), {'DESCRIPTOR': _ADVANCEDEXTENSION, '__module__': 'substrait.extensions.extensions_pb2'})
_sym_db.RegisterMessage(AdvancedExtension)
if _descriptor._USE_C_DESCRIPTORS == False:
    DESCRIPTOR._options = None
    DESCRIPTOR._serialized_options = b'\n\x12io.substrait.protoP\x01\xaa\x02\x12Substrait.Protobuf'
    _SIMPLEEXTENSIONURI._serialized_start = 90
    _SIMPLEEXTENSIONURI._serialized_end = 178
    _SIMPLEEXTENSIONDECLARATION._serialized_start = 181
    _SIMPLEEXTENSIONDECLARATION._serialized_end = 1001
    _SIMPLEEXTENSIONDECLARATION_EXTENSIONTYPE._serialized_start = 567
    _SIMPLEEXTENSIONDECLARATION_EXTENSIONTYPE._serialized_end = 691
    _SIMPLEEXTENSIONDECLARATION_EXTENSIONTYPEVARIATION._serialized_start = 694
    _SIMPLEEXTENSIONDECLARATION_EXTENSIONTYPEVARIATION._serialized_end = 846
    _SIMPLEEXTENSIONDECLARATION_EXTENSIONFUNCTION._serialized_start = 849
    _SIMPLEEXTENSIONDECLARATION_EXTENSIONFUNCTION._serialized_end = 985
    _ADVANCEDEXTENSION._serialized_start = 1004
    _ADVANCEDEXTENSION._serialized_end = 1137