import pandas as pd
from dotenv import load_dotenv
from langchain.agents import create_agent
from langchain.tools import tool
from langchain_groq import ChatGroq

from data_loader import load_reviews
import json


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


load_dotenv()

llm = ChatGroq(
    model="openai/gpt-oss-20b"
)


@tool
def analyze_mood(message: str) -> str:
    """Analyze the sentiment and emotion expressed in a customer review."""

    response = llm.invoke(
        f"""
        Analyze the following customer review about a mobile phone.

        Review:
        {message}

        Your task is to identify the customer's overall sentiment and
        primary emotion based ONLY on the review content.

        Sentiment must be exactly ONE of:
        - Positive: The customer expresses overall satisfaction or approval.
        - Neutral: The customer is mainly factual, balanced, or shows no clear
        positive or negative feeling.
        - Negative: The customer expresses overall dissatisfaction, criticism,
        or a clearly negative experience.

        Emotion must be exactly ONE primary emotion from:
        Happy, Satisfied, Excited, Neutral, Disappointed, Frustrated,
        Angry, Sad, Confused.

        Choose the emotion that best represents the customer's main feeling.
        Do not simply infer emotion from the rating.
        Consider the Review Title, Category, and Comments together.
        If the review contains both positive and negative points, determine
        the overall sentiment from the customer's overall experience.

        Return ONLY valid JSON.
        Do not include Markdown, explanations, or additional text.

        Required format:
        {{
            "sentiment": "Positive/Neutral/Negative",
            "emotion": "one-word emotion"
        }}
        """
    )

    return get_text(response.content)


agent = create_agent(
    model=llm,
    tools=[analyze_mood],
    system_prompt="""
    You are MoodMate, a customer feedback analysis assistant for mobile phone reviews.

    Your task is to analyze customer feedback for sentiment and emotion.

    Always use the analyze_mood tool to perform the analysis.
    Do not perform the analysis yourself.

    After the tool returns its result, return ONLY the exact JSON produced by the tool.
    Do not modify the values.
    Do not add explanations, Markdown, headings, or additional text.
    """
)


reviews = load_reviews(limit=15) 

results = []

print("Analyzing customer reviews...")

for review in reviews:

    result = agent.invoke(
        {
            "messages": [
                {
                    "role": "user",
                    "content": f"""
                    Analyze this customer review:

                    Review Title: {review["Review Title"]}
                    Category: {review["Category"]}
                    Comments: {review["Comments"]}
                    """
                }
            ]
        }
    )

    analysis = get_text(result["messages"][-1].content)
    analysis = json.loads(analysis)

    results.append({
        "Review Title": review["Review Title"],
        "Rating": review["Rating"],
        "Category": review["Category"],
        "Comments": review["Comments"],
        "Sentiment": analysis["sentiment"],
        "Emotion": analysis["emotion"]
    })



output_df = pd.DataFrame(results)

output_df.to_excel(
    "MoodMate_Analysis.xlsx",
    index=False
)

print("\nAnalysis completed!")
print("Output saved as MoodMate_Analysis.xlsx")