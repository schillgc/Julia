import config
import openai

openai.api_key = config.api_key

response = openai.Completion.create(
  model="text-davinci-003",
  prompt=input("Input code to be explained what it does:\n"),
  temperature=0,
  max_tokens=150,
  top_p=1.0,
  frequency_penalty=0.0,
  presence_penalty=0.0
)
