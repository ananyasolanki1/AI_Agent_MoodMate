import pandas as pd   # Data analysis library

def load_reviews(limit=5):
    df = pd.read_csv("data/redmi_reviews.csv")
    
    # Convert each row into a dictionary (each row = one record)
    return df.head(limit).to_dict(orient="records")


def load_mobile_details():
    return pd.read_csv("data/mobile_details.csv")