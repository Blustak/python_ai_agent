import os
from typing import Iterable
from dotenv import load_dotenv
from openai import OpenAI
import argparse


model_name = "openrouter/free"

def parse_args(args:Iterable[str]|None=None):
  parser = argparse.ArgumentParser(description="Openrouter AI chatbot")
  parser.add_argument("user_prompt", type=str, help="User's prompt")
  return parser.parse_args(args)

def main():
  load_dotenv()
  api_key = os.environ.get("OPENROUTER_API_KEY")
  if api_key is None:
    raise RuntimeError("OPENROUTER_API_KEY not set; please enter in your .env file, or include as an environment variable when running this script")

  client = OpenAI(
      base_url="https://openrouter.ai/api/v1",
      api_key=api_key
      )

  args = parse_args()
  prompt = args.user_prompt
  response = client.chat.completions.create(
      model=model_name,
      messages=[
        {
          "role":"user",
          "content":prompt
          }
        ]
      )
  if response.usage is None:
    raise RuntimeError("Response usage field is none.")
  prompt_tokens = response.usage.prompt_tokens
  completion_tokens = response.usage.completion_tokens

  print(f"Prompt: {prompt}")
  print(f"Prompt tokens: {prompt_tokens}")
  print(f"Response tokens: {completion_tokens}")
  print("Response:")
  print(response.choices[0].message.content)


if __name__ == "__main__":
    main()
