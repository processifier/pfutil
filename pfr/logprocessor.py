import logging
import pandas as pd
from pfr.engine import *
from pfr.config.schema import *


LOG = logging.getLogger(__name__)


class LogProcessor:
    def __init__(self, input_config):
        self._input_config = input_config

    def get_global_stats(self, tables):
        number_of_variants = len(tables[Variant])
        number_of_cases = len(tables[Case])
        result = pd.DataFrame({GlobalStats.number_of_variants: [number_of_variants],
                      GlobalStats.number_of_cases: [number_of_cases]})
        return result

    def create_model(self, raw_eventlog):
        e_etl = EventlogEtl(self._input_config)
        eventlog = e_etl.create(raw_eventlog)
        vf = VariantFactory()
        variant_df, case_to_variant = vf.create(eventlog)
        cf = CasesFactory(self._input_config)
        case = cf.create(eventlog, case_to_variant)
        tables = {Eventlog: eventlog,
                  Variant: variant_df,
                  Case: case}
        global_stats = self.get_global_stats(tables)
        return tables | {GlobalStats: global_stats}
