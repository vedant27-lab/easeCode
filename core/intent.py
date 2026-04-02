import google.generativeai as genai

genai.configure(api_key="AIzaSyDATHVOS5HdOMMN-eiPVzFJKGtrjFJEzaE")
model = genai.GenerativeModel("gemini-3.1-pro-preview")