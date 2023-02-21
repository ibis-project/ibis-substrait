"""Generated protocol buffer code."""
from google.protobuf.internal import builder as _builder
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
_sym_db = _symbol_database.Default()
from ...substrait.ibis import algebra_pb2 as substrait_dot_ibis_dot_algebra__pb2
from ...substrait.ibis.extensions import extensions_pb2 as substrait_dot_ibis_dot_extensions_dot_extensions__pb2
from ...substrait.ibis import plan_pb2 as substrait_dot_ibis_dot_plan__pb2
from ...substrait.ibis import type_pb2 as substrait_dot_ibis_dot_type__pb2
DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n(substrait/ibis/extended_expression.proto\x12\x0esubstrait.ibis\x1a\x1csubstrait/ibis/algebra.proto\x1a*substrait/ibis/extensions/extensions.proto\x1a\x19substrait/ibis/plan.proto\x1a\x19substrait/ibis/type.proto"\xc2\x01\n\x13ExpressionReference\x12<\n\nexpression\x18\x01 \x01(\x0b2\x1a.substrait.ibis.ExpressionH\x00R\nexpression\x12=\n\x07measure\x18\x02 \x01(\x0b2!.substrait.ibis.AggregateFunctionH\x00R\x07measure\x12!\n\x0coutput_names\x18\x03 \x03(\tR\x0boutputNamesB\x0b\n\texpr_type"\x89\x04\n\x12ExtendedExpression\x121\n\x07version\x18\x07 \x01(\x0b2\x17.substrait.ibis.VersionR\x07version\x12T\n\x0eextension_uris\x18\x01 \x03(\x0b2-.substrait.ibis.extensions.SimpleExtensionURIR\rextensionUris\x12U\n\nextensions\x18\x02 \x03(\x0b25.substrait.ibis.extensions.SimpleExtensionDeclarationR\nextensions\x12H\n\rreferred_expr\x18\x03 \x03(\x0b2#.substrait.ibis.ExpressionReferenceR\x0creferredExpr\x12<\n\x0bbase_schema\x18\x04 \x01(\x0b2\x1b.substrait.ibis.NamedStructR\nbaseSchema\x12]\n\x13advanced_extensions\x18\x05 \x01(\x0b2,.substrait.ibis.extensions.AdvancedExtensionR\x12advancedExtensions\x12,\n\x12expected_type_urls\x18\x06 \x03(\tR\x10expectedTypeUrlsB5\n\x17io.substrait.ibis.protoP\x01\xaa\x02\x17Substrait.Ibis.Protobufb\x06proto3')
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, globals())
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'substrait.ibis.extended_expression_pb2', globals())
if _descriptor._USE_C_DESCRIPTORS == False:
    DESCRIPTOR._options = None
    DESCRIPTOR._serialized_options = b'\n\x17io.substrait.ibis.protoP\x01\xaa\x02\x17Substrait.Ibis.Protobuf'
    _EXPRESSIONREFERENCE._serialized_start = 189
    _EXPRESSIONREFERENCE._serialized_end = 383
    _EXTENDEDEXPRESSION._serialized_start = 386
    _EXTENDEDEXPRESSION._serialized_end = 907