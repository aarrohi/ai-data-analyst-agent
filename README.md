# AI Data Analyst Agent

AI Data Analyst Agent is a Python application that uses the OpenAI Responses API to analyze structured datasets and generate business insights.

Rather than sending a dataset directly to an LLM, the application follows an agentic workflow. It first profiles the dataset, creates an analysis plan, selects the appropriate analytics tools, executes those tools, and then generates an executive-style business report.

This project was built to explore how AI agents can automate analytics workflows while keeping the architecture modular, extensible, and easy to maintain.

---

## Features

- Profiles structured datasets
- Summarizes dataset structure and data quality
- Generates an AI-driven analysis plan
- Dynamically selects analytics tools
- Executes Python analytics tools
- Produces executive-style business reports
- Uses a shared agent state throughout the workflow
- Modular tool registry for adding new capabilities

---

## Workflow

```
Load Dataset
      ↓
Profile Dataset
      ↓
Create Agent State
      ↓
Generate Analysis Plan
      ↓
Select Analytics Tools
      ↓
Execute Selected Tools
      ↓
Generate Executive Report
```

---

## Technologies

- Python
- Pandas
- OpenAI Responses API
- python-dotenv
- Git
- GitHub

---

## Project Structure

```
ai-data-analyst-agent/
│
├── main.py
├── README.md
├── requirements.txt
├── .env.example
├── .gitignore
└── sales.csv
```

---

## Getting Started

### Clone the repository

```bash
git clone https://github.com/YOUR_USERNAME/ai-data-analyst-agent.git
```

### Navigate to the project

```bash
cd ai-data-analyst-agent
```

### Install dependencies

```bash
pip install -r requirements.txt
```

### Create a `.env` file

Create a file named `.env` in the project directory and add your OpenAI API key:

```
OPENAI_API_KEY=your_openai_api_key
```

### Run the application

```bash
python main.py
```

---

## Planned Enhancements

This project is designed to evolve over time. Planned improvements include:

- Additional analytics tools
- Structured outputs
- Improved prompt engineering
- LangGraph workflow orchestration
- Retrieval-Augmented Generation (RAG)
- Evaluation framework
- Multi-agent collaboration
- Interactive web interface
- Cloud deployment

---

## Why I Built This

Data analysts spend a significant amount of time exploring datasets, checking data quality, deciding which analyses to perform, and summarizing findings.

This project explores how an AI agent can automate those repetitive tasks by combining planning, tool execution, and business reasoning into a single workflow while maintaining a clean and extensible architecture.

As the project evolves, it will incorporate more advanced agentic AI techniques such as workflow orchestration, retrieval, evaluation, and multi-agent collaboration.