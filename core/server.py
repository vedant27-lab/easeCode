import google.generativeai as genai
import subprocess
import webbrowser
import pyautogui
import time
import json

genai.configure(api_key="AIzaSyDATHVOS5HdOMMN-eiPVzFJKGtrjFJEzaE")
model = genai.GenerativeModel("gemini-3.1-pro-preview")

