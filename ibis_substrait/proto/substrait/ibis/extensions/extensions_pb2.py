"""Generated protocol buffer code."""
from google.protobuf.internal import builder as _builder
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
_sym_db = _symbol_database.Default()
from google.protobuf import any_pb2 as google_dot_protobuf_dot_any__pb2
DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n*substrait/ibis/extensions/extensions.proto\x12\x19substrait.ibis.extensions\x1a\x19google/protobuf/any.proto"X\n\x12SimpleExtensionURI\x120\n\x14extension_uri_anchor\x18\x01 \x01(\rR\x12extensionUriAnchor\x12\x10\n\x03uri\x18\x02 \x01(\tR\x03uri"\xc3\x06\n\x1aSimpleExtensionDeclaration\x12l\n\x0eextension_type\x18\x01 \x01(\x0b2C.substrait.ibis.extensions.SimpleExtensionDeclaration.ExtensionTypeH\x00R\rextensionType\x12\x88\x01\n\x18extension_type_variation\x18\x02 \x01(\x0b2L.substrait.ibis.extensions.SimpleExtensionDeclaration.ExtensionTypeVariationH\x00R\x16extensionTypeVariation\x12x\n\x12extension_function\x18\x03 \x01(\x0b2G.substrait.ibis.extensions.SimpleExtensionDeclaration.ExtensionFunctionH\x00R\x11extensionFunction\x1a|\n\rExtensionType\x126\n\x17extension_uri_reference\x18\x01 \x01(\rR\x15extensionUriReference\x12\x1f\n\x0btype_anchor\x18\x02 \x01(\rR\ntypeAnchor\x12\x12\n\x04name\x18\x03 \x01(\tR\x04name\x1a\x98\x01\n\x16ExtensionTypeVariation\x126\n\x17extension_uri_reference\x18\x01 \x01(\rR\x15extensionUriReference\x122\n\x15type_variation_anchor\x18\x02 \x01(\rR\x13typeVariationAnchor\x12\x12\n\x04name\x18\x03 \x01(\tR\x04name\x1a\x88\x01\n\x11ExtensionFunction\x126\n\x17extension_uri_reference\x18\x01 \x01(\rR\x15extensionUriReference\x12\'\n\x0ffunction_anchor\x18\x02 \x01(\rR\x0efunctionAnchor\x12\x12\n\x04name\x18\x03 \x01(\tR\x04nameB\x0e\n\x0cmapping_type"\x85\x01\n\x11AdvancedExtension\x128\n\x0coptimization\x18\x01 \x01(\x0b2\x14.google.protobuf.AnyR\x0coptimization\x126\n\x0benhancement\x18\x02 \x01(\x0b2\x14.google.protobuf.AnyR\x0benhancementB5\n\x17io.substrait.ibis.protoP\x01\xaa\x02\x17Substrait.Ibis.Protobufb\x06proto3')
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, globals())
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'substrait.ibis.extensions.extensions_pb2', globals())
if _descriptor._USE_C_DESCRIPTORS == False:
    DESCRIPTOR._options = None
    DESCRIPTOR._serialized_options = b'\n\x17io.substrait.ibis.protoP\x01\xaa\x02\x17Substrait.Ibis.Protobuf'
    _SIMPLEEXTENSIONURI._serialized_start = 100
    _SIMPLEEXTENSIONURI._serialized_end = 188
    _SIMPLEEXTENSIONDECLARATION._serialized_start = 191
    _SIMPLEEXTENSIONDECLARATION._serialized_end = 1026
    _SIMPLEEXTENSIONDECLARATION_EXTENSIONTYPE._serialized_start = 592
    _SIMPLEEXTENSIONDECLARATION_EXTENSIONTYPE._serialized_end = 716
    _SIMPLEEXTENSIONDECLARATION_EXTENSIONTYPEVARIATION._serialized_start = 719
    _SIMPLEEXTENSIONDECLARATION_EXTENSIONTYPEVARIATION._serialized_end = 871
    _SIMPLEEXTENSIONDECLARATION_EXTENSIONFUNCTION._serialized_start = 874
    _SIMPLEEXTENSIONDECLARATION_EXTENSIONFUNCTION._serialized_end = 1010
    _ADVANCEDEXTENSION._serialized_start = 1029
    _ADVANCEDEXTENSION._serialized_end = 1162