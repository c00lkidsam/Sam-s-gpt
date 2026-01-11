from flask import Flask, request, jsonify, render_template_string
import requests
import os

# Use environment variable for OpenAI key (set this in Render)
API_KEY = os.environ.get("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")
if not API_KEY:
    raise Exception("OPENAI_API_KEY not set! Go to Render > Environment Variables and set it.")

SYSTEM_PROMPT = "You are Sam GPT, a friendly and intelligent chatbot. Talk casually and clearly. No NSFW, no hate."

app = Flask(__name__)
MAX_MESSAGES = 10
messages = [{"role": "system", "content": SYSTEM_PROMPT}]

# Hawk logo URL
HAWK_LOGO_URL = "https://upload.wikimedia.org/wikipedia/commons/1/12/Hawk_icon.png"

HTML_PAGE = f"""
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<title>Sam GPT - Gronk Style</title>
<style>
body {{
    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    background: #0a0a0a;
    color: #fff;
    display: flex;
    flex-direction: column;
    align-items: center;
    padding: 10px;
}}
#header {{
    display: flex;
    align-items: center;
    margin-bottom: 10px;
}}
#logo {{
    width: 50px;
    height: 50px;
    margin-right: 10px;
}}
#title {{
    font-size: 24px;
    font-weight: bold;
    color: #00c6ff;
}}
#chat {{
    max-width: 600px;
    width: 100%;
    height: 70vh;
    overflow-y: auto;
    padding: 10px;
    background: #1a1a1a;
    border-radius: 10px;
    box-shadow: 0 0 20px rgba(0,255,255,0.2);
}}
.message {{
    padding: 12px;
    margin: 6px 0;
    border-radius: 12px;
    max-width: 80%;
    word-wrap: break-word;
    font-size: 16px;
}}
.user {{
    background: linear-gradient(120deg, #ff6a00, #ee0979);
    text-align: right;
    color: #fff;
    margin-left: auto;
}}
.bot {{
    background: linear-gradient(120deg, #00c6ff, #0072ff);
    text-align: left;
    color: #fff;
    margin-right: auto;
}}
#input-area {{
    display: flex;
    margin-top: 10px;
    width: 100%;
    max-width: 600px;
}}
#userInput {{
    flex: 1;
    padding: 12px;
    border-radius: 8px 0 0 8px;
    border: none;
    outline: none;
    font-size: 16px;
}}
button {{
    padding: 12px;
    background: #ff6a00;
    border: none;
    color: #fff;
    font-weight: bold;
    cursor: pointer;
    border-radius: 0 8px 8px 0;
    transition: all 0.2s ease;
}}
button:hover {{
    background: #ee0979;
}}
::-webkit-scrollbar {{
    width: 8px;
}}
::-webkit-scrollbar-thumb {{
    background: #ff6a00;
    border-radius: 4px;
}}
</style>
</head>
<body>
<div id="header">
    <img src="{HAWK_LOGO_URL}" alt="Hawk Logo" id="logo">
    <div id="title">Sam GPT</div>
</div>
<div id="chat"></div>
<div id="input-area">
    <input type="text" id="userInput" placeholder="Type your message...">
    <button>Send</button>
</div>
<script>
window.onload = function() {{
    async function sendMessage() {{
        const input = document.getElementById("userInput");
        const message = input.value;
        if(!message) return;
        addMessage(message,'user');
        input.value='';
        try {{
            const res = await fetch('/chat',{{method:'POST',headers:{{'Content-Type':'application/json'}},body:JSON.stringify({{message}})}});
            const data = await res.json();
            addMessage(data.reply,'bot');
        }} catch (err) {{
            addMessage("Error connecting to server!","bot");
        }}
    }}

    function addMessage(msg,type){{
        const chat=document.getElementById("chat");
        const div=document.createElement("div");
        div.textContent=msg;
        div.className="message "+type;
        chat.appendChild(div);
        chat.scrollTop=chat.scrollHeight;
    }}

    document.querySelector("button").onclick = sendMessage;
    document.getElementById("userInput").onkeypress = function(e){{
        if(e.key==='Enter') sendMessage();
    }}
}}
</script>
</body>
</html>
"""

@app.route("/")
def home():
    return render_template_string(HTML_PAGE)

@app.route("/chat", methods=["POST"])
def chat():
    global messages
    user_input = request.json.get("message")
    messages.append({"role": "user", "content": user_input})

    if len(messages) > MAX_MESSAGES:
        messages = [messages[0]] + messages[-(MAX_MESSAGES-1):]

    try:
        response = requests.post(
            "https://api.openai.com/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {API_KEY}",
                "Content-Type": "application/json"
            },
            json={
                "model": "gpt-4o-mini",
                "messages": messages
            }
        )
        data = response.json()
        # Check if OpenAI returned an error
        if "error" in data:
            reply = f"OpenAI API Error: {data['error']['message']}"
        else:
            reply = data["choices"][0]["message"]["content"]
    except Exception as e:
        reply = f"Server Error: {str(e)}"

    messages.append({"role": "assistant", "content": reply})
    return jsonify({"reply": reply})

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
