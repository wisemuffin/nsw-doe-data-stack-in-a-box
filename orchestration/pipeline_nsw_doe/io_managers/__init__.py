import pandas as pd
from dagster import ConfigurableIOManager, InputContext, OutputContext


class PandasParquetIOManager(ConfigurableIOManager):
    extension: str = ".parquet"
    bucket_name: str
    prefix: str = ""

    def _get_s3_url(self, context: OutputContext) -> str:
        if context.has_asset_key:
            id = context.get_asset_identifier()
        else:
            id = context.get_identifier()
        return f"s3://{self.bucket_name}/{self.prefix}/{'/'.join(id)}.parquet"

    def handle_output(self, context: OutputContext, obj) -> None:
        if obj is None:
            return

        s3_url = self._get_s3_url(context)
        obj.to_parquet(s3_url)

    def load_input(self, context: InputContext):
        s3_url = self._get_s3_url(context)
        return pd.read_parquet(s3_url)


class PandasCSVIOManager(ConfigurableIOManager):
    extension: str = ".parquet"
    bucket_name: str
    prefix: str = ""

    def _get_s3_url(self, context) -> str:
        if context.has_asset_key:
            id = context.get_asset_identifier()
        else:
            id = context.get_identifier()
        return f"s3://{self.bucket_name}/{self.prefix}{'/'.join(id)}.parquet"

    def handle_output(self, context: OutputContext, obj) -> None:
        if obj is None:
            return

        s3_url = self._get_s3_url(context)
        obj.to_parquet(s3_url)

    def load_input(self, context: InputContext):
        s3_url = self._get_s3_url(context)
        return pd.read_parquet(s3_url)
