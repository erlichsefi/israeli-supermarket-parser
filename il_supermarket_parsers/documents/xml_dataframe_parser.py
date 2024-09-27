import pandas as pd
from il_supermarket_parsers.utils import (
    count_tag_in_xml,
    collect_unique_keys_from_xml,
    collect_unique_columns_from_nested_json,
)
from .base import XmlBaseConverter


class XmlDataFrameConverter(XmlBaseConverter):
    """parser the xml docuement"""

    def reduce_size(self, data):
        for col in data.columns:
            data[col] = data[col].mask(data[col] == data[col].shift())
        return data

    def validate_succussful_extraction(self, data, source_file):
        # if there is an empty file
        # we expected it to reuturn none
        tag_count = count_tag_in_xml(source_file, self.id_field)

        if tag_count > 0:
            for root in self.roots:
                if root not in data.columns:
                    raise ValueError(
                        f"parse error, columns {root} missing from {data.columns}"
                    )

            if self.id_field not in data.columns:
                raise ValueError(
                    f"parse error, id {self.id_field} missing from {data.columns}"
                )

            if data.shape[0] != max(tag_count, 1):
                raise ValueError("missing data")

            keys_not_used = (
                set(collect_unique_keys_from_xml(source_file))
                - collect_unique_columns_from_nested_json(data)
                - set(self.ignore_column)
            )
            if len(keys_not_used) > 0:
                raise ValueError(f"there is data we didn't get {keys_not_used}")

    def _phrse(
        self,
        root,
        found_folder,
        file_name,
        root_store,
        **kwarg,
    ):
        rows = []

        # if not root and "Super-Pharm" in file:
        #     return pd.DataFrame()  # shufersal don't add count=0

        if root is None:
            raise ValueError(f"{self.list_key} is wrong")

        elements = list(root)
        if len(root) == 0:
            columns = [self.id_field] + self.roots
            return pd.DataFrame(columns=columns)

        for elem in elements:

            values = {
                "found_folder": found_folder,
                "file_name": file_name,
                **root_store,
            }
            for name in list(elem):
                tag = name.tag
                value = self.build_value(name, no_content="")

                values[tag] = value
            rows.append(values.copy())

        return pd.DataFrame(rows)
