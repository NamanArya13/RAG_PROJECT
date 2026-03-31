from openai import OpenAI
import os

class LLMService:

    def __init__(self):
        self.client = OpenAI(
            base_url="https://openrouter.ai/api/v1",
            api_key="sk-or-v1-"
        )

    def generate(self, prompt: str) -> str:
        try:
            response = self.client.chat.completions.create(
                model="openrouter/auto", 
                messages=[
                    {
                        "role": "system",
                        "content": "Answer ONLY using the provided context. If not found, say 'I don't know'."
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ]
            )

            return response.choices[0].message.content

        except Exception as e:
            return f"LLM Error: {str(e)}"