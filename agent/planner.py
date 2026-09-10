import os, json
from google import genai
from google.genai import types
GEMINI_MODEL=os.environ.get("GEMINI_MODEL","gemini-3.5-flash-lite")
def _json(prompt, system, schema, model=GEMINI_MODEL):
    key=os.environ.get("GEMINI_API_KEY")
    if not key: raise RuntimeError("GEMINI_API_KEY is not set")
    client=genai.Client(api_key=key)
    try:
        response=client.models.generate_content(model=model,contents=prompt,config=types.GenerateContentConfig(system_instruction=system,response_mime_type="application/json",response_schema=schema,temperature=0))
        return json.loads(response.text)
    finally: client.close()
PLAN_SCHEMA={"type":"OBJECT","properties":{"requirement":{"type":"STRING"},"url":{"type":"STRING"},"steps":{"type":"ARRAY","items":{"type":"OBJECT","properties":{"action":{"type":"STRING"},"selector":{"type":"STRING","nullable":True},"value":{"type":"STRING","nullable":True},"expect_text":{"type":"STRING","nullable":True}},"required":["action","selector","value","expect_text"]}}},"required":["requirement","url","steps"]}
def plan_test_case(requirement,url,context="",model=GEMINI_MODEL):
    prompt=f"Requirement: {requirement}\nURL: {url}\nContext: {context}\nReturn a JSON test plan. Use actions navigate, click, fill, assert_visible, assert_text. Use robust Playwright selectors."
    return _json(prompt,"You are a senior QA engineer. Return only valid JSON matching the schema.",PLAN_SCHEMA,model)
def explain_failure(requirement,failed_step,detail,model=GEMINI_MODEL):
    schema={"type":"OBJECT","properties":{"title":{"type":"STRING"},"expected":{"type":"STRING"},"actual":{"type":"STRING"},"severity":{"type":"STRING","enum":["low","medium","high"]}},"required":["title","expected","actual","severity"]}
    prompt=f"Requirement: {requirement}\nFailed step: {json.dumps(failed_step)}\nFailure: {detail}\nReturn a concise JSON bug report."
    return _json(prompt,"You are a senior QA engineer. Return only JSON.",schema,model)
