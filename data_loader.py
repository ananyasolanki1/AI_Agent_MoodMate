import pandas as pd


def load_reviews(limit=15):
    df = pd.read_csv("redmi.csv")
    return df.head(limit).to_dict(orient="records")