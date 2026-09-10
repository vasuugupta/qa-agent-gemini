from dataclasses import dataclass
from playwright.sync_api import sync_playwright
@dataclass
class TestStepResult:
    action: str
    target: str
    passed: bool
    detail: str = ""
@dataclass
class BugReport:
    title: str
    steps_to_reproduce: list[str]
    expected: str
    actual: str
    severity: str = "medium"
    def to_markdown(self):
        return f"### 🐞 {self.title}\n**Severity:** {self.severity}\n\n**Expected:** {self.expected}\n**Actual:** {self.actual}"
class BrowserSession:
    def __init__(self, headless=True): self._pw=None; self.browser=None; self.page=None; self.headless=headless
    def start(self): self._pw=sync_playwright().start(); self.browser=self._pw.chromium.launch(headless=self.headless); self.page=self.browser.new_page(); return self
    def stop(self):
        if self.browser: self.browser.close()
        if self._pw: self._pw.stop()
    def navigate_page(self,url):
        try: self.page.goto(url,wait_until="load",timeout=15000); return TestStepResult("navigate",url,True,f"Loaded {url}")
        except Exception as e: return TestStepResult("navigate",url,False,str(e))
    def run_test_case(self,action,selector,value=None,expect_text=None):
        try:
            if action=="click": self.page.click(selector,timeout=5000)
            elif action=="fill": self.page.fill(selector,value or "",timeout=5000)
            elif action=="assert_visible": self.page.wait_for_selector(selector,state="visible",timeout=5000)
            elif action=="assert_text":
                actual=self.page.inner_text(selector,timeout=5000)
                if expect_text not in actual: return TestStepResult(action,selector,False,f"expected '{expect_text}' in '{actual}'")
            else: return TestStepResult(action,selector,False,f"unknown action: {action}")
            return TestStepResult(action,selector,True,"ok")
        except Exception as e: return TestStepResult(action,selector,False,str(e))
