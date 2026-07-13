# AI Data Analyst Agent

An agentic AI application that translates natural language business questions into executable analytics workflows.

The application profiles CSV datasets, creates structured analysis plans, dynamically selects Python analytics tools, executes real data analysis using Pandas, and generates executive-style business reports using the OpenAI Responses API.

---

## Features

- Load CSV datasets using Pandas
- Automatically profile datasets
  - Dataset shape
  - Column names
  - Data types
  - Missing values
  - Summary statistics
- Translate business questions into structured analytics plans
- Dynamically select analytics tools
- Execute Python analytics tools automatically
- Perform grouped business analysis (e.g. Revenue by Country)
- Validate tool arguments before execution
- Generate executive-style analytics reports
- Local fallback mode when no OpenAI API key is configured

---

## Example Workflow

```
Business Question
        │
        ▼
Dataset Profiling
        │
        ▼
AI Planning
        │
        ▼
Tool Selection
        │
        ▼
Python Tool Execution
        │
        ▼
Executive Report
```

Example question:

```
Revenue by country
```

The AI agent creates an execution plan similar to:

```json
{
  "plan": "Calculate total revenue grouped by country.",
  "tools": [
    {
      "name": "calculate_grouped_metric",
      "arguments": {
        "group_by": "country",
        "metric": "revenue",
        "aggregation": "sum"
      }
    }
  ]
}
```

The Python analytics engine executes the selected tool and generates an executive-style report.

---

# Version History

## Version 1.0

- Built an AI-powered data analyst capable of profiling CSV datasets
- Generated analytics plans using the OpenAI Responses API
- Dynamically selected and executed Python analytics tools
- Produced executive-style analytics reports

---

## Version 2.0

- Introduced a metadata-driven tool registry
- Added tool descriptions for improved AI planning
- Generated planning prompts dynamically from the tool registry
- Improved tool execution architecture
- Added safe handling for unknown tool selections
- Refactored the codebase using reusable helper functions

---

## Version 3.0

- Introduced structured AI planning using JSON
- Added argument-aware tool execution
- Implemented grouped business analysis using Pandas
- Added dynamic aggregation (sum, average, count, min, max)
- Added validation for tool names and required arguments
- Implemented fallback planning without an OpenAI API key
- Improved report generation using actual analytics results
- Enhanced error handling throughout the workflow

---

# Technologies

- Python
- Pandas
- OpenAI Responses API
- python-dotenv

---

# Project Structure

```text
ai-data-analyst-agent/
│
├── main.py
├── sales.csv
├── requirements.txt
├── .env.example
├── .gitignore
└── README.md
```

---

# Installation

Clone the repository:

```bash
git clone https://github.com/aarrohi/ai-data-analyst-agent.git
```

Navigate to the project directory:

```bash
cd ai-data-analyst-agent
```

Install the required packages:

```bash
python3 -m pip install -r requirements.txt
```

(Optional) Create a `.env` file:

```text
OPENAI_API_KEY=your_api_key_here
```

---

# Running the Application

Run:

```bash
python3 main.py
```

Example:

```text
Enter the path to your CSV file:
sales.csv

Enter the business goal or question:
revenue by country
```

Example output:

```text
USA        4500
Canada     2300
UK         1100
Germany     950
```

The application will:

1. Profile the dataset
2. Generate an AI analysis plan
3. Select analytics tools
4. Execute Python analytics tools
5. Generate an executive analytics report

---

# Current Capabilities

- Dataset profiling
- AI-generated planning
- Structured tool selection
- Metadata-driven tool registry
- Argument-aware tool execution
- Dynamic grouped analytics
- Executive-style reporting
- Local fallback mode

---

# Roadmap

Planned future enhancements include:

- Retrieval-Augmented Generation (RAG)
- LangGraph workflow orchestration
- Evaluation framework for AI outputs
- Multi-agent architecture
- SQL database integrations
- FastAPI deployment
- Interactive web interface

---

# Author

**Aarrohi Aagrawal**

GitHub: https://github.com/aarrohi