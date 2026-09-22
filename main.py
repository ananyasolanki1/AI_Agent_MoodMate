from dotenv import load_dotenv
from langchain_groq import ChatGroq

from tools.mood_tool import create_mood_tool
from tools.recommendation_tool import create_recommendation_tool
from agents.reviewmate_agent import create_reviewmate_agent


load_dotenv()

# Create the Groq LLM
llm = ChatGroq(
    model="openai/gpt-oss-20b"
)

# Create ReviewMate tools
mood_tool = create_mood_tool(llm)
recommendation_tool = create_recommendation_tool(llm)

# Create the ReviewMate agent
agent = create_reviewmate_agent(
    llm,
    mood_tool,
    recommendation_tool
)