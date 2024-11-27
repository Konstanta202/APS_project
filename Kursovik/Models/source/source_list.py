from Kursovik.Models.source.source import Source
from Kursovik.Models.DataAnalis.data_analysis import Data
import pandas as pd

class SourceList:
    source_list: list[Source]

    def __init__(self, source_count: int, lambda_: float, stats: Data) -> None:
        self.source_list = [Source(i, lambda_, stats) for i in range(source_count)]
    
    def get_source_by_id(self, id: int) -> Source:
        for source in self.source_list:
            if source.get_id() == id:
                return source
    
    def to_df(self) -> pd.DataFrame:
        return pd.DataFrame.from_records(source.__dict__ for source in self.source_list)