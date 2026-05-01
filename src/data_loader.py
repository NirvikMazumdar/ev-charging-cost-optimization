import pandas as pd


def load_price_data(csv_path):
    df = pd.read_csv(csv_path)

    df.rename(
        columns={
            df.columns[0]: "timestamp",
            df.columns[1]: "price_mwh"
        },
        inplace=True
    )

    df["timestamp"] = pd.to_datetime(df["timestamp"], dayfirst=True)
    df["price"] = df["price_mwh"] / 1000.0
    df["price"] = df["price"].clip(lower=0)

    return df[["timestamp", "price"]].sort_values("timestamp").reset_index(drop=True)