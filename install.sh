#!/usr/bin/env bash
# ==============================================================================
# PyHawk — Automated Cross-Platform Installer for macOS & Linux
# «Sharp as a hawk, fast as math»
# ==============================================================================

set -e

CYAN='\033[0;36m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color
BOLD='\033[1m'

echo -e "${CYAN}${BOLD}"
echo "    __   __  _______  _     _  ___   _ "
echo "   |  | |  ||   _   || | _ | ||   | | |"
echo "   |  |_|  ||  |_|  || || || ||   |_| |"
echo "   |       ||       ||       ||      _|"
echo "   |       ||       ||       ||     |_ "
echo "   |   _   ||   _   ||   _   ||    _  |"
echo "   |__| |__||__| |__||__| |__||___| |_|"
echo "  PyHawk Installer — macOS & Linux"
echo -e "${NC}"

# 1. Check Python 3
echo -e "${YELLOW}Checking requirements...${NC}"
if ! command -v python3 &>/dev/null; then
    echo -e "${RED}[ERROR] Python 3 is required but was not found in PATH.${NC}"
    echo "Please install Python 3.8 or newer (https://www.python.org) and run this installer again."
    exit 1
fi

PY_VERSION=$(python3 -c 'import sys; print(f"{sys.version_info.major}.{sys.version_info.minor}")')
echo -e "   ${GREEN}[OK]${NC} Python $PY_VERSION found: $(command -v python3)"

# 2. Check C Compiler for native compilation
if command -v clang &>/dev/null; then
    echo -e "   ${GREEN}[OK]${NC} C compiler found: clang ($(clang --version | head -n 1))"
elif command -v gcc &>/dev/null; then
    echo -e "   ${GREEN}[OK]${NC} C compiler found: gcc ($(gcc --version | head -n 1))"
else
    echo -e "   ${YELLOW}[WARN]${NC} No C compiler (clang/gcc) found. Native C compilation ('pyhawk build') requires clang or gcc."
    if [[ "$(uname)" == "Darwin" ]]; then
        echo "     Tip on macOS: run 'xcode-select --install'"
    else
        echo "     Tip on Linux: run 'sudo apt install build-essential' or 'sudo dnf groupinstall \"Development Tools\"'"
    fi
fi

# 3. Determine installation directory
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
INSTALL_DIR="$HOME/.pyhawk"

if [[ -f "$SCRIPT_DIR/hawk_cli.py" ]]; then
    # Running from repository
    SOURCE_DIR="$SCRIPT_DIR"
else
    SOURCE_DIR="$INSTALL_DIR"
fi

echo -e "\n${YELLOW}Installing PyHawk to ${INSTALL_DIR}...${NC}"
mkdir -p "$INSTALL_DIR"
mkdir -p "$INSTALL_DIR/bin"

if [[ "$SOURCE_DIR" != "$INSTALL_DIR" ]]; then
    cp -R "$SOURCE_DIR/hawk" "$INSTALL_DIR/"
    cp -R "$SOURCE_DIR/examples" "$INSTALL_DIR/" 2>/dev/null || true
    cp -R "$SOURCE_DIR/vscode-hawk" "$INSTALL_DIR/" 2>/dev/null || true
    cp "$SOURCE_DIR/hawk_cli.py" "$INSTALL_DIR/"
    cp "$SOURCE_DIR/README.md" "$INSTALL_DIR/" 2>/dev/null || true
fi

# 4. Create launcher wrapper scripts in ~/.local/bin and $INSTALL_DIR/bin
BIN_DIR="$HOME/.local/bin"
mkdir -p "$BIN_DIR"

for CMD_NAME in "pyhawk" "hawk"; do
    WRAPPER="$BIN_DIR/$CMD_NAME"
    cat << EOF > "$WRAPPER"
#!/usr/bin/env bash
exec python3 "$INSTALL_DIR/hawk_cli.py" "\$@"
EOF
    chmod +x "$WRAPPER"
    cp "$WRAPPER" "$INSTALL_DIR/bin/$CMD_NAME"
