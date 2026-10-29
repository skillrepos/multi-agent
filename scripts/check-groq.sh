#!/usr/bin/env bash
# Check that your Groq key works and that the model the labs use is available.
# Usage:  bash scripts/check-groq.sh
#
# Labs 1, 2, and 5 use Groq when GROQ_API_KEY is set. Labs 3 and 4 don't use
# an AI model at all.
set -uo pipefail

MODEL="openai/gpt-oss-120b"

if [ -z "${GROQ_API_KEY:-}" ]; then
  echo "GROQ_API_KEY is not set in this terminal."
  echo
  echo "Run:  source scripts/setup-key.sh"
  echo "(Without a key the labs still run, using the slower local model.)"
  exit 1
fi
echo "GROQ_API_KEY is set (${#GROQ_API_KEY} characters)"
echo "Asking Groq for a short reply from $MODEL ..."

body=$(curl -sS -w '\n%{http_code}' https://api.groq.com/openai/v1/chat/completions \
  -H "Authorization: Bearer $GROQ_API_KEY" -H "Content-Type: application/json" \
  -d "{\"model\":\"$MODEL\",\"messages\":[{\"role\":\"user\",\"content\":\"Say OK\"}],\"max_tokens\":20}" 2>&1)
code=$(printf '%s' "$body" | tail -n 1)
reply=$(printf '%s' "$body" | sed '$d')
detail=$(printf '%s' "$reply" | python3 -c 'import sys,json
try: print(json.load(sys.stdin).get("error",{}).get("message",""))
except Exception: pass' 2>/dev/null)

echo
case "$code" in
  200)
    echo "OK    Your key works and $MODEL is answering. You're ready for the labs." ;;
  401)
    echo "FAIL  Groq rejected the key (it may be mistyped, deleted, or expired)."
    echo "      Create a new key at https://console.groq.com/keys, then run:"
    echo "          source scripts/setup-key.sh"
    echo "      Or skip Groq and use the local model:  unset GROQ_API_KEY" ;;
  429)
    echo "WAIT  Your key works, but you've hit Groq's free-tier rate limit."
    echo "      Wait a minute and try again." ;;
  404|400)
    echo "FAIL  $MODEL isn't available on your key (Groq may have retired it)."
    [ -n "$detail" ] && echo "      Groq says: $detail"
    echo "      See 'model_decommissioned' under Troubleshooting in README.md,"
    echo "      or skip Groq and use the local model:  unset GROQ_API_KEY" ;;
  *)
    echo "FAIL  Couldn't reach Groq (HTTP status: ${code:-none})."
    [ -n "$detail" ] && echo "      Groq says: $detail"
    echo "      Check your internet connection and try again." ;;
esac
[ "$code" = "200" ]
