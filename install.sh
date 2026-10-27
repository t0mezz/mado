#!/bin/sh
# Put `mado` on your PATH by symlinking it into ~/.local/bin (macOS, Ubuntu, other Linux).
set -e
src=$(cd "$(dirname "$0")" && pwd)/mado
bin="${MADO_BIN:-$HOME/.local/bin}"

command -v python3 >/dev/null || { echo "mado: python3 not found (Ubuntu: sudo apt install python3)" >&2; exit 1; }

mkdir -p "$bin"
ln -sf "$src" "$bin/mado"
echo "linked $bin/mado -> $src"

case ":$PATH:" in
  *":$bin:"*) echo "done. try: mado notes.md" ;;
  *)
    case "$(basename "${SHELL:-}")" in
      zsh) rc="$HOME/.zshrc" ;;
      *)   rc="$HOME/.bashrc" ;;
    esac
    line="export PATH=\"$bin:\$PATH\""
    grep -qsF "$line" "$rc" || printf '\n# added by mado install.sh\n%s\n' "$line" >> "$rc"
    echo "added $bin to PATH in $rc — run: source $rc"
    ;;
esac
