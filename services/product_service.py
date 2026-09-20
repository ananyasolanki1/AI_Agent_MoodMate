import pandas as pd


MOBILE_DETAILS_PATH = "data/mobile_details.csv"


def load_products():
    return pd.read_csv(MOBILE_DETAILS_PATH)


def get_product(product_name):
    products = load_products()

    product = products[
        products["Product Name"].str.lower() == product_name.lower()
    ]

    if product.empty:
        return None

    return product.iloc[0]


def get_similar_price_products(product_name, price):
    products = load_products()

    lower_price = price * 0.80
    upper_price = price * 1.20

    candidates = products[
        (products["Price"] >= lower_price)
        & (products["Price"] <= upper_price)
        & (products["Product Name"].str.lower() != product_name.lower())
    ].copy()

    candidates["price_difference"] = (
        candidates["Price"] - price
    ).abs()

    return candidates.sort_values("price_difference").head(8)