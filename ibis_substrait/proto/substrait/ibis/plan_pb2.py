"""Generated protocol buffer code."""
from google.protobuf.internal import builder as _builder
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
_sym_db = _symbol_database.Default()
from ...substrait.ibis import algebra_pb2 as substrait_dot_ibis_dot_algebra__pb2
from ...substrait.ibis.extensions import extensions_pb2 as substrait_dot_ibis_dot_extensions_dot_extensions__pb2
DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x19substrait/ibis/plan.proto\x12\x0esubstrait.ibis\x1a\x1csubstrait/ibis/algebra.proto\x1a*substrait/ibis/extensions/extensions.proto"m\n\x07PlanRel\x12\'\n\x03rel\x18\x01 \x01(\x0b2\x13.substrait.ibis.RelH\x00R\x03rel\x12-\n\x04root\x18\x02 \x01(\x0b2\x17.substrait.ibis.RelRootH\x00R\x04rootB\n\n\x08rel_type"\xaa\x03\n\x04Plan\x121\n\x07version\x18\x06 \x01(\x0b2\x17.substrait.ibis.VersionR\x07version\x12T\n\x0eextension_uris\x18\x01 \x03(\x0b2-.substrait.ibis.extensions.SimpleExtensionURIR\rextensionUris\x12U\n\nextensions\x18\x02 \x03(\x0b25.substrait.ibis.extensions.SimpleExtensionDeclarationR\nextensions\x125\n\trelations\x18\x03 \x03(\x0b2\x17.substrait.ibis.PlanRelR\trelations\x12]\n\x13advanced_extensions\x18\x04 \x01(\x0b2,.substrait.ibis.extensions.AdvancedExtensionR\x12advancedExtensions\x12,\n\x12expected_type_urls\x18\x05 \x03(\tR\x10expectedTypeUrls"@\n\x0bPlanVersion\x121\n\x07version\x18\x06 \x01(\x0b2\x17.substrait.ibis.VersionR\x07version"\xa9\x01\n\x07Version\x12!\n\x0cmajor_number\x18\x01 \x01(\rR\x0bmajorNumber\x12!\n\x0cminor_number\x18\x02 \x01(\rR\x0bminorNumber\x12!\n\x0cpatch_number\x18\x03 \x01(\rR\x0bpatchNumber\x12\x19\n\x08git_hash\x18\x04 \x01(\tR\x07gitHash\x12\x1a\n\x08producer\x18\x05 \x01(\tR\x08producerB5\n\x17io.substrait.ibis.protoP\x01\xaa\x02\x17Substrait.Ibis.Protobufb\x06proto3')
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, globals())
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'substrait.ibis.plan_pb2', globals())
if _descriptor._USE_C_DESCRIPTORS == False:
    DESCRIPTOR._options = None
    DESCRIPTOR._serialized_options = b'\n\x17io.substrait.ibis.protoP\x01\xaa\x02\x17Substrait.Ibis.Protobuf'
    _PLANREL._serialized_start = 119
    _PLANREL._serialized_end = 228
    _PLAN._serialized_start = 231
    _PLAN._serialized_end = 657
    _PLANVERSION._serialized_start = 659
    _PLANVERSION._serialized_end = 723
    _VERSION._serialized_start = 726
    _VERSION._serialized_end = 895