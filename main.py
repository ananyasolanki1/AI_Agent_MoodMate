from dotenv import load_dotenv
from langchain_groq import ChatGroq

from tools.mood_tool import create_mood_tool
from tools.recommendation_tool import create_recommendation_tool
from agents.moodmate_agent import create_moodmate_agent


load_dotenv()

# Create the Groq LLM
llm = ChatGroq(
    model="openai/gpt-oss-20b"
)

# Create MoodMate tools
mood_tool = create_mood_tool(llm)
recommendation_tool = create_recommendation_tool(llm)

# Create the MoodMate agent
agent = create_moodmate_agent(
    llm,
    mood_tool,
    recommendation_tool
)