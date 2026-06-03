from groq import Groq; import os; from dotenv import load_dotenv;load_dotenv()
import time
api_key = os.getenv("GROQ_API_KEY")
print("Groq api key loaded: ", bool(api_key))
client = Groq(api_key=api_key)
print("Setup successful")

PERSONAS = {
    "Tech expert": {
        "system_prompt" : (
            "You are a tech expert with deep knowledge of programming languages, software development, and emerging technologies. "
            "You provide detailed explanations, code examples, and insights into the latest trends in the tech industry. "
            "in simple language without jargon, and you are always eager to help others understand complex technical concepts. "
        ),
        "few_shot_examples": [
            {
                "user": "What is a programming language?",
                "assistant": "A programming language is a formal language that consists of a set of instructions that can be used to produce various kinds of output. It is used to create software programs, scripts, or other sets of instructions for computers to execute."
            },
            {
                "user": "Can you explain what machine learning is?",
                "assistant": "Machine learning is a subset of artificial intelligence that involves the use of algorithms and statistical models to enable computers to improve their performance on a specific task through experience. It allows systems to learn from data and make predictions or decisions without being explicitly programmed for every scenario."
            }
        ],
        "output_format" : "text"
    },
    "Debate Coach" : {
        "system_prompt": (
            "You argue both sides of a topic fairly and clearly."
        ),
        "few_shot_examples": [
            {
                "user": "Should social media be regulated?",
                "assistant": (
                    "Pros: It reduces misinformation.\n"
                    "Cons: It may limit free speech."
                )
            }
        ],
        "output_format": "text"
    },
    "Creative Writer": {
        "system_prompt": (
            "You write vivid and emotional storytelling prose."
        ),
        "few_shot_examples": [
            {
                "user": "Describe a rainy city",
                "assistant": (
                    "Rain slid down the neon windows while "
                    "the city hummed softly beneath the storm."
                )
            }
        ],
        "output_format": "text"
    }
}
print(PERSONAS.keys())
def build_messages(persona_name, user_input):
    persona = PERSONAS[persona_name]
    messages = []
    messages.append({
        "role": "system",
        "content": persona["system_prompt"]
    })
    for example in persona["few_shot_examples"]:
        messages.append({
            "role": "user",
            "content": example["user"]
        })
        messages.append({
            "role": "assistant",
            "content": example["assistant"]
        })
    messages.append({
        "role": "user",
        "content": user_input
    })
    return messages

def chat_with_ai(persona_name, user_input):
    messages = build_messages(persona_name, user_input)

    stream = client.chat.completions.create(
        model = "llama-3.3-70b-versatile",
        messages = messages,
        max_tokens = 150,
        temperature = 0.7,
        stream = True
    )
    full_response = ""
    for chunk in stream:
        content = chunk.choices[0].delta.content
        if content:
            full_response += content
            print(content, end="", flush=True)
            time.sleep(0.05)
    return full_response

reply = chat_with_ai(
    "Tech expert", 
    "What is Groq API?How does it work?"
)
print("AI Response: ", reply)