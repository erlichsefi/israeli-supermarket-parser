import shutil
import pytest
import pandas as pd
from kniot_parser.parsers import UnifiedConverter
from kniot_parser.utils import (
    read_dump_folder,
    get_sample_price_data,
    get_sample_store_data,
    get_sample_promo_full_data,
    get_sample_promo_data,
    get_sample_price_full_data,
    get_all_chain_ids
)
from il_supermarket_scarper import ScraperFactory


def check_converting_columns_mergable(folder, expected_store_columns, row_limit=None):
    """create one data frame with all columns"""
    files_to_scan = read_dump_folder(folder=folder)

    all_data_frames = []
    count_empty = 0
    for _, row in files_to_scan.iterrows():

        converter = UnifiedConverter(row["store_name"], row["file_type"])
        data_frame = converter.convert(row["full_path"], row_limit=row_limit)

        sorted_columns_names = sorted(data_frame.columns)
        if data_frame.empty:
            count_empty+=1
        
        if not (
            data_frame.empty
            or (
                len(sorted_columns_names) == len(expected_store_columns)
                and (sorted_columns_names == expected_store_columns)
            )
        ):
            print()
        all_data_frames.append(data_frame.copy())

    final = pd.concat(all_data_frames)
    assert len(final["chainid"].unique()) == len(get_all_chain_ids())
    assert (len(final["file_id"].unique()) + count_empty) == files_to_scan.shape[0]


@pytest.mark.run(order=1)
def test_unifiing_store_columns():
    """test converting to data frame"""

    folder = get_sample_store_data()
    check_converting_columns_mergable(
        folder,
        [
            "address",
            "bikoretno",
            "chainid",
            "chainname",
            "city",
            "file_id",
            "lastupdatedate",
            "lastupdatetime",
            "storeid",
            "storename",
            "storetype",
            "subchainid",
            "subchainname",
            "zipcode",
        ],
    )


@pytest.mark.run(order=2)
def test_unifiing_prices_columns():
    """test converting to data frame"""

    folder = get_sample_price_data()
    check_converting_columns_mergable(
        folder,
        [
            "allowdiscount",
            "bikoretno",
            "bisweighted",
            "chainid",
            "file_id",
            "itemcode",
            "itemid",
            "itemname",
            "itemprice",
            "itemstatus",
            "itemtype",
            "lastupdatedate",
            "lastupdatetime",
            "manufacturecountry",
            "manufactureritemdescription",
            "manufacturername",
            "priceupdatedate",
            "qtyinpackage",
            "quantity",
            "storeid",
            "subchainid",
            "unitofmeasure",
            "unitofmeasureprice",
            "unitqty",
        ],
    )


@pytest.mark.run(order=3)
def test_unifiing_prices_full_columns():
    """test converting to data frame"""

    folder = get_sample_price_full_data()
    check_converting_columns_mergable(
        folder,
        [
            "allowdiscount",
            "bikoretno",
            "bisweighted",
            "chainid",
            "file_id",
            "itemcode",
            "itemid",
            "itemname",
            "itemprice",
            "itemstatus",
            "itemtype",
            'lastupdatedate', 'lastupdatetime',
            "manufacturecountry",
            "manufactureritemdescription",
            "manufacturername",
            "priceupdatedate",
            "qtyinpackage",
            "quantity",
            "storeid",
            "subchainid",
            "unitofmeasure",
            "unitofmeasureprice",
            "unitqty",
        ],
    )

    # shutil.rmtree(folder)


@pytest.mark.run(order=3)
def test_unifiing_promo():
    """test converting to data frame"""

    folder = get_sample_promo_data()
    check_converting_columns_mergable(
        folder,
        [
            "allowmultiplediscounts",
            "bikoretno",
            "chainid",
            "file_id",
            "isgiftitem",
            "itemcode",
            "priceupdatedate",
            "promotiondetails",
            "promotionid",
            "rewardtype",
            "storeid",
            "subchainid",
        ],
    )
    # shutil.rmtree(folder)


@pytest.mark.run(order=3)
def test_unifiing_promo_all():
    """test converting to data frame"""

    folder = get_sample_promo_full_data()
    check_converting_columns_mergable(
        folder,
        [
            "allowdiscount",
            "bikoretno",
            "bisweighted",
            "chainid",
            "file_id",
            "itemcode",
            "itemid",
            "itemname",
            "itemprice",
            "itemstatus",
            "itemtype",
            "manufacturecountry",
            "manufactureritemdescription",
            "manufacturername",
            "priceupdatedate",
            "qtyinpackage",
            "quantity",
            "storeid",
            "subchainid",
            "unitofmeasure",
            "unitofmeasureprice",
            "unitqty",
        ],
    )
    # shutil.rmtree(folder)
