"""Generated protocol buffer code."""
from google.protobuf.internal import enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
_sym_db = _symbol_database.Default()
from ..substrait import type_pb2 as substrait_dot_type__pb2
from ..substrait.extensions import extensions_pb2 as substrait_dot_extensions_dot_extensions__pb2
from google.protobuf import any_pb2 as google_dot_protobuf_dot_any__pb2
DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x17substrait/algebra.proto\x12\tsubstrait\x1a\x14substrait/type.proto\x1a%substrait/extensions/extensions.proto\x1a\x19google/protobuf/any.proto"\xb2\x06\n\tRelCommon\x125\n\x06direct\x18\x01 \x01(\x0b2\x1b.substrait.RelCommon.DirectH\x00R\x06direct\x12/\n\x04emit\x18\x02 \x01(\x0b2\x19.substrait.RelCommon.EmitH\x00R\x04emit\x12-\n\x04hint\x18\x03 \x01(\x0b2\x19.substrait.RelCommon.HintR\x04hint\x12V\n\x12advanced_extension\x18\x04 \x01(\x0b2\'.substrait.extensions.AdvancedExtensionR\x11advancedExtension\x1a\x08\n\x06Direct\x1a-\n\x04Emit\x12%\n\x0eoutput_mapping\x18\x01 \x03(\x05R\routputMapping\x1a\xef\x03\n\x04Hint\x125\n\x05stats\x18\x01 \x01(\x0b2\x1f.substrait.RelCommon.Hint.StatsR\x05stats\x12K\n\nconstraint\x18\x02 \x01(\x0b2+.substrait.RelCommon.Hint.RuntimeConstraintR\nconstraint\x12V\n\x12advanced_extension\x18\n \x01(\x0b2\'.substrait.extensions.AdvancedExtensionR\x11advancedExtension\x1a\x9d\x01\n\x05Stats\x12\x1b\n\trow_count\x18\x01 \x01(\x01R\x08rowCount\x12\x1f\n\x0brecord_size\x18\x02 \x01(\x01R\nrecordSize\x12V\n\x12advanced_extension\x18\n \x01(\x0b2\'.substrait.extensions.AdvancedExtensionR\x11advancedExtension\x1ak\n\x11RuntimeConstraint\x12V\n\x12advanced_extension\x18\n \x01(\x0b2\'.substrait.extensions.AdvancedExtensionR\x11advancedExtensionB\x0b\n\temit_kind"\x9d\x0b\n\x07ReadRel\x12,\n\x06common\x18\x01 \x01(\x0b2\x14.substrait.RelCommonR\x06common\x127\n\x0bbase_schema\x18\x02 \x01(\x0b2\x16.substrait.NamedStructR\nbaseSchema\x12-\n\x06filter\x18\x03 \x01(\x0b2\x15.substrait.ExpressionR\x06filter\x12D\n\nprojection\x18\x04 \x01(\x0b2$.substrait.Expression.MaskExpressionR\nprojection\x12V\n\x12advanced_extension\x18\n \x01(\x0b2\'.substrait.extensions.AdvancedExtensionR\x11advancedExtension\x12F\n\rvirtual_table\x18\x05 \x01(\x0b2\x1f.substrait.ReadRel.VirtualTableH\x00R\x0cvirtualTable\x12@\n\x0blocal_files\x18\x06 \x01(\x0b2\x1d.substrait.ReadRel.LocalFilesH\x00R\nlocalFiles\x12@\n\x0bnamed_table\x18\x07 \x01(\x0b2\x1d.substrait.ReadRel.NamedTableH\x00R\nnamedTable\x12L\n\x0fextension_table\x18\x08 \x01(\x0b2!.substrait.ReadRel.ExtensionTableH\x00R\x0eextensionTable\x1az\n\nNamedTable\x12\x14\n\x05names\x18\x01 \x03(\tR\x05names\x12V\n\x12advanced_extension\x18\n \x01(\x0b2\'.substrait.extensions.AdvancedExtensionR\x11advancedExtension\x1aL\n\x0cVirtualTable\x12<\n\x06values\x18\x01 \x03(\x0b2$.substrait.Expression.Literal.StructR\x06values\x1a>\n\x0eExtensionTable\x12,\n\x06detail\x18\x01 \x01(\x0b2\x14.google.protobuf.AnyR\x06detail\x1a\xac\x04\n\nLocalFiles\x12?\n\x05items\x18\x01 \x03(\x0b2).substrait.ReadRel.LocalFiles.FileOrFilesR\x05items\x12V\n\x12advanced_extension\x18\n \x01(\x0b2\'.substrait.extensions.AdvancedExtensionR\x11advancedExtension\x1a\x84\x03\n\x0bFileOrFiles\x12\x1b\n\x08uri_path\x18\x01 \x01(\tH\x00R\x07uriPath\x12$\n\ruri_path_glob\x18\x02 \x01(\tH\x00R\x0buriPathGlob\x12\x1b\n\x08uri_file\x18\x03 \x01(\tH\x00R\x07uriFile\x12\x1f\n\nuri_folder\x18\x04 \x01(\tH\x00R\turiFolder\x12L\n\x06format\x18\x05 \x01(\x0e24.substrait.ReadRel.LocalFiles.FileOrFiles.FileFormatR\x06format\x12\'\n\x0fpartition_index\x18\x06 \x01(\x04R\x0epartitionIndex\x12\x14\n\x05start\x18\x07 \x01(\x04R\x05start\x12\x16\n\x06length\x18\x08 \x01(\x04R\x06length"B\n\nFileFormat\x12\x1b\n\x17FILE_FORMAT_UNSPECIFIED\x10\x00\x12\x17\n\x13FILE_FORMAT_PARQUET\x10\x01B\x0b\n\tpath_typeB\x0b\n\tread_type"\xf1\x01\n\nProjectRel\x12,\n\x06common\x18\x01 \x01(\x0b2\x14.substrait.RelCommonR\x06common\x12$\n\x05input\x18\x02 \x01(\x0b2\x0e.substrait.RelR\x05input\x127\n\x0bexpressions\x18\x03 \x03(\x0b2\x15.substrait.ExpressionR\x0bexpressions\x12V\n\x12advanced_extension\x18\n \x01(\x0b2\'.substrait.extensions.AdvancedExtensionR\x11advancedExtension"\xbb\x04\n\x07JoinRel\x12,\n\x06common\x18\x01 \x01(\x0b2\x14.substrait.RelCommonR\x06common\x12"\n\x04left\x18\x02 \x01(\x0b2\x0e.substrait.RelR\x04left\x12$\n\x05right\x18\x03 \x01(\x0b2\x0e.substrait.RelR\x05right\x125\n\nexpression\x18\x04 \x01(\x0b2\x15.substrait.ExpressionR\nexpression\x12?\n\x10post_join_filter\x18\x05 \x01(\x0b2\x15.substrait.ExpressionR\x0epostJoinFilter\x12/\n\x04type\x18\x06 \x01(\x0e2\x1b.substrait.JoinRel.JoinTypeR\x04type\x12V\n\x12advanced_extension\x18\n \x01(\x0b2\'.substrait.extensions.AdvancedExtensionR\x11advancedExtension"\xb6\x01\n\x08JoinType\x12\x19\n\x15JOIN_TYPE_UNSPECIFIED\x10\x00\x12\x13\n\x0fJOIN_TYPE_INNER\x10\x01\x12\x13\n\x0fJOIN_TYPE_OUTER\x10\x02\x12\x12\n\x0eJOIN_TYPE_LEFT\x10\x03\x12\x13\n\x0fJOIN_TYPE_RIGHT\x10\x04\x12\x12\n\x0eJOIN_TYPE_SEMI\x10\x05\x12\x12\n\x0eJOIN_TYPE_ANTI\x10\x06\x12\x14\n\x10JOIN_TYPE_SINGLE\x10\x07"\xda\x01\n\x08CrossRel\x12,\n\x06common\x18\x01 \x01(\x0b2\x14.substrait.RelCommonR\x06common\x12"\n\x04left\x18\x02 \x01(\x0b2\x0e.substrait.RelR\x04left\x12$\n\x05right\x18\x03 \x01(\x0b2\x0e.substrait.RelR\x05right\x12V\n\x12advanced_extension\x18\n \x01(\x0b2\'.substrait.extensions.AdvancedExtensionR\x11advancedExtension"\xe4\x01\n\x08FetchRel\x12,\n\x06common\x18\x01 \x01(\x0b2\x14.substrait.RelCommonR\x06common\x12$\n\x05input\x18\x02 \x01(\x0b2\x0e.substrait.RelR\x05input\x12\x16\n\x06offset\x18\x03 \x01(\x03R\x06offset\x12\x14\n\x05count\x18\x04 \x01(\x03R\x05count\x12V\n\x12advanced_extension\x18\n \x01(\x0b2\'.substrait.extensions.AdvancedExtensionR\x11advancedExtension"\xff\x03\n\x0cAggregateRel\x12,\n\x06common\x18\x01 \x01(\x0b2\x14.substrait.RelCommonR\x06common\x12$\n\x05input\x18\x02 \x01(\x0b2\x0e.substrait.RelR\x05input\x12>\n\tgroupings\x18\x03 \x03(\x0b2 .substrait.AggregateRel.GroupingR\tgroupings\x12;\n\x08measures\x18\x04 \x03(\x0b2\x1f.substrait.AggregateRel.MeasureR\x08measures\x12V\n\x12advanced_extension\x18\n \x01(\x0b2\'.substrait.extensions.AdvancedExtensionR\x11advancedExtension\x1aT\n\x08Grouping\x12H\n\x14grouping_expressions\x18\x01 \x03(\x0b2\x15.substrait.ExpressionR\x13groupingExpressions\x1ap\n\x07Measure\x126\n\x07measure\x18\x01 \x01(\x0b2\x1c.substrait.AggregateFunctionR\x07measure\x12-\n\x06filter\x18\x02 \x01(\x0b2\x15.substrait.ExpressionR\x06filter"\xe1\x01\n\x07SortRel\x12,\n\x06common\x18\x01 \x01(\x0b2\x14.substrait.RelCommonR\x06common\x12$\n\x05input\x18\x02 \x01(\x0b2\x0e.substrait.RelR\x05input\x12*\n\x05sorts\x18\x03 \x03(\x0b2\x14.substrait.SortFieldR\x05sorts\x12V\n\x12advanced_extension\x18\n \x01(\x0b2\'.substrait.extensions.AdvancedExtensionR\x11advancedExtension"\xec\x01\n\tFilterRel\x12,\n\x06common\x18\x01 \x01(\x0b2\x14.substrait.RelCommonR\x06common\x12$\n\x05input\x18\x02 \x01(\x0b2\x0e.substrait.RelR\x05input\x123\n\tcondition\x18\x03 \x01(\x0b2\x15.substrait.ExpressionR\tcondition\x12V\n\x12advanced_extension\x18\n \x01(\x0b2\'.substrait.extensions.AdvancedExtensionR\x11advancedExtension"\xaa\x03\n\x06SetRel\x12,\n\x06common\x18\x01 \x01(\x0b2\x14.substrait.RelCommonR\x06common\x12&\n\x06inputs\x18\x02 \x03(\x0b2\x0e.substrait.RelR\x06inputs\x12\'\n\x02op\x18\x03 \x01(\x0e2\x17.substrait.SetRel.SetOpR\x02op\x12V\n\x12advanced_extension\x18\n \x01(\x0b2\'.substrait.extensions.AdvancedExtensionR\x11advancedExtension"\xc8\x01\n\x05SetOp\x12\x16\n\x12SET_OP_UNSPECIFIED\x10\x00\x12\x18\n\x14SET_OP_MINUS_PRIMARY\x10\x01\x12\x19\n\x15SET_OP_MINUS_MULTISET\x10\x02\x12\x1f\n\x1bSET_OP_INTERSECTION_PRIMARY\x10\x03\x12 \n\x1cSET_OP_INTERSECTION_MULTISET\x10\x04\x12\x19\n\x15SET_OP_UNION_DISTINCT\x10\x05\x12\x14\n\x10SET_OP_UNION_ALL\x10\x06"\x96\x01\n\x12ExtensionSingleRel\x12,\n\x06common\x18\x01 \x01(\x0b2\x14.substrait.RelCommonR\x06common\x12$\n\x05input\x18\x02 \x01(\x0b2\x0e.substrait.RelR\x05input\x12,\n\x06detail\x18\x03 \x01(\x0b2\x14.google.protobuf.AnyR\x06detail"n\n\x10ExtensionLeafRel\x12,\n\x06common\x18\x01 \x01(\x0b2\x14.substrait.RelCommonR\x06common\x12,\n\x06detail\x18\x02 \x01(\x0b2\x14.google.protobuf.AnyR\x06detail"\x97\x01\n\x11ExtensionMultiRel\x12,\n\x06common\x18\x01 \x01(\x0b2\x14.substrait.RelCommonR\x06common\x12&\n\x06inputs\x18\x02 \x03(\x0b2\x0e.substrait.RelR\x06inputs\x12,\n\x06detail\x18\x03 \x01(\x0b2\x14.google.protobuf.AnyR\x06detail"E\n\x07RelRoot\x12$\n\x05input\x18\x01 \x01(\x0b2\x0e.substrait.RelR\x05input\x12\x14\n\x05names\x18\x02 \x03(\tR\x05names"\x87\x05\n\x03Rel\x12(\n\x04read\x18\x01 \x01(\x0b2\x12.substrait.ReadRelH\x00R\x04read\x12.\n\x06filter\x18\x02 \x01(\x0b2\x14.substrait.FilterRelH\x00R\x06filter\x12+\n\x05fetch\x18\x03 \x01(\x0b2\x13.substrait.FetchRelH\x00R\x05fetch\x127\n\taggregate\x18\x04 \x01(\x0b2\x17.substrait.AggregateRelH\x00R\taggregate\x12(\n\x04sort\x18\x05 \x01(\x0b2\x12.substrait.SortRelH\x00R\x04sort\x12(\n\x04join\x18\x06 \x01(\x0b2\x12.substrait.JoinRelH\x00R\x04join\x121\n\x07project\x18\x07 \x01(\x0b2\x15.substrait.ProjectRelH\x00R\x07project\x12%\n\x03set\x18\x08 \x01(\x0b2\x11.substrait.SetRelH\x00R\x03set\x12J\n\x10extension_single\x18\t \x01(\x0b2\x1d.substrait.ExtensionSingleRelH\x00R\x0fextensionSingle\x12G\n\x0fextension_multi\x18\n \x01(\x0b2\x1c.substrait.ExtensionMultiRelH\x00R\x0eextensionMulti\x12D\n\x0eextension_leaf\x18\x0b \x01(\x0b2\x1b.substrait.ExtensionLeafRelH\x00R\rextensionLeaf\x12+\n\x05cross\x18\x0c \x01(\x0b2\x13.substrait.CrossRelH\x00R\x05crossB\n\n\x08rel_type"\x9eF\n\nExpression\x129\n\x07literal\x18\x01 \x01(\x0b2\x1d.substrait.Expression.LiteralH\x00R\x07literal\x12D\n\tselection\x18\x02 \x01(\x0b2$.substrait.Expression.FieldReferenceH\x00R\tselection\x12O\n\x0fscalar_function\x18\x03 \x01(\x0b2$.substrait.Expression.ScalarFunctionH\x00R\x0escalarFunction\x12O\n\x0fwindow_function\x18\x05 \x01(\x0b2$.substrait.Expression.WindowFunctionH\x00R\x0ewindowFunction\x127\n\x07if_then\x18\x06 \x01(\x0b2\x1c.substrait.Expression.IfThenH\x00R\x06ifThen\x12U\n\x11switch_expression\x18\x07 \x01(\x0b2&.substrait.Expression.SwitchExpressionH\x00R\x10switchExpression\x12P\n\x10singular_or_list\x18\x08 \x01(\x0b2$.substrait.Expression.SingularOrListH\x00R\x0esingularOrList\x12G\n\rmulti_or_list\x18\t \x01(\x0b2!.substrait.Expression.MultiOrListH\x00R\x0bmultiOrList\x120\n\x04enum\x18\n \x01(\x0b2\x1a.substrait.Expression.EnumH\x00R\x04enum\x120\n\x04cast\x18\x0b \x01(\x0b2\x1a.substrait.Expression.CastH\x00R\x04cast\x12<\n\x08subquery\x18\x0c \x01(\x0b2\x1e.substrait.Expression.SubqueryH\x00R\x08subquery\x1a\x82\x01\n\x04Enum\x12\x1e\n\tspecified\x18\x01 \x01(\tH\x00R\tspecified\x12D\n\x0bunspecified\x18\x02 \x01(\x0b2 .substrait.Expression.Enum.EmptyH\x00R\x0bunspecified\x1a\x07\n\x05EmptyB\x0b\n\tenum_kind\x1a\xc7\r\n\x07Literal\x12\x1a\n\x07boolean\x18\x01 \x01(\x08H\x00R\x07boolean\x12\x10\n\x02i8\x18\x02 \x01(\x05H\x00R\x02i8\x12\x12\n\x03i16\x18\x03 \x01(\x05H\x00R\x03i16\x12\x12\n\x03i32\x18\x05 \x01(\x05H\x00R\x03i32\x12\x12\n\x03i64\x18\x07 \x01(\x03H\x00R\x03i64\x12\x14\n\x04fp32\x18\n \x01(\x02H\x00R\x04fp32\x12\x14\n\x04fp64\x18\x0b \x01(\x01H\x00R\x04fp64\x12\x18\n\x06string\x18\x0c \x01(\tH\x00R\x06string\x12\x18\n\x06binary\x18\r \x01(\x0cH\x00R\x06binary\x12\x1e\n\ttimestamp\x18\x0e \x01(\x03H\x00R\ttimestamp\x12\x14\n\x04date\x18\x10 \x01(\x05H\x00R\x04date\x12\x14\n\x04time\x18\x11 \x01(\x03H\x00R\x04time\x12h\n\x16interval_year_to_month\x18\x13 \x01(\x0b21.substrait.Expression.Literal.IntervalYearToMonthH\x00R\x13intervalYearToMonth\x12h\n\x16interval_day_to_second\x18\x14 \x01(\x0b21.substrait.Expression.Literal.IntervalDayToSecondH\x00R\x13intervalDayToSecond\x12\x1f\n\nfixed_char\x18\x15 \x01(\tH\x00R\tfixedChar\x12B\n\x08var_char\x18\x16 \x01(\x0b2%.substrait.Expression.Literal.VarCharH\x00R\x07varChar\x12#\n\x0cfixed_binary\x18\x17 \x01(\x0cH\x00R\x0bfixedBinary\x12A\n\x07decimal\x18\x18 \x01(\x0b2%.substrait.Expression.Literal.DecimalH\x00R\x07decimal\x12>\n\x06struct\x18\x19 \x01(\x0b2$.substrait.Expression.Literal.StructH\x00R\x06struct\x125\n\x03map\x18\x1a \x01(\x0b2!.substrait.Expression.Literal.MapH\x00R\x03map\x12#\n\x0ctimestamp_tz\x18\x1b \x01(\x03H\x00R\x0btimestampTz\x12\x14\n\x04uuid\x18\x1c \x01(\x0cH\x00R\x04uuid\x12%\n\x04null\x18\x1d \x01(\x0b2\x0f.substrait.TypeH\x00R\x04null\x128\n\x04list\x18\x1e \x01(\x0b2".substrait.Expression.Literal.ListH\x00R\x04list\x125\n\nempty_list\x18\x1f \x01(\x0b2\x14.substrait.Type.ListH\x00R\temptyList\x122\n\tempty_map\x18  \x01(\x0b2\x13.substrait.Type.MapH\x00R\x08emptyMap\x12\x1a\n\x08nullable\x182 \x01(\x08R\x08nullable\x1a7\n\x07VarChar\x12\x14\n\x05value\x18\x01 \x01(\tR\x05value\x12\x16\n\x06length\x18\x02 \x01(\rR\x06length\x1aS\n\x07Decimal\x12\x14\n\x05value\x18\x01 \x01(\x0cR\x05value\x12\x1c\n\tprecision\x18\x02 \x01(\x05R\tprecision\x12\x14\n\x05scale\x18\x03 \x01(\x05R\x05scale\x1a\xc2\x01\n\x03Map\x12I\n\nkey_values\x18\x01 \x03(\x0b2*.substrait.Expression.Literal.Map.KeyValueR\tkeyValues\x1ap\n\x08KeyValue\x12/\n\x03key\x18\x01 \x01(\x0b2\x1d.substrait.Expression.LiteralR\x03key\x123\n\x05value\x18\x02 \x01(\x0b2\x1d.substrait.Expression.LiteralR\x05value\x1aC\n\x13IntervalYearToMonth\x12\x14\n\x05years\x18\x01 \x01(\x05R\x05years\x12\x16\n\x06months\x18\x02 \x01(\x05R\x06months\x1aC\n\x13IntervalDayToSecond\x12\x12\n\x04days\x18\x01 \x01(\x05R\x04days\x12\x18\n\x07seconds\x18\x02 \x01(\x05R\x07seconds\x1a?\n\x06Struct\x125\n\x06fields\x18\x01 \x03(\x0b2\x1d.substrait.Expression.LiteralR\x06fields\x1a=\n\x04List\x125\n\x06values\x18\x01 \x03(\x0b2\x1d.substrait.Expression.LiteralR\x06valuesB\x0e\n\x0cliteral_type\x1a\x9c\x01\n\x0eScalarFunction\x12-\n\x12function_reference\x18\x01 \x01(\rR\x11functionReference\x12)\n\x04args\x18\x02 \x03(\x0b2\x15.substrait.ExpressionR\x04args\x120\n\x0boutput_type\x18\x03 \x01(\x0b2\x0f.substrait.TypeR\noutputType\x1a\x9f\x07\n\x0eWindowFunction\x12-\n\x12function_reference\x18\x01 \x01(\rR\x11functionReference\x125\n\npartitions\x18\x02 \x03(\x0b2\x15.substrait.ExpressionR\npartitions\x12*\n\x05sorts\x18\x03 \x03(\x0b2\x14.substrait.SortFieldR\x05sorts\x12K\n\x0bupper_bound\x18\x04 \x01(\x0b2*.substrait.Expression.WindowFunction.BoundR\nupperBound\x12K\n\x0blower_bound\x18\x05 \x01(\x0b2*.substrait.Expression.WindowFunction.BoundR\nlowerBound\x121\n\x05phase\x18\x06 \x01(\x0e2\x1b.substrait.AggregationPhaseR\x05phase\x120\n\x0boutput_type\x18\x07 \x01(\x0b2\x0f.substrait.TypeR\noutputType\x12)\n\x04args\x18\x08 \x03(\x0b2\x15.substrait.ExpressionR\x04args\x1a\xd0\x03\n\x05Bound\x12T\n\tpreceding\x18\x01 \x01(\x0b24.substrait.Expression.WindowFunction.Bound.PrecedingH\x00R\tpreceding\x12T\n\tfollowing\x18\x02 \x01(\x0b24.substrait.Expression.WindowFunction.Bound.FollowingH\x00R\tfollowing\x12X\n\x0bcurrent_row\x18\x03 \x01(\x0b25.substrait.Expression.WindowFunction.Bound.CurrentRowH\x00R\ncurrentRow\x12T\n\tunbounded\x18\x04 \x01(\x0b24.substrait.Expression.WindowFunction.Bound.UnboundedH\x00R\tunbounded\x1a#\n\tPreceding\x12\x16\n\x06offset\x18\x01 \x01(\x03R\x06offset\x1a#\n\tFollowing\x12\x16\n\x06offset\x18\x01 \x01(\x03R\x06offset\x1a\x0c\n\nCurrentRow\x1a\x0b\n\tUnboundedB\x06\n\x04kind\x1a\xca\x01\n\x06IfThen\x127\n\x03ifs\x18\x01 \x03(\x0b2%.substrait.Expression.IfThen.IfClauseR\x03ifs\x12)\n\x04else\x18\x02 \x01(\x0b2\x15.substrait.ExpressionR\x04else\x1a\\\n\x08IfClause\x12%\n\x02if\x18\x01 \x01(\x0b2\x15.substrait.ExpressionR\x02if\x12)\n\x04then\x18\x02 \x01(\x0b2\x15.substrait.ExpressionR\x04then\x1aX\n\x04Cast\x12#\n\x04type\x18\x01 \x01(\x0b2\x0f.substrait.TypeR\x04type\x12+\n\x05input\x18\x02 \x01(\x0b2\x15.substrait.ExpressionR\x05input\x1a\xe4\x01\n\x10SwitchExpression\x12@\n\x03ifs\x18\x01 \x03(\x0b2..substrait.Expression.SwitchExpression.IfValueR\x03ifs\x12)\n\x04else\x18\x02 \x01(\x0b2\x15.substrait.ExpressionR\x04else\x1ac\n\x07IfValue\x12-\n\x02if\x18\x01 \x01(\x0b2\x1d.substrait.Expression.LiteralR\x02if\x12)\n\x04then\x18\x02 \x01(\x0b2\x15.substrait.ExpressionR\x04then\x1an\n\x0eSingularOrList\x12+\n\x05value\x18\x01 \x01(\x0b2\x15.substrait.ExpressionR\x05value\x12/\n\x07options\x18\x02 \x03(\x0b2\x15.substrait.ExpressionR\x07options\x1a\xb7\x01\n\x0bMultiOrList\x12+\n\x05value\x18\x01 \x03(\x0b2\x15.substrait.ExpressionR\x05value\x12B\n\x07options\x18\x02 \x03(\x0b2(.substrait.Expression.MultiOrList.RecordR\x07options\x1a7\n\x06Record\x12-\n\x06fields\x18\x01 \x03(\x0b2\x15.substrait.ExpressionR\x06fields\x1a\x93\x04\n\x10EmbeddedFunction\x123\n\targuments\x18\x01 \x03(\x0b2\x15.substrait.ExpressionR\targuments\x120\n\x0boutput_type\x18\x02 \x01(\x0b2\x0f.substrait.TypeR\noutputType\x12s\n\x16python_pickle_function\x18\x03 \x01(\x0b2;.substrait.Expression.EmbeddedFunction.PythonPickleFunctionH\x00R\x14pythonPickleFunction\x12p\n\x15web_assembly_function\x18\x04 \x01(\x0b2:.substrait.Expression.EmbeddedFunction.WebAssemblyFunctionH\x00R\x13webAssemblyFunction\x1aV\n\x14PythonPickleFunction\x12\x1a\n\x08function\x18\x01 \x01(\x0cR\x08function\x12"\n\x0cprerequisite\x18\x02 \x03(\tR\x0cprerequisite\x1aQ\n\x13WebAssemblyFunction\x12\x16\n\x06script\x18\x01 \x01(\x0cR\x06script\x12"\n\x0cprerequisite\x18\x02 \x03(\tR\x0cprerequisiteB\x06\n\x04kind\x1a\xe8\x04\n\x10ReferenceSegment\x12H\n\x07map_key\x18\x01 \x01(\x0b2-.substrait.Expression.ReferenceSegment.MapKeyH\x00R\x06mapKey\x12W\n\x0cstruct_field\x18\x02 \x01(\x0b22.substrait.Expression.ReferenceSegment.StructFieldH\x00R\x0bstructField\x12W\n\x0clist_element\x18\x03 \x01(\x0b22.substrait.Expression.ReferenceSegment.ListElementH\x00R\x0blistElement\x1a~\n\x06MapKey\x126\n\x07map_key\x18\x01 \x01(\x0b2\x1d.substrait.Expression.LiteralR\x06mapKey\x12<\n\x05child\x18\x02 \x01(\x0b2&.substrait.Expression.ReferenceSegmentR\x05child\x1aa\n\x0bStructField\x12\x14\n\x05field\x18\x01 \x01(\x05R\x05field\x12<\n\x05child\x18\x02 \x01(\x0b2&.substrait.Expression.ReferenceSegmentR\x05child\x1ac\n\x0bListElement\x12\x16\n\x06offset\x18\x01 \x01(\x05R\x06offset\x12<\n\x05child\x18\x02 \x01(\x0b2&.substrait.Expression.ReferenceSegmentR\x05childB\x10\n\x0ereference_type\x1a\xa2\x0b\n\x0eMaskExpression\x12I\n\x06select\x18\x01 \x01(\x0b21.substrait.Expression.MaskExpression.StructSelectR\x06select\x128\n\x18maintain_singular_struct\x18\x02 \x01(\x08R\x16maintainSingularStruct\x1a\xe8\x01\n\x06Select\x12K\n\x06struct\x18\x01 \x01(\x0b21.substrait.Expression.MaskExpression.StructSelectH\x00R\x06struct\x12E\n\x04list\x18\x02 \x01(\x0b2/.substrait.Expression.MaskExpression.ListSelectH\x00R\x04list\x12B\n\x03map\x18\x03 \x01(\x0b2..substrait.Expression.MaskExpression.MapSelectH\x00R\x03mapB\x06\n\x04type\x1ab\n\x0cStructSelect\x12R\n\x0cstruct_items\x18\x01 \x03(\x0b2/.substrait.Expression.MaskExpression.StructItemR\x0bstructItems\x1ae\n\nStructItem\x12\x14\n\x05field\x18\x01 \x01(\x05R\x05field\x12A\n\x05child\x18\x02 \x01(\x0b2+.substrait.Expression.MaskExpression.SelectR\x05child\x1a\xe6\x03\n\nListSelect\x12\\\n\tselection\x18\x01 \x03(\x0b2>.substrait.Expression.MaskExpression.ListSelect.ListSelectItemR\tselection\x12A\n\x05child\x18\x02 \x01(\x0b2+.substrait.Expression.MaskExpression.SelectR\x05child\x1a\xb6\x02\n\x0eListSelectItem\x12`\n\x04item\x18\x01 \x01(\x0b2J.substrait.Expression.MaskExpression.ListSelect.ListSelectItem.ListElementH\x00R\x04item\x12`\n\x05slice\x18\x02 \x01(\x0b2H.substrait.Expression.MaskExpression.ListSelect.ListSelectItem.ListSliceH\x00R\x05slice\x1a#\n\x0bListElement\x12\x14\n\x05field\x18\x01 \x01(\x05R\x05field\x1a3\n\tListSlice\x12\x14\n\x05start\x18\x01 \x01(\x05R\x05start\x12\x10\n\x03end\x18\x02 \x01(\x05R\x03endB\x06\n\x04type\x1a\xeb\x02\n\tMapSelect\x12I\n\x03key\x18\x01 \x01(\x0b25.substrait.Expression.MaskExpression.MapSelect.MapKeyH\x00R\x03key\x12a\n\nexpression\x18\x02 \x01(\x0b2?.substrait.Expression.MaskExpression.MapSelect.MapKeyExpressionH\x00R\nexpression\x12A\n\x05child\x18\x03 \x01(\x0b2+.substrait.Expression.MaskExpression.SelectR\x05child\x1a!\n\x06MapKey\x12\x17\n\x07map_key\x18\x01 \x01(\tR\x06mapKey\x1a@\n\x10MapKeyExpression\x12,\n\x12map_key_expression\x18\x01 \x01(\tR\x10mapKeyExpressionB\x08\n\x06select\x1a\x8d\x04\n\x0eFieldReference\x12S\n\x10direct_reference\x18\x01 \x01(\x0b2&.substrait.Expression.ReferenceSegmentH\x00R\x0fdirectReference\x12Q\n\x10masked_reference\x18\x02 \x01(\x0b2$.substrait.Expression.MaskExpressionH\x00R\x0fmaskedReference\x127\n\nexpression\x18\x03 \x01(\x0b2\x15.substrait.ExpressionH\x01R\nexpression\x12[\n\x0eroot_reference\x18\x04 \x01(\x0b22.substrait.Expression.FieldReference.RootReferenceH\x01R\rrootReference\x12^\n\x0fouter_reference\x18\x05 \x01(\x0b23.substrait.Expression.FieldReference.OuterReferenceH\x01R\x0eouterReference\x1a\x0f\n\rRootReference\x1a-\n\x0eOuterReference\x12\x1b\n\tsteps_out\x18\x01 \x01(\rR\x08stepsOutB\x10\n\x0ereference_typeB\x0b\n\troot_type\x1a\x95\n\n\x08Subquery\x12?\n\x06scalar\x18\x01 \x01(\x0b2%.substrait.Expression.Subquery.ScalarH\x00R\x06scalar\x12O\n\x0cin_predicate\x18\x02 \x01(\x0b2*.substrait.Expression.Subquery.InPredicateH\x00R\x0binPredicate\x12R\n\rset_predicate\x18\x03 \x01(\x0b2+.substrait.Expression.Subquery.SetPredicateH\x00R\x0csetPredicate\x12U\n\x0eset_comparison\x18\x04 \x01(\x0b2,.substrait.Expression.Subquery.SetComparisonH\x00R\rsetComparison\x1a.\n\x06Scalar\x12$\n\x05input\x18\x01 \x01(\x0b2\x0e.substrait.RelR\x05input\x1aj\n\x0bInPredicate\x12/\n\x07needles\x18\x01 \x03(\x0b2\x15.substrait.ExpressionR\x07needles\x12*\n\x08haystack\x18\x02 \x01(\x0b2\x0e.substrait.RelR\x08haystack\x1a\xf1\x01\n\x0cSetPredicate\x12Z\n\x0cpredicate_op\x18\x01 \x01(\x0e27.substrait.Expression.Subquery.SetPredicate.PredicateOpR\x0bpredicateOp\x12&\n\x06tuples\x18\x02 \x01(\x0b2\x0e.substrait.RelR\x06tuples"]\n\x0bPredicateOp\x12\x1c\n\x18PREDICATE_OP_UNSPECIFIED\x10\x00\x12\x17\n\x13PREDICATE_OP_EXISTS\x10\x01\x12\x17\n\x13PREDICATE_OP_UNIQUE\x10\x02\x1a\xaa\x04\n\rSetComparison\x12[\n\x0creduction_op\x18\x01 \x01(\x0e28.substrait.Expression.Subquery.SetComparison.ReductionOpR\x0breductionOp\x12^\n\rcomparison_op\x18\x02 \x01(\x0e29.substrait.Expression.Subquery.SetComparison.ComparisonOpR\x0ccomparisonOp\x12)\n\x04left\x18\x03 \x01(\x0b2\x15.substrait.ExpressionR\x04left\x12$\n\x05right\x18\x04 \x01(\x0b2\x0e.substrait.RelR\x05right"\xb1\x01\n\x0cComparisonOp\x12\x1d\n\x19COMPARISON_OP_UNSPECIFIED\x10\x00\x12\x14\n\x10COMPARISON_OP_EQ\x10\x01\x12\x14\n\x10COMPARISON_OP_NE\x10\x02\x12\x14\n\x10COMPARISON_OP_LT\x10\x03\x12\x14\n\x10COMPARISON_OP_GT\x10\x04\x12\x14\n\x10COMPARISON_OP_LE\x10\x05\x12\x14\n\x10COMPARISON_OP_GE\x10\x06"W\n\x0bReductionOp\x12\x1c\n\x18REDUCTION_OP_UNSPECIFIED\x10\x00\x12\x14\n\x10REDUCTION_OP_ANY\x10\x01\x12\x14\n\x10REDUCTION_OP_ALL\x10\x02B\x0f\n\rsubquery_typeB\n\n\x08rex_type"\xad\x03\n\tSortField\x12)\n\x04expr\x18\x01 \x01(\x0b2\x15.substrait.ExpressionR\x04expr\x12B\n\tdirection\x18\x02 \x01(\x0e2".substrait.SortField.SortDirectionH\x00R\tdirection\x12D\n\x1dcomparison_function_reference\x18\x03 \x01(\rH\x00R\x1bcomparisonFunctionReference"\xdd\x01\n\rSortDirection\x12\x1e\n\x1aSORT_DIRECTION_UNSPECIFIED\x10\x00\x12"\n\x1eSORT_DIRECTION_ASC_NULLS_FIRST\x10\x01\x12!\n\x1dSORT_DIRECTION_ASC_NULLS_LAST\x10\x02\x12#\n\x1fSORT_DIRECTION_DESC_NULLS_FIRST\x10\x03\x12"\n\x1eSORT_DIRECTION_DESC_NULLS_LAST\x10\x04\x12\x1c\n\x18SORT_DIRECTION_CLUSTERED\x10\x05B\x0b\n\tsort_kind"\xfe\x01\n\x11AggregateFunction\x12-\n\x12function_reference\x18\x01 \x01(\rR\x11functionReference\x12)\n\x04args\x18\x02 \x03(\x0b2\x15.substrait.ExpressionR\x04args\x12*\n\x05sorts\x18\x03 \x03(\x0b2\x14.substrait.SortFieldR\x05sorts\x121\n\x05phase\x18\x04 \x01(\x0e2\x1b.substrait.AggregationPhaseR\x05phase\x120\n\x0boutput_type\x18\x05 \x01(\x0b2\x0f.substrait.TypeR\noutputType*\xef\x01\n\x10AggregationPhase\x12!\n\x1dAGGREGATION_PHASE_UNSPECIFIED\x10\x00\x12-\n)AGGREGATION_PHASE_INITIAL_TO_INTERMEDIATE\x10\x01\x122\n.AGGREGATION_PHASE_INTERMEDIATE_TO_INTERMEDIATE\x10\x02\x12\'\n#AGGREGATION_PHASE_INITIAL_TO_RESULT\x10\x03\x12,\n(AGGREGATION_PHASE_INTERMEDIATE_TO_RESULT\x10\x04B+\n\x12io.substrait.protoP\x01\xaa\x02\x12Substrait.Protobufb\x06proto3')
_AGGREGATIONPHASE = DESCRIPTOR.enum_types_by_name['AggregationPhase']
AggregationPhase = enum_type_wrapper.EnumTypeWrapper(_AGGREGATIONPHASE)
AGGREGATION_PHASE_UNSPECIFIED = 0
AGGREGATION_PHASE_INITIAL_TO_INTERMEDIATE = 1
AGGREGATION_PHASE_INTERMEDIATE_TO_INTERMEDIATE = 2
AGGREGATION_PHASE_INITIAL_TO_RESULT = 3
AGGREGATION_PHASE_INTERMEDIATE_TO_RESULT = 4
_RELCOMMON = DESCRIPTOR.message_types_by_name['RelCommon']
_RELCOMMON_DIRECT = _RELCOMMON.nested_types_by_name['Direct']
_RELCOMMON_EMIT = _RELCOMMON.nested_types_by_name['Emit']
_RELCOMMON_HINT = _RELCOMMON.nested_types_by_name['Hint']
_RELCOMMON_HINT_STATS = _RELCOMMON_HINT.nested_types_by_name['Stats']
_RELCOMMON_HINT_RUNTIMECONSTRAINT = _RELCOMMON_HINT.nested_types_by_name['RuntimeConstraint']
_READREL = DESCRIPTOR.message_types_by_name['ReadRel']
_READREL_NAMEDTABLE = _READREL.nested_types_by_name['NamedTable']
_READREL_VIRTUALTABLE = _READREL.nested_types_by_name['VirtualTable']
_READREL_EXTENSIONTABLE = _READREL.nested_types_by_name['ExtensionTable']
_READREL_LOCALFILES = _READREL.nested_types_by_name['LocalFiles']
_READREL_LOCALFILES_FILEORFILES = _READREL_LOCALFILES.nested_types_by_name['FileOrFiles']
_PROJECTREL = DESCRIPTOR.message_types_by_name['ProjectRel']
_JOINREL = DESCRIPTOR.message_types_by_name['JoinRel']
_CROSSREL = DESCRIPTOR.message_types_by_name['CrossRel']
_FETCHREL = DESCRIPTOR.message_types_by_name['FetchRel']
_AGGREGATEREL = DESCRIPTOR.message_types_by_name['AggregateRel']
_AGGREGATEREL_GROUPING = _AGGREGATEREL.nested_types_by_name['Grouping']
_AGGREGATEREL_MEASURE = _AGGREGATEREL.nested_types_by_name['Measure']
_SORTREL = DESCRIPTOR.message_types_by_name['SortRel']
_FILTERREL = DESCRIPTOR.message_types_by_name['FilterRel']
_SETREL = DESCRIPTOR.message_types_by_name['SetRel']
_EXTENSIONSINGLEREL = DESCRIPTOR.message_types_by_name['ExtensionSingleRel']
_EXTENSIONLEAFREL = DESCRIPTOR.message_types_by_name['ExtensionLeafRel']
_EXTENSIONMULTIREL = DESCRIPTOR.message_types_by_name['ExtensionMultiRel']
_RELROOT = DESCRIPTOR.message_types_by_name['RelRoot']
_REL = DESCRIPTOR.message_types_by_name['Rel']
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
_EXPRESSION_FIELDREFERENCE_OUTERREFERENCE = _EXPRESSION_FIELDREFERENCE.nested_types_by_name['OuterReference']
_EXPRESSION_SUBQUERY = _EXPRESSION.nested_types_by_name['Subquery']
_EXPRESSION_SUBQUERY_SCALAR = _EXPRESSION_SUBQUERY.nested_types_by_name['Scalar']
_EXPRESSION_SUBQUERY_INPREDICATE = _EXPRESSION_SUBQUERY.nested_types_by_name['InPredicate']
_EXPRESSION_SUBQUERY_SETPREDICATE = _EXPRESSION_SUBQUERY.nested_types_by_name['SetPredicate']
_EXPRESSION_SUBQUERY_SETCOMPARISON = _EXPRESSION_SUBQUERY.nested_types_by_name['SetComparison']
_SORTFIELD = DESCRIPTOR.message_types_by_name['SortField']
_AGGREGATEFUNCTION = DESCRIPTOR.message_types_by_name['AggregateFunction']
_READREL_LOCALFILES_FILEORFILES_FILEFORMAT = _READREL_LOCALFILES_FILEORFILES.enum_types_by_name['FileFormat']
_JOINREL_JOINTYPE = _JOINREL.enum_types_by_name['JoinType']
_SETREL_SETOP = _SETREL.enum_types_by_name['SetOp']
_EXPRESSION_SUBQUERY_SETPREDICATE_PREDICATEOP = _EXPRESSION_SUBQUERY_SETPREDICATE.enum_types_by_name['PredicateOp']
_EXPRESSION_SUBQUERY_SETCOMPARISON_COMPARISONOP = _EXPRESSION_SUBQUERY_SETCOMPARISON.enum_types_by_name['ComparisonOp']
_EXPRESSION_SUBQUERY_SETCOMPARISON_REDUCTIONOP = _EXPRESSION_SUBQUERY_SETCOMPARISON.enum_types_by_name['ReductionOp']
_SORTFIELD_SORTDIRECTION = _SORTFIELD.enum_types_by_name['SortDirection']
RelCommon = _reflection.GeneratedProtocolMessageType('RelCommon', (_message.Message,), {'Direct': _reflection.GeneratedProtocolMessageType('Direct', (_message.Message,), {'DESCRIPTOR': _RELCOMMON_DIRECT, '__module__': 'substrait.algebra_pb2'}), 'Emit': _reflection.GeneratedProtocolMessageType('Emit', (_message.Message,), {'DESCRIPTOR': _RELCOMMON_EMIT, '__module__': 'substrait.algebra_pb2'}), 'Hint': _reflection.GeneratedProtocolMessageType('Hint', (_message.Message,), {'Stats': _reflection.GeneratedProtocolMessageType('Stats', (_message.Message,), {'DESCRIPTOR': _RELCOMMON_HINT_STATS, '__module__': 'substrait.algebra_pb2'}), 'RuntimeConstraint': _reflection.GeneratedProtocolMessageType('RuntimeConstraint', (_message.Message,), {'DESCRIPTOR': _RELCOMMON_HINT_RUNTIMECONSTRAINT, '__module__': 'substrait.algebra_pb2'}), 'DESCRIPTOR': _RELCOMMON_HINT, '__module__': 'substrait.algebra_pb2'}), 'DESCRIPTOR': _RELCOMMON, '__module__': 'substrait.algebra_pb2'})
_sym_db.RegisterMessage(RelCommon)
_sym_db.RegisterMessage(RelCommon.Direct)
_sym_db.RegisterMessage(RelCommon.Emit)
_sym_db.RegisterMessage(RelCommon.Hint)
_sym_db.RegisterMessage(RelCommon.Hint.Stats)
_sym_db.RegisterMessage(RelCommon.Hint.RuntimeConstraint)
ReadRel = _reflection.GeneratedProtocolMessageType('ReadRel', (_message.Message,), {'NamedTable': _reflection.GeneratedProtocolMessageType('NamedTable', (_message.Message,), {'DESCRIPTOR': _READREL_NAMEDTABLE, '__module__': 'substrait.algebra_pb2'}), 'VirtualTable': _reflection.GeneratedProtocolMessageType('VirtualTable', (_message.Message,), {'DESCRIPTOR': _READREL_VIRTUALTABLE, '__module__': 'substrait.algebra_pb2'}), 'ExtensionTable': _reflection.GeneratedProtocolMessageType('ExtensionTable', (_message.Message,), {'DESCRIPTOR': _READREL_EXTENSIONTABLE, '__module__': 'substrait.algebra_pb2'}), 'LocalFiles': _reflection.GeneratedProtocolMessageType('LocalFiles', (_message.Message,), {'FileOrFiles': _reflection.GeneratedProtocolMessageType('FileOrFiles', (_message.Message,), {'DESCRIPTOR': _READREL_LOCALFILES_FILEORFILES, '__module__': 'substrait.algebra_pb2'}), 'DESCRIPTOR': _READREL_LOCALFILES, '__module__': 'substrait.algebra_pb2'}), 'DESCRIPTOR': _READREL, '__module__': 'substrait.algebra_pb2'})
_sym_db.RegisterMessage(ReadRel)
_sym_db.RegisterMessage(ReadRel.NamedTable)
_sym_db.RegisterMessage(ReadRel.VirtualTable)
_sym_db.RegisterMessage(ReadRel.ExtensionTable)
_sym_db.RegisterMessage(ReadRel.LocalFiles)
_sym_db.RegisterMessage(ReadRel.LocalFiles.FileOrFiles)
ProjectRel = _reflection.GeneratedProtocolMessageType('ProjectRel', (_message.Message,), {'DESCRIPTOR': _PROJECTREL, '__module__': 'substrait.algebra_pb2'})
_sym_db.RegisterMessage(ProjectRel)
JoinRel = _reflection.GeneratedProtocolMessageType('JoinRel', (_message.Message,), {'DESCRIPTOR': _JOINREL, '__module__': 'substrait.algebra_pb2'})
_sym_db.RegisterMessage(JoinRel)
CrossRel = _reflection.GeneratedProtocolMessageType('CrossRel', (_message.Message,), {'DESCRIPTOR': _CROSSREL, '__module__': 'substrait.algebra_pb2'})
_sym_db.RegisterMessage(CrossRel)
FetchRel = _reflection.GeneratedProtocolMessageType('FetchRel', (_message.Message,), {'DESCRIPTOR': _FETCHREL, '__module__': 'substrait.algebra_pb2'})
_sym_db.RegisterMessage(FetchRel)
AggregateRel = _reflection.GeneratedProtocolMessageType('AggregateRel', (_message.Message,), {'Grouping': _reflection.GeneratedProtocolMessageType('Grouping', (_message.Message,), {'DESCRIPTOR': _AGGREGATEREL_GROUPING, '__module__': 'substrait.algebra_pb2'}), 'Measure': _reflection.GeneratedProtocolMessageType('Measure', (_message.Message,), {'DESCRIPTOR': _AGGREGATEREL_MEASURE, '__module__': 'substrait.algebra_pb2'}), 'DESCRIPTOR': _AGGREGATEREL, '__module__': 'substrait.algebra_pb2'})
_sym_db.RegisterMessage(AggregateRel)
_sym_db.RegisterMessage(AggregateRel.Grouping)
_sym_db.RegisterMessage(AggregateRel.Measure)
SortRel = _reflection.GeneratedProtocolMessageType('SortRel', (_message.Message,), {'DESCRIPTOR': _SORTREL, '__module__': 'substrait.algebra_pb2'})
_sym_db.RegisterMessage(SortRel)
FilterRel = _reflection.GeneratedProtocolMessageType('FilterRel', (_message.Message,), {'DESCRIPTOR': _FILTERREL, '__module__': 'substrait.algebra_pb2'})
_sym_db.RegisterMessage(FilterRel)
SetRel = _reflection.GeneratedProtocolMessageType('SetRel', (_message.Message,), {'DESCRIPTOR': _SETREL, '__module__': 'substrait.algebra_pb2'})
_sym_db.RegisterMessage(SetRel)
ExtensionSingleRel = _reflection.GeneratedProtocolMessageType('ExtensionSingleRel', (_message.Message,), {'DESCRIPTOR': _EXTENSIONSINGLEREL, '__module__': 'substrait.algebra_pb2'})
_sym_db.RegisterMessage(ExtensionSingleRel)
ExtensionLeafRel = _reflection.GeneratedProtocolMessageType('ExtensionLeafRel', (_message.Message,), {'DESCRIPTOR': _EXTENSIONLEAFREL, '__module__': 'substrait.algebra_pb2'})
_sym_db.RegisterMessage(ExtensionLeafRel)
ExtensionMultiRel = _reflection.GeneratedProtocolMessageType('ExtensionMultiRel', (_message.Message,), {'DESCRIPTOR': _EXTENSIONMULTIREL, '__module__': 'substrait.algebra_pb2'})
_sym_db.RegisterMessage(ExtensionMultiRel)
RelRoot = _reflection.GeneratedProtocolMessageType('RelRoot', (_message.Message,), {'DESCRIPTOR': _RELROOT, '__module__': 'substrait.algebra_pb2'})
_sym_db.RegisterMessage(RelRoot)
Rel = _reflection.GeneratedProtocolMessageType('Rel', (_message.Message,), {'DESCRIPTOR': _REL, '__module__': 'substrait.algebra_pb2'})
_sym_db.RegisterMessage(Rel)
Expression = _reflection.GeneratedProtocolMessageType('Expression', (_message.Message,), {'Enum': _reflection.GeneratedProtocolMessageType('Enum', (_message.Message,), {'Empty': _reflection.GeneratedProtocolMessageType('Empty', (_message.Message,), {'DESCRIPTOR': _EXPRESSION_ENUM_EMPTY, '__module__': 'substrait.algebra_pb2'}), 'DESCRIPTOR': _EXPRESSION_ENUM, '__module__': 'substrait.algebra_pb2'}), 'Literal': _reflection.GeneratedProtocolMessageType('Literal', (_message.Message,), {'VarChar': _reflection.GeneratedProtocolMessageType('VarChar', (_message.Message,), {'DESCRIPTOR': _EXPRESSION_LITERAL_VARCHAR, '__module__': 'substrait.algebra_pb2'}), 'Decimal': _reflection.GeneratedProtocolMessageType('Decimal', (_message.Message,), {'DESCRIPTOR': _EXPRESSION_LITERAL_DECIMAL, '__module__': 'substrait.algebra_pb2'}), 'Map': _reflection.GeneratedProtocolMessageType('Map', (_message.Message,), {'KeyValue': _reflection.GeneratedProtocolMessageType('KeyValue', (_message.Message,), {'DESCRIPTOR': _EXPRESSION_LITERAL_MAP_KEYVALUE, '__module__': 'substrait.algebra_pb2'}), 'DESCRIPTOR': _EXPRESSION_LITERAL_MAP, '__module__': 'substrait.algebra_pb2'}), 'IntervalYearToMonth': _reflection.GeneratedProtocolMessageType('IntervalYearToMonth', (_message.Message,), {'DESCRIPTOR': _EXPRESSION_LITERAL_INTERVALYEARTOMONTH, '__module__': 'substrait.algebra_pb2'}), 'IntervalDayToSecond': _reflection.GeneratedProtocolMessageType('IntervalDayToSecond', (_message.Message,), {'DESCRIPTOR': _EXPRESSION_LITERAL_INTERVALDAYTOSECOND, '__module__': 'substrait.algebra_pb2'}), 'Struct': _reflection.GeneratedProtocolMessageType('Struct', (_message.Message,), {'DESCRIPTOR': _EXPRESSION_LITERAL_STRUCT, '__module__': 'substrait.algebra_pb2'}), 'List': _reflection.GeneratedProtocolMessageType('List', (_message.Message,), {'DESCRIPTOR': _EXPRESSION_LITERAL_LIST, '__module__': 'substrait.algebra_pb2'}), 'DESCRIPTOR': _EXPRESSION_LITERAL, '__module__': 'substrait.algebra_pb2'}), 'ScalarFunction': _reflection.GeneratedProtocolMessageType('ScalarFunction', (_message.Message,), {'DESCRIPTOR': _EXPRESSION_SCALARFUNCTION, '__module__': 'substrait.algebra_pb2'}), 'WindowFunction': _reflection.GeneratedProtocolMessageType('WindowFunction', (_message.Message,), {'Bound': _reflection.GeneratedProtocolMessageType('Bound', (_message.Message,), {'Preceding': _reflection.GeneratedProtocolMessageType('Preceding', (_message.Message,), {'DESCRIPTOR': _EXPRESSION_WINDOWFUNCTION_BOUND_PRECEDING, '__module__': 'substrait.algebra_pb2'}), 'Following': _reflection.GeneratedProtocolMessageType('Following', (_message.Message,), {'DESCRIPTOR': _EXPRESSION_WINDOWFUNCTION_BOUND_FOLLOWING, '__module__': 'substrait.algebra_pb2'}), 'CurrentRow': _reflection.GeneratedProtocolMessageType('CurrentRow', (_message.Message,), {'DESCRIPTOR': _EXPRESSION_WINDOWFUNCTION_BOUND_CURRENTROW, '__module__': 'substrait.algebra_pb2'}), 'Unbounded': _reflection.GeneratedProtocolMessageType('Unbounded', (_message.Message,), {'DESCRIPTOR': _EXPRESSION_WINDOWFUNCTION_BOUND_UNBOUNDED, '__module__': 'substrait.algebra_pb2'}), 'DESCRIPTOR': _EXPRESSION_WINDOWFUNCTION_BOUND, '__module__': 'substrait.algebra_pb2'}), 'DESCRIPTOR': _EXPRESSION_WINDOWFUNCTION, '__module__': 'substrait.algebra_pb2'}), 'IfThen': _reflection.GeneratedProtocolMessageType('IfThen', (_message.Message,), {'IfClause': _reflection.GeneratedProtocolMessageType('IfClause', (_message.Message,), {'DESCRIPTOR': _EXPRESSION_IFTHEN_IFCLAUSE, '__module__': 'substrait.algebra_pb2'}), 'DESCRIPTOR': _EXPRESSION_IFTHEN, '__module__': 'substrait.algebra_pb2'}), 'Cast': _reflection.GeneratedProtocolMessageType('Cast', (_message.Message,), {'DESCRIPTOR': _EXPRESSION_CAST, '__module__': 'substrait.algebra_pb2'}), 'SwitchExpression': _reflection.GeneratedProtocolMessageType('SwitchExpression', (_message.Message,), {'IfValue': _reflection.GeneratedProtocolMessageType('IfValue', (_message.Message,), {'DESCRIPTOR': _EXPRESSION_SWITCHEXPRESSION_IFVALUE, '__module__': 'substrait.algebra_pb2'}), 'DESCRIPTOR': _EXPRESSION_SWITCHEXPRESSION, '__module__': 'substrait.algebra_pb2'}), 'SingularOrList': _reflection.GeneratedProtocolMessageType('SingularOrList', (_message.Message,), {'DESCRIPTOR': _EXPRESSION_SINGULARORLIST, '__module__': 'substrait.algebra_pb2'}), 'MultiOrList': _reflection.GeneratedProtocolMessageType('MultiOrList', (_message.Message,), {'Record': _reflection.GeneratedProtocolMessageType('Record', (_message.Message,), {'DESCRIPTOR': _EXPRESSION_MULTIORLIST_RECORD, '__module__': 'substrait.algebra_pb2'}), 'DESCRIPTOR': _EXPRESSION_MULTIORLIST, '__module__': 'substrait.algebra_pb2'}), 'EmbeddedFunction': _reflection.GeneratedProtocolMessageType('EmbeddedFunction', (_message.Message,), {'PythonPickleFunction': _reflection.GeneratedProtocolMessageType('PythonPickleFunction', (_message.Message,), {'DESCRIPTOR': _EXPRESSION_EMBEDDEDFUNCTION_PYTHONPICKLEFUNCTION, '__module__': 'substrait.algebra_pb2'}), 'WebAssemblyFunction': _reflection.GeneratedProtocolMessageType('WebAssemblyFunction', (_message.Message,), {'DESCRIPTOR': _EXPRESSION_EMBEDDEDFUNCTION_WEBASSEMBLYFUNCTION, '__module__': 'substrait.algebra_pb2'}), 'DESCRIPTOR': _EXPRESSION_EMBEDDEDFUNCTION, '__module__': 'substrait.algebra_pb2'}), 'ReferenceSegment': _reflection.GeneratedProtocolMessageType('ReferenceSegment', (_message.Message,), {'MapKey': _reflection.GeneratedProtocolMessageType('MapKey', (_message.Message,), {'DESCRIPTOR': _EXPRESSION_REFERENCESEGMENT_MAPKEY, '__module__': 'substrait.algebra_pb2'}), 'StructField': _reflection.GeneratedProtocolMessageType('StructField', (_message.Message,), {'DESCRIPTOR': _EXPRESSION_REFERENCESEGMENT_STRUCTFIELD, '__module__': 'substrait.algebra_pb2'}), 'ListElement': _reflection.GeneratedProtocolMessageType('ListElement', (_message.Message,), {'DESCRIPTOR': _EXPRESSION_REFERENCESEGMENT_LISTELEMENT, '__module__': 'substrait.algebra_pb2'}), 'DESCRIPTOR': _EXPRESSION_REFERENCESEGMENT, '__module__': 'substrait.algebra_pb2'}), 'MaskExpression': _reflection.GeneratedProtocolMessageType('MaskExpression', (_message.Message,), {'Select': _reflection.GeneratedProtocolMessageType('Select', (_message.Message,), {'DESCRIPTOR': _EXPRESSION_MASKEXPRESSION_SELECT, '__module__': 'substrait.algebra_pb2'}), 'StructSelect': _reflection.GeneratedProtocolMessageType('StructSelect', (_message.Message,), {'DESCRIPTOR': _EXPRESSION_MASKEXPRESSION_STRUCTSELECT, '__module__': 'substrait.algebra_pb2'}), 'StructItem': _reflection.GeneratedProtocolMessageType('StructItem', (_message.Message,), {'DESCRIPTOR': _EXPRESSION_MASKEXPRESSION_STRUCTITEM, '__module__': 'substrait.algebra_pb2'}), 'ListSelect': _reflection.GeneratedProtocolMessageType('ListSelect', (_message.Message,), {'ListSelectItem': _reflection.GeneratedProtocolMessageType('ListSelectItem', (_message.Message,), {'ListElement': _reflection.GeneratedProtocolMessageType('ListElement', (_message.Message,), {'DESCRIPTOR': _EXPRESSION_MASKEXPRESSION_LISTSELECT_LISTSELECTITEM_LISTELEMENT, '__module__': 'substrait.algebra_pb2'}), 'ListSlice': _reflection.GeneratedProtocolMessageType('ListSlice', (_message.Message,), {'DESCRIPTOR': _EXPRESSION_MASKEXPRESSION_LISTSELECT_LISTSELECTITEM_LISTSLICE, '__module__': 'substrait.algebra_pb2'}), 'DESCRIPTOR': _EXPRESSION_MASKEXPRESSION_LISTSELECT_LISTSELECTITEM, '__module__': 'substrait.algebra_pb2'}), 'DESCRIPTOR': _EXPRESSION_MASKEXPRESSION_LISTSELECT, '__module__': 'substrait.algebra_pb2'}), 'MapSelect': _reflection.GeneratedProtocolMessageType('MapSelect', (_message.Message,), {'MapKey': _reflection.GeneratedProtocolMessageType('MapKey', (_message.Message,), {'DESCRIPTOR': _EXPRESSION_MASKEXPRESSION_MAPSELECT_MAPKEY, '__module__': 'substrait.algebra_pb2'}), 'MapKeyExpression': _reflection.GeneratedProtocolMessageType('MapKeyExpression', (_message.Message,), {'DESCRIPTOR': _EXPRESSION_MASKEXPRESSION_MAPSELECT_MAPKEYEXPRESSION, '__module__': 'substrait.algebra_pb2'}), 'DESCRIPTOR': _EXPRESSION_MASKEXPRESSION_MAPSELECT, '__module__': 'substrait.algebra_pb2'}), 'DESCRIPTOR': _EXPRESSION_MASKEXPRESSION, '__module__': 'substrait.algebra_pb2'}), 'FieldReference': _reflection.GeneratedProtocolMessageType('FieldReference', (_message.Message,), {'RootReference': _reflection.GeneratedProtocolMessageType('RootReference', (_message.Message,), {'DESCRIPTOR': _EXPRESSION_FIELDREFERENCE_ROOTREFERENCE, '__module__': 'substrait.algebra_pb2'}), 'OuterReference': _reflection.GeneratedProtocolMessageType('OuterReference', (_message.Message,), {'DESCRIPTOR': _EXPRESSION_FIELDREFERENCE_OUTERREFERENCE, '__module__': 'substrait.algebra_pb2'}), 'DESCRIPTOR': _EXPRESSION_FIELDREFERENCE, '__module__': 'substrait.algebra_pb2'}), 'Subquery': _reflection.GeneratedProtocolMessageType('Subquery', (_message.Message,), {'Scalar': _reflection.GeneratedProtocolMessageType('Scalar', (_message.Message,), {'DESCRIPTOR': _EXPRESSION_SUBQUERY_SCALAR, '__module__': 'substrait.algebra_pb2'}), 'InPredicate': _reflection.GeneratedProtocolMessageType('InPredicate', (_message.Message,), {'DESCRIPTOR': _EXPRESSION_SUBQUERY_INPREDICATE, '__module__': 'substrait.algebra_pb2'}), 'SetPredicate': _reflection.GeneratedProtocolMessageType('SetPredicate', (_message.Message,), {'DESCRIPTOR': _EXPRESSION_SUBQUERY_SETPREDICATE, '__module__': 'substrait.algebra_pb2'}), 'SetComparison': _reflection.GeneratedProtocolMessageType('SetComparison', (_message.Message,), {'DESCRIPTOR': _EXPRESSION_SUBQUERY_SETCOMPARISON, '__module__': 'substrait.algebra_pb2'}), 'DESCRIPTOR': _EXPRESSION_SUBQUERY, '__module__': 'substrait.algebra_pb2'}), 'DESCRIPTOR': _EXPRESSION, '__module__': 'substrait.algebra_pb2'})
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
_sym_db.RegisterMessage(Expression.FieldReference.OuterReference)
_sym_db.RegisterMessage(Expression.Subquery)
_sym_db.RegisterMessage(Expression.Subquery.Scalar)
_sym_db.RegisterMessage(Expression.Subquery.InPredicate)
_sym_db.RegisterMessage(Expression.Subquery.SetPredicate)
_sym_db.RegisterMessage(Expression.Subquery.SetComparison)
SortField = _reflection.GeneratedProtocolMessageType('SortField', (_message.Message,), {'DESCRIPTOR': _SORTFIELD, '__module__': 'substrait.algebra_pb2'})
_sym_db.RegisterMessage(SortField)
AggregateFunction = _reflection.GeneratedProtocolMessageType('AggregateFunction', (_message.Message,), {'DESCRIPTOR': _AGGREGATEFUNCTION, '__module__': 'substrait.algebra_pb2'})
_sym_db.RegisterMessage(AggregateFunction)
if _descriptor._USE_C_DESCRIPTORS == False:
    DESCRIPTOR._options = None
    DESCRIPTOR._serialized_options = b'\n\x12io.substrait.protoP\x01\xaa\x02\x12Substrait.Protobuf'
    _AGGREGATIONPHASE._serialized_start = 15890
    _AGGREGATIONPHASE._serialized_end = 16129
    _RELCOMMON._serialized_start = 127
    _RELCOMMON._serialized_end = 945
    _RELCOMMON_DIRECT._serialized_start = 379
    _RELCOMMON_DIRECT._serialized_end = 387
    _RELCOMMON_EMIT._serialized_start = 389
    _RELCOMMON_EMIT._serialized_end = 434
    _RELCOMMON_HINT._serialized_start = 437
    _RELCOMMON_HINT._serialized_end = 932
    _RELCOMMON_HINT_STATS._serialized_start = 666
    _RELCOMMON_HINT_STATS._serialized_end = 823
    _RELCOMMON_HINT_RUNTIMECONSTRAINT._serialized_start = 825
    _RELCOMMON_HINT_RUNTIMECONSTRAINT._serialized_end = 932
    _READREL._serialized_start = 948
    _READREL._serialized_end = 2385
    _READREL_NAMEDTABLE._serialized_start = 1549
    _READREL_NAMEDTABLE._serialized_end = 1671
    _READREL_VIRTUALTABLE._serialized_start = 1673
    _READREL_VIRTUALTABLE._serialized_end = 1749
    _READREL_EXTENSIONTABLE._serialized_start = 1751
    _READREL_EXTENSIONTABLE._serialized_end = 1813
    _READREL_LOCALFILES._serialized_start = 1816
    _READREL_LOCALFILES._serialized_end = 2372
    _READREL_LOCALFILES_FILEORFILES._serialized_start = 1984
    _READREL_LOCALFILES_FILEORFILES._serialized_end = 2372
    _READREL_LOCALFILES_FILEORFILES_FILEFORMAT._serialized_start = 2293
    _READREL_LOCALFILES_FILEORFILES_FILEFORMAT._serialized_end = 2359
    _PROJECTREL._serialized_start = 2388
    _PROJECTREL._serialized_end = 2629
    _JOINREL._serialized_start = 2632
    _JOINREL._serialized_end = 3203
    _JOINREL_JOINTYPE._serialized_start = 3021
    _JOINREL_JOINTYPE._serialized_end = 3203
    _CROSSREL._serialized_start = 3206
    _CROSSREL._serialized_end = 3424
    _FETCHREL._serialized_start = 3427
    _FETCHREL._serialized_end = 3655
    _AGGREGATEREL._serialized_start = 3658
    _AGGREGATEREL._serialized_end = 4169
    _AGGREGATEREL_GROUPING._serialized_start = 3971
    _AGGREGATEREL_GROUPING._serialized_end = 4055
    _AGGREGATEREL_MEASURE._serialized_start = 4057
    _AGGREGATEREL_MEASURE._serialized_end = 4169
    _SORTREL._serialized_start = 4172
    _SORTREL._serialized_end = 4397
    _FILTERREL._serialized_start = 4400
    _FILTERREL._serialized_end = 4636
    _SETREL._serialized_start = 4639
    _SETREL._serialized_end = 5065
    _SETREL_SETOP._serialized_start = 4865
    _SETREL_SETOP._serialized_end = 5065
    _EXTENSIONSINGLEREL._serialized_start = 5068
    _EXTENSIONSINGLEREL._serialized_end = 5218
    _EXTENSIONLEAFREL._serialized_start = 5220
    _EXTENSIONLEAFREL._serialized_end = 5330
    _EXTENSIONMULTIREL._serialized_start = 5333
    _EXTENSIONMULTIREL._serialized_end = 5484
    _RELROOT._serialized_start = 5486
    _RELROOT._serialized_end = 5555
    _REL._serialized_start = 5558
    _REL._serialized_end = 6205
    _EXPRESSION._serialized_start = 6208
    _EXPRESSION._serialized_end = 15198
    _EXPRESSION_ENUM._serialized_start = 6975
    _EXPRESSION_ENUM._serialized_end = 7105
    _EXPRESSION_ENUM_EMPTY._serialized_start = 7085
    _EXPRESSION_ENUM_EMPTY._serialized_end = 7092
    _EXPRESSION_LITERAL._serialized_start = 7108
    _EXPRESSION_LITERAL._serialized_end = 8843
    _EXPRESSION_LITERAL_VARCHAR._serialized_start = 8224
    _EXPRESSION_LITERAL_VARCHAR._serialized_end = 8279
    _EXPRESSION_LITERAL_DECIMAL._serialized_start = 8281
    _EXPRESSION_LITERAL_DECIMAL._serialized_end = 8364
    _EXPRESSION_LITERAL_MAP._serialized_start = 8367
    _EXPRESSION_LITERAL_MAP._serialized_end = 8561
    _EXPRESSION_LITERAL_MAP_KEYVALUE._serialized_start = 8449
    _EXPRESSION_LITERAL_MAP_KEYVALUE._serialized_end = 8561
    _EXPRESSION_LITERAL_INTERVALYEARTOMONTH._serialized_start = 8563
    _EXPRESSION_LITERAL_INTERVALYEARTOMONTH._serialized_end = 8630
    _EXPRESSION_LITERAL_INTERVALDAYTOSECOND._serialized_start = 8632
    _EXPRESSION_LITERAL_INTERVALDAYTOSECOND._serialized_end = 8699
    _EXPRESSION_LITERAL_STRUCT._serialized_start = 8701
    _EXPRESSION_LITERAL_STRUCT._serialized_end = 8764
    _EXPRESSION_LITERAL_LIST._serialized_start = 8766
    _EXPRESSION_LITERAL_LIST._serialized_end = 8827
    _EXPRESSION_SCALARFUNCTION._serialized_start = 8846
    _EXPRESSION_SCALARFUNCTION._serialized_end = 9002
    _EXPRESSION_WINDOWFUNCTION._serialized_start = 9005
    _EXPRESSION_WINDOWFUNCTION._serialized_end = 9932
    _EXPRESSION_WINDOWFUNCTION_BOUND._serialized_start = 9468
    _EXPRESSION_WINDOWFUNCTION_BOUND._serialized_end = 9932
    _EXPRESSION_WINDOWFUNCTION_BOUND_PRECEDING._serialized_start = 9825
    _EXPRESSION_WINDOWFUNCTION_BOUND_PRECEDING._serialized_end = 9860
    _EXPRESSION_WINDOWFUNCTION_BOUND_FOLLOWING._serialized_start = 9862
    _EXPRESSION_WINDOWFUNCTION_BOUND_FOLLOWING._serialized_end = 9897
    _EXPRESSION_WINDOWFUNCTION_BOUND_CURRENTROW._serialized_start = 9899
    _EXPRESSION_WINDOWFUNCTION_BOUND_CURRENTROW._serialized_end = 9911
    _EXPRESSION_WINDOWFUNCTION_BOUND_UNBOUNDED._serialized_start = 9913
    _EXPRESSION_WINDOWFUNCTION_BOUND_UNBOUNDED._serialized_end = 9924
    _EXPRESSION_IFTHEN._serialized_start = 9935
    _EXPRESSION_IFTHEN._serialized_end = 10137
    _EXPRESSION_IFTHEN_IFCLAUSE._serialized_start = 10045
    _EXPRESSION_IFTHEN_IFCLAUSE._serialized_end = 10137
    _EXPRESSION_CAST._serialized_start = 10139
    _EXPRESSION_CAST._serialized_end = 10227
    _EXPRESSION_SWITCHEXPRESSION._serialized_start = 10230
    _EXPRESSION_SWITCHEXPRESSION._serialized_end = 10458
    _EXPRESSION_SWITCHEXPRESSION_IFVALUE._serialized_start = 10359
    _EXPRESSION_SWITCHEXPRESSION_IFVALUE._serialized_end = 10458
    _EXPRESSION_SINGULARORLIST._serialized_start = 10460
    _EXPRESSION_SINGULARORLIST._serialized_end = 10570
    _EXPRESSION_MULTIORLIST._serialized_start = 10573
    _EXPRESSION_MULTIORLIST._serialized_end = 10756
    _EXPRESSION_MULTIORLIST_RECORD._serialized_start = 10701
    _EXPRESSION_MULTIORLIST_RECORD._serialized_end = 10756
    _EXPRESSION_EMBEDDEDFUNCTION._serialized_start = 10759
    _EXPRESSION_EMBEDDEDFUNCTION._serialized_end = 11290
    _EXPRESSION_EMBEDDEDFUNCTION_PYTHONPICKLEFUNCTION._serialized_start = 11113
    _EXPRESSION_EMBEDDEDFUNCTION_PYTHONPICKLEFUNCTION._serialized_end = 11199
    _EXPRESSION_EMBEDDEDFUNCTION_WEBASSEMBLYFUNCTION._serialized_start = 11201
    _EXPRESSION_EMBEDDEDFUNCTION_WEBASSEMBLYFUNCTION._serialized_end = 11282
    _EXPRESSION_REFERENCESEGMENT._serialized_start = 11293
    _EXPRESSION_REFERENCESEGMENT._serialized_end = 11909
    _EXPRESSION_REFERENCESEGMENT_MAPKEY._serialized_start = 11565
    _EXPRESSION_REFERENCESEGMENT_MAPKEY._serialized_end = 11691
    _EXPRESSION_REFERENCESEGMENT_STRUCTFIELD._serialized_start = 11693
    _EXPRESSION_REFERENCESEGMENT_STRUCTFIELD._serialized_end = 11790
    _EXPRESSION_REFERENCESEGMENT_LISTELEMENT._serialized_start = 11792
    _EXPRESSION_REFERENCESEGMENT_LISTELEMENT._serialized_end = 11891
    _EXPRESSION_MASKEXPRESSION._serialized_start = 11912
    _EXPRESSION_MASKEXPRESSION._serialized_end = 13354
    _EXPRESSION_MASKEXPRESSION_SELECT._serialized_start = 12064
    _EXPRESSION_MASKEXPRESSION_SELECT._serialized_end = 12296
    _EXPRESSION_MASKEXPRESSION_STRUCTSELECT._serialized_start = 12298
    _EXPRESSION_MASKEXPRESSION_STRUCTSELECT._serialized_end = 12396
    _EXPRESSION_MASKEXPRESSION_STRUCTITEM._serialized_start = 12398
    _EXPRESSION_MASKEXPRESSION_STRUCTITEM._serialized_end = 12499
    _EXPRESSION_MASKEXPRESSION_LISTSELECT._serialized_start = 12502
    _EXPRESSION_MASKEXPRESSION_LISTSELECT._serialized_end = 12988
    _EXPRESSION_MASKEXPRESSION_LISTSELECT_LISTSELECTITEM._serialized_start = 12678
    _EXPRESSION_MASKEXPRESSION_LISTSELECT_LISTSELECTITEM._serialized_end = 12988
    _EXPRESSION_MASKEXPRESSION_LISTSELECT_LISTSELECTITEM_LISTELEMENT._serialized_start = 12892
    _EXPRESSION_MASKEXPRESSION_LISTSELECT_LISTSELECTITEM_LISTELEMENT._serialized_end = 12927
    _EXPRESSION_MASKEXPRESSION_LISTSELECT_LISTSELECTITEM_LISTSLICE._serialized_start = 12929
    _EXPRESSION_MASKEXPRESSION_LISTSELECT_LISTSELECTITEM_LISTSLICE._serialized_end = 12980
    _EXPRESSION_MASKEXPRESSION_MAPSELECT._serialized_start = 12991
    _EXPRESSION_MASKEXPRESSION_MAPSELECT._serialized_end = 13354
    _EXPRESSION_MASKEXPRESSION_MAPSELECT_MAPKEY._serialized_start = 13245
    _EXPRESSION_MASKEXPRESSION_MAPSELECT_MAPKEY._serialized_end = 13278
    _EXPRESSION_MASKEXPRESSION_MAPSELECT_MAPKEYEXPRESSION._serialized_start = 13280
    _EXPRESSION_MASKEXPRESSION_MAPSELECT_MAPKEYEXPRESSION._serialized_end = 13344
    _EXPRESSION_FIELDREFERENCE._serialized_start = 13357
    _EXPRESSION_FIELDREFERENCE._serialized_end = 13882
    _EXPRESSION_FIELDREFERENCE_ROOTREFERENCE._serialized_start = 13789
    _EXPRESSION_FIELDREFERENCE_ROOTREFERENCE._serialized_end = 13804
    _EXPRESSION_FIELDREFERENCE_OUTERREFERENCE._serialized_start = 13806
    _EXPRESSION_FIELDREFERENCE_OUTERREFERENCE._serialized_end = 13851
    _EXPRESSION_SUBQUERY._serialized_start = 13885
    _EXPRESSION_SUBQUERY._serialized_end = 15186
    _EXPRESSION_SUBQUERY_SCALAR._serialized_start = 14214
    _EXPRESSION_SUBQUERY_SCALAR._serialized_end = 14260
    _EXPRESSION_SUBQUERY_INPREDICATE._serialized_start = 14262
    _EXPRESSION_SUBQUERY_INPREDICATE._serialized_end = 14368
    _EXPRESSION_SUBQUERY_SETPREDICATE._serialized_start = 14371
    _EXPRESSION_SUBQUERY_SETPREDICATE._serialized_end = 14612
    _EXPRESSION_SUBQUERY_SETPREDICATE_PREDICATEOP._serialized_start = 14519
    _EXPRESSION_SUBQUERY_SETPREDICATE_PREDICATEOP._serialized_end = 14612
    _EXPRESSION_SUBQUERY_SETCOMPARISON._serialized_start = 14615
    _EXPRESSION_SUBQUERY_SETCOMPARISON._serialized_end = 15169
    _EXPRESSION_SUBQUERY_SETCOMPARISON_COMPARISONOP._serialized_start = 14903
    _EXPRESSION_SUBQUERY_SETCOMPARISON_COMPARISONOP._serialized_end = 15080
    _EXPRESSION_SUBQUERY_SETCOMPARISON_REDUCTIONOP._serialized_start = 15082
    _EXPRESSION_SUBQUERY_SETCOMPARISON_REDUCTIONOP._serialized_end = 15169
    _SORTFIELD._serialized_start = 15201
    _SORTFIELD._serialized_end = 15630
    _SORTFIELD_SORTDIRECTION._serialized_start = 15396
    _SORTFIELD_SORTDIRECTION._serialized_end = 15617
    _AGGREGATEFUNCTION._serialized_start = 15633
    _AGGREGATEFUNCTION._serialized_end = 15887