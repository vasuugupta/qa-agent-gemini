# qa-agent-gemini
Gemini-powered QA agent using Playwright and LangGraph
# QA Agent with Gemini

This project turns a plain-English QA requirement into a structured test plan with Gemini, executes it in a browser with Playwright, and reports failures through a LangGraph workflow.

## Files

- agent/planner.py: Gemini planning and failure analysis.
- agent/tools.py: Playwright browser actions and result objects.
- agent/graph.py: plan -> execute -> report workflow.
- main.py: command-line entry point.

## Run locally or in Colab

Install dependencies and the Playwright browser:

    pip install -r requirements.txt
    playwright install chromium

Set your Gemini key as an environment variable. Do not commit it:

    export GEMINI_API_KEY=your_key_here

Run a test against Sauce Demo:

    python main.py "user can add an item to the cart"

The default test site uses the published practice credentials standard_user / secret_sauce. The Gemini API key is only used for planning and failure explanations; Playwright performs the browser actions.
