import json
from langchain.tools import tool

from services.product_service import (
    get_product,
    get_similar_price_products
)


def get_text(content):
    # Extract text from the LLM response
    if isinstance(content, str):
        return content

    if isinstance(content, list):
        return "\n".join(
            item["text"]
            for item in content
            if item.get("type") == "text"
        )

    return str(content)


def create_recommendation_tool(llm):

    @tool
    def recommend_products(
        product_name: str,
        category: str,
        comments: str,
        sentiment: str,
        emotion: str
    ) -> str:
        """
        Recommend two alternative Redmi/Xiaomi phones based on
        price, review category, comments, sentiment and emotion.
        """

        # Get the current phone from MySQL
        current_product = get_product(product_name)

        if current_product is None:
            return json.dumps({
                "error": f"Product '{product_name}' not found."
            })

        # Get the current phone's price
        current_price = float(current_product["price"])

        # Get similar-priced phones from MySQL
        candidates = get_similar_price_products(
            product_name,
            current_price
        )

        if len(candidates) < 2:
            return json.dumps({
                "error": "Not enough similar-price phones available."
            })

        # Convert database rows into text for the LLM
        candidate_text = "\n".join(
            f"- {row['product_name']} | "
            f"Price: ₹{row['price']} | "
            f"Display: {row['display']} | "
            f"Camera: {row['camera']} | "
            f"Battery: {row['battery']} mAh | "
            f"Processor: {row['processor']} | "
            f"Key Qualities: {row['key_qualities']}"
            for row in candidates
        )

        # Ask the LLM to choose the two most suitable alternatives
        response = llm.invoke(
            f"""
            You are a mobile phone recommendation assistant.

            Current phone:
            {product_name}

            Current phone price:
            ₹{current_price}

            Review category:
            {category}

            Customer comments:
            {comments}

            Sentiment:
            {sentiment}

            Emotion:
            {emotion}

            Available alternative phones:
            {candidate_text}

            Choose exactly TWO phones from the available alternatives.

            Recommendation rules:
            - Consider the customer's review category and comments carefully.
            - Consider the customer's sentiment and emotion.
            - Prefer phones that could address the customer's complaint
              or better match what they value.
            - Keep the alternatives reasonably close in price.
            - Do not recommend the current phone.
            - Do not invent phone names.
            - The two recommendations must be different.

            Also generate ONE short, kind, polite, and empathetic
            recommendation message.

            Return ONLY valid JSON:

            {{
                "suggestion_1": "exact phone name",
                "suggestion_2": "exact phone name",
                "message": "one short recommendation sentence"
            }}
            """
        )

        # Convert the LLM response into normal text
        raw_result = get_text(response.content)

        try:
            # Convert JSON text into a Python dictionary
            result = json.loads(raw_result)

            # Get valid product names from MySQL results
            valid_products = {
                row["product_name"] for row in candidates
            }

            suggestion_1 = result["suggestion_1"]
            suggestion_2 = result["suggestion_2"]

            # Make sure the LLM selected valid and different phones
            if (
                suggestion_1 not in valid_products
                or suggestion_2 not in valid_products
                or suggestion_1 == suggestion_2
            ):
                raise ValueError("Invalid recommendations")

            return json.dumps({
                "suggestion_1": suggestion_1,
                "suggestion_2": suggestion_2,
                "message": result["message"]
            })

        except (json.JSONDecodeError, KeyError, ValueError):

            # Use the first two valid candidates if LLM output fails
            fallback = candidates[:2]

            return json.dumps({
                "suggestion_1": fallback[0]["product_name"],
                "suggestion_2": fallback[1]["product_name"],
                "message": (
                    "If you're considering an exchange, "
                    "you can also explore these similar-priced phones."
                )
            })

    # Return the configured recommendation tool
    return recommend_products