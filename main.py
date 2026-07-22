import os

import pandas as pd
from openai import OpenAI
from dotenv import load_dotenv


load_dotenv()


def welcome_user():
    print("Welcome to AI Data Analyst Agent")
    print()


def get_csv_file_path():
    file_path = input("Enter the path to your CSV file: ")
    return file_path


def load_dataset(file_path):
    if not os.path.exists(file_path):
        print("Error: File does not exist.")
        return None

    df = pd.read_csv(file_path)
    return df


def get_business_goal():
    goal = input("Enter the business goal or question: ")
    return goal


def create_agent_state(df, business_goal):
    return {
        "df": df,
        "business_goal": business_goal,
        "dataset_summary": "",
        "plan": "",
        "tool_results": {},
        "final_report": ""
    }


def get_dataset_summary(df):
    return f"""
Rows and columns:
{df.shape}

Column names:
{list(df.columns)}

Data types:
{df.dtypes}

Missing values:
{df.isnull().sum()}

Numeric summary:
{df.describe()}
"""


def check_missing_values(df):
    return df.isnull().sum()


def summarize_numeric_columns(df):
    return df.describe()


def get_column_names(df):
    return list(df.columns)


def create_tool_registry():
    return {
        "check_missing_values": {
            "function": check_missing_values,
            "description": "Counts missing values in each column."
        },
        "summarize_numeric_columns": {
            "function": summarize_numeric_columns,
            "description": "Returns summary statistics for numeric columns."
        },
        "get_column_names": {
            "function": get_column_names,
            "description": "Returns the column names in the dataset."
        }
    }


def format_tools_for_prompt(tool_registry):
    tool_descriptions = []

    for tool_name, tool_info in tool_registry.items():
        description = tool_info["description"]
        tool_descriptions.append(f"- {tool_name}: {description}")

    return "\n".join(tool_descriptions)


def build_planning_prompt(agent_state, tool_registry):
    available_tools = format_tools_for_prompt(tool_registry)

    return f"""
You are an AI Data Analyst Agent.

Dataset Summary:
{agent_state["dataset_summary"]}

Business Goal:
{agent_state["business_goal"]}

Choose the best tools to use from this list:
{available_tools}

Return your response in this exact format:

PLAN:
Brief explanation of your approach.

TOOLS:
List one or more tool names, one tool per line.
Only use tools from the list provided.
"""


def build_report_prompt(agent_state):
    return f"""
You are an AI Data Analyst Agent.

Business Goal:
{agent_state["business_goal"]}

Dataset Summary:
{agent_state["dataset_summary"]}

Tool Results:
{agent_state["tool_results"]}

Write an executive-style analytics report.

Include:
1. Summary
2. Key Observations
3. Data Quality Issues
4. Recommended Next Steps
"""


def ask_gpt(prompt):
    api_key = os.getenv("OPENAI_API_KEY")

    if not api_key:
        if "Choose the best tools" in prompt:
            return """
PLAN:
Since no OpenAI API key is configured, this is a sample plan. The agent will inspect the dataset structure, check for missing values, and summarize numeric columns.

TOOLS:
get_column_names
check_missing_values
summarize_numeric_columns
"""

        return """
1. Summary
The dataset was profiled successfully using local Python tools. The agent inspected the available columns, checked for missing values, and summarized numeric fields.

2. Key Observations
The dataset contains structured business data that can be used for analysis. Numeric columns can support metric analysis, while categorical columns can help segment results.

3. Data Quality Issues
The missing value check should be reviewed before making business decisions. Any columns with missing values may require cleaning, filtering, or business rule clarification.

4. Recommended Next Steps
Next, the analysis can be expanded by adding tools for grouped metrics, trend analysis, revenue by segment, and automated chart generation.
"""

    client = OpenAI(api_key=api_key)

    response = client.responses.create(
        model="gpt-5.5",
        input=prompt
    )

    return response.output_text


def extract_tools_from_plan(plan, tool_registry):
    selected_tools = []

    for tool_name in tool_registry:
        if tool_name in plan:
            selected_tools.append(tool_name)

    return selected_tools


def execute_tools(agent_state, selected_tools, tool_registry):
    df = agent_state["df"]

    for tool_name in selected_tools:
        if tool_name not in tool_registry:
            agent_state["tool_results"][tool_name] = "Tool not found."
            continue

        tool_function = tool_registry[tool_name]["function"]
        result = tool_function(df)
        agent_state["tool_results"][tool_name] = result

    return agent_state


def generate_final_report(agent_state):
    prompt = build_report_prompt(agent_state)
    final_report = ask_gpt(prompt)
    agent_state["final_report"] = final_report
    return agent_state


def show_final_report(agent_state):
    print()
    print("==============================")
    print("AI Data Analyst Agent Report")
    print("==============================")
    print()
    print(agent_state["final_report"])


def main():
    welcome_user()

    file_path = get_csv_file_path()

    df = load_dataset(file_path)

    if df is None:
        return

    business_goal = get_business_goal()

    agent_state = create_agent_state(df, business_goal)

    agent_state["dataset_summary"] = get_dataset_summary(df)

    tool_registry = create_tool_registry()

    planning_prompt = build_planning_prompt(agent_state, tool_registry)

    plan = ask_gpt(planning_prompt)

    agent_state["plan"] = plan

    selected_tools = extract_tools_from_plan(plan, tool_registry)

    agent_state = execute_tools(
        agent_state,
        selected_tools,
        tool_registry
    )

    agent_state = generate_final_report(agent_state)

    show_final_report(agent_state)


main()