from flask import Flask, request, jsonify, render_template_string
import requests
import os

# Your OpenAI API Key
API_KEY = "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"

SYSTEM_PROMPT = "You are Sam GPT, a friendly and intelligent chatbot. Talk casually and clearly. No NSFW, no hate."

app = Flask(__name__)
MAX_MESSAGES = 10
messages = [{"role": "system", "content": SYSTEM_PROMPT}]

# Hawk logo URL
HAWK_LOGO_URL = "https://upload.wikimedia.org/wikipedia/commons/1/12/Hawk_icon.png"

# HTML + CSS + JS all in one
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
    max-wid
