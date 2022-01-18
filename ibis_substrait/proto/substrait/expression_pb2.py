"""Generated protocol buffer code."""
from google.protobuf.internal import enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
_sym_db = _symbol_database.Default()
from ..substrait import type_pb2 as substrait_dot_type__pb2
DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x1asubstrait/expression.proto\x12\tsubstrait\x1a\x14substrait/type.proto"\xb9:\n\nExpression\x129\n\x07literal\x18\x01 \x01(\x0b2\x1d.substrait.Expression.LiteralH\x00R\x07literal\x12D\n\tselection\x18\x02 \x01(\x0b2$.substrait.Expression.FieldReferenceH\x00R\tselection\x12O\n\x0fscalar_function\x18\x03 \x01(\x0b2$.substrait.Expression.ScalarFunctionH\x00R\x0escalarFunction\x12O\n\x0fwindow_function\x18\x05 \x01(\x0b2$.substrait.Expression.WindowFunctionH\x00R\x0ewindowFunction\x127\n\x07if_then\x18\x06 \x01(\x0b2\x1c.substrait.Expression.IfThenH\x00R\x06ifThen\x12U\n\x11switch_expression\x18\x07 \x01(\x0b2&.substrait.Expression.SwitchExpressionH\x00R\x10switchExpression\x12P\n\x10singular_or_list\x18\x08 \x01(\x0b2$.substrait.Expression.SingularOrListH\x00R\x0esingularOrList\x12G\n\rmulti_or_list\x18\t \x01(\x0b2!.substrait.Expression.MultiOrListH\x00R\x0bmultiOrList\x120\n\x04enum\x18\n \x01(\x0b2\x1a.substrait.Expression.EnumH\x00R\x04enum\x120\n\x04cast\x18\x0b \x01(\x0b2\x1a.substrait.Expression.CastH\x00R\x04cast\x1a\x82\x01\n\x04Enum\x12\x1e\n\tspecified\x18\x01 \x01(\tH\x00R\tspecified\x12D\n\x0bunspecified\x18\x02 \x01(\x0b2 .substrait.Expression.Enum.EmptyH\x00R\x0bunspecified\x1a\x07\n\x05EmptyB\x0b\n\tenum_kind\x1a\xc7\r\n\x07Literal\x12\x1a\n\x07boolean\x18\x01 \x01(\x08H\x00R\x07boolean\x12\x10\n\x02i8\x18\x02 \x01(\x05H\x00R\x02i8\x12\x12\n\x03i16\x18\x03 \x01(\x05H\x00R\x03i16\x12\x12\n\x03i32\x18\x05 \x01(\x05H\x00R\x03i32\x12\x12\n\x03i64\x18\x07 \x01(\x03H\x00R\x03i64\x12\x14\n\x04fp32\x18\n \x01(\x02H\x00R\x04fp32\x12\x14\n\x04fp64\x18\x0b \x01(\x01H\x00R\x04fp64\x12\x18\n\x06string\x18\x0c \x01(\tH\x00R\x06string\x12\x18\n\x06binary\x18\r \x01(\x0cH\x00R\x06binary\x12\x1e\n\ttimestamp\x18\x0e \x01(\x03H\x00R\ttimestamp\x12\x14\n\x04date\x18\x10 \x01(\x05H\x00R\x04date\x12\x14\n\x04time\x18\x11 \x01(\x03H\x00R\x04time\x12h\n\x16interval_year_to_month\x18\x13 \x01(\x0b21.substrait.Expression.Literal.IntervalYearToMonthH\x00R\x13intervalYearToMonth\x12h\n\x16interval_day_to_second\x18\x14 \x01(\x0b21.substrait.Expression.Literal.IntervalDayToSecondH\x00R\x13intervalDayToSecond\x12\x1f\n\nfixed_char\x18\x15 \x01(\tH\x00R\tfixedChar\x12B\n\x08var_char\x18\x16 \x01(\x0b2%.substrait.Expression.Literal.VarCharH\x00R\x07varChar\x12#\n\x0cfixed_binary\x18\x17 \x01(\x0cH\x00R\x0bfixedBinary\x12A\n\x07decimal\x18\x18 \x01(\x0b2%.substrait.Expression.Literal.DecimalH\x00R\x07decimal\x12>\n\x06struct\x18\x19 \x01(\x0b2$.substrait.Expression.Literal.StructH\x00R\x06struct\x125\n\x03map\x18\x1a \x01(\x0b2!.substrait.Expression.Literal.MapH\x00R\x03map\x12#\n\x0ctimestamp_tz\x18\x1b \x01(\x03H\x00R\x0btimestampTz\x12\x14\n\x04uuid\x18\x1c \x01(\x0cH\x00R\x04uuid\x12%\n\x04null\x18\x1d \x01(\x0b2\x0f.substrait.TypeH\x00R\x04null\x128\n\x04list\x18\x1e \x01(\x0b2".substrait.Expression.Literal.ListH\x00R\x04list\x125\n\nempty_list\x18\x1f \x01(\x0b2\x14.substrait.Type.ListH\x00R\temptyList\x122\n\tempty_map\x18  \x01(\x0b2\x13.substrait.Type.MapH\x00R\x08emptyMap\x12\x1a\n\x08nullable\x182 \x01(\x08R\x08nullable\x1a7\n\x07VarChar\x12\x14\n\x05value\x18\x01 \x01(\tR\x05value\x12\x16\n\x06length\x18\x02 \x01(\rR\x06length\x1aS\n\x07Decimal\x12\x14\n\x05value\x18\x01 \x01(\x0cR\x05value\x12\x1c\n\tprecision\x18\x02 \x01(\x05R\tprecision\x12\x14\n\x05scale\x18\x03 \x01(\x05R\x05scale\x1a\xc2\x01\n\x03Map\x12I\n\nkey_values\x18\x01 \x03(\x0b2*.substrait.Expression.Literal.Map.KeyValueR\tkeyValues\x1ap\n\x08KeyValue\x12/\n\x03key\x18\x01 \x01(\x0b2\x1d.substrait.Expression.LiteralR\x03key\x123\n\x05value\x18\x02 \x01(\x0b2\x1d.substrait.Expression.LiteralR\x05value\x1aC\n\x13IntervalYearToMonth\x12\x14\n\x05years\x18\x01 \x01(\x05R\x05years\x12\x16\n\x06months\x18\x02 \x01(\x05R\x06months\x1aC\n\x13IntervalDayToSecond\x12\x12\n\x04days\x18\x01 \x01(\x05R\x04days\x12\x18\n\x07seconds\x18\x02 \x01(\x05R\x07seconds\x1a?\n\x06Struct\x125\n\x06fields\x18\x01 \x03(\x0b2\x1d.substrait.Expression.LiteralR\x06fields\x1a=\n\x04List\x125\n\x06values\x18\x01 \x03(\x0b2\x1d.substrait.Expression.LiteralR\x06valuesB\x0e\n\x0cliteral_type\x1a\x9c\x01\n\x0eScalarFunction\x12-\n\x12function_reference\x18\x01 \x01(\rR\x11functionReference\x12)\n\x04args\x18\x02 \x03(\x0b2\x15.substrait.ExpressionR\x04args\x120\n\x0boutput_type\x18\x03 \x01(\x0b2\x0f.substrait.TypeR\noutputType\x1a\x9f\x07\n\x0eWindowFunction\x12-\n\x12function_reference\x18\x01 \x01(\rR\x11functionReference\x125\n\npartitions\x18\x02 \x03(\x0b2\x15.substrait.ExpressionR\npartitions\x12*\n\x05sorts\x18\x03 \x03(\x0b2\x14.substrait.SortFieldR\x05sorts\x12K\n\x0bupper_bound\x18\x04 \x01(\x0b2*.substrait.Expression.WindowFunction.BoundR\nupperBound\x12K\n\x0blower_bound\x18\x05 \x01(\x0b2*.substrait.Expression.WindowFunction.BoundR\nlowerBound\x121\n\x05phase\x18\x06 \x01(\x0e2\x1b.substrait.AggregationPhaseR\x05phase\x120\n\x0boutput_type\x18\x07 \x01(\x0b2\x0f.substrait.TypeR\noutputType\x12)\n\x04args\x18\x08 \x03(\x0b2\x15.substrait.ExpressionR\x04args\x1a\xd0\x03\n\x05Bound\x12T\n\tpreceding\x18\x01 \x01(\x0b24.substrait.Expression.WindowFunction.Bound.PrecedingH\x00R\tpreceding\x12T\n\tfollowing\x18\x02 \x01(\x0b24.substrait.Expression.WindowFunction.Bound.FollowingH\x00R\tfollowing\x12X\n\x0bcurrent_row\x18\x03 \x01(\x0b25.substrait.Expression.WindowFunction.Bound.CurrentRowH\x00R\ncurrentRow\x12T\n\tunbounded\x18\x04 \x01(\x0b24.substrait.Expression.WindowFunction.Bound.UnboundedH\x00R\tunbounded\x1a#\n\tPreceding\x12\x16\n\x06offset\x18\x01 \x01(\x03R\x06offset\x1a#\n\tFollowing\x12\x16\n\x06offset\x18\x01 \x01(\x03R\x06offset\x1a\x0c\n\nCurrentRow\x1a\x0b\n\tUnboundedB\x06\n\x04kind\x1a\xca\x01\n\x06IfThen\x127\n\x03ifs\x18\x01 \x03(\x0b2%.substrait.Expression.IfThen.IfClauseR\x03ifs\x12)\n\x04else\x18\x02 \x01(\x0b2\x15.substrait.ExpressionR\x04else\x1a\\\n\x08IfClause\x12%\n\x02if\x18\x01 \x01(\x0b2\x15.substrait.ExpressionR\x02if\x12)\n\x04then\x18\x02 \x01(\x0b2\x15.substrait.ExpressionR\x04then\x1aX\n\x04Cast\x12#\n\x04type\x18\x01 \x01(\x0b2\x0f.substrait.TypeR\x04type\x12+\n\x05input\x18\x02 \x01(\x0b2\x15.substrait.ExpressionR\x05input\x1a\xe4\x01\n\x10SwitchExpression\x12@\n\x03ifs\x18\x01 \x03(\x0b2..substrait.Expression.SwitchExpression.IfValueR\x03ifs\x12)\n\x04else\x18\x02 \x01(\x0b2\x15.substrait.ExpressionR\x04else\x1ac\n\x07IfValue\x12-\n\x02if\x18\x01 \x01(\x0b2\x1d.substrait.Expression.LiteralR\x02if\x12)\n\x04then\x18\x02 \x01(\x0b2\x15.substrait.ExpressionR\x04then\x1an\n\x0eSingularOrList\x12+\n\x05value\x18\x01 \x01(\x0b2\x15.substrait.ExpressionR\x05value\x12/\n\x07options\x18\x02 \x03(\x0b2\x15.substrait.ExpressionR\x07options\x1a\xb7\x01\n\x0bMultiOrList\x12+\n\x05value\x18\x01 \x03(\x0b2\x15.substrait.ExpressionR\x05value\x12B\n\x07options\x18\x02 \x03(\x0b2(.substrait.Expression.MultiOrList.RecordR\x07options\x1a7\n\x06Record\x12-\n\x06fields\x18\x01 \x03(\x0b2\x15.substrait.ExpressionR\x06fields\x1a\x93\x04\n\x10EmbeddedFunction\x123\n\targuments\x18\x01 \x03(\x0b2\x15.substrait.ExpressionR\targuments\x120\n\x0boutput_type\x18\x02 \x01(\x0b2\x0f.substrait.TypeR\noutputType\x12s\n\x16python_pickle_function\x18\x03 \x01(\x0b2;.substrait.Expression.EmbeddedFunction.PythonPickleFunctionH\x00R\x14pythonPickleFunction\x12p\n\x15web_assembly_function\x18\x04 \x01(\x0b2:.substrait.Expression.EmbeddedFunction.WebAssemblyFunctionH\x00R\x13webAssemblyFunction\x1aV\n\x14PythonPickleFunction\x12\x1a\n\x08function\x18\x01 \x01(\x0cR\x08function\x12"\n\x0cprerequisite\x18\x02 \x03(\tR\x0cprerequisite\x1aQ\n\x13WebAssemblyFunction\x12\x16\n\x06script\x18\x01 \x01(\x0cR\x06script\x12"\n\x0cprerequisite\x18\x02 \x03(\tR\x0cprerequisiteB\x06\n\x04kind\x1a\xe8\x04\n\x10ReferenceSegment\x12H\n\x07map_key\x18\x01 \x01(\x0b2-.substrait.Expression.ReferenceSegment.MapKeyH\x00R\x06mapKey\x12W\n\x0cstruct_field\x18\x02 \x01(\x0b22.substrait.Expression.ReferenceSegment.StructFieldH\x00R\x0bstructField\x12W\n\x0clist_element\x18\x03 \x01(\x0b22.substrait.Expression.ReferenceSegment.ListElementH\x00R\x0blistElement\x1a~\n\x06MapKey\x126\n\x07map_key\x18\x01 \x01(\x0b2\x1d.substrait.Expression.LiteralR\x06mapKey\x12<\n\x05child\x18\x02 \x01(\x0b2&.substrait.Expression.ReferenceSegmentR\x05child\x1aa\n\x0bStructField\x12\x14\n\x05field\x18\x01 \x01(\x05R\x05field\x12<\n\x05child\x18\x02 \x01(\x0b2&.substrait.Expression.ReferenceSegmentR\x05child\x1ac\n\x0bListElement\x12\x16\n\x06offset\x18\x01 \x01(\x05R\x06offset\x12<\n\x05child\x18\x02 \x01(\x0b2&.substrait.Expression.ReferenceSegmentR\x05childB\x10\n\x0ereference_type\x1a\xa2\x0b\n\x0eMaskExpression\x12I\n\x06select\x18\x01 \x01(\x0b21.substrait.Expression.MaskExpression.StructSelectR\x06select\x128\n\x18maintain_singular_struct\x18\x02 \x01(\x08R\x16maintainSingularStruct\x1a\xe8\x01\n\x06Select\x12K\n\x06struct\x18\x01 \x01(\x0b21.substrait.Expression.MaskExpression.StructSelectH\x00R\x06struct\x12E\n\x04list\x18\x02 \x01(\x0b2/.substrait.Expression.MaskExpression.ListSelectH\x00R\x04list\x12B\n\x03map\x18\x03 \x01(\x0b2..substrait.Expression.MaskExpression.MapSelectH\x00R\x03mapB\x06\n\x04type\x1ab\n\x0cStructSelect\x12R\n\x0cstruct_items\x18\x01 \x03(\x0b2/.substrait.Expression.MaskExpression.StructItemR\x0bstructItems\x1ae\n\nStructItem\x12\x14\n\x05field\x18\x01 \x01(\x05R\x05field\x12A\n\x05child\x18\x02 \x01(\x0b2+.substrait.Expression.MaskExpression.SelectR\x05child\x1a\xe6\x03\n\nListSelect\x12\\\n\tselection\x18\x01 \x03(\x0b2>.substrait.Expression.MaskExpression.ListSelect.ListSelectItemR\tselection\x12A\n\x05child\x18\x02 \x01(\x0b2+.substrait.Expression.MaskExpression.SelectR\x05child\x1a\xb6\x02\n\x0eListSelectItem\x12`\n\x04item\x18\x01 \x01(\x0b2J.substrait.Expression.MaskExpression.ListSelect.ListSelectItem.ListElementH\x00R\x04item\x12`\n\x05slice\x18\x02 \x01(\x0b2H.substrait.Expression.MaskExpression.ListSelect.ListSelectItem.ListSliceH\x00R\x05slice\x1a#\n\x0bListElement\x12\x14\n\x05field\x18\x01 \x01(\x05R\x05field\x1a3\n\tListSlice\x12\x14\n\x05start\x18\x01 \x01(\x05R\x05start\x12\x10\n\x03end\x18\x02 \x01(\x05R\x03endB\x06\n\x04type\x1a\xeb\x02\n\tMapSelect\x12I\n\x03key\x18\x01 \x01(\x0b25.substrait.Expression.MaskExpression.MapSelect.MapKeyH\x00R\x03key\x12a\n\nexpression\x18\x02 \x01(\x0b2?.substrait.Expression.MaskExpression.MapSelect.MapKeyExpressionH\x00R\nexpression\x12A\n\x05child\x18\x03 \x01(\x0b2+.substrait.Expression.MaskExpression.SelectR\x05child\x1a!\n\x06MapKey\x12\x17\n\x07map_key\x18\x01 \x01(\tR\x06mapKey\x1a@\n\x10MapKeyExpression\x12,\n\x12map_key_expression\x18\x01 \x01(\tR\x10mapKeyExpressionB\x08\n\x06select\x1a\xfe\x02\n\x0eFieldReference\x12S\n\x10direct_reference\x18\x01 \x01(\x0b2&.substrait.Expression.ReferenceSegmentH\x00R\x0fdirectReference\x12Q\n\x10masked_reference\x18\x02 \x01(\x0b2$.substrait.Expression.MaskExpressionH\x00R\x0fmaskedReference\x127\n\nexpression\x18\x03 \x01(\x0b2\x15.substrait.ExpressionH\x01R\nexpression\x12[\n\x0eroot_reference\x18\x04 \x01(\x0b22.substrait.Expression.FieldReference.RootReferenceH\x01R\rrootReference\x1a\x0f\n\rRootReferenceB\x10\n\x0ereference_typeB\x0b\n\troot_typeB\n\n\x08rex_type"\xad\x03\n\tSortField\x12)\n\x04expr\x18\x01 \x01(\x0b2\x15.substrait.ExpressionR\x04expr\x12B\n\tdirection\x18\x02 \x01(\x0e2".substrait.SortField.SortDirectionH\x00R\tdirection\x12D\n\x1dcomparison_function_reference\x18\x03 \x01(\rH\x00R\x1bcomparisonFunctionReference"\xdd\x01\n\rSortDirection\x12\x1e\n\x1aSORT_DIRECTION_UNSPECIFIED\x10\x00\x12"\n\x1eSORT_DIRECTION_ASC_NULLS_FIRST\x10\x01\x12!\n\x1dSORT_DIRECTION_ASC_NULLS_LAST\x10\x02\x12#\n\x1fSORT_DIRECTION_DESC_NULLS_FIRST\x10\x03\x12"\n\x1eSORT_DIRECTION_DESC_NULLS_LAST\x10\x04\x12\x1c\n\x18SORT_DIRECTION_CLUSTERED\x10\x05B\x0b\n\tsort_kind"\xfe\x01\n\x11AggregateFunction\x12-\n\x12function_reference\x18\x01 \x01(\rR\x11functionReference\x12)\n\x04args\x18\x02 \x03(\x0b2\x15.substrait.ExpressionR\x04args\x12*\n\x05sorts\x18\x03 \x03(\x0b2\x14.substrait.SortFieldR\x05sorts\x121\n\x05phase\x18\x04 \x01(\x0e2\x1b.substrait.AggregationPhaseR\x05phase\x120\n\x0boutput_type\x18\x05 \x01(\x0b2\x0f.substrait.TypeR\noutputType*\xef\x01\n\x10AggregationPhase\x12!\n\x1dAGGREGATION_PHASE_UNSPECIFIED\x10\x00\x12-\n)AGGREGATION_PHASE_INITIAL_TO_INTERMEDIATE\x10\x01\x122\n.AGGREGATION_PHASE_INTERMEDIATE_TO_INTERMEDIATE\x10\x02\x12\'\n#AGGREGATION_PHASE_INITIAL_TO_RESULT\x10\x03\x12,\n(AGGREGATION_PHASE_INTERMEDIATE_TO_RESULT\x10\x04B+\n\x12io.substrait.protoP\x01\xaa\x02\x12Substrait.Protobufb\x06proto3')
_AGGREGATIONPHASE = DESCRIPTOR.enum_types_by_name['AggregationPhase']
AggregationPhase = enum_type_wrapper.EnumTypeWrapper(_AGGREGATIONPHASE)
AGGREGATION_PHASE_UNSPECIFIED = 0
AGGREGATION_PHASE_INITIAL_TO_INTERMEDIATE = 1
AGGREGATION_PHASE_INTERMEDIATE_TO_INTERMEDIATE = 2
AGGREGATION_PHASE_INITIAL_TO_RESULT = 3
AGGREGATION_PHASE_INTERMEDIATE_TO_RESULT = 4
_EXPRESSION = DESCRIPTOR.message_types_by_name['Expression']
_EXPRESSION_ENUM = _EXPRESSION.nested_types_by_name['Enum']
_EXPRESSION_ENUM_EMPTY = _EXPRESSION_ENUM.nested_types_by_name['Empty']
_EXPRESSION_LITERAL = _EXPRESSION.nested_types_by_name['Literal']
_EXPRESSION_LITERAL_VARCHAR = _EXPRESSION_LITERAL.nested_types_by_name['VarChar']
_EXPRESSION_LITERAL_DECIMAL = _EXPRESSION_LITERAL.nested_types_by_name['Decimal']
_EXPRESSION_LITERAL_MAP = _EXPRESSION_LITERAL.nested_types_by_name['Map']
_EXPRESSION_LITERAL_MAP_KEYVALUE = _EXPRESSION_LITERAL_MAP.nested_types_by_name['KeyValue']
_EXPRESSION_LITERAL_INTERVALYEARTOMONTH = _EXPRESSION_LITERAL.nested_types_by_name['IntervalYearToMonth']
_EXPRESSION_LITERAL_INTERVALDAYTOSECOND = _EXPRESSION_LITERAL.nested_types_by_name['IntervalDayToSecond']
_EXPRESSION_LITERAL_STRUCT = _EXPRESSION_LITERAL.nested_types_by_name['Struct']
_EXPRESSION_LITERAL_LIST = _EXPRESSION_LITERAL.nested_types_by_name['List']
_EXPRESSION_SCALARFUNCTION = _EXPRESSION.nested_types_by_name['ScalarFunction']
_EXPRESSION_WINDOWFUNCTION = _EXPRESSION.nested_types_by_name['WindowFunction']
_EXPRESSION_WINDOWFUNCTION_BOUND = _EXPRESSION_WINDOWFUNCTION.nested_types_by_name['Bound']
_EXPRESSION_WINDOWFUNCTION_BOUND_PRECEDING = _EXPRESSION_WINDOWFUNCTION_BOUND.nested_types_by_name['Preceding']
_EXPRESSION_WINDOWFUNCTION_BOUND_FOLLOWING = _EXPRESSION_WINDOWFUNCTION_BOUND.nested_types_by_name['Following']
_EXPRESSION_WINDOWFUNCTION_BOUND_CURRENTROW = _EXPRESSION_WINDOWFUNCTION_BOUND.nested_types_by_name['CurrentRow']
_EXPRESSION_WINDOWFUNCTION_BOUND_UNBOUNDED = _EXPRESSION_WINDOWFUNCTION_BOUND.nested_types_by_name['Unbounded']
_EXPRESSION_IFTHEN = _EXPRESSION.nested_types_by_name['IfThen']
_EXPRESSION_IFTHEN_IFCLAUSE = _EXPRESSION_IFTHEN.nested_types_by_name['IfClause']
_EXPRESSION_CAST = _EXPRESSION.nested_types_by_name['Cast']
_EXPRESSION_SWITCHEXPRESSION = _EXPRESSION.nested_types_by_name['SwitchExpression']
_EXPRESSION_SWITCHEXPRESSION_IFVALUE = _EXPRESSION_SWITCHEXPRESSION.nested_types_by_name['IfValue']
_EXPRESSION_SINGULARORLIST = _EXPRESSION.nested_types_by_name['SingularOrList']
_EXPRESSION_MULTIORLIST = _EXPRESSION.nested_types_by_name['MultiOrList']
_EXPRESSION_MULTIORLIST_RECORD = _EXPRESSION_MULTIORLIST.nested_types_by_name['Record']
_EXPRESSION_EMBEDDEDFUNCTION = _EXPRESSION.nested_types_by_name['EmbeddedFunction']
_EXPRESSION_EMBEDDEDFUNCTION_PYTHONPICKLEFUNCTION = _EXPRESSION_EMBEDDEDFUNCTION.nested_types_by_name['PythonPickleFunction']
_EXPRESSION_EMBEDDEDFUNCTION_WEBASSEMBLYFUNCTION = _EXPRESSION_EMBEDDEDFUNCTION.nested_types_by_name['WebAssemblyFunction']
_EXPRESSION_REFERENCESEGMENT = _EXPRESSION.nested_types_by_name['ReferenceSegment']
_EXPRESSION_REFERENCESEGMENT_MAPKEY = _EXPRESSION_REFERENCESEGMENT.nested_types_by_name['MapKey']
_EXPRESSION_REFERENCESEGMENT_STRUCTFIELD = _EXPRESSION_REFERENCESEGMENT.nested_types_by_name['StructField']
_EXPRESSION_REFERENCESEGMENT_LISTELEMENT = _EXPRESSION_REFERENCESEGMENT.nested_types_by_name['ListElement']
_EXPRESSION_MASKEXPRESSION = _EXPRESSION.nested_types_by_name['MaskExpression']
_EXPRESSION_MASKEXPRESSION_SELECT = _EXPRESSION_MASKEXPRESSION.nested_types_by_name['Select']
_EXPRESSION_MASKEXPRESSION_STRUCTSELECT = _EXPRESSION_MASKEXPRESSION.nested_types_by_name['StructSelect']
_EXPRESSION_MASKEXPRESSION_STRUCTITEM = _EXPRESSION_MASKEXPRESSION.nested_types_by_name['StructItem']
_EXPRESSION_MASKEXPRESSION_LISTSELECT = _EXPRESSION_MASKEXPRESSION.nested_types_by_name['ListSelect']
_EXPRESSION_MASKEXPRESSION_LISTSELECT_LISTSELECTITEM = _EXPRESSION_MASKEXPRESSION_LISTSELECT.nested_types_by_name['ListSelectItem']
_EXPRESSION_MASKEXPRESSION_LISTSELECT_LISTSELECTITEM_LISTELEMENT = _EXPRESSION_MASKEXPRESSION_LISTSELECT_LISTSELECTITEM.nested_types_by_name['ListElement']
_EXPRESSION_MASKEXPRESSION_LISTSELECT_LISTSELECTITEM_LISTSLICE = _EXPRESSION_MASKEXPRESSION_LISTSELECT_LISTSELECTITEM.nested_types_by_name['ListSlice']
_EXPRESSION_MASKEXPRESSION_MAPSELECT = _EXPRESSION_MASKEXPRESSION.nested_types_by_name['MapSelect']
_EXPRESSION_MASKEXPRESSION_MAPSELECT_MAPKEY = _EXPRESSION_MASKEXPRESSION_MAPSELECT.nested_types_by_name['MapKey']
_EXPRESSION_MASKEXPRESSION_MAPSELECT_MAPKEYEXPRESSION = _EXPRESSION_MASKEXPRESSION_MAPSELECT.nested_types_by_name['MapKeyExpression']
_EXPRESSION_FIELDREFERENCE = _EXPRESSION.nested_types_by_name['FieldReference']
_EXPRESSION_FIELDREFERENCE_ROOTREFERENCE = _EXPRESSION_FIELDREFERENCE.nested_types_by_name['RootReference']
_SORTFIELD = DESCRIPTOR.message_types_by_name['SortField']
_AGGREGATEFUNCTION = DESCRIPTOR.message_types_by_name['AggregateFunction']
_SORTFIELD_SORTDIRECTION = _SORTFIELD.enum_types_by_name['SortDirection']
Expression = _reflection.GeneratedProtocolMessageType('Expression', (_message.Message,), {'Enum': _reflection.GeneratedProtocolMessageType('Enum', (_message.Message,), {'Empty': _reflection.GeneratedProtocolMessageType('Empty', (_message.Message,), {'DESCRIPTOR': _EXPRESSION_ENUM_EMPTY, '__module__': 'substrait.expression_pb2'}), 'DESCRIPTOR': _EXPRESSION_ENUM, '__module__': 'substrait.expression_pb2'}), 'Literal': _reflection.GeneratedProtocolMessageType('Literal', (_message.Message,), {'VarChar': _reflection.GeneratedProtocolMessageType('VarChar', (_message.Message,), {'DESCRIPTOR': _EXPRESSION_LITERAL_VARCHAR, '__module__': 'substrait.expression_pb2'}), 'Decimal': _reflection.GeneratedProtocolMessageType('Decimal', (_message.Message,), {'DESCRIPTOR': _EXPRESSION_LITERAL_DECIMAL, '__module__': 'substrait.expression_pb2'}), 'Map': _reflection.GeneratedProtocolMessageType('Map', (_message.Message,), {'KeyValue': _reflection.GeneratedProtocolMessageType('KeyValue', (_message.Message,), {'DESCRIPTOR': _EXPRESSION_LITERAL_MAP_KEYVALUE, '__module__': 'substrait.expression_pb2'}), 'DESCRIPTOR': _EXPRESSION_LITERAL_MAP, '__module__': 'substrait.expression_pb2'}), 'IntervalYearToMonth': _reflection.GeneratedProtocolMessageType('IntervalYearToMonth', (_message.Message,), {'DESCRIPTOR': _EXPRESSION_LITERAL_INTERVALYEARTOMONTH, '__module__': 'substrait.expression_pb2'}), 'IntervalDayToSecond': _reflection.GeneratedProtocolMessageType('IntervalDayToSecond', (_message.Message,), {'DESCRIPTOR': _EXPRESSION_LITERAL_INTERVALDAYTOSECOND, '__module__': 'substrait.expression_pb2'}), 'Struct': _reflection.GeneratedProtocolMessageType('Struct', (_message.Message,), {'DESCRIPTOR': _EXPRESSION_LITERAL_STRUCT, '__module__': 'substrait.expression_pb2'}), 'List': _reflection.GeneratedProtocolMessageType('List', (_message.Message,), {'DESCRIPTOR': _EXPRESSION_LITERAL_LIST, '__module__': 'substrait.expression_pb2'}), 'DESCRIPTOR': _EXPRESSION_LITERAL, '__module__': 'substrait.expression_pb2'}), 'ScalarFunction': _reflection.GeneratedProtocolMessageType('ScalarFunction', (_message.Message,), {'DESCRIPTOR': _EXPRESSION_SCALARFUNCTION, '__module__': 'substrait.expression_pb2'}), 'WindowFunction': _reflection.GeneratedProtocolMessageType('WindowFunction', (_message.Message,), {'Bound': _reflection.GeneratedProtocolMessageType('Bound', (_message.Message,), {'Preceding': _reflection.GeneratedProtocolMessageType('Preceding', (_message.Message,), {'DESCRIPTOR': _EXPRESSION_WINDOWFUNCTION_BOUND_PRECEDING, '__module__': 'substrait.expression_pb2'}), 'Following': _reflection.GeneratedProtocolMessageType('Following', (_message.Message,), {'DESCRIPTOR': _EXPRESSION_WINDOWFUNCTION_BOUND_FOLLOWING, '__module__': 'substrait.expression_pb2'}), 'CurrentRow': _reflection.GeneratedProtocolMessageType('CurrentRow', (_message.Message,), {'DESCRIPTOR': _EXPRESSION_WINDOWFUNCTION_BOUND_CURRENTROW, '__module__': 'substrait.expression_pb2'}), 'Unbounded': _reflection.GeneratedProtocolMessageType('Unbounded', (_message.Message,), {'DESCRIPTOR': _EXPRESSION_WINDOWFUNCTION_BOUND_UNBOUNDED, '__module__': 'substrait.expression_pb2'}), 'DESCRIPTOR': _EXPRESSION_WINDOWFUNCTION_BOUND, '__module__': 'substrait.expression_pb2'}), 'DESCRIPTOR': _EXPRESSION_WINDOWFUNCTION, '__module__': 'substrait.expression_pb2'}), 'IfThen': _reflection.GeneratedProtocolMessageType('IfThen', (_message.Message,), {'IfClause': _reflection.GeneratedProtocolMessageType('IfClause', (_message.Message,), {'DESCRIPTOR': _EXPRESSION_IFTHEN_IFCLAUSE, '__module__': 'substrait.expression_pb2'}), 'DESCRIPTOR': _EXPRESSION_IFTHEN, '__module__': 'substrait.expression_pb2'}), 'Cast': _reflection.GeneratedProtocolMessageType('Cast', (_message.Message,), {'DESCRIPTOR': _EXPRESSION_CAST, '__module__': 'substrait.expression_pb2'}), 'SwitchExpression': _reflection.GeneratedProtocolMessageType('SwitchExpression', (_message.Message,), {'IfValue': _reflection.GeneratedProtocolMessageType('IfValue', (_message.Message,), {'DESCRIPTOR': _EXPRESSION_SWITCHEXPRESSION_IFVALUE, '__module__': 'substrait.expression_pb2'}), 'DESCRIPTOR': _EXPRESSION_SWITCHEXPRESSION, '__module__': 'substrait.expression_pb2'}), 'SingularOrList': _reflection.GeneratedProtocolMessageType('SingularOrList', (_message.Message,), {'DESCRIPTOR': _EXPRESSION_SINGULARORLIST, '__module__': 'substrait.expression_pb2'}), 'MultiOrList': _reflection.GeneratedProtocolMessageType('MultiOrList', (_message.Message,), {'Record': _reflection.GeneratedProtocolMessageType('Record', (_message.Message,), {'DESCRIPTOR': _EXPRESSION_MULTIORLIST_RECORD, '__module__': 'substrait.expression_pb2'}), 'DESCRIPTOR': _EXPRESSION_MULTIORLIST, '__module__': 'substrait.expression_pb2'}), 'EmbeddedFunction': _reflection.GeneratedProtocolMessageType('EmbeddedFunction', (_message.Message,), {'PythonPickleFunction': _reflection.GeneratedProtocolMessageType('PythonPickleFunction', (_message.Message,), {'DESCRIPTOR': _EXPRESSION_EMBEDDEDFUNCTION_PYTHONPICKLEFUNCTION, '__module__': 'substrait.expression_pb2'}), 'WebAssemblyFunction': _reflection.GeneratedProtocolMessageType('WebAssemblyFunction', (_message.Message,), {'DESCRIPTOR': _EXPRESSION_EMBEDDEDFUNCTION_WEBASSEMBLYFUNCTION, '__module__': 'substrait.expression_pb2'}), 'DESCRIPTOR': _EXPRESSION_EMBEDDEDFUNCTION, '__module__': 'substrait.expression_pb2'}), 'ReferenceSegment': _reflection.GeneratedProtocolMessageType('ReferenceSegment', (_message.Message,), {'MapKey': _reflection.GeneratedProtocolMessageType('MapKey', (_message.Message,), {'DESCRIPTOR': _EXPRESSION_REFERENCESEGMENT_MAPKEY, '__module__': 'substrait.expression_pb2'}), 'StructField': _reflection.GeneratedProtocolMessageType('StructField', (_message.Message,), {'DESCRIPTOR': _EXPRESSION_REFERENCESEGMENT_STRUCTFIELD, '__module__': 'substrait.expression_pb2'}), 'ListElement': _reflection.GeneratedProtocolMessageType('ListElement', (_message.Message,), {'DESCRIPTOR': _EXPRESSION_REFERENCESEGMENT_LISTELEMENT, '__module__': 'substrait.expression_pb2'}), 'DESCRIPTOR': _EXPRESSION_REFERENCESEGMENT, '__module__': 'substrait.expression_pb2'}), 'MaskExpression': _reflection.GeneratedProtocolMessageType('MaskExpression', (_message.Message,), {'Select': _reflection.GeneratedProtocolMessageType('Select', (_message.Message,), {'DESCRIPTOR': _EXPRESSION_MASKEXPRESSION_SELECT, '__module__': 'substrait.expression_pb2'}), 'StructSelect': _reflection.GeneratedProtocolMessageType('StructSelect', (_message.Message,), {'DESCRIPTOR': _EXPRESSION_MASKEXPRESSION_STRUCTSELECT, '__module__': 'substrait.expression_pb2'}), 'StructItem': _reflection.GeneratedProtocolMessageType('StructItem', (_message.Message,), {'DESCRIPTOR': _EXPRESSION_MASKEXPRESSION_STRUCTITEM, '__module__': 'substrait.expression_pb2'}), 'ListSelect': _reflection.GeneratedProtocolMessageType('ListSelect', (_message.Message,), {'ListSelectItem': _reflection.GeneratedProtocolMessageType('ListSelectItem', (_message.Message,), {'ListElement': _reflection.GeneratedProtocolMessageType('ListElement', (_message.Message,), {'DESCRIPTOR': _EXPRESSION_MASKEXPRESSION_LISTSELECT_LISTSELECTITEM_LISTELEMENT, '__module__': 'substrait.expression_pb2'}), 'ListSlice': _reflection.GeneratedProtocolMessageType('ListSlice', (_message.Message,), {'DESCRIPTOR': _EXPRESSION_MASKEXPRESSION_LISTSELECT_LISTSELECTITEM_LISTSLICE, '__module__': 'substrait.expression_pb2'}), 'DESCRIPTOR': _EXPRESSION_MASKEXPRESSION_LISTSELECT_LISTSELECTITEM, '__module__': 'substrait.expression_pb2'}), 'DESCRIPTOR': _EXPRESSION_MASKEXPRESSION_LISTSELECT, '__module__': 'substrait.expression_pb2'}), 'MapSelect': _reflection.GeneratedProtocolMessageType('MapSelect', (_message.Message,), {'MapKey': _reflection.GeneratedProtocolMessageType('MapKey', (_message.Message,), {'DESCRIPTOR': _EXPRESSION_MASKEXPRESSION_MAPSELECT_MAPKEY, '__module__': 'substrait.expression_pb2'}), 'MapKeyExpression': _reflection.GeneratedProtocolMessageType('MapKeyExpression', (_message.Message,), {'DESCRIPTOR': _EXPRESSION_MASKEXPRESSION_MAPSELECT_MAPKEYEXPRESSION, '__module__': 'substrait.expression_pb2'}), 'DESCRIPTOR': _EXPRESSION_MASKEXPRESSION_MAPSELECT, '__module__': 'substrait.expression_pb2'}), 'DESCRIPTOR': _EXPRESSION_MASKEXPRESSION, '__module__': 'substrait.expression_pb2'}), 'FieldReference': _reflection.GeneratedProtocolMessageType('FieldReference', (_message.Message,), {'RootReference': _reflection.GeneratedProtocolMessageType('RootReference', (_message.Message,), {'DESCRIPTOR': _EXPRESSION_FIELDREFERENCE_ROOTREFERENCE, '__module__': 'substrait.expression_pb2'}), 'DESCRIPTOR': _EXPRESSION_FIELDREFERENCE, '__module__': 'substrait.expression_pb2'}), 'DESCRIPTOR': _EXPRESSION, '__module__': 'substrait.expression_pb2'})
_sym_db.RegisterMessage(Expression)
_sym_db.RegisterMessage(Expression.Enum)
_sym_db.RegisterMessage(Expression.Enum.Empty)
_sym_db.RegisterMessage(Expression.Literal)
_sym_db.RegisterMessage(Expression.Literal.VarChar)
_sym_db.RegisterMessage(Expression.Literal.Decimal)
_sym_db.RegisterMessage(Expression.Literal.Map)
_sym_db.RegisterMessage(Expression.Literal.Map.KeyValue)
_sym_db.RegisterMessage(Expression.Literal.IntervalYearToMonth)
_sym_db.RegisterMessage(Expression.Literal.IntervalDayToSecond)
_sym_db.RegisterMessage(Expression.Literal.Struct)
_sym_db.RegisterMessage(Expression.Literal.List)
_sym_db.RegisterMessage(Expression.ScalarFunction)
_sym_db.RegisterMessage(Expression.WindowFunction)
_sym_db.RegisterMessage(Expression.WindowFunction.Bound)
_sym_db.RegisterMessage(Expression.WindowFunction.Bound.Preceding)
_sym_db.RegisterMessage(Expression.WindowFunction.Bound.Following)
_sym_db.RegisterMessage(Expression.WindowFunction.Bound.CurrentRow)
_sym_db.RegisterMessage(Expression.WindowFunction.Bound.Unbounded)
_sym_db.RegisterMessage(Expression.IfThen)
_sym_db.RegisterMessage(Expression.IfThen.IfClause)
_sym_db.RegisterMessage(Expression.Cast)
_sym_db.RegisterMessage(Expression.SwitchExpression)
_sym_db.RegisterMessage(Expression.SwitchExpression.IfValue)
_sym_db.RegisterMessage(Expression.SingularOrList)
_sym_db.RegisterMessage(Expression.MultiOrList)
_sym_db.RegisterMessage(Expression.MultiOrList.Record)
_sym_db.RegisterMessage(Expression.EmbeddedFunction)
_sym_db.RegisterMessage(Expression.EmbeddedFunction.PythonPickleFunction)
_sym_db.RegisterMessage(Expression.EmbeddedFunction.WebAssemblyFunction)
_sym_db.RegisterMessage(Expression.ReferenceSegment)
_sym_db.RegisterMessage(Expression.ReferenceSegment.MapKey)
_sym_db.RegisterMessage(Expression.ReferenceSegment.StructField)
_sym_db.RegisterMessage(Expression.ReferenceSegment.ListElement)
_sym_db.RegisterMessage(Expression.MaskExpression)
_sym_db.RegisterMessage(Expression.MaskExpression.Select)
_sym_db.RegisterMessage(Expression.MaskExpression.StructSelect)
_sym_db.RegisterMessage(Expression.MaskExpression.StructItem)
_sym_db.RegisterMessage(Expression.MaskExpression.ListSelect)
_sym_db.RegisterMessage(Expression.MaskExpression.ListSelect.ListSelectItem)
_sym_db.RegisterMessage(Expression.MaskExpression.ListSelect.ListSelectItem.ListElement)
_sym_db.RegisterMessage(Expression.MaskExpression.ListSelect.ListSelectItem.ListSlice)
_sym_db.RegisterMessage(Expression.MaskExpression.MapSelect)
_sym_db.RegisterMessage(Expression.MaskExpression.MapSelect.MapKey)
_sym_db.RegisterMessage(Expression.MaskExpression.MapSelect.MapKeyExpression)
_sym_db.RegisterMessage(Expression.FieldReference)
_sym_db.RegisterMessage(Expression.FieldReference.RootReference)
SortField = _reflection.GeneratedProtocolMessageType('SortField', (_message.Message,), {'DESCRIPTOR': _SORTFIELD, '__module__': 'substrait.expression_pb2'})
_sym_db.RegisterMessage(SortField)
AggregateFunction = _reflection.GeneratedProtocolMessageType('AggregateFunction', (_message.Message,), {'DESCRIPTOR': _AGGREGATEFUNCTION, '__module__': 'substrait.expression_pb2'})
_sym_db.RegisterMessage(AggregateFunction)
if _descriptor._USE_C_DESCRIPTORS == False:
    DESCRIPTOR._options = None
    DESCRIPTOR._serialized_options = b'\n\x12io.substrait.protoP\x01\xaa\x02\x12Substrait.Protobuf'
    _AGGREGATIONPHASE._serialized_start = 8237
    _AGGREGATIONPHASE._serialized_end = 8476
    _EXPRESSION._serialized_start = 64
    _EXPRESSION._serialized_end = 7545
    _EXPRESSION_ENUM._serialized_start = 769
    _EXPRESSION_ENUM._serialized_end = 899
    _EXPRESSION_ENUM_EMPTY._serialized_start = 879
    _EXPRESSION_ENUM_EMPTY._serialized_end = 886
    _EXPRESSION_LITERAL._serialized_start = 902
    _EXPRESSION_LITERAL._serialized_end = 2637
    _EXPRESSION_LITERAL_VARCHAR._serialized_start = 2018
    _EXPRESSION_LITERAL_VARCHAR._serialized_end = 2073
    _EXPRESSION_LITERAL_DECIMAL._serialized_start = 2075
    _EXPRESSION_LITERAL_DECIMAL._serialized_end = 2158
    _EXPRESSION_LITERAL_MAP._serialized_start = 2161
    _EXPRESSION_LITERAL_MAP._serialized_end = 2355
    _EXPRESSION_LITERAL_MAP_KEYVALUE._serialized_start = 2243
    _EXPRESSION_LITERAL_MAP_KEYVALUE._serialized_end = 2355
    _EXPRESSION_LITERAL_INTERVALYEARTOMONTH._serialized_start = 2357
    _EXPRESSION_LITERAL_INTERVALYEARTOMONTH._serialized_end = 2424
    _EXPRESSION_LITERAL_INTERVALDAYTOSECOND._serialized_start = 2426
    _EXPRESSION_LITERAL_INTERVALDAYTOSECOND._serialized_end = 2493
    _EXPRESSION_LITERAL_STRUCT._serialized_start = 2495
    _EXPRESSION_LITERAL_STRUCT._serialized_end = 2558
    _EXPRESSION_LITERAL_LIST._serialized_start = 2560
    _EXPRESSION_LITERAL_LIST._serialized_end = 2621
    _EXPRESSION_SCALARFUNCTION._serialized_start = 2640
    _EXPRESSION_SCALARFUNCTION._serialized_end = 2796
    _EXPRESSION_WINDOWFUNCTION._serialized_start = 2799
    _EXPRESSION_WINDOWFUNCTION._serialized_end = 3726
    _EXPRESSION_WINDOWFUNCTION_BOUND._serialized_start = 3262
    _EXPRESSION_WINDOWFUNCTION_BOUND._serialized_end = 3726
    _EXPRESSION_WINDOWFUNCTION_BOUND_PRECEDING._serialized_start = 3619
    _EXPRESSION_WINDOWFUNCTION_BOUND_PRECEDING._serialized_end = 3654
    _EXPRESSION_WINDOWFUNCTION_BOUND_FOLLOWING._serialized_start = 3656
    _EXPRESSION_WINDOWFUNCTION_BOUND_FOLLOWING._serialized_end = 3691
    _EXPRESSION_WINDOWFUNCTION_BOUND_CURRENTROW._serialized_start = 3693
    _EXPRESSION_WINDOWFUNCTION_BOUND_CURRENTROW._serialized_end = 3705
    _EXPRESSION_WINDOWFUNCTION_BOUND_UNBOUNDED._serialized_start = 3707
    _EXPRESSION_WINDOWFUNCTION_BOUND_UNBOUNDED._serialized_end = 3718
    _EXPRESSION_IFTHEN._serialized_start = 3729
    _EXPRESSION_IFTHEN._serialized_end = 3931
    _EXPRESSION_IFTHEN_IFCLAUSE._serialized_start = 3839
    _EXPRESSION_IFTHEN_IFCLAUSE._serialized_end = 3931
    _EXPRESSION_CAST._serialized_start = 3933
    _EXPRESSION_CAST._serialized_end = 4021
    _EXPRESSION_SWITCHEXPRESSION._serialized_start = 4024
    _EXPRESSION_SWITCHEXPRESSION._serialized_end = 4252
    _EXPRESSION_SWITCHEXPRESSION_IFVALUE._serialized_start = 4153
    _EXPRESSION_SWITCHEXPRESSION_IFVALUE._serialized_end = 4252
    _EXPRESSION_SINGULARORLIST._serialized_start = 4254
    _EXPRESSION_SINGULARORLIST._serialized_end = 4364
    _EXPRESSION_MULTIORLIST._serialized_start = 4367
    _EXPRESSION_MULTIORLIST._serialized_end = 4550
    _EXPRESSION_MULTIORLIST_RECORD._serialized_start = 4495
    _EXPRESSION_MULTIORLIST_RECORD._serialized_end = 4550
    _EXPRESSION_EMBEDDEDFUNCTION._serialized_start = 4553
    _EXPRESSION_EMBEDDEDFUNCTION._serialized_end = 5084
    _EXPRESSION_EMBEDDEDFUNCTION_PYTHONPICKLEFUNCTION._serialized_start = 4907
    _EXPRESSION_EMBEDDEDFUNCTION_PYTHONPICKLEFUNCTION._serialized_end = 4993
    _EXPRESSION_EMBEDDEDFUNCTION_WEBASSEMBLYFUNCTION._serialized_start = 4995
    _EXPRESSION_EMBEDDEDFUNCTION_WEBASSEMBLYFUNCTION._serialized_end = 5076
    _EXPRESSION_REFERENCESEGMENT._serialized_start = 5087
    _EXPRESSION_REFERENCESEGMENT._serialized_end = 5703
    _EXPRESSION_REFERENCESEGMENT_MAPKEY._serialized_start = 5359
    _EXPRESSION_REFERENCESEGMENT_MAPKEY._serialized_end = 5485
    _EXPRESSION_REFERENCESEGMENT_STRUCTFIELD._serialized_start = 5487
    _EXPRESSION_REFERENCESEGMENT_STRUCTFIELD._serialized_end = 5584
    _EXPRESSION_REFERENCESEGMENT_LISTELEMENT._serialized_start = 5586
    _EXPRESSION_REFERENCESEGMENT_LISTELEMENT._serialized_end = 5685
    _EXPRESSION_MASKEXPRESSION._serialized_start = 5706
    _EXPRESSION_MASKEXPRESSION._serialized_end = 7148
    _EXPRESSION_MASKEXPRESSION_SELECT._serialized_start = 5858
    _EXPRESSION_MASKEXPRESSION_SELECT._serialized_end = 6090
    _EXPRESSION_MASKEXPRESSION_STRUCTSELECT._serialized_start = 6092
    _EXPRESSION_MASKEXPRESSION_STRUCTSELECT._serialized_end = 6190
    _EXPRESSION_MASKEXPRESSION_STRUCTITEM._serialized_start = 6192
    _EXPRESSION_MASKEXPRESSION_STRUCTITEM._serialized_end = 6293
    _EXPRESSION_MASKEXPRESSION_LISTSELECT._serialized_start = 6296
    _EXPRESSION_MASKEXPRESSION_LISTSELECT._serialized_end = 6782
    _EXPRESSION_MASKEXPRESSION_LISTSELECT_LISTSELECTITEM._serialized_start = 6472
    _EXPRESSION_MASKEXPRESSION_LISTSELECT_LISTSELECTITEM._serialized_end = 6782
    _EXPRESSION_MASKEXPRESSION_LISTSELECT_LISTSELECTITEM_LISTELEMENT._serialized_start = 6686
    _EXPRESSION_MASKEXPRESSION_LISTSELECT_LISTSELECTITEM_LISTELEMENT._serialized_end = 6721
    _EXPRESSION_MASKEXPRESSION_LISTSELECT_LISTSELECTITEM_LISTSLICE._serialized_start = 6723
    _EXPRESSION_MASKEXPRESSION_LISTSELECT_LISTSELECTITEM_LISTSLICE._serialized_end = 6774
    _EXPRESSION_MASKEXPRESSION_MAPSELECT._serialized_start = 6785
    _EXPRESSION_MASKEXPRESSION_MAPSELECT._serialized_end = 7148
    _EXPRESSION_MASKEXPRESSION_MAPSELECT_MAPKEY._serialized_start = 7039
    _EXPRESSION_MASKEXPRESSION_MAPSELECT_MAPKEY._serialized_end = 7072
    _EXPRESSION_MASKEXPRESSION_MAPSELECT_MAPKEYEXPRESSION._serialized_start = 7074
    _EXPRESSION_MASKEXPRESSION_MAPSELECT_MAPKEYEXPRESSION._serialized_end = 7138
    _EXPRESSION_FIELDREFERENCE._serialized_start = 7151
    _EXPRESSION_FIELDREFERENCE._serialized_end = 7533
    _EXPRESSION_FIELDREFERENCE_ROOTREFERENCE._serialized_start = 7487
    _EXPRESSION_FIELDREFERENCE_ROOTREFERENCE._serialized_end = 7502
    _SORTFIELD._serialized_start = 7548
    _SORTFIELD._serialized_end = 7977
    _SORTFIELD_SORTDIRECTION._serialized_start = 7743
    _SORTFIELD_SORTDIRECTION._serialized_end = 7964
    _AGGREGATEFUNCTION._serialized_start = 7980
    _AGGREGATEFUNCTION._serialized_end = 8234