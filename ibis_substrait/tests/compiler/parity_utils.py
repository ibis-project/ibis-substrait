from abc import ABC, abstractmethod

import datafusion
import pyarrow as pa


class SubstraitConsumer(ABC):
    @abstractmethod
    def with_tables(self, datasets: dict[str, pa.Table]):
        pass

    @abstractmethod
    def execute(self, plan) -> pa.Table:
        pass


class AceroSubstraitConsumer(SubstraitConsumer):
    def __init__(self) -> None:
        super().__init__()

    def with_tables(self, datasets: dict[str, pa.Table]):
        self.datasets = datasets
        return self

    def execute(self, plan) -> pa.Table:
        import pyarrow.substrait as pa_substrait

        def get_table_provider(datasets):
            def table_provider(names, schema):
                return datasets[names[0]]

            return table_provider

        query_bytes = plan.SerializeToString()
        result = pa_substrait.run_query(
            pa.py_buffer(query_bytes),
            table_provider=get_table_provider(self.datasets),
        )

        return result.read_all()


class DatafusionSubstraitConsumer(SubstraitConsumer):
    def __init__(self) -> None:
        self.connection = datafusion.SessionContext()

    def with_tables(self, datasets: dict[str, pa.Table]):
        for k, v in datasets.items():
            self.connection.deregister_table(k)
            self.connection.register_record_batches(k, [v.to_batches()])
        return self

    def execute(self, plan) -> pa.Table:
        plan_data = plan.SerializeToString()
        substrait_plan = datafusion.substrait.serde.deserialize_bytes(plan_data)
        logical_plan = datafusion.substrait.consumer.from_substrait_plan(
            self.connection, substrait_plan
        )

        df = self.connection.create_dataframe_from_logical_plan(logical_plan)
        for column_number, column_name in enumerate(df.schema().names):
            df = df.with_column_renamed(
                column_name, plan.relations[0].root.names[column_number]
            )
        record_batch = df.collect()
        return pa.Table.from_batches(record_batch)
