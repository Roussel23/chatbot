import os
import google.generativeai as genai

genai.configure(api_key="AIzaSyA98LVWa3dCYxq62gsq5id0ziP5zjrNw84")

# Create the model
generation_config = {
  "temperature": 1,
  "top_p": 0.95,
  "top_k": 40,
  "max_output_tokens": 8192,
  "response_mime_type": "text/plain",
}

model = genai.GenerativeModel(
  model_name="gemini-1.5-flash",
  generation_config=generation_config,
)

chat_session = model.start_chat(
  history=[
  ]
)

response = chat_session.send_message("hi")

print(response.text)