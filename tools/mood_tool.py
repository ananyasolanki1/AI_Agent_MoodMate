from langchain.tools import tool


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


def create_mood_tool(llm):

    @tool
    def analyze_mood(
        product_name: str,
        review_title: str,
        category: str,
        comments: str
    ) -> str:
        """Analyze sentiment and primary emotion of a mobile phone review."""

        response = llm.invoke(
            f"""
            Analyze this customer review about a mobile phone.

            Product Name: {product_name}
            Review Title: {review_title}
            Category: {category}
            Comments: {comments}

            Sentiment must be exactly one:
            Positive, Neutral, Negative

            Emotion must be exactly one:
            Happy, Satisfied, Excited, Neutral, Disappointed,
            Frustrated, Angry, Sad, Confused

            Consider the actual review content.
            Do not rely only on the rating.

            Return ONLY valid JSON:

            {{
                "sentiment": "Positive/Neutral/Negative",
                "emotion": "one-word emotion"
            }}
            """
        )

        return get_text(response.content)

    return analyze_mood