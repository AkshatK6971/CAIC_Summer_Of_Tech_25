import os
from dotenv import load_dotenv
from groq import Groq
from google import genai
from google.genai import types as gtypes

load_dotenv()
groq_key = os.getenv("GROQ_KEY")
gemini_key = os.getenv("GEMINI_KEY")
groq_client = Groq(api_key=groq_key)
gemini_client = genai.Client(api_key=gemini_key)

def call_groq_api(prompt):
    chat_completion = groq_client.chat.completions.create(
        messages=[
            {
                "role": "system",
                "content": (
                    "You are Agent-A, a concise domain expert. "
                    "Answer the user's question accurately in one paragraph."
                ),
            },
            {
                "role": "user",
                "content": prompt,
            }
        ],
        model="llama3-8b-8192",
        temperature=0.7,
    )
    return chat_completion.choices[0].message.content


def call_gemini_api(prompt, prompt_ans):
    sys_msg = ("You are Agent-B, a meticulous critic. "
                  "Evaluate the expert's answer for correctness, clarity, and completeness. "
                  "If fixes are needed, provide them; otherwise confirm it is correct.")
    
    resp = gemini_client.models.generate_content(
        model="gemini-2.0-flash",
        contents=f"Original question: {prompt}\n\nExpert answer: {prompt_ans}\n\nYour critique:",
        config=gtypes.GenerateContentConfig(
            temperature=0.5,
            max_output_tokens=500,
            system_instruction=sys_msg,
        )
    )
    return resp.text.strip()

def run_bot():
    while True:
        try:
            prompt = input("[YOU] ").strip()
        except (KeyboardInterrupt, EOFError):
            print("Exiting the bot. Goodbye!"); 
            break

        if prompt.lower() in ["exit", "quit"]:
            print("Exiting the bot. Goodbye!")
            break
        if not prompt:
            continue

        try:
            response = call_groq_api(prompt)
            print(f"[GROQ_BOT]: {response}")
        except Exception as e:
            print(f"[GROQ_BOT_EXCEPTION]: {e}")
        
        try:
            crit_response = call_gemini_api(prompt, response)
            print(f"[GEMINI_BOT]: {crit_response}")
        except Exception as e:
            print(f"[GEMINI_BOT_EXCEPTION]: {e}")

if __name__ == "__main__":
    run_bot()