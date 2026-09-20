import json
import pandas as pd

from dotenv import load_dotenv
from langchain_groq import ChatGroq

from data_loader import load_reviews
from tools.mood_tool import create_mood_tool
from tools.recommendation_tool import create_recommendation_tool
from agents.moodmate_agent import create_moodmate_agent


# Load environment variables
load_dotenv()


# Create LLM
llm = ChatGroq(
    model="openai/gpt-oss-20b"
)


# Create tools
mood_tool = create_mood_tool(llm)

recommendation_tool = create_recommendation_tool(llm)


# Create MoodMate agent
agent = create_moodmate_agent(
    llm,
    mood_tool,
    recommendation_tool
)


# Load reviews
reviews = load_reviews(limit=5)


results = []


# Process each review
for review in reviews:

    result = agent.invoke(
        {
            "messages": [
                {
                    "role": "user",
                    "content": f"""
                    Analyze this customer review and provide
                    alternative phone recommendations.

                    Product Name: {review["Product Name"]}
                    Review Title: {review["Review Title"]}
                    Rating: {review["Rating"]}
                    Category: {review["Category"]}
                    Comments: {review["Comments"]}
                    """
                }
            ]
        }
    )

    # Get final agent response
    final_response = result["messages"][-1].content

    # Convert JSON string into Python dictionary
    analysis = json.loads(final_response)

    # Store result
    results.append({
        "Product Name": review["Product Name"],
        "Review Title": review["Review Title"],
        "Rating": review["Rating"],
        "Category": review["Category"],
        "Comments": review["Comments"],
        "Sentiment": analysis["sentiment"],
        "Emotion": analysis["emotion"],
        "Suggestion 1": analysis["suggestion_1"],
        "Suggestion 2": analysis["suggestion_2"],
        "Recommendation Message": analysis["message"]
    })


# Create output DataFrame
output_df = pd.DataFrame(results)


# Save results
output_df.to_excel(
    "MoodMate_Analysis.xlsx",
    index=False
)


print("\nAnalysis completed!")
print("Output saved as MoodMate_Analysis.xlsx")