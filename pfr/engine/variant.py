import pandas as pd
from collections import defaultdict
from pm4py.objects.conversion.log import converter as log_converter
from pm4py.algo.filtering.log.variants import variants_filter
import hashlib
from collections import Counter

from pfr.config.schema import Eventlog, Variant


class VariantFactory:

    def create(self, eventlog):
        variants_map, variants_pm4py = self._get_variants_mapping(eventlog)
        case_to_variant = self._get_case_to_variants(variants_pm4py, variants_map)
        variants_df = self._get_variants_stats(case_to_variant, variants_map)
        return variants_df, case_to_variant

    def _convert_log(self, eventlog):
        df = eventlog.copy(deep=True)
        df.rename(columns={Eventlog.case_id.name: 'case:concept:name',
                           Eventlog.activity_start_ts.name: 'time:timestamp',
                           Eventlog.activity.name: 'concept:name'}, inplace=True)
        result = log_converter.apply(df, variant=log_converter.Variants.TO_EVENT_LOG)
        return result

    def _get_variants_mapping(self, eventlog):
        df = eventlog.copy(deep=True)
        converted_log = self._convert_log(df)
        variants_pm4py = variants_filter.get_variants(converted_log)
        variants_map = self._label_variants(variants_pm4py)
        return variants_map, variants_pm4py

    def _label_variants(self, variants_pm4py):
        variants_map = {}
        index = 0
        for v in variants_pm4py:
            variants_map[v] = index
            index = index + 1
        return variants_map

    def _get_case_to_variants(self, variants_pm4py, variants_map):
        variants = variants_pm4py
        variants_list = list(variants)
        case_to_variant = defaultdict()
        for v in variants_list:
            for case in variants[v]:
                case_to_variant[case._attributes["concept:name"]] = variants_map[v]
        return case_to_variant

    def _get_variants_stats(self, case_to_variant, variants_map):
        hash_df = pd.DataFrame(list(variants_map.items()),
                          columns=["_tmp_activity_name", Variant.id.name])
        hash_df[Variant.variant_hash.name] = (hash_df.apply(lambda row: hashlib.sha512(str(row["_tmp_activity_name"])
                                                                                       .encode()).hexdigest(), axis=1))
        variant2hash = dict(zip(hash_df[Variant.id.name], hash_df[Variant.variant_hash.name]))
        df = pd.DataFrame(variant2hash.items(),
                          columns=[Variant.id.name, Variant.variant_hash.name])
        variant_freq = Counter(case_to_variant.values())
        df[Variant.variant_freq.name] = df.apply(lambda row: variant_freq[row[Variant.id.name]], axis=1)
        df.sort_values(by=[Variant.variant_freq.name], inplace=True, ascending=False)
        df[Variant.variant_rank.name] = range(1, len(df)+1)
        return df
