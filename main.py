# requests: package — used to call external APIs
import requests

# dotenv: package — loads variables from the .env file
from dotenv import load_dotenv

# langchain.agents: module — create_agent creates an AI agent
from langchain.agents import create_agent

# langchain.tools: module — @tool converts a function into an agent tool
from langchain.tools import tool

# langchain_google_genai: package
# ChatGoogleGenerativeAI: class — connects LangChain to Gemini
from langchain_google_genai import ChatGoogleGenerativeAI


# Converts Gemini's response into readable text
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


# Load the Gemini API key from .env
load_dotenv()


# Create the Gemini model
llm = ChatGoogleGenerativeAI(
    model="gemini-3.6-flash"
)


# @tool converts this function into a tool the agent can call
@tool
def analyze_mood(message: str) -> str:
    """Analyze the mood and emotion expressed in a message."""

    print("\n[TOOL] Mood analysis tool called!")
    print("[TOOL] Sending message to Gemini...")

    # Send the message to Gemini for analysis
    response = llm.invoke(
        f"""
        Analyze the mood of this message.

        Message:
        {message}

        Give:
        1. Mood
        2. Emotion
        3. Short explanation
        """
    )

    print("[TOOL] Gemini response received!")

    return get_text(response.content)


# Create an agent and provide it with the mood-analysis tool
agent = create_agent(
    model=llm,
    tools=[analyze_mood],
    system_prompt="""
    You are MoodMate, a mood-analysis assistant.
    When given a message, use the analyze_mood tool.
    """
)


# Fetch a message from an external API
url = "https://jsonplaceholder.typicode.com/comments/1"

print("[API] Sending GET request...")

response = requests.get(url)

print("[API] Response received!")
print("[API] Status code:", response.status_code)

# Convert JSON response into a Python dictionary
data = response.json()

# Extract the message from the API response
message = data["body"]

print("\nMessage received from external API:")
print(message)


# Send the message to the LangChain agent
print("\n[AGENT] Starting MoodMate agent...")

result = agent.invoke(
    {
        "messages": [
            {
                "role": "user",
                "content": f"Analyze the mood of this message:\n{message}"
            }
        ]
    }
)


# Display the agent's final response
print("\n[AGENT] Agent execution completed!")

print("\nFinal answer:")

final_content = result["messages"][-1].content

print(get_text(final_content))