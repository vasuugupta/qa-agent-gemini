"""CLI entry point for the Gemini-powered QA agent."""
import sys
from dotenv import load_dotenv
from agent.graph import run_requirement
load_dotenv()
DEFAULT_URL = "https://www.saucedemo.com"
DEFAULT_CONTEXT = ("This is Sauce Demo. Log in first if the requirement needs it, using " "username 'standard_user' and password 'secret_sauce', selectors " "#user-name, #password, #login-button. After login the app lands on " "the inventory page. 'Add to cart' buttons use data-test attributes " "like [data-test='add-to-cart-sauce-labs-backpack']. Cart badge is " "'.shopping_cart_badge'.")
def main():
    if len(sys.argv) < 2:
        print('Usage: python main.py "<requirement>" ["<url>"] ["<context>"]')
        sys.exit(1)
    requirement = sys.argv[1]
    url = sys.argv[2] if len(sys.argv) > 2 else DEFAULT_URL
    context = sys.argv[3] if len(sys.argv) > 3 else (DEFAULT_CONTEXT if url == DEFAULT_URL else "")
    print(f"\n🧪 Testing: {requirement}\n🌐 Target: {url}\n")
    final_state = run_requirement(requirement, url, context, headless=True)
    print("── Steps run ──")
    for r in final_state["results"]:
        status = "✅" if r.passed else "❌"
        print(f"{status} {r.action} {r.target} — {r.detail}")
    if final_state["bugs"]:
        print("\n── Bugs found ──")
        for bug in final_state["bugs"]: print(bug.to_markdown())
    else: print("\n✅ No bugs found — all steps passed.")
if __name__ == "__main__": main()
