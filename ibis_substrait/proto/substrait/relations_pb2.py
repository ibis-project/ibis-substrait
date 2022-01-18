"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
_sym_db = _symbol_database.Default()
from ..substrait import type_pb2 as substrait_dot_type__pb2
from ..substrait import expression_pb2 as substrait_dot_expression__pb2
from ..substrait.extensions import extensions_pb2 as substrait_dot_extensions_dot_extensions__pb2
from google.protobuf import any_pb2 as google_dot_protobuf_dot_any__pb2
DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x19substrait/relations.proto\x12\tsubstrait\x1a\x14substrait/type.proto\x1a\x1asubstrait/expression.proto\x1a%substrait/extensions/extensions.proto\x1a\x19google/protobuf/any.proto"\xb2\x06\n\tRelCommon\x125\n\x06direct\x18\x01 \x01(\x0b2\x1b.substrait.RelCommon.DirectH\x00R\x06direct\x12/\n\x04emit\x18\x02 \x01(\x0b2\x19.substrait.RelCommon.EmitH\x00R\x04emit\x12-\n\x04hint\x18\x03 \x01(\x0b2\x19.substrait.RelCommon.HintR\x04hint\x12V\n\x12advanced_extension\x18\x04 \x01(\x0b2\'.substrait.extensions.AdvancedExtensionR\x11advancedExtension\x1a\x08\n\x06Direct\x1a-\n\x04Emit\x12%\n\x0eoutput_mapping\x18\x01 \x03(\x05R\routputMapping\x1a\xef\x03\n\x04Hint\x125\n\x05stats\x18\x01 \x01(\x0b2\x1f.substrait.RelCommon.Hint.StatsR\x05stats\x12K\n\nconstraint\x18\x02 \x01(\x0b2+.substrait.RelCommon.Hint.RuntimeConstraintR\nconstraint\x12V\n\x12advanced_extension\x18\n \x01(\x0b2\'.substrait.extensions.AdvancedExtensionR\x11advancedExtension\x1a\x9d\x01\n\x05Stats\x12\x1b\n\trow_count\x18\x01 \x01(\x01R\x08rowCount\x12\x1f\n\x0brecord_size\x18\x02 \x01(\x01R\nrecordSize\x12V\n\x12advanced_extension\x18\n \x01(\x0b2\'.substrait.extensions.AdvancedExtensionR\x11advancedExtension\x1ak\n\x11RuntimeConstraint\x12V\n\x12advanced_extension\x18\n \x01(\x0b2\'.substrait.extensions.AdvancedExtensionR\x11advancedExtensionB\x0b\n\temit_kind"\x9d\x0b\n\x07ReadRel\x12,\n\x06common\x18\x01 \x01(\x0b2\x14.substrait.RelCommonR\x06common\x127\n\x0bbase_schema\x18\x02 \x01(\x0b2\x16.substrait.NamedStructR\nbaseSchema\x12-\n\x06filter\x18\x03 \x01(\x0b2\x15.substrait.ExpressionR\x06filter\x12D\n\nprojection\x18\x04 \x01(\x0b2$.substrait.Expression.MaskExpressionR\nprojection\x12V\n\x12advanced_extension\x18\n \x01(\x0b2\'.substrait.extensions.AdvancedExtensionR\x11advancedExtension\x12F\n\rvirtual_table\x18\x05 \x01(\x0b2\x1f.substrait.ReadRel.VirtualTableH\x00R\x0cvirtualTable\x12@\n\x0blocal_files\x18\x06 \x01(\x0b2\x1d.substrait.ReadRel.LocalFilesH\x00R\nlocalFiles\x12@\n\x0bnamed_table\x18\x07 \x01(\x0b2\x1d.substrait.ReadRel.NamedTableH\x00R\nnamedTable\x12L\n\x0fextension_table\x18\x08 \x01(\x0b2!.substrait.ReadRel.ExtensionTableH\x00R\x0eextensionTable\x1az\n\nNamedTable\x12\x14\n\x05names\x18\x01 \x03(\tR\x05names\x12V\n\x12advanced_extension\x18\n \x01(\x0b2\'.substrait.extensions.AdvancedExtensionR\x11advancedExtension\x1aL\n\x0cVirtualTable\x12<\n\x06values\x18\x01 \x03(\x0b2$.substrait.Expression.Literal.StructR\x06values\x1a>\n\x0eExtensionTable\x12,\n\x06detail\x18\x01 \x01(\x0b2\x14.google.protobuf.AnyR\x06detail\x1a\xac\x04\n\nLocalFiles\x12?\n\x05items\x18\x01 \x03(\x0b2).substrait.ReadRel.LocalFiles.FileOrFilesR\x05items\x12V\n\x12advanced_extension\x18\n \x01(\x0b2\'.substrait.extensions.AdvancedExtensionR\x11advancedExtension\x1a\x84\x03\n\x0bFileOrFiles\x12\x1b\n\x08uri_path\x18\x01 \x01(\tH\x00R\x07uriPath\x12$\n\ruri_path_glob\x18\x02 \x01(\tH\x00R\x0buriPathGlob\x12\x1b\n\x08uri_file\x18\x03 \x01(\tH\x00R\x07uriFile\x12\x1f\n\nuri_folder\x18\x04 \x01(\tH\x00R\turiFolder\x12L\n\x06format\x18\x05 \x01(\x0e24.substrait.ReadRel.LocalFiles.FileOrFiles.FileFormatR\x06format\x12\'\n\x0fpartition_index\x18\x06 \x01(\x04R\x0epartitionIndex\x12\x14\n\x05start\x18\x07 \x01(\x04R\x05start\x12\x16\n\x06length\x18\x08 \x01(\x04R\x06length"B\n\nFileFormat\x12\x1b\n\x17FILE_FORMAT_UNSPECIFIED\x10\x00\x12\x17\n\x13FILE_FORMAT_PARQUET\x10\x01B\x0b\n\tpath_typeB\x0b\n\tread_type"\xf1\x01\n\nProjectRel\x12,\n\x06common\x18\x01 \x01(\x0b2\x14.substrait.RelCommonR\x06common\x12$\n\x05input\x18\x02 \x01(\x0b2\x0e.substrait.RelR\x05input\x127\n\x0bexpressions\x18\x03 \x03(\x0b2\x15.substrait.ExpressionR\x0bexpressions\x12V\n\x12advanced_extension\x18\n \x01(\x0b2\'.substrait.extensions.AdvancedExtensionR\x11advancedExtension"\xa5\x04\n\x07JoinRel\x12,\n\x06common\x18\x01 \x01(\x0b2\x14.substrait.RelCommonR\x06common\x12"\n\x04left\x18\x02 \x01(\x0b2\x0e.substrait.RelR\x04left\x12$\n\x05right\x18\x03 \x01(\x0b2\x0e.substrait.RelR\x05right\x125\n\nexpression\x18\x04 \x01(\x0b2\x15.substrait.ExpressionR\nexpression\x12?\n\x10post_join_filter\x18\x05 \x01(\x0b2\x15.substrait.ExpressionR\x0epostJoinFilter\x12/\n\x04type\x18\x06 \x01(\x0e2\x1b.substrait.JoinRel.JoinTypeR\x04type\x12V\n\x12advanced_extension\x18\n \x01(\x0b2\'.substrait.extensions.AdvancedExtensionR\x11advancedExtension"\xa0\x01\n\x08JoinType\x12\x19\n\x15JOIN_TYPE_UNSPECIFIED\x10\x00\x12\x13\n\x0fJOIN_TYPE_INNER\x10\x01\x12\x13\n\x0fJOIN_TYPE_OUTER\x10\x02\x12\x12\n\x0eJOIN_TYPE_LEFT\x10\x03\x12\x13\n\x0fJOIN_TYPE_RIGHT\x10\x04\x12\x12\n\x0eJOIN_TYPE_SEMI\x10\x05\x12\x12\n\x0eJOIN_TYPE_ANTI\x10\x06"\xe4\x01\n\x08FetchRel\x12,\n\x06common\x18\x01 \x01(\x0b2\x14.substrait.RelCommonR\x06common\x12$\n\x05input\x18\x02 \x01(\x0b2\x0e.substrait.RelR\x05input\x12\x16\n\x06offset\x18\x03 \x01(\x03R\x06offset\x12\x14\n\x05count\x18\x04 \x01(\x03R\x05count\x12V\n\x12advanced_extension\x18\n \x01(\x0b2\'.substrait.extensions.AdvancedExtensionR\x11advancedExtension"\xff\x03\n\x0cAggregateRel\x12,\n\x06common\x18\x01 \x01(\x0b2\x14.substrait.RelCommonR\x06common\x12$\n\x05input\x18\x02 \x01(\x0b2\x0e.substrait.RelR\x05input\x12>\n\tgroupings\x18\x03 \x03(\x0b2 .substrait.AggregateRel.GroupingR\tgroupings\x12;\n\x08measures\x18\x04 \x03(\x0b2\x1f.substrait.AggregateRel.MeasureR\x08measures\x12V\n\x12advanced_extension\x18\n \x01(\x0b2\'.substrait.extensions.AdvancedExtensionR\x11advancedExtension\x1aT\n\x08Grouping\x12H\n\x14grouping_expressions\x18\x01 \x03(\x0b2\x15.substrait.ExpressionR\x13groupingExpressions\x1ap\n\x07Measure\x126\n\x07measure\x18\x01 \x01(\x0b2\x1c.substrait.AggregateFunctionR\x07measure\x12-\n\x06filter\x18\x02 \x01(\x0b2\x15.substrait.ExpressionR\x06filter"\xe1\x01\n\x07SortRel\x12,\n\x06common\x18\x01 \x01(\x0b2\x14.substrait.RelCommonR\x06common\x12$\n\x05input\x18\x02 \x01(\x0b2\x0e.substrait.RelR\x05input\x12*\n\x05sorts\x18\x03 \x03(\x0b2\x14.substrait.SortFieldR\x05sorts\x12V\n\x12advanced_extension\x18\n \x01(\x0b2\'.substrait.extensions.AdvancedExtensionR\x11advancedExtension"\xec\x01\n\tFilterRel\x12,\n\x06common\x18\x01 \x01(\x0b2\x14.substrait.RelCommonR\x06common\x12$\n\x05input\x18\x02 \x01(\x0b2\x0e.substrait.RelR\x05input\x123\n\tcondition\x18\x03 \x01(\x0b2\x15.substrait.ExpressionR\tcondition\x12V\n\x12advanced_extension\x18\n \x01(\x0b2\'.substrait.extensions.AdvancedExtensionR\x11advancedExtension"\xaa\x03\n\x06SetRel\x12,\n\x06common\x18\x01 \x01(\x0b2\x14.substrait.RelCommonR\x06common\x12&\n\x06inputs\x18\x02 \x03(\x0b2\x0e.substrait.RelR\x06inputs\x12\'\n\x02op\x18\x03 \x01(\x0e2\x17.substrait.SetRel.SetOpR\x02op\x12V\n\x12advanced_extension\x18\n \x01(\x0b2\'.substrait.extensions.AdvancedExtensionR\x11advancedExtension"\xc8\x01\n\x05SetOp\x12\x16\n\x12SET_OP_UNSPECIFIED\x10\x00\x12\x18\n\x14SET_OP_MINUS_PRIMARY\x10\x01\x12\x19\n\x15SET_OP_MINUS_MULTISET\x10\x02\x12\x1f\n\x1bSET_OP_INTERSECTION_PRIMARY\x10\x03\x12 \n\x1cSET_OP_INTERSECTION_MULTISET\x10\x04\x12\x19\n\x15SET_OP_UNION_DISTINCT\x10\x05\x12\x14\n\x10SET_OP_UNION_ALL\x10\x06"\x96\x01\n\x12ExtensionSingleRel\x12,\n\x06common\x18\x01 \x01(\x0b2\x14.substrait.RelCommonR\x06common\x12$\n\x05input\x18\x02 \x01(\x0b2\x0e.substrait.RelR\x05input\x12,\n\x06detail\x18\x03 \x01(\x0b2\x14.google.protobuf.AnyR\x06detail"n\n\x10ExtensionLeafRel\x12,\n\x06common\x18\x01 \x01(\x0b2\x14.substrait.RelCommonR\x06common\x12,\n\x06detail\x18\x02 \x01(\x0b2\x14.google.protobuf.AnyR\x06detail"\x97\x01\n\x11ExtensionMultiRel\x12,\n\x06common\x18\x01 \x01(\x0b2\x14.substrait.RelCommonR\x06common\x12&\n\x06inputs\x18\x02 \x03(\x0b2\x0e.substrait.RelR\x06inputs\x12,\n\x06detail\x18\x03 \x01(\x0b2\x14.google.protobuf.AnyR\x06detail"E\n\x07RelRoot\x12$\n\x05input\x18\x01 \x01(\x0b2\x0e.substrait.RelR\x05input\x12\x14\n\x05names\x18\x02 \x03(\tR\x05names"\xda\x04\n\x03Rel\x12(\n\x04read\x18\x01 \x01(\x0b2\x12.substrait.ReadRelH\x00R\x04read\x12.\n\x06filter\x18\x02 \x01(\x0b2\x14.substrait.FilterRelH\x00R\x06filter\x12+\n\x05fetch\x18\x03 \x01(\x0b2\x13.substrait.FetchRelH\x00R\x05fetch\x127\n\taggregate\x18\x04 \x01(\x0b2\x17.substrait.AggregateRelH\x00R\taggregate\x12(\n\x04sort\x18\x05 \x01(\x0b2\x12.substrait.SortRelH\x00R\x04sort\x12(\n\x04join\x18\x06 \x01(\x0b2\x12.substrait.JoinRelH\x00R\x04join\x121\n\x07project\x18\x07 \x01(\x0b2\x15.substrait.ProjectRelH\x00R\x07project\x12%\n\x03set\x18\x08 \x01(\x0b2\x11.substrait.SetRelH\x00R\x03set\x12J\n\x10extension_single\x18\t \x01(\x0b2\x1d.substrait.ExtensionSingleRelH\x00R\x0fextensionSingle\x12G\n\x0fextension_multi\x18\n \x01(\x0b2\x1c.substrait.ExtensionMultiRelH\x00R\x0eextensionMulti\x12D\n\x0eextension_leaf\x18\x0b \x01(\x0b2\x1b.substrait.ExtensionLeafRelH\x00R\rextensionLeafB\n\n\x08rel_typeB+\n\x12io.substrait.protoP\x01\xaa\x02\x12Substrait.Protobufb\x06proto3')
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
_READREL_LOCALFILES_FILEORFILES_FILEFORMAT = _READREL_LOCALFILES_FILEORFILES.enum_types_by_name['FileFormat']
_JOINREL_JOINTYPE = _JOINREL.enum_types_by_name['JoinType']
_SETREL_SETOP = _SETREL.enum_types_by_name['SetOp']
RelCommon = _reflection.GeneratedProtocolMessageType('RelCommon', (_message.Message,), {'Direct': _reflection.GeneratedProtocolMessageType('Direct', (_message.Message,), {'DESCRIPTOR': _RELCOMMON_DIRECT, '__module__': 'substrait.relations_pb2'}), 'Emit': _reflection.GeneratedProtocolMessageType('Emit', (_message.Message,), {'DESCRIPTOR': _RELCOMMON_EMIT, '__module__': 'substrait.relations_pb2'}), 'Hint': _reflection.GeneratedProtocolMessageType('Hint', (_message.Message,), {'Stats': _reflection.GeneratedProtocolMessageType('Stats', (_message.Message,), {'DESCRIPTOR': _RELCOMMON_HINT_STATS, '__module__': 'substrait.relations_pb2'}), 'RuntimeConstraint': _reflection.GeneratedProtocolMessageType('RuntimeConstraint', (_message.Message,), {'DESCRIPTOR': _RELCOMMON_HINT_RUNTIMECONSTRAINT, '__module__': 'substrait.relations_pb2'}), 'DESCRIPTOR': _RELCOMMON_HINT, '__module__': 'substrait.relations_pb2'}), 'DESCRIPTOR': _RELCOMMON, '__module__': 'substrait.relations_pb2'})
_sym_db.RegisterMessage(RelCommon)
_sym_db.RegisterMessage(RelCommon.Direct)
_sym_db.RegisterMessage(RelCommon.Emit)
_sym_db.RegisterMessage(RelCommon.Hint)
_sym_db.RegisterMessage(RelCommon.Hint.Stats)
_sym_db.RegisterMessage(RelCommon.Hint.RuntimeConstraint)
ReadRel = _reflection.GeneratedProtocolMessageType('ReadRel', (_message.Message,), {'NamedTable': _reflection.GeneratedProtocolMessageType('NamedTable', (_message.Message,), {'DESCRIPTOR': _READREL_NAMEDTABLE, '__module__': 'substrait.relations_pb2'}), 'VirtualTable': _reflection.GeneratedProtocolMessageType('VirtualTable', (_message.Message,), {'DESCRIPTOR': _READREL_VIRTUALTABLE, '__module__': 'substrait.relations_pb2'}), 'ExtensionTable': _reflection.GeneratedProtocolMessageType('ExtensionTable', (_message.Message,), {'DESCRIPTOR': _READREL_EXTENSIONTABLE, '__module__': 'substrait.relations_pb2'}), 'LocalFiles': _reflection.GeneratedProtocolMessageType('LocalFiles', (_message.Message,), {'FileOrFiles': _reflection.GeneratedProtocolMessageType('FileOrFiles', (_message.Message,), {'DESCRIPTOR': _READREL_LOCALFILES_FILEORFILES, '__module__': 'substrait.relations_pb2'}), 'DESCRIPTOR': _READREL_LOCALFILES, '__module__': 'substrait.relations_pb2'}), 'DESCRIPTOR': _READREL, '__module__': 'substrait.relations_pb2'})
_sym_db.RegisterMessage(ReadRel)
_sym_db.RegisterMessage(ReadRel.NamedTable)
_sym_db.RegisterMessage(ReadRel.VirtualTable)
_sym_db.RegisterMessage(ReadRel.ExtensionTable)
_sym_db.RegisterMessage(ReadRel.LocalFiles)
_sym_db.RegisterMessage(ReadRel.LocalFiles.FileOrFiles)
ProjectRel = _reflection.GeneratedProtocolMessageType('ProjectRel', (_message.Message,), {'DESCRIPTOR': _PROJECTREL, '__module__': 'substrait.relations_pb2'})
_sym_db.RegisterMessage(ProjectRel)
JoinRel = _reflection.GeneratedProtocolMessageType('JoinRel', (_message.Message,), {'DESCRIPTOR': _JOINREL, '__module__': 'substrait.relations_pb2'})
_sym_db.RegisterMessage(JoinRel)
FetchRel = _reflection.GeneratedProtocolMessageType('FetchRel', (_message.Message,), {'DESCRIPTOR': _FETCHREL, '__module__': 'substrait.relations_pb2'})
_sym_db.RegisterMessage(FetchRel)
AggregateRel = _reflection.GeneratedProtocolMessageType('AggregateRel', (_message.Message,), {'Grouping': _reflection.GeneratedProtocolMessageType('Grouping', (_message.Message,), {'DESCRIPTOR': _AGGREGATEREL_GROUPING, '__module__': 'substrait.relations_pb2'}), 'Measure': _reflection.GeneratedProtocolMessageType('Measure', (_message.Message,), {'DESCRIPTOR': _AGGREGATEREL_MEASURE, '__module__': 'substrait.relations_pb2'}), 'DESCRIPTOR': _AGGREGATEREL, '__module__': 'substrait.relations_pb2'})
_sym_db.RegisterMessage(AggregateRel)
_sym_db.RegisterMessage(AggregateRel.Grouping)
_sym_db.RegisterMessage(AggregateRel.Measure)
SortRel = _reflection.GeneratedProtocolMessageType('SortRel', (_message.Message,), {'DESCRIPTOR': _SORTREL, '__module__': 'substrait.relations_pb2'})
_sym_db.RegisterMessage(SortRel)
FilterRel = _reflection.GeneratedProtocolMessageType('FilterRel', (_message.Message,), {'DESCRIPTOR': _FILTERREL, '__module__': 'substrait.relations_pb2'})
_sym_db.RegisterMessage(FilterRel)
SetRel = _reflection.GeneratedProtocolMessageType('SetRel', (_message.Message,), {'DESCRIPTOR': _SETREL, '__module__': 'substrait.relations_pb2'})
_sym_db.RegisterMessage(SetRel)
ExtensionSingleRel = _reflection.GeneratedProtocolMessageType('ExtensionSingleRel', (_message.Message,), {'DESCRIPTOR': _EXTENSIONSINGLEREL, '__module__': 'substrait.relations_pb2'})
_sym_db.RegisterMessage(ExtensionSingleRel)
ExtensionLeafRel = _reflection.GeneratedProtocolMessageType('ExtensionLeafRel', (_message.Message,), {'DESCRIPTOR': _EXTENSIONLEAFREL, '__module__': 'substrait.relations_pb2'})
_sym_db.RegisterMessage(ExtensionLeafRel)
ExtensionMultiRel = _reflection.GeneratedProtocolMessageType('ExtensionMultiRel', (_message.Message,), {'DESCRIPTOR': _EXTENSIONMULTIREL, '__module__': 'substrait.relations_pb2'})
_sym_db.RegisterMessage(ExtensionMultiRel)
RelRoot = _reflection.GeneratedProtocolMessageType('RelRoot', (_message.Message,), {'DESCRIPTOR': _RELROOT, '__module__': 'substrait.relations_pb2'})
_sym_db.RegisterMessage(RelRoot)
Rel = _reflection.GeneratedProtocolMessageType('Rel', (_message.Message,), {'DESCRIPTOR': _REL, '__module__': 'substrait.relations_pb2'})
_sym_db.RegisterMessage(Rel)
if _descriptor._USE_C_DESCRIPTORS == False:
    DESCRIPTOR._options = None
    DESCRIPTOR._serialized_options = b'\n\x12io.substrait.protoP\x01\xaa\x02\x12Substrait.Protobuf'
    _RELCOMMON._serialized_start = 157
    _RELCOMMON._serialized_end = 975
    _RELCOMMON_DIRECT._serialized_start = 409
    _RELCOMMON_DIRECT._serialized_end = 417
    _RELCOMMON_EMIT._serialized_start = 419
    _RELCOMMON_EMIT._serialized_end = 464
    _RELCOMMON_HINT._serialized_start = 467
    _RELCOMMON_HINT._serialized_end = 962
    _RELCOMMON_HINT_STATS._serialized_start = 696
    _RELCOMMON_HINT_STATS._serialized_end = 853
    _RELCOMMON_HINT_RUNTIMECONSTRAINT._serialized_start = 855
    _RELCOMMON_HINT_RUNTIMECONSTRAINT._serialized_end = 962
    _READREL._serialized_start = 978
    _READREL._serialized_end = 2415
    _READREL_NAMEDTABLE._serialized_start = 1579
    _READREL_NAMEDTABLE._serialized_end = 1701
    _READREL_VIRTUALTABLE._serialized_start = 1703
    _READREL_VIRTUALTABLE._serialized_end = 1779
    _READREL_EXTENSIONTABLE._serialized_start = 1781
    _READREL_EXTENSIONTABLE._serialized_end = 1843
    _READREL_LOCALFILES._serialized_start = 1846
    _READREL_LOCALFILES._serialized_end = 2402
    _READREL_LOCALFILES_FILEORFILES._serialized_start = 2014
    _READREL_LOCALFILES_FILEORFILES._serialized_end = 2402
    _READREL_LOCALFILES_FILEORFILES_FILEFORMAT._serialized_start = 2323
    _READREL_LOCALFILES_FILEORFILES_FILEFORMAT._serialized_end = 2389
    _PROJECTREL._serialized_start = 2418
    _PROJECTREL._serialized_end = 2659
    _JOINREL._serialized_start = 2662
    _JOINREL._serialized_end = 3211
    _JOINREL_JOINTYPE._serialized_start = 3051
    _JOINREL_JOINTYPE._serialized_end = 3211
    _FETCHREL._serialized_start = 3214
    _FETCHREL._serialized_end = 3442
    _AGGREGATEREL._serialized_start = 3445
    _AGGREGATEREL._serialized_end = 3956
    _AGGREGATEREL_GROUPING._serialized_start = 3758
    _AGGREGATEREL_GROUPING._serialized_end = 3842
    _AGGREGATEREL_MEASURE._serialized_start = 3844
    _AGGREGATEREL_MEASURE._serialized_end = 3956
    _SORTREL._serialized_start = 3959
    _SORTREL._serialized_end = 4184
    _FILTERREL._serialized_start = 4187
    _FILTERREL._serialized_end = 4423
    _SETREL._serialized_start = 4426
    _SETREL._serialized_end = 4852
    _SETREL_SETOP._serialized_start = 4652
    _SETREL_SETOP._serialized_end = 4852
    _EXTENSIONSINGLEREL._serialized_start = 4855
    _EXTENSIONSINGLEREL._serialized_end = 5005
    _EXTENSIONLEAFREL._serialized_start = 5007
    _EXTENSIONLEAFREL._serialized_end = 5117
    _EXTENSIONMULTIREL._serialized_start = 5120
    _EXTENSIONMULTIREL._serialized_end = 5271
    _RELROOT._serialized_start = 5273
    _RELROOT._serialized_end = 5342
    _REL._serialized_start = 5345
    _REL._serialized_end = 5947