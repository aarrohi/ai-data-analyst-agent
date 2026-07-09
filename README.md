# AI Data Analyst Agent

An agentic AI application that profiles CSV datasets, creates analysis plans, dynamically selects Python analytics tools, executes those tools, and generates executive-style business reports using the OpenAI Responses API.

---

## Features

- Load CSV datasets using Pandas
- Automatically profile datasets
  - Dataset shape
  - Column names
  - Data types
  - Missing values
  - Summary statistics
- Generate an AI analysis plan based on a business goal
- Dynamically select analytics tools using a metadata-driven tool registry
- Execute Python analytics tools automatically
- Generate executive-style analytics reports
- Safely handle unknown tool selections

---

## Version History

### Version 1.0

- Built an AI-powered data analyst capable of profiling CSV datasets
- Generated analytics plans using the OpenAI Responses API
- Dynamically selected and executed Python analytics tools
- Produced executive-style analytics reports

### Version 2.0

- Introduced a metadata-driven tool registry
- Added tool descriptions for improved AI planning
- Generated planning prompts dynamically from the tool registry
- Improved tool execution architecture
- Added safe handling for unknown tool selections
- Refactored the codebase with reusable helper functions

---

## Technologies

- Python
- Pandas
- OpenAI Responses API
- python-dotenv

---

## Project Structure

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

## Installation

Clone the repository:

```bash
git clone https://github.com/aarrohi/ai-data-analyst-agent.git
```

Navigate to the project folder:

```bash
cd ai-data-analyst-agent
```

Install the required packages:

```bash
pip install -r requirements.txt
```

(Optional) Create a `.env` file in the project directory:

```text
OPENAI_API_KEY=your_api_key_here
```

---

## Running the Application

Run:

```bash
python3 main.py
```

Example:

```text
Enter the path to your CSV file:
sales.csv

Enter the business goal or question:
Revenue by country
```

The application will:

1. Profile the dataset
2. Generate an AI analysis plan
3. Select analytics tools
4. Execute Python analytics tools
5. Generate an executive analytics report

---

## Current Capabilities

✔ Dataset profiling

✔ AI-generated analytics planning

✔ Dynamic tool selection

✔ Metadata-driven tool registry

✔ Automated Python tool execution

✔ Executive-style report generation

---

## Upcoming Improvements

This project is under active development. Future versions will expand the agent with more advanced planning, reasoning, retrieval, and orchestration capabilities.

---

## Author

**Aarrohi Aagrawal**

GitHub: https://github.com/aarrohi