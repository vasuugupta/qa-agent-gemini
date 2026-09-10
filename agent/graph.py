from typing import TypedDict
from langgraph.graph import StateGraph, END
from .tools import BrowserSession, BugReport
from .planner import plan_test_case, explain_failure
class AgentState(TypedDict):
    requirement:str; url:str; context:str; plan:list[dict]; step_index:int; results:list; bugs:list; done:bool
def make_graph(session):
    def plan_node(state):
        state["plan"]=plan_test_case(state["requirement"],state["url"],state.get("context",""))["steps"]; state["step_index"]=0; return state
    def execute_node(state):
        step=state["plan"][state["step_index"]]
        result=session.navigate_page(state["url"]) if step["action"]=="navigate" else session.run_test_case(step["action"],step.get("selector"),step.get("value"),step.get("expect_text"))
        state["results"].append(result)
        if not result.passed:
            bug=explain_failure(state["requirement"],step,result.detail)
            state["bugs"].append(BugReport(bug["title"],[f"{r.action} {r.target}" for r in state["results"]],bug["expected"],bug["actual"],bug.get("severity","medium")))
        state["step_index"]+=1; return state
    def next_step(state): return "end" if state["step_index"]>=len(state["plan"]) or (state["results"] and not state["results"][-1].passed) else "continue"
    g=StateGraph(AgentState); g.add_node("plan",plan_node); g.add_node("execute",execute_node); g.set_entry_point("plan"); g.add_edge("plan","execute"); g.add_conditional_edges("execute",next_step,{"continue":"execute","end":END}); return g.compile()
def run_requirement(requirement,url,context="",headless=True):
    session=BrowserSession(headless).start()
    try:
        return make_graph(session).invoke({"requirement":requirement,"url":url,"context":context,"plan":[],"step_index":0,"results":[],"bugs":[],"done":False})
    finally: session.stop()
