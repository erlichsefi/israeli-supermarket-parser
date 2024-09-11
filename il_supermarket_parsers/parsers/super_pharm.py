from il_supermarket_parsers.engines import BigIDFileConverter
from il_supermarket_parsers.documents import XmlDataFrameConverter


class SuperPharmFileConverter(BigIDFileConverter):
    """for super-pharam"""

    def __init__(self):
        super().__init__(
            promofull_parser=XmlDataFrameConverter(
                list_key="Details",
                id_field=["PromotionId", "PriceUpdateDate", "ItemCode"],
                roots=["ChainId", "SubChainId", "StoreId", "BikoretNo"],
            ),
            promo_parser=XmlDataFrameConverter(
                list_key="Details",
                id_field=["PromotionId", "PriceUpdateDate", "ItemCode"],
                roots=["ChainId", "SubChainId", "StoreId", "BikoretNo"],
            ),
            pricefull_parser=XmlDataFrameConverter(
                list_key="Details",
                id_field=["ItemCode"],
                roots=["ChainId", "SubChainId", "StoreId", "BikoretNo"],
            ),
            price_parser=XmlDataFrameConverter(
                list_key="Details",
                id_field=["ItemCode", "PriceUpdateDate"],
                roots=["ChainId", "SubChainId", "StoreId", "BikoretNo"],
            ),
            stores_parser=XmlDataFrameConverter(
                list_key="Details",
                id_field=["StoreId"],
                roots=["ChainId", "SubChainId"],
            ),
        )
