import json
import os

import pandas as pd
from dotenv import load_dotenv
from openai import OpenAI


load_dotenv()


def welcome_user():
    print("Welcome to AI Data Analyst Agent")
    print()


def get_csv_file_path():
    file_path = input("Enter the path to your CSV file: ").strip()
    return file_path


def load_dataset(file_path):
    if not os.path.exists(file_path):
        print("Error: File does not exist.")
        return None

    try:
        df = pd.read_csv(file_path)
        return df

    except pd.errors.EmptyDataError:
        print("Error: The CSV file is empty.")
        return None

    except pd.errors.ParserError:
        print("Error: The CSV file could not be parsed.")
        return None

    except Exception as error:
        print(f"Error loading dataset: {error}")
        return None


def get_business_goal():
    goal = input("Enter the business goal or question: ").strip()
    return goal


def create_agent_state(df, business_goal):
    return {
        "df": df,
        "business_goal": business_goal,
        "dataset_summary": "",
        "plan": {},
        "selected_tools": [],
        "tool_results": {},
        "final_report": ""
    }


def get_dataset_summary(df):
    numeric_columns = df.select_dtypes(include="number")

    if numeric_columns.empty:
        numeric_summary = "No numeric columns were found."
    else:
        numeric_summary = numeric_columns.describe().to_string()

    return f"""
Rows: {df.shape[0]}
Columns: {df.shape[1]}

Column names:
{list(df.columns)}

Data types:
{df.dtypes.to_string()}

Missing values:
{df.isnull().sum().to_string()}

Numeric summary:
{numeric_summary}
"""


# -----------------------------
# Analytics tools
# -----------------------------

def check_missing_values(df):
    return df.isnull().sum()


def summarize_numeric_columns(df):
    numeric_columns = df.select_dtypes(include="number")

    if numeric_columns.empty:
        return "No numeric columns were found."

    return numeric_columns.describe()


def get_column_names(df):
    return list(df.columns)


def calculate_grouped_metric(
    df,
    group_by,
    metric,
    aggregation
):
    if group_by not in df.columns:
        return f"Error: Group-by column '{group_by}' was not found."

    if metric not in df.columns:
        return f"Error: Metric column '{metric}' was not found."

    allowed_aggregations = {
        "sum": "sum",
        "mean": "mean",
        "average": "mean",
        "count": "count",
        "min": "min",
        "max": "max"
    }

    aggregation = aggregation.lower()

    if aggregation not in allowed_aggregations:
        return (
            f"Error: Aggregation '{aggregation}' is not supported. "
            "Use sum, mean, average, count, min, or max."
        )

    pandas_aggregation = allowed_aggregations[aggregation]

    if pandas_aggregation in ["sum", "mean", "min", "max"]:
        if not pd.api.types.is_numeric_dtype(df[metric]):
            return (
                f"Error: Column '{metric}' must be numeric "
                f"for the '{aggregation}' aggregation."
            )

    result = (
        df.groupby(group_by, dropna=False)[metric]
        .agg(pandas_aggregation)
        .reset_index()
        .sort_values(
            by=metric,
            ascending=False
        )
    )

    return result


# -----------------------------
# Tool registry
# -----------------------------

def create_tool_registry():
    return {
        "check_missing_values": {
            "function": check_missing_values,
            "description": "Counts missing values in every column.",
            "required_arguments": []
        },

        "summarize_numeric_columns": {
            "function": summarize_numeric_columns,
            "description": (
                "Returns descriptive statistics for numeric columns."
            ),
            "required_arguments": []
        },

        "get_column_names": {
            "function": get_column_names,
            "description": "Returns all column names in the dataset.",
            "required_arguments": []
        },

        "calculate_grouped_metric": {
            "function": calculate_grouped_metric,
            "description": (
                "Groups the dataset by one column and calculates "
                "sum, mean, average, count, min, or max for a metric."
            ),
            "required_arguments": [
                "group_by",
                "metric",
                "aggregation"
            ]
        }
    }


def format_tools_for_prompt(tool_registry):
    tool_descriptions = []

    for tool_name, tool_info in tool_registry.items():
        description = tool_info["description"]
        required_arguments = tool_info["required_arguments"]

        tool_descriptions.append(
            f"- {tool_name}\n"
            f"  Description: {description}\n"
            f"  Required arguments: {required_arguments}"
        )

    return "\n".join(tool_descriptions)


# -----------------------------
# Prompts
# -----------------------------

