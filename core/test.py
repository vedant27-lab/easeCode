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

def ask_gemini(command, fields):
    prompt = f"""
You control a browser. The user said: "{command}"

Fields on the current page:
{json.dumps(fields, indent=2)}

Reply ONLY with a JSON array of actions. No explanation. No markdown. No code blocks.
Each action must be one of:
  {{"action": "fill", "selector": "id or name value", "by": "id|name|placeholder", "value": "..."}}
  {{"action": "click", "selector": "id or name value", "by": "id|name"}}
  {{"action": "wait", "seconds": 2}}

Example:
[
  {{"action": "fill", "by": "name", "selector": "username", "value": "tomsmith"}},
  {{"action": "fill", "by": "name", "selector": "password", "value": "SuperSecretPassword!"}},
  {{"action": "click", "by": "css", "selector": "button[type=submit]"}}
]
"""
    response = model.generate_content(prompt)
    raw = response.text.strip()
    if "```" in raw:
        raw = raw.split("```")[1]
        if raw.startswith("json"):
            raw = raw[4:]
    
    return json.loads(raw.strip())
def run_actions(driver, actions):
    for step in actions:
        act = step["action"]
        print(f" doing: {step}")
        if act == "fill":
            by = By.ID if step["by"] == "id" else By.NAME if step["by"] == "name" else By.CSS_SELECTOR
            selector = step["selector"] if step["by"] != "placeholder" else f'[placeholder = "{step["selector"]}"]'
            el = driver.find_element(by, selector)
            el.clear()
            el.send_keys(step["value"])
        elif act == "click":
            if step["by"] == "css":
                driver.find_element(By.CSS_SELECTOR, step["selector"]).click()
            else:
                by = By.ID if step["by"] == "id" else By.NAME
                driver.find_element(by, step["selector"]).click()

        elif act == "wait":
            time.sleep(step.get("seconds", 2))

        time.sleep(0.5)

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

url = input("Enter URL: ")

driver.get(url)
time.sleep(2)

command = input("What do you want to do? ")
fields = get_page_fields(driver)
actions = ask_gemini(command, fields)

print("\nGemini's plan:", json.dumps(actions, indent=2))
run_actions(driver, actions)
input("\nDone. Please enter to close.")

response = model.generate_content(command)
print(response.text)

driver.quit()


