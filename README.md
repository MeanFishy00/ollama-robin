# Ollama Robinhood Chat 🤖📈

An interactive, terminal-based AI assistant powered by local Ollama (`gemma4:e4b`) with built-in tools for **Exa Web Search** and complete **Robinhood Trading & Portfolio Automation** via the `robin_stocks` SDK.

---

## Key Features

- **Local AI Chat**: Chat natively with `gemma4:e4b` running on your local Ollama instance.
- **Web Search Tool**: Powered by Exa Search API to retrieve real-time news, information, and answers.
- **Robinhood Portfolio Analytics**: Fetch accounts profile details, portfolio values, cash balances, buying power, and open stock/options positions.
- **Equities & Options Trading**: Query real-time quotes, chains, historical charts, list watchlists, place market/limit orders, and cancel open orders.
- **Pre-Trade Simulation Reviews**: Safe order review tools calculate estimated costs, check buying power, and inspect asset tradability flags before committing any trades.
- **Smart Decimal Formatting**: Automatically sanitizes raw Robinhood API outputs (e.g., converting `$2.7100` to `$2.71`) for clean AI communication.
- **Interactive Multi-Factor Authentication (MFA)**: Prompts dynamically in the terminal to securely type in SMS or authenticator codes upon boot.

---

## Project Structure

```text
ollama-robin/
├── .env.example       # Template env file for credentials
├── .gitignore         # Prevents committing API keys / secrets
├── README.md          # Guide & setup documentation
├── requirements.txt   # Pinned python dependency packages
├── chat.py            # Main interactive CLI chat loop
└── tools/
    ├── __init__.py
    ├── formatter.py   # Recursive clean-up helper (2.7100 -> 2.71)
    ├── schemas.py     # Declarative JSON schemas for Ollama tools
    └── handlers.py    # Python logic calling Exa and Robinhood APIs
```

---

## Installation & Setup

### 1. Prerequisites
- [Python 3.10+](https://www.python.org/)
- [Ollama](https://ollama.com/) running locally with `gemma4:e4b` pulled:
  ```bash
  ollama pull gemma4:e4b
  ```

### 2. Install Python Dependencies
```bash
pip install ollama exa-py robin_stocks python-dotenv
```

### 3. Configure Environment Variables
Create a file named `.env.local` in the project root:
```env
# Exa API Key
EXA_API_KEY="your-exa-api-key-here"

# Robinhood Credentials
ROBINHOOD_USERNAME="your-login-email@example.com"
ROBINHOOD_PASSWORD="your-robinhood-password"
```

---

## Running the Application

To start the interactive chat client:
```bash
python chat.py
```

- **MFA Warning**: If your Robinhood account has MFA active, the script will pause and prompt you to input the code directly into the terminal window during startup.
- **Fallback Mode**: If you run without Robinhood credentials, the chat will automatically disable Robinhood tools and fall back to standard chat + Exa web search.