def build_planning_prompt(agent_state, tool_registry):
    available_tools = format_tools_for_prompt(tool_registry)

    return f"""
You are an AI Data Analyst Agent.

Your job is to select the correct analytics tools and arguments
needed to answer the user's business question.

Business question:
{agent_state["business_goal"]}

Dataset summary:
{agent_state["dataset_summary"]}

Available tools:
{available_tools}

Return only valid JSON using this exact structure:

{{
  "plan": "Brief explanation of the analysis approach.",
  "tools": [
    {{
      "name": "tool_name",
      "arguments": {{
        "argument_name": "argument_value"
      }}
    }}
  ]
}}

Rules:
- Only use tools from the available-tools list.
- Use exact column names from the dataset.
- For tools without arguments, return an empty arguments object.
- For questions such as "revenue by country", use:
  calculate_grouped_metric
- In that example:
  group_by should be country
  metric should be revenue
  aggregation should be sum
- Do not include Markdown code fences.
- Do not include any text outside the JSON object.
"""


def format_tool_results_for_prompt(tool_results):
    formatted_results = []

    for tool_name, result in tool_results.items():
        if isinstance(result, pd.DataFrame):
            result_text = result.to_string(index=False)
        elif isinstance(result, pd.Series):
            result_text = result.to_string()
        else:
            result_text = str(result)

        formatted_results.append(
            f"Tool: {tool_name}\nResult:\n{result_text}"
        )

    return "\n\n".join(formatted_results)


def build_report_prompt(agent_state):
    formatted_results = format_tool_results_for_prompt(
        agent_state["tool_results"]
    )

    return f"""
You are an AI Data Analyst Agent.

Write a concise executive-style analytics report based only on the
actual tool results provided below.

Business question:
{agent_state["business_goal"]}

Analysis plan:
{agent_state["plan"]}

Tool results:
{formatted_results}

Include these sections:

1. Summary
2. Key Observations
3. Data Quality Issues
4. Recommended Next Steps

Rules:
- Directly answer the business question.
- Use values from the tool results.
- Do not invent results.
- Clearly mention any errors or missing information.
"""


# -----------------------------
# OpenAI and JSON handling
# -----------------------------

def ask_gpt(prompt):
    api_key = os.getenv("OPENAI_API_KEY")

    if not api_key:
        return None

    client = OpenAI(api_key=api_key)

    response = client.responses.create(
        model="gpt-5.5",
        input=prompt
    )

    return response.output_text


def parse_json_response(response_text):
    if not response_text:
        return None

    cleaned_response = response_text.strip()

    if cleaned_response.startswith("```json"):
        cleaned_response = cleaned_response[7:]

    if cleaned_response.startswith("```"):
        cleaned_response = cleaned_response[3:]

    if cleaned_response.endswith("```"):
        cleaned_response = cleaned_response[:-3]

    cleaned_response = cleaned_response.strip()

    try:
        return json.loads(cleaned_response)

    except json.JSONDecodeError as error:
        print(f"Error: The planning response was not valid JSON: {error}")
        return None


# -----------------------------
# Local fallback planner
# -----------------------------

def normalize_text(value):
    return (
        str(value)
        .strip()
        .lower()
        .replace("_", " ")
        .replace("-", " ")
    )


def find_matching_column(search_text, columns):
    normalized_search_text = normalize_text(search_text)

    for column in columns:
        if normalize_text(column) == normalized_search_text:
            return column

    for column in columns:
        normalized_column = normalize_text(column)

        if normalized_column in normalized_search_text:
            return column

    return None


def detect_aggregation(business_goal):
    words = normalize_text(business_goal).split()

    if "average" in words or "mean" in words:
        return "mean"

    if "count" in words:
        return "count"

    if "minimum" in words or "min" in words or "lowest" in words:
        return "min"

    if "maximum" in words or "max" in words or "highest" in words:
        return "max"

    return "sum"


def build_local_fallback_plan(agent_state):
    business_goal = agent_state["business_goal"]
    columns = list(agent_state["df"].columns)

    normalized_goal = normalize_text(business_goal)

    if " by " in normalized_goal:
        metric_text, group_by_text = normalized_goal.split(
            " by ",
            maxsplit=1
        )

        metric = find_matching_column(metric_text, columns)
        group_by = find_matching_column(group_by_text, columns)
        aggregation = detect_aggregation(business_goal)

        if metric and group_by:
            return {
                "plan": (
                    f"Calculate {aggregation} of {metric}, "
                    f"grouped by {group_by}."
                ),
                "tools": [
                    {
                        "name": "calculate_grouped_metric",
                        "arguments": {
                            "group_by": group_by,
                            "metric": metric,
                            "aggregation": aggregation
                        }
                    },
                    {
                        "name": "check_missing_values",
                        "arguments": {}
                    }
                ]
            }

    return {
        "plan": (
            "Inspect the dataset structure, numeric fields, "
            "and missing values."
        ),
        "tools": [
            {
                "name": "get_column_names",
                "arguments": {}
            },
            {
                "name": "check_missing_values",
                "arguments": {}
            },
            {
                "name": "summarize_numeric_columns",
                "arguments": {}
            }
        ]
    }


