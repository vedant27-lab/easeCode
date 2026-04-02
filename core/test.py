from dotenv import load_dotenv
import google.generativeai as genai
import os

load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

model = genai.GenerativeModel("gemini-3-flash-preview")
#inp = input("Enter your prompt:")
#response = model.generate_content(inp)

#print(response.text)

#while True:
#    try:
#        i = input("Enter your Prompt:")
#        response = model.generate_content(i)
#        print(response.text)
#    except KeyboardInterrupt:
#        break
#    #finally:
#    #    print("Keyboard Interruption!")

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
import json, time



#driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
#driver.get("https://google.com")
#input("Press enter to close")
#driver.quit()

def get_page_fields(driver):
    return driver.execute_script("""
    let fields = [];
    document.querySelectorAll('input, button, textarea').forEach(el =>{
        fields.push({
            tag: el.tagName,
            type: el.type || '',
            id: el.id || '',
            name: el.name || '',
            placeholder: el.placeholder || ''
                                 });
                                 });
        return fields;
    """)

def ask_gemini(commands, fields):
    prompt = f""""""