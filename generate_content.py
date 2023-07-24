import sys
import json
import time
import asyncio
from langchain.llms import OpenAIChat
import os

# Load API Key
os.environ["OPENAI_API_KEY"]

async def async_generate(llm, topic, module):
  resp = await llm.agenerate([
    f"You are a helpful assistant that provides explanations for modules in a learning topic. Explain the {module} module for learning the topic: {topic} in great detail with examples if needed. Format response in markdown."
  ])
  return resp.generations[0][0].text


async def generate_concurrently(topic, sections):
  llm = OpenAIChat(temperature=0.9)
  tasks = [async_generate(llm, topic, module) for module in sections]
  results = await asyncio.gather(*tasks)
  return results


def save_to_json(topic, sections, contents):
  content_data = {
    section: content
    for section, content in zip(sections, contents)
  }
  with open(f"{topic}_content.json", "w") as f:
    json.dump(content_data, f, indent=4)


def async_main(topic, sections):
  s = time.perf_counter()
  contents = asyncio.run(generate_concurrently(topic, sections))
  elapsed = time.perf_counter() - s

  save_to_json(topic, sections, contents)



if __name__ == "__main__":
  user_topic = sys.argv[1]
  sections = sys.argv[2:]
  async_main(user_topic, sections)
