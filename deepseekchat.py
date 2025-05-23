from flask import Flask, request, jsonify
from flask_cors import CORS
import ollama

full_transcript = [
    {"role":"system", "content":"you are a banking assistant, you should keep your answers short and concise, maximum 200 characters, and respond fast, maximum 1 second."}
]

app = Flask(__name__)
CORS(app)

def generate_response(prompt):
    """
    Generate a response by calling the Deepseek model through Ollama.
    Make sure that Ollama is installed and Deepseek is set up locally.
    """
    # # Construct the command to call Deepseek via Ollama
    # command = ["ollama", "run", "deepseek", "--prompt", prompt]

    # print(prompt)
    # Run the command and capture the output
    response = ollama.chat(
        model = "deepseek-r1:7b",
        messages = prompt
    )
    answer = response.message.content

    # print("DeepSeek R1:", end="\r\n")
    # text_buffer = ""
    # full_text = ""

    # print(ollama_stream, flush=True)
    # for chunk in ollama_stream:
    #     text_buffer += chunk['message']['content']
    #     if text_buffer.endswith('.'):
    #         print(text_buffer, end="\n", flush=True)
    #         full_text += text_buffer
    #         text_buffer = ""

    # if text_buffer:
    #     print(text_buffer, end="\n", flush=True)
    #     full_text += text_buffer

    # print(full_text)
    del full_transcript[-1]
    # full_transcript.append({"role":"assistant", "content":answer})

    return answer

@app.route("/chat", methods=["POST"])
def chat():
    """
    API endpoint to receive a user message and return a chatbot response.
    """
    data = request.get_json()
    user_message = data.get("message", "")
    full_transcript.append({"role":"user", "content":data.get("message", "")})
    user_message = full_transcript
    if not user_message:
        return jsonify({"error": "No message provided"}), 400
    print(full_transcript)
    response_text = generate_response(user_message)
    return jsonify({"response": response_text})

# Optionally, serve the frontend from the Flask app
@app.route("/")
def home():
    return app.send_static_file("index.html")

if __name__ == "__main__":
    app.run(debug=True, port=5005)
    # chat()
