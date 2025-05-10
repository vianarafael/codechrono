# 🧠 CodeChrono isn’t just for estimates — it’s your personal feedback loop. Know where your time goes. Learn to go faster.

A local LLM-powered dev session logger that watches your terminal, code changes, and app focus — then summarizes what you worked on.

Built to help you estimate how long real work takes—based on your own history, not guesswork.

---

## 🚀 Features

- ✅ Tracks terminal commands and app focus
- ✅ Summarizes git diffs
- ✅ Uses a local LLM (via [Ollama](https://ollama.com)) to generate summaries
- ✅ Stores everything locally in SQLite
- ✅ **Estimates time to complete new tasks based on your real history**
- ✅ Fully offline, no tracking

---

## 📦 Requirements

- Python 3.8+
- `xdotool` (for app tracking – Linux only)
- [Ollama](https://ollama.com) installed and running a model (e.g. `mistral`)
- Shell that supports `PROMPT_COMMAND` (bash, zsh)

---

## 📥 Setup

1. **Clone this repo**

2. **Install Python dependencies**
   ```bash
   pip install -r requirements.txt
```

3. **Set up terminal logging and run ollama**
```bash
bash scripts/setup_terminal_logger.sh
source ~/.bashrc   # or source ~/.zshrc

ollama run qwen3:14b-q4_K_M  
```

## 🛠 Usage

```bash
python run.py start -m "refactor login flow"

python run.py stop

# view recent summaries
python run.py report
```


**🧪 Example Output**
```bash
## Summary (2h session)
- Fixed bug in `auth.py` handling token expiration
- Ran tests and confirmed fix
- Researched error via Stack Overflow
```

# 🔮 Estimate time for a new feature
```bash
python run.py estimate -m "build settings page for admin panel"
```


**🧪 Example Output**
```bash
🧮 Estimated Time: 2–3 hours.
This task is similar to your previous “settings UI” session (3h), but may go faster based on recency.

```

