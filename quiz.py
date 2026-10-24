import requests

# 1. Read the user's notes from a text file
with open("notes.txt", "r", encoding="utf-8") as file:
    notes = file.read()

# 2. The instruction for the AI
prompt = f"Create a 3-question multiple-choice quiz based on these notes. Include an answer key at the bottom:\n\n{notes}"

# 3. Talk to your local Ollama server
url = "http://localhost:11434/api/generate"
data = {
    "model": "qwen2.5:0.5b",
    "prompt": prompt,
    "stream": False
}

print("Reading notes and asking AI to write your quiz... (this might take a few seconds)")

# 4. Get the response
response = requests.post(url, json=data)
quiz_content = response.json()["response"]

# 5. Save the AI's generated quiz into a new file
with open("quiz.txt", "w", encoding="utf-8") as file:
    file.write(quiz_content)

print("Success! Your quiz has been saved to a new file named: quiz.txt")