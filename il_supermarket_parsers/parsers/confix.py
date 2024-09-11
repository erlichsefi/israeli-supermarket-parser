from il_supermarket_parsers.engines import BaseFileConverter
from il_supermarket_parsers.documents import XmlDataFrameConverter


class CofixFileConverter(BaseFileConverter):

    def __init__(self) -> None:
        super().__init__(
            price_parsers=XmlDataFrameConverter(
                list_key="Items",
                id_field=["ItemCode", "PriceUpdateDate", "ItemId"],
                roots=["ChainId", "SubChainId", "StoreId", "BikoretNo"],
            ),
            pricefull_parser=XmlDataFrameConverter(
                list_key="Items",
                id_field=["ItemCode", "PriceUpdateDate", "ItemId"],
                roots=["ChainId", "SubChainId", "StoreId", "BikoretNo"],
            ),
        )
