#!/bin/bash

LOG_DIR="$HOME/.code_narrator"
mkdir -p "$LOG_DIR"

LOG_FILE="$LOG_DIR/terminal.log"
touch "$LOG_FILE"

echo "🔧 Adding PROMPT_COMMAND to your shell config..."

if [ -f "$HOME/.zshrc" ]; then
    SHELL_RC="$HOME/.zshrc"
elif [ -f "$HOME/.bashrc" ]; then
    SHELL_RC="$HOME/.bashrc"
else
    echo "❌ Could not find .bashrc or .zshrc"
    exit 1
fi

if ! grep -q "PROMPT_COMMAND.*code_narrator" "$SHELL_RC"; then
    echo -e "\n# >>> Code Narrator Logger >>>" >> "$SHELL_RC"
    echo "export PROMPT_COMMAND='echo \$(date +%s) ::: \$(history 1 | sed \"s/ *[0-9]* *//\") >> $LOG_FILE'" >> "$SHELL_RC"
    echo "# <<< Code Narrator Logger <<<" >> "$SHELL_RC"
    echo "✅ Logger added to $SHELL_RC"
else
    echo "⚠️ PROMPT_COMMAND hook already exists."
fi

echo "🟢 Done. Restart your terminal or run: source $SHELL_RC"
