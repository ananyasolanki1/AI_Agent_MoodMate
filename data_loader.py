import pandas as pd


def load_reviews(limit=1):
    # Load review data from the CSV
    df = pd.read_csv("data/redmi_reviews.csv")

    # Convert selected rows into dictionaries for the agent
    return df.head(limit).to_dict(orient="records")