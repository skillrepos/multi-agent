# Set your Groq API key for this terminal AND every terminal you open later.
#
# Usage (run it with "source" so this terminal gets the key too):
#     source scripts/setup-key.sh            # asks you to paste the key
#     source scripts/setup-key.sh <key>      # or pass it directly
#
# Works in the Codespace, in a local dev container, in WSL, and on a Mac
# (bash or zsh). The key is saved in your shell's startup file (~/.bashrc,
# ~/.zshrc, or ~/.bash_profile) so new terminals pick it up automatically.
# Run it again any time to replace the key.

_gk_main() {
  _gk_key="${1:-}"
  if [ -z "$_gk_key" ]; then
    printf 'Paste your Groq API key and press Enter (it will not be shown): '
    read -rs _gk_key
    echo
  fi
  # Drop any spaces or line breaks picked up while copying.
  _gk_key=$(printf '%s' "$_gk_key" | tr -d '[:space:]')

  if [ -z "$_gk_key" ]; then
    echo "No key entered - nothing was changed."
    return 1
  fi
  case "$_gk_key" in
    gsk_*) ;;
    *) echo "Warning: Groq keys normally start with 'gsk_'. Saving it anyway." ;;
  esac

  # Was the key already supplied by the environment (for example a personal
  # Codespaces secret), rather than by an earlier run of this script?
  _gk_preexisting="${GROQ_API_KEY:-}"

  # 1. This terminal
  export GROQ_API_KEY="$_gk_key"

  # 2. Future terminals: the startup file for each shell in use
  _gk_files=""
  for _gk_sh in "${SHELL:-}" "$(ps -p $$ -o comm= 2>/dev/null)"; do
    case "$_gk_sh" in
      *zsh)  _gk_files="$_gk_files $HOME/.zshrc" ;;
      *bash)
        if [ "$(uname)" = "Darwin" ]; then
          _gk_files="$_gk_files $HOME/.bash_profile"   # Mac bash reads this one
        else
          _gk_files="$_gk_files $HOME/.bashrc"
        fi ;;
    esac
  done
  [ -z "$_gk_files" ] && _gk_files="$HOME/.bashrc"

  _gk_saved=""
  for _gk_rc in $(echo "$_gk_files" | tr ' ' '\n' | sort -u); do
    if [ -f "$_gk_rc" ] && grep -q '^export GROQ_API_KEY=' "$_gk_rc"; then
      # An earlier run wrote the key here - replace it.
      # ("|| true": grep reports failure when every line is a key line.)
      { grep -v '^export GROQ_API_KEY=' "$_gk_rc" || true; } > "$_gk_rc.gktmp"
      cat "$_gk_rc.gktmp" > "$_gk_rc"
      rm -f "$_gk_rc.gktmp"
    elif [ -n "$_gk_preexisting" ]; then
      # The key comes from the environment itself. Don't copy it into the
      # startup file, where an old copy would hide a newer one later.
      continue
    fi
    printf "export GROQ_API_KEY='%s'\n" "$_gk_key" >> "$_gk_rc"
    _gk_saved="$_gk_saved $_gk_rc"
  done

  echo "Done! GROQ_API_KEY is set for this terminal."
  if [ -n "$_gk_saved" ]; then
    echo "New terminals will get it too (saved in:$_gk_saved)."
  else
    echo "Your environment already supplies GROQ_API_KEY, so no startup file was changed."
  fi
  echo "Check it works with:  bash scripts/check-groq.sh"
}

_gk_main "$@"
_gk_rc_status=$?

# Warn if the script was run instead of sourced (then this terminal didn't get the key).
_gk_sourced=0
if [ -n "${ZSH_VERSION:-}" ]; then
  case "${ZSH_EVAL_CONTEXT:-}" in *:file*) _gk_sourced=1 ;; esac
elif [ -n "${BASH_VERSION:-}" ]; then
  [ "${BASH_SOURCE[0]}" != "$0" ] && _gk_sourced=1
fi
if [ "$_gk_sourced" = 0 ] && [ "$_gk_rc_status" = 0 ]; then
  echo
  echo "NOTE: you ran this with 'bash' instead of 'source', so THIS terminal"
  echo "      does not have the key yet. Open a new terminal, or run:"
  echo "      source scripts/setup-key.sh"
fi

unset -f _gk_main
unset _gk_key _gk_preexisting _gk_files _gk_sh _gk_rc _gk_saved _gk_sourced
unset _gk_rc_status
