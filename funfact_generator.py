from uagents import Agent, Context
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize the agent
agent = Agent(name="AI_Fun_Fact_Bot", seed="fun_fact_secret")

def get_fun_fact(topic: str) -> str:
    """
    Call LLM API to get a fun fact
    """
    url = "https://api.asi1.ai/v1/chat/completions"
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {os.getenv("ASI1_API_KEY")}'
    }

    prompt = f"""Give me a mind-blowing fun fact about {topic}. 
    Keep it short and surprising!"""

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
async def generate_fun_fact(ctx: Context):
    """
    On startup, fetch a fun fact about a cool topic
    """
    topic = "space"  # Change this for different topics

    ctx.logger.info(f"Fetching fun fact about: {topic}")

    fact = get_fun_fact(topic)

    ctx.logger.info(f"Fun Fact: {fact}")

if __name__ == "__main__":
    agent.run()