def create_analysis_plan(agent_state, tool_registry):
    planning_prompt = build_planning_prompt(
        agent_state,
        tool_registry
    )

    response_text = ask_gpt(planning_prompt)

    if response_text is None:
        print()
        print("No OpenAI API key found. Using local fallback planning.")
        return build_local_fallback_plan(agent_state)

    parsed_plan = parse_json_response(response_text)

    if parsed_plan is None:
        print("Using local fallback planning instead.")
        return build_local_fallback_plan(agent_state)

    return parsed_plan


# -----------------------------
# Tool selection and execution
# -----------------------------

def extract_tools_from_plan(plan):
    tools = plan.get("tools", [])

    if not isinstance(tools, list):
        return []

    return tools


def validate_tool_arguments(
    tool_name,
    arguments,
    tool_registry
):
    required_arguments = tool_registry[tool_name][
        "required_arguments"
    ]

    missing_arguments = []

    for argument_name in required_arguments:
        if argument_name not in arguments:
            missing_arguments.append(argument_name)

    return missing_arguments


def execute_tools(
    agent_state,
    selected_tools,
    tool_registry
):
    df = agent_state["df"]

    for tool_request in selected_tools:
        tool_name = tool_request.get("name")
        arguments = tool_request.get("arguments", {})

        if not tool_name:
            continue

        if tool_name not in tool_registry:
            agent_state["tool_results"][tool_name] = (
                "Error: Tool not found."
            )
            continue

        if not isinstance(arguments, dict):
            agent_state["tool_results"][tool_name] = (
                "Error: Tool arguments must be a dictionary."
            )
            continue

        missing_arguments = validate_tool_arguments(
            tool_name,
            arguments,
            tool_registry
        )

        if missing_arguments:
            agent_state["tool_results"][tool_name] = (
                "Error: Missing required arguments: "
                f"{missing_arguments}"
            )
            continue

        tool_function = tool_registry[tool_name]["function"]

        try:
            result = tool_function(
                df,
                **arguments
            )

            agent_state["tool_results"][tool_name] = result

        except TypeError as error:
            agent_state["tool_results"][tool_name] = (
                f"Error executing tool: {error}"
            )

        except Exception as error:
            agent_state["tool_results"][tool_name] = (
                f"Unexpected tool error: {error}"
            )

    return agent_state


# -----------------------------
# Final report
# -----------------------------

def build_local_fallback_report(agent_state):
    business_goal = agent_state["business_goal"]
    tool_results = agent_state["tool_results"]

    report_sections = [
        "1. Summary",
        f"The agent analyzed the business question: {business_goal}.",
        "",
        "2. Key Observations"
    ]

    for tool_name, result in tool_results.items():
        report_sections.append(f"\n{tool_name}:")

        if isinstance(result, pd.DataFrame):
            report_sections.append(
                result.to_string(index=False)
            )

        elif isinstance(result, pd.Series):
            report_sections.append(
                result.to_string()
            )

        else:
            report_sections.append(str(result))

    report_sections.extend([
        "",
        "3. Data Quality Issues",
        (
            "Review the missing-value results and confirm that the "
            "selected metric and grouping columns follow the intended "
            "business definitions."
        ),
        "",
        "4. Recommended Next Steps",
        (
            "Validate the results with a business stakeholder, add "
            "filters or time dimensions where appropriate, and create "
            "a visualization for easier comparison."
        )
    ])

    return "\n".join(report_sections)


def generate_final_report(agent_state):
    report_prompt = build_report_prompt(agent_state)
    final_report = ask_gpt(report_prompt)

    if final_report is None:
        final_report = build_local_fallback_report(agent_state)

    agent_state["final_report"] = final_report

    return agent_state


def show_final_report(agent_state):
    print()
    print("==============================")
    print("AI Data Analyst Agent Report")
    print("==============================")
    print()
    print(agent_state["final_report"])


# -----------------------------
# Main application
# -----------------------------

def main():
    welcome_user()

    file_path = get_csv_file_path()

    df = load_dataset(file_path)

    if df is None:
        return

    business_goal = get_business_goal()

    if not business_goal:
        print("Error: A business goal is required.")
        return

    agent_state = create_agent_state(
        df,
        business_goal
    )

    agent_state["dataset_summary"] = get_dataset_summary(df)

    tool_registry = create_tool_registry()

    plan = create_analysis_plan(
        agent_state,
        tool_registry
    )

    agent_state["plan"] = plan

    selected_tools = extract_tools_from_plan(plan)

    agent_state["selected_tools"] = selected_tools

    agent_state = execute_tools(
        agent_state,
        selected_tools,
        tool_registry
    )

    agent_state = generate_final_report(agent_state)

    show_final_report(agent_state)


if __name__ == "__main__":
    main()