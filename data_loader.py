import pandas as pd   # Data analysis library

def load_reviews(limit=15):
    df = pd.read_csv("redmi.csv")
    
    # Convert each row into a dictionary (each row = one record)
    return df.head(limit).to_dict(orient="records")