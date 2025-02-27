import requests
from uagents import Agent, Context
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize the agent
agent = Agent(name="AI_Advice_Bot", seed="simple_demo_agent")

def get_ai_advice(question: str) -> str:
    """
    Call LLM API to get advice
    """
    url = "https://api.asi1.ai/v1/chat/completions"
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {os.getenv("ASI1_API_KEY")}'
    }

    prompt = f"""You are a wise and humorous AI guru. Answer this question with a mix of wisdom and humor:

    {question}
    
    Keep it short and fun!"""

    payload = {
        "model": "asi1-mini",
        "messages": [{"role": "user", "content": prompt}],
        "temperature": 0.7,
        "max_tokens": 0
    }

    try:
        response = requests.post(url, headers=headers, json=payload)
        response.raise_for_status()
        return response.json()['choices'][0]['message']['content']

    except requests.exceptions.RequestException as e:
        return f"API Request Error: {str(e)}"

    except json.JSONDecodeError:
        return "API Error: Unable to parse JSON response"

@agent.on_event("startup")
async def ask_ai_advice(ctx: Context):
    """
    On startup, ask a life question and get AI advice
    """
    question = "How do I get a job?"  # Change this for different questions

    ctx.logger.info(f"Asking AI: {question}")

    advice = get_ai_advice(question)

    ctx.logger.info(f"AI Advice: {advice}")

if __name__ == "__main__":
    agent.run()
