# 💰 Finance Coach MCP

A personal finance coach app built with Python, Streamlit, OpenAI GPT-4o-mini, and the MCP (Model Context Protocol) SDK.

## ✨ Features

- 💬 **AI Chat Agent** — talk naturally to log expenses, income, budgets, and get advice
- 📊 **Analytics Dashboard** — 4 detailed pages with charts, trends, and breakdowns
- 🎯 **Budget Tracking** — set limits, get alerts when you're close or over
- 🏆 **Health Score** — 0–100 financial health score based on your data
- 🤖 **MCP Server** — 18 tools exposed via the Model Context Protocol
- 💾 **Local JSON Storage** — simple file-based persistence, no database needed

## 🛠️ Tech Stack

| Layer | Technology |
|-------|-----------|
| UI | Streamlit |
| AI | OpenAI GPT-4o-mini |
| Protocol | MCP SDK (FastMCP) |
| Storage | JSON files |
| Charts | Plotly |
| Language | Python 3.11+ |

## 📁 Project Structure

```
finance-coach-mcp/
├── dashboard/
│   ├── app.py                  ← Main AI chat dashboard
│   └── pages/
│       ├── 1_expenses.py       ← Expense analytics
│       ├── 2_income.py         ← Income analytics
│       ├── 3_budgets.py        ← Budget tracking
│       └── 4_advice.py         ← AI advice history
├── data/                       ← JSON storage (auto-created)
├── mcp_server/
│   ├── server.py               ← FastMCP server (18 tools)
│   └── tools/
│       ├── expenses.py
│       ├── income.py
│       ├── budgets.py
│       ├── summary.py
│       ├── context.py
│       └── advice.py
├── utils/
│   ├── storage.py              ← JSON read/write helpers
│   └── ai_client.py            ← OpenAI client wrapper
├── main.py                     ← Entry point
├── requirements.txt
└── .env.example
```

## 🚀 Getting Started

### 1. Clone & install

```bash
git clone https://github.com/chai-sura/finance-coach-mcp
cd finance-coach-mcp
python -m venv fin_env
source fin_env/bin/activate      # Windows: fin_env\Scripts\activate
pip install -r requirements.txt
```

### 2. Set up your API key

```bash
cp .env.example .env
# Edit .env and add your OpenAI API key
```

`.env`:
```
OPENAI_API_KEY=sk-...
```

### 3. Run

```bash
# Dashboard only (recommended)
python main.py --mode dashboard

# MCP server only
python main.py --mode mcp

# Both together
python main.py
```

Dashboard opens at **http://localhost:8501**

## 🔧 MCP Tools

The MCP server exposes 18 tools:

| Category | Tools |
|----------|-------|
| Expenses | `log_expense`, `get_expenses`, `get_expenses_by_category`, `delete_expense` |
| Income | `log_income`, `get_income`, `get_income_by_source`, `delete_income` |
| Budgets | `set_budget`, `get_budgets`, `get_budget_alerts` |
| Summary | `get_summary`, `get_monthly_trend` |
| Context | `view_context`, `get_financial_health_score` |
| Advice | `get_advice`, `get_advice_history`, `get_latest_advice` |

## 💬 Example Chat Commands

```
"I spent $50 on groceries"
"I earned $3000 salary"
"Set $300 monthly budget for dining"
"Show my financial summary"
"Give me financial advice"
"What's my health score?"
```

## ⚠️ Notes

- JSON storage is for **local/personal use only** — not production-ready
- OpenAI API costs are minimal (GPT-4o-mini, ~$0.01 per conversation)
- Data is stored in the `data/` folder — add to `.gitignore` if sensitive

## 📄 License

MIT