from flask import Flask, render_template, request
import requests

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    quiz_content = None
    
    if request.method == "POST":
        # Get the uploaded file
        file = request.files["note_file"]
        if file:
            notes = file.read().decode("utf-8")
            
            # Send to local Ollama
            prompt = f"Create a 3-question multiple-choice quiz based on these notes. Include an answer key at the bottom:\n\n{notes}"
            url = "http://localhost:11434/api/generate"
            data = {
                "model": "qwen2.5:0.5b",
                "prompt": prompt,
                "stream": False
            }
            
            response = requests.post(url, json=data)
            quiz_content = response.json()["response"]
            
    return render_template("index.html", quiz_content=quiz_content)

if __name__ == "__main__":
    app.run(debug=True)