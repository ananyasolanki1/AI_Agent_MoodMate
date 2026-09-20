import json
from langchain.tools import tool

from services.product_service import (
    get_product,
    get_similar_price_products
)


def get_text(content):
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

        # 1. Find the current phone
        current_product = get_product(product_name)

        if current_product is None:
            return json.dumps({
                "error": f"Product '{product_name}' not found."
            })

        current_price = float(current_product["Price"])

        # 2. Find phones in a similar price range
        candidates = get_similar_price_products(
            product_name,
            current_price
        )

        if len(candidates) < 2:
            return json.dumps({
                "error": "Not enough similar-price phones available."
            })

        # 3. Prepare candidate information for the LLM
        candidate_text = "\n".join(
            f"- {row['Product Name']} | Price: ₹{row['Price']} | "
            f"Display: {row['Display']} | "
            f"Camera: {row['Camera']} | "
            f"Battery: {row['Battery (mAh)']} mAh | "
            f"Processor: {row['Processor']} | "
            f"Key Qualities: {row['Key Qualities']}"
            for _, row in candidates.iterrows()
        )

        # 4. Ask LLM to choose the most relevant alternatives
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

            The message should:
            - Acknowledge the customer's experience naturally.
            - Sound helpful and respectful, never pushy or sales-like.
            - Be concise: one short sentence only.
            - If the customer is satisfied or the review is casual,
            present the alternatives as optional, without implying
            that they need a new phone.
            - If the review is negative, acknowledge their concern
            briefly and suggest the alternatives as an optional
            exchange.

            Return ONLY valid JSON:

            {{
                "suggestion_1": "exact phone name",
                "suggestion_2": "exact phone name",
                "message": "one short recommendation sentence"
            }}
            """
        )

        raw_result = get_text(response.content)

        try:
            result = json.loads(raw_result)

            valid_products = set(candidates["Product Name"])

            suggestion_1 = result["suggestion_1"]
            suggestion_2 = result["suggestion_2"]

            # Validate LLM recommendations
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

            # Safe fallback if LLM returns invalid output
            fallback = candidates.head(2)

            return json.dumps({
                "suggestion_1": fallback.iloc[0]["Product Name"],
                "suggestion_2": fallback.iloc[1]["Product Name"],
                "message": (
                    "If you're considering an exchange, "
                    "you can also explore these similar-priced phones."
                )
            })

    return recommend_products