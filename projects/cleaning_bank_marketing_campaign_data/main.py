# -*- coding: utf-8 -*-
# @Author: VU Anh Tuan
# @Date:   2024-08-28 14:55:27
# @Last Modified by:   VU Anh Tuan
# @Last Modified time: 2024-08-28 18:00:30

"""
Project: Cleaning Bank Marketing Campaign Data
"""

from datetime import datetime
from enum import Enum
from pathlib import Path
from typing import List, Tuple

import numpy as np
import pandas as pd


class Constant(Enum):
    """
    Class of constant values
    """

    CLIENT_COLS = (
        "client_id",
        "age",
        "job",
        "marital",
        "education",
        "credit_default",
        "mortgage",
    )
    CAMPAIGN_COLS = (
        "client_id",
        "number_contacts",
        "contact_duration",
        "previous_campaign_contacts",
        "previous_outcome",
        "campaign_outcome",
        "day",
        "month",
    )
    ECONOMICS_COLS = ("client_id", "cons_price_idx", "euribor_three_months")
    SOURCE_FILE = "bank_marketing.csv"
    CLIENT_FILE = "client.csv"
    CAMPAIGN_FILE = "campaign.csv"
    ECONOMICS_FILE = "economics.csv"

    def __str__(self) -> str:
        return str(self.value)

    @property
    def to_list(self) -> List[str]:
        """
        Converts object to list
        """
        return list(self.value)


def clean_na(df_data: pd.DataFrame, *cols: Tuple[str, ...]) -> pd.DataFrame:
    """
    Returns dataframe which have cleaned "N/A" value in the given columns.
    """
    df_cleaned = df_data
    for col in cols:
        df_cleaned = df_cleaned[df_cleaned[col] != "N/A"]
    return df_cleaned


def dot_to_underscore(df_data: pd.DataFrame, *cols: Tuple[str, ...]) -> None:
    """
    Converts dot in values of given columns to underscore.
    """
    for col in cols:
        df_data[col] = df_data[col].str.replace(".", "_", regex=False)


def get_bool_value(value: str, ground_truth: str) -> int:
    """
    Returns 1 if the given value equals ground truth, otherwise 0
    """
    return 1 if value == ground_truth else 0


def value_to_boolean(df_data: pd.DataFrame, *col_vals: Tuple[Tuple[str, str], ...]) -> None:
    """
    Converts value in the given column to 1 if it equals the given ground truth, otherwise 0
    """
    for col, ground_truth in col_vals:
        df_data[col] = df_data[col].apply(get_bool_value, args=(ground_truth,))
        df_data[col] = df_data[col].astype("bool")


def get_client_data(df_data: pd.DataFrame) -> pd.DataFrame:
    """
    Returns client data cleaned from the given bank marketing data
    """
    df_client = df_data[Constant.CLIENT_COLS.to_list]
    df_client = clean_na(df_client, "client_id", "age", "marital")
    dot_to_underscore(df_client, "job", "education")
    value_to_boolean(df_client, ("credit_default", "yes"), ("mortgage", "yes"))
    df_client["education"] = df_client["education"].replace("unknown", np.nan)
    return df_client


def get_campaign_data(df_data: pd.DataFrame) -> pd.DataFrame:
    """
    Returns campaign data cleaned from the given bank marketing data
    """
    df_campaign = df_data[Constant.CAMPAIGN_COLS.to_list]
    df_campaign = clean_na(
        df_campaign,
        "client_id",
        "number_contacts",
        "contact_duration",
        "previous_campaign_contacts",
    )
    value_to_boolean(df_campaign, ("previous_outcome", "success"), ("campaign_outcome", "yes"))
    df_campaign["last_contact_date"] = df_campaign.apply(
        lambda row: datetime.strptime(f"{row['month'].title()} {row['day']} 2022", "%b %d %Y"),
        axis=1,
    )
    df_campaign.drop(["day", "month"], axis=1, inplace=True)
    return df_campaign


def get_economics_data(df_data: pd.DataFrame) -> pd.DataFrame:
    """
    Returns economics data cleaned from the given bank marketing data
    """
    df_economics = df_data[Constant.ECONOMICS_COLS.to_list]
    df_economics = clean_na(df_economics, "client_id", "cons_price_idx", "euribor_three_months")
    return df_economics


def main():
    """
    Main function
    """
    base_dir = Path(__file__).parent
    dispatcher = {
        Constant.CLIENT_FILE: get_client_data,
        Constant.CAMPAIGN_FILE: get_campaign_data,
        Constant.ECONOMICS_FILE: get_economics_data,
    }
    df_data = pd.read_csv(base_dir.joinpath(f"{Constant.SOURCE_FILE}"))

    for filename, func in dispatcher.items():
        file_path = base_dir.joinpath(f"{filename}")
        df_cleaned = func(df_data)
        df_cleaned.to_csv(file_path, index=False)
        print(f"{filename.name.replace('_', ' ').lower()} was created at {file_path}.")


if __name__ == "__main__":
    main()
