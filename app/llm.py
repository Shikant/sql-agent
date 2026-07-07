import os
from dotenv import load_dotenv
from openai import OpenAI
load_dotenv()
client = OpenAI()
def ask_llm(prompt: str) -> str:
    resp = client.chat.completions.create(
        model='gpt-4o-mini',
        messages=[{'role':'user','content':prompt}])
    return resp.choices[0].message.content
if __name__ == '__main__':
    print(ask_llm('Say hello in one sentence.'))