done

echo -e "   ${GREEN}[OK]${NC} Created CLI commands in: $BIN_DIR/pyhawk and $BIN_DIR/hawk"

# 5. Check and configure PATH
PATH_CONFIGURED=false
case ":$PATH:" in
    *":$BIN_DIR:"*) PATH_CONFIGURED=true ;;
esac

if [ "$PATH_CONFIGURED" = false ]; then
    echo -e "${YELLOW}Configuring PATH in shell profiles...${NC}"
    ADD_PATH_CMD="export PATH=\"\$HOME/.local/bin:\$PATH\""
    
    # Configure for zsh
    if [[ -f "$HOME/.zshrc" ]] || [[ "$SHELL" == *"zsh"* ]]; then
        if ! grep -q ".local/bin" "$HOME/.zshrc" 2>/dev/null; then
            echo -e "\n# PyHawk CLI\n$ADD_PATH_CMD" >> "$HOME/.zshrc"
            echo -e "   ${GREEN}[OK]${NC} Added to ~/.zshrc"
        fi
    fi
    
    # Configure for bash
    for BASH_FILE in "$HOME/.bashrc" "$HOME/.bash_profile"; do
        if [[ -f "$BASH_FILE" ]]; then
            if ! grep -q ".local/bin" "$BASH_FILE"; then
                echo -e "\n# PyHawk CLI\n$ADD_PATH_CMD" >> "$BASH_FILE"
                echo -e "   ${GREEN}[OK]${NC} Added to $BASH_FILE"
            fi
        fi
    done

    # Configure for fish
    if command -v fish &>/dev/null && [[ -d "$HOME/.config/fish" ]]; then
        mkdir -p "$HOME/.config/fish"
        FISH_CONF="$HOME/.config/fish/config.fish"
        if ! grep -q ".local/bin" "$FISH_CONF" 2>/dev/null; then
            echo -e "\n# PyHawk CLI\nfish_add_path \$HOME/.local/bin" >> "$FISH_CONF"
            echo -e "   ${GREEN}[OK]${NC} Added to $FISH_CONF"
        fi
    fi
else
    echo -e "   ${GREEN}[OK]${NC} $BIN_DIR is already in your PATH."
fi

# 6. Install VS Code Extension if 'code' is installed
VSIX_PATH=$(find "$INSTALL_DIR/vscode-hawk" -name "hawk-language-*.vsix" 2>/dev/null | sort -V | tail -n 1 || true)
if [[ -z "$VSIX_PATH" && -d "$SOURCE_DIR/vscode-hawk" ]]; then
    VSIX_PATH=$(find "$SOURCE_DIR/vscode-hawk" -name "hawk-language-*.vsix" 2>/dev/null | sort -V | tail -n 1 || true)
fi

if [[ -n "$VSIX_PATH" && -f "$VSIX_PATH" ]]; then
    if command -v code &>/dev/null; then
        echo -e "\n${YELLOW}Installing VS Code extension (PyHawk)...${NC}"
        code --install-extension "$VSIX_PATH" --force 2>/dev/null || true
        echo -e "   ${GREEN}[OK]${NC} VS Code extension installed! ($(basename "$VSIX_PATH"))"
    fi
fi

echo -e "\n${GREEN}${BOLD}PyHawk installed successfully!${NC}"
echo -e "Try it right now:"
echo -e "  ${CYAN}pyhawk version${NC}             # Check version"
echo -e "  ${CYAN}pyhawk repl${NC}                # Interactive mathematical REPL"
echo -e "  ${CYAN}pyhawk run <file.hwk>${NC}      # Run PyHawk script (Interpreter)"
echo -e "  ${CYAN}pyhawk build <file.hwk>${NC}    # Compile to native C99 binary (clang -O3)"
echo -e "\n${BOLD}Sharp as a hawk, fast as math.${NC}\n"
