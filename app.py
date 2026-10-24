from flask import Flask, render_template, request, redirect, url_for, session, send_file
import requests
import os
import uuid

app = Flask(__name__)
# Secret key is required to use sessions
app.secret_key = "hackathon_super_secret"

# Create a folder to temporarily store generated files
os.makedirs("temp_quizzes", exist_ok=True)

@app.route("/", methods=["GET", "POST"])
def index():
    # Page 1: Only file upload
    if request.method == "POST":
        file = request.files.get("note_file")
        if file and file.filename.endswith('.txt'):
            session['notes'] = file.read().decode("utf-8")
            return redirect(url_for('configure'))
    return render_template("index.html")

@app.route("/configure", methods=["GET", "POST"])
def configure():
    if 'notes' not in session:
        return redirect(url_for('index'))
        
    if request.method == "POST":
        session['format'] = request.form.get("format", "txt")
        session['questions'] = request.form.get("questions", "3")
        
        # Keep the prompt simple so the small model doesn't get confused
        prompt = f"Create a {session['questions']}-question multiple-choice quiz based on these notes. "
        if session['format'] == "html":
            prompt += "Format the output using simple HTML tags like <h3> for questions, <ul> and <li> for choices, and <p> for the answer key.\n\n"
        elif session['format'] == "md":
            prompt += "Format output STRICTLY in Markdown.\n\n"
        else:
            prompt += "Format output in plain text.\n\n"
            
        prompt += f"Notes:\n{session['notes']}\n\nInclude an answer key at the bottom."

        try:
            response = requests.post("http://localhost:11434/api/generate", json={
                "model": "qwen2.5:0.5b",
                "prompt": prompt,
                "stream": False
            })
            quiz_content = response.json()["response"]
        except Exception:
            quiz_content = "Error: Could not connect to local Ollama server."

        # Wrap HTML output in a professional styled template
        if session['format'] == "html":
            styled_html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Your AI Quiz</title>
    <style>
        body {{ font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; background-color: #f0f2f5; padding: 40px; color: #333; }}
        .quiz-container {{ max-width: 800px; margin: auto; background: white; padding: 40px; border-radius: 12px; box-shadow: 0 4px 15px rgba(0,0,0,0.1); }}
        h1 {{ color: #4f46e5; text-align: center; border-bottom: 2px solid #eee; padding-bottom: 20px; }}
        h3 {{ color: #2c3e50; margin-top: 30px; }}
        ul {{ list-style-type: none; padding: 0; }}
        li {{ background: #f8fafc; margin: 10px 0; padding: 15px; border-radius: 8px; border: 1px solid #e2e8f0; }}
        .answer-key {{ margin-top: 40px; padding: 20px; background: #e0e7ff; border-radius: 8px; font-weight: bold; }}
    </style>
</head>
<body>
    <div class="quiz-container">
        <h1>🎯 Your AI Generated Quiz</h1>
        {quiz_content.replace('Answer Key', '<div class="answer-key">Answer Key</div>')}
    </div>
</body>
</html>"""
            final_content = styled_html
        else:
            final_content = quiz_content

        # Save to a unique temporary file
        filename = f"temp_quizzes/quiz_{uuid.uuid4().hex}.{session['format']}"
        with open(filename, "w", encoding="utf-8") as f:
            f.write(final_content)
            
        session['last_file'] = filename
        session['quiz_content'] = quiz_content # Show raw text in preview
        return redirect(url_for('result'))
        
    return render_template("configure.html")

@app.route("/result")
def result():
    # Page 3: Preview and Download
    if 'quiz_content' not in session:
        return redirect(url_for('index'))
    return render_template("result.html", content=session['quiz_content'])

@app.route("/download")
def download():
    # Endpoint to handle the file download
    filename = session.get('last_file')
    ext = session.get('format', 'txt')
    if filename and os.path.exists(filename):
        return send_file(filename, as_attachment=True, download_name=f"Note2Quiz.{ext}")
    return redirect(url_for('index'))

if __name__ == "__main__":
    app.run(debug=True)