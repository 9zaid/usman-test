"""Ops agent: answers questions and runs maintenance tasks.

Test fixture for the Cytex AI-BOM scanner: excessive agency on purpose.
"""
import os
import subprocess

from crewai import Agent, Crew, Task
from langchain_community.tools import ShellTool
from langchain_core.tools import tool
from langchain_openai import ChatOpenAI
from langgraph.prebuilt import create_react_agent

llm = ChatOpenAI(model="gpt-4o", temperature=0)


@tool
def run_command(command: str) -> str:
    """Run a shell command on the host and return its output."""
    # The model picks the command (cytex-ai.py.agent-tool-shell-exec).
    return subprocess.run(command, shell=True, capture_output=True, text=True).stdout


@tool
def evaluate(expression: str) -> str:
    """Evaluate a Python expression."""
    return str(eval(expression))


# Built-in shell tool handed to the model (cytex-ai.py.agent-builtin-shell-tool).
shell = ShellTool()

ops_agent = create_react_agent(llm, tools=[run_command, evaluate, shell])


def answer(question: str) -> str:
    result = ops_agent.invoke({"messages": [("user", question)]})
    return result["messages"][-1].content


researcher = Agent(
    role="Researcher",
    goal="Find and summarise the latest incidents",
    backstory="A careful analyst.",
    llm=ChatOpenAI(model="gpt-4o-mini"),
)

crew = Crew(
    agents=[researcher],
    tasks=[Task(description="Summarise today's incidents", expected_output="A short report", agent=researcher)],
)

if __name__ == "__main__":
    print(answer(input("ask> ")))
    print(crew.kickoff(inputs={"topic": os.environ.get("TOPIC", "outages")}))
