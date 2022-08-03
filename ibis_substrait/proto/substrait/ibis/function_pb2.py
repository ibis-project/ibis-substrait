"""Generated protocol buffer code."""
from google.protobuf.internal import builder as _builder
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
_sym_db = _symbol_database.Default()
from ...substrait.ibis import parameterized_types_pb2 as substrait_dot_ibis_dot_parameterized__types__pb2
from ...substrait.ibis import type_pb2 as substrait_dot_ibis_dot_type__pb2
from ...substrait.ibis import type_expressions_pb2 as substrait_dot_ibis_dot_type__expressions__pb2
DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x1dsubstrait/ibis/function.proto\x12\x0esubstrait.ibis\x1a(substrait/ibis/parameterized_types.proto\x1a\x19substrait/ibis/type.proto\x1a%substrait/ibis/type_expressions.proto"\xe5\x1a\n\x11FunctionSignature\x1a\xc1\x02\n\x10FinalArgVariadic\x12\x19\n\x08min_args\x18\x01 \x01(\x03R\x07minArgs\x12\x19\n\x08max_args\x18\x02 \x01(\x03R\x07maxArgs\x12i\n\x0bconsistency\x18\x03 \x01(\x0e2G.substrait.ibis.FunctionSignature.FinalArgVariadic.ParameterConsistencyR\x0bconsistency"\x8b\x01\n\x14ParameterConsistency\x12%\n!PARAMETER_CONSISTENCY_UNSPECIFIED\x10\x00\x12$\n PARAMETER_CONSISTENCY_CONSISTENT\x10\x01\x12&\n"PARAMETER_CONSISTENCY_INCONSISTENT\x10\x02\x1a\x10\n\x0eFinalArgNormal\x1a\xe6\x04\n\x06Scalar\x12H\n\targuments\x18\x02 \x03(\x0b2*.substrait.ibis.FunctionSignature.ArgumentR\targuments\x12\x12\n\x04name\x18\x03 \x03(\tR\x04name\x12O\n\x0bdescription\x18\x04 \x01(\x0b2-.substrait.ibis.FunctionSignature.DescriptionR\x0bdescription\x12$\n\rdeterministic\x18\x07 \x01(\x08R\rdeterministic\x12+\n\x11session_dependent\x18\x08 \x01(\x08R\x10sessionDependent\x12E\n\x0boutput_type\x18\t \x01(\x0b2$.substrait.ibis.DerivationExpressionR\noutputType\x12P\n\x08variadic\x18\n \x01(\x0b22.substrait.ibis.FunctionSignature.FinalArgVariadicH\x00R\x08variadic\x12J\n\x06normal\x18\x0b \x01(\x0b20.substrait.ibis.FunctionSignature.FinalArgNormalH\x00R\x06normal\x12Z\n\x0fimplementations\x18\x0c \x03(\x0b20.substrait.ibis.FunctionSignature.ImplementationR\x0fimplementationsB\x19\n\x17final_variable_behavior\x1a\xdf\x05\n\tAggregate\x12H\n\targuments\x18\x02 \x03(\x0b2*.substrait.ibis.FunctionSignature.ArgumentR\targuments\x12\x12\n\x04name\x18\x03 \x01(\tR\x04name\x12O\n\x0bdescription\x18\x04 \x01(\x0b2-.substrait.ibis.FunctionSignature.DescriptionR\x0bdescription\x12$\n\rdeterministic\x18\x07 \x01(\x08R\rdeterministic\x12+\n\x11session_dependent\x18\x08 \x01(\x08R\x10sessionDependent\x12E\n\x0boutput_type\x18\t \x01(\x0b2$.substrait.ibis.DerivationExpressionR\noutputType\x12P\n\x08variadic\x18\n \x01(\x0b22.substrait.ibis.FunctionSignature.FinalArgVariadicH\x00R\x08variadic\x12J\n\x06normal\x18\x0b \x01(\x0b20.substrait.ibis.FunctionSignature.FinalArgNormalH\x00R\x06normal\x12\x18\n\x07ordered\x18\x0e \x01(\x08R\x07ordered\x12\x17\n\x07max_set\x18\x0c \x01(\x04R\x06maxSet\x12A\n\x11intermediate_type\x18\r \x01(\x0b2\x14.substrait.ibis.TypeR\x10intermediateType\x12Z\n\x0fimplementations\x18\x0f \x03(\x0b20.substrait.ibis.FunctionSignature.ImplementationR\x0fimplementationsB\x19\n\x17final_variable_behavior\x1a\xa3\x07\n\x06Window\x12H\n\targuments\x18\x02 \x03(\x0b2*.substrait.ibis.FunctionSignature.ArgumentR\targuments\x12\x12\n\x04name\x18\x03 \x03(\tR\x04name\x12O\n\x0bdescription\x18\x04 \x01(\x0b2-.substrait.ibis.FunctionSignature.DescriptionR\x0bdescription\x12$\n\rdeterministic\x18\x07 \x01(\x08R\rdeterministic\x12+\n\x11session_dependent\x18\x08 \x01(\x08R\x10sessionDependent\x12Q\n\x11intermediate_type\x18\t \x01(\x0b2$.substrait.ibis.DerivationExpressionR\x10intermediateType\x12E\n\x0boutput_type\x18\n \x01(\x0b2$.substrait.ibis.DerivationExpressionR\noutputType\x12P\n\x08variadic\x18\x10 \x01(\x0b22.substrait.ibis.FunctionSignature.FinalArgVariadicH\x00R\x08variadic\x12J\n\x06normal\x18\x11 \x01(\x0b20.substrait.ibis.FunctionSignature.FinalArgNormalH\x00R\x06normal\x12\x18\n\x07ordered\x18\x0b \x01(\x08R\x07ordered\x12\x17\n\x07max_set\x18\x0c \x01(\x04R\x06maxSet\x12T\n\x0bwindow_type\x18\x0e \x01(\x0e23.substrait.ibis.FunctionSignature.Window.WindowTypeR\nwindowType\x12Z\n\x0fimplementations\x18\x0f \x03(\x0b20.substrait.ibis.FunctionSignature.ImplementationR\x0fimplementations"_\n\nWindowType\x12\x1b\n\x17WINDOW_TYPE_UNSPECIFIED\x10\x00\x12\x19\n\x15WINDOW_TYPE_STREAMING\x10\x01\x12\x19\n\x15WINDOW_TYPE_PARTITION\x10\x02B\x19\n\x17final_variable_behavior\x1a=\n\x0bDescription\x12\x1a\n\x08language\x18\x01 \x01(\tR\x08language\x12\x12\n\x04body\x18\x02 \x01(\tR\x04body\x1a\xb6\x01\n\x0eImplementation\x12I\n\x04type\x18\x01 \x01(\x0e25.substrait.ibis.FunctionSignature.Implementation.TypeR\x04type\x12\x10\n\x03uri\x18\x02 \x01(\tR\x03uri"G\n\x04Type\x12\x14\n\x10TYPE_UNSPECIFIED\x10\x00\x12\x15\n\x11TYPE_WEB_ASSEMBLY\x10\x01\x12\x12\n\x0eTYPE_TRINO_JAR\x10\x02\x1a\x90\x04\n\x08Argument\x12\x12\n\x04name\x18\x01 \x01(\tR\x04name\x12P\n\x05value\x18\x02 \x01(\x0b28.substrait.ibis.FunctionSignature.Argument.ValueArgumentH\x00R\x05value\x12M\n\x04type\x18\x03 \x01(\x0b27.substrait.ibis.FunctionSignature.Argument.TypeArgumentH\x00R\x04type\x12M\n\x04enum\x18\x04 \x01(\x0b27.substrait.ibis.FunctionSignature.Argument.EnumArgumentH\x00R\x04enum\x1ab\n\rValueArgument\x125\n\x04type\x18\x01 \x01(\x0b2!.substrait.ibis.ParameterizedTypeR\x04type\x12\x1a\n\x08constant\x18\x02 \x01(\x08R\x08constant\x1aE\n\x0cTypeArgument\x125\n\x04type\x18\x01 \x01(\x0b2!.substrait.ibis.ParameterizedTypeR\x04type\x1aD\n\x0cEnumArgument\x12\x18\n\x07options\x18\x01 \x03(\tR\x07options\x12\x1a\n\x08optional\x18\x02 \x01(\x08R\x08optionalB\x0f\n\rargument_kindB5\n\x17io.substrait.ibis.protoP\x01\xaa\x02\x17Substrait.Ibis.Protobufb\x06proto3')
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, globals())
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'substrait.ibis.function_pb2', globals())
if _descriptor._USE_C_DESCRIPTORS == False:
    DESCRIPTOR._options = None
    DESCRIPTOR._serialized_options = b'\n\x17io.substrait.ibis.protoP\x01\xaa\x02\x17Substrait.Ibis.Protobuf'
    _FUNCTIONSIGNATURE._serialized_start = 158
    _FUNCTIONSIGNATURE._serialized_end = 3587
    _FUNCTIONSIGNATURE_FINALARGVARIADIC._serialized_start = 180
    _FUNCTIONSIGNATURE_FINALARGVARIADIC._serialized_end = 501
    _FUNCTIONSIGNATURE_FINALARGVARIADIC_PARAMETERCONSISTENCY._serialized_start = 362
    _FUNCTIONSIGNATURE_FINALARGVARIADIC_PARAMETERCONSISTENCY._serialized_end = 501
    _FUNCTIONSIGNATURE_FINALARGNORMAL._serialized_start = 503
    _FUNCTIONSIGNATURE_FINALARGNORMAL._serialized_end = 519
    _FUNCTIONSIGNATURE_SCALAR._serialized_start = 522
    _FUNCTIONSIGNATURE_SCALAR._serialized_end = 1136
    _FUNCTIONSIGNATURE_AGGREGATE._serialized_start = 1139
    _FUNCTIONSIGNATURE_AGGREGATE._serialized_end = 1874
    _FUNCTIONSIGNATURE_WINDOW._serialized_start = 1877
    _FUNCTIONSIGNATURE_WINDOW._serialized_end = 2808
    _FUNCTIONSIGNATURE_WINDOW_WINDOWTYPE._serialized_start = 2686
    _FUNCTIONSIGNATURE_WINDOW_WINDOWTYPE._serialized_end = 2781
    _FUNCTIONSIGNATURE_DESCRIPTION._serialized_start = 2810
    _FUNCTIONSIGNATURE_DESCRIPTION._serialized_end = 2871
    _FUNCTIONSIGNATURE_IMPLEMENTATION._serialized_start = 2874
    _FUNCTIONSIGNATURE_IMPLEMENTATION._serialized_end = 3056
    _FUNCTIONSIGNATURE_IMPLEMENTATION_TYPE._serialized_start = 2985
    _FUNCTIONSIGNATURE_IMPLEMENTATION_TYPE._serialized_end = 3056
    _FUNCTIONSIGNATURE_ARGUMENT._serialized_start = 3059
    _FUNCTIONSIGNATURE_ARGUMENT._serialized_end = 3587
    _FUNCTIONSIGNATURE_ARGUMENT_VALUEARGUMENT._serialized_start = 3331
    _FUNCTIONSIGNATURE_ARGUMENT_VALUEARGUMENT._serialized_end = 3429
    _FUNCTIONSIGNATURE_ARGUMENT_TYPEARGUMENT._serialized_start = 3431
    _FUNCTIONSIGNATURE_ARGUMENT_TYPEARGUMENT._serialized_end = 3500
    _FUNCTIONSIGNATURE_ARGUMENT_ENUMARGUMENT._serialized_start = 3502
    _FUNCTIONSIGNATURE_ARGUMENT_ENUMARGUMENT._serialized_end = 3570