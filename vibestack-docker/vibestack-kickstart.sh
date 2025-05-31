#!/bin/bash

# VibeStack Interactive Startup Menu
# This script provides an interactive menu system for VibeStack

# Function to display VibeStack logo and wait for input
show_intro_screen() {
    clear
    echo ""
    
    # Check if lolcat is available, otherwise use basic colors
    if command -v lolcat &> /dev/null; then
        figlet -f big "VIBESTACK" | lolcat
        echo ""
        echo "█▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀█" | lolcat
        echo "█                                                     █" | lolcat
        echo "█          ⚡ SYSTEM INITIALIZATION COMPLETE ⚡       █" | lolcat
        echo "█                                                     █" | lolcat
        echo "█                 Claude Code Terminal                █" | lolcat
        echo "█              Powered by Anthropic AI                █" | lolcat
        echo "█                                                     █" | lolcat
        echo "█▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄█" | lolcat
    else
        # Fallback with ANSI colors
        echo -e "\033[1;36m$(figlet -f big 'VIBESTACK')\033[0m"
        echo ""
        echo -e "\033[1;35m█▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀█\033[0m"
        echo -e "\033[1;35m█                                                        █\033[0m"
        echo -e "\033[1;33m█          ⚡ SYSTEM INITIALIZATION COMPLETE ⚡          █\033[0m"
        echo -e "\033[1;35m█                                                        █\033[0m"
        echo -e "\033[1;32m█                 Claude Code Terminal                   █\033[0m"
        echo -e "\033[1;32m█              Powered by Anthropic AI                   █\033[0m"
        echo -e "\033[1;35m█                                                        █\033[0m"
        echo -e "\033[1;35m█▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄█\033[0m"
    fi
    
    echo ""
    echo -e "\033[1;37m                    STATUS: \033[1;32mREADY\033[0m"
    echo ""
    echo -e "\033[1;37m              [ PRESS \033[1;33mS\033[1;37m TO ENTER SETUP ]\033[0m"
    echo ""
    
    # Wait for 's' key press
    while true; do
        read -rsn1 key
        if [[ "$key" == "s" || "$key" == "S" ]]; then
            break
        fi
    done
}

# Function to show setup menu
show_setup_menu() {
    clear
    echo ""
    if command -v lolcat &> /dev/null; then
        echo "╔══════════════════════════════════════════════════════════╗" | lolcat
        echo "║              ✨ CREATE YOUR VIBE CODING KIT ✨         ║" | lolcat  
        echo "╚══════════════════════════════════════════════════════════╝" | lolcat
    else
        echo -e "\033[1;36m╔══════════════════════════════════════════════════════════╗\033[0m"
        echo -e "\033[1;36m║              ✨ CREATE YOUR VIBE CODING KIT ✨         ║\033[0m"
        echo -e "\033[1;36m╚══════════════════════════════════════════════════════════╝\033[0m"
    fi
    echo ""
    
    local choice
    choice=$(whiptail --title "✨ BUILD YOUR VIBE KIT ✨" --menu "█ Set up your perfect coding environment █" 17 65 5 \
        "1" "🔑 Configure API Keys" \
        "2" "🔧 Add MCP Tools" \
        "3" "🤖 Select LLM Tool" \
        "4" "🚀 Start Coding Session" \
        3>&1 1>&2 2>&3)
    
    case $choice in
        1)
            show_api_keys_menu
            ;;
        2)
            show_mcp_menu
            ;;
        3)
            show_llm_menu
            ;;
        4)
            echo ""
            echo -e "\033[1;32m⚡ STARTING CODING SESSION... ⚡\033[0m"
            echo -e "\033[1;37mYour tools are ready! Type '\033[1;33mclaude\033[1;37m' or '\033[1;33mllm\033[1;37m' to begin\033[0m"
            echo ""
            return 0
            ;;
        *)
            echo ""
            echo -e "\033[1;32m🎉 YOUR VIBE KIT IS READY! 🎉\033[0m"
            echo -e "\033[1;37mYour tools are ready! Type '\033[1;33mclaude\033[1;37m' or '\033[1;33mllm\033[1;37m' to begin\033[0m"
            echo ""
            return 0
            ;;
    esac
}

# Function to show API keys menu
show_api_keys_menu() {
    local choice
    choice=$(whiptail --title "🔑 API KEYS CONFIG 🔑" --menu "█ Connect your AI tools █" 15 65 4 \
        "1" "🧠 Anthropic API Key (Claude)" \
        "2" "🔌 OpenAI API Key" \
        "3" "← Back to Setup" \
        3>&1 1>&2 2>&3)
    
    case $choice in
        1)
            configure_anthropic_key
            ;;
        2)
            configure_openai_key
            ;;
        3)
            show_setup_menu
            ;;
        *)
            show_setup_menu
            ;;
    esac
}

# Function to show MCP servers menu
show_mcp_menu() {
    local choice
    choice=$(whiptail --title "🔧 ENHANCE YOUR TOOLKIT 🔧" --menu "█ Add powerful development tools █" 15 65 4 \
        "1" "🎭 Playwright (Web Automation)" \
        "2" "← Back to Setup" \
        3>&1 1>&2 2>&3)
    
    case $choice in
        1)
            install_playwright_mcp
            ;;
        2)
            show_setup_menu
            ;;
        *)
            show_setup_menu
            ;;
    esac
}

# Function to show LLM providers menu
show_llm_menu() {
    local choice
    choice=$(whiptail --title "🤖 LLM TOOL SELECTOR 🤖" --menu "█ Choose your AI coding companion █" 15 65 5 \
        "1" "🧠 Claude Code (Interactive Assistant)" \
        "2" "💬 LLM CLI (Command Line Tool)" \
        "3" "← Back to Setup" \
        3>&1 1>&2 2>&3)
    
    case $choice in
        1)
            setup_claude_provider
            ;;
        2)
            setup_llm_provider
            ;;
        3)
            show_setup_menu
            ;;
        *)
            show_setup_menu
            ;;
    esac
}

# Function to configure Anthropic API key
configure_anthropic_key() {
    local api_key
    api_key=$(whiptail --title "🧠 ANTHROPIC API KEY 🧠" --inputbox "Enter your Anthropic API key for Claude:" 10 65 3>&1 1>&2 2>&3)
    
    if [ $? -eq 0 ] && [ -n "$api_key" ]; then
         echo "export ANTHROPIC_API_KEY=\"$api_key\"" >> /workdir/.keys
        
        whiptail --title "✅ KEY ADDED ✅" --msgbox "Anthropic API key has been connected!\n\nClaude Code is now ready to use." 8 60
    fi
    show_api_keys_menu
}

# Function to configure OpenAI API key
configure_openai_key() {
    local api_key
    api_key=$(whiptail --title "🔌 OPENAI API KEY 🔌" --inputbox "Enter your OpenAI API key:" 10 65 3>&1 1>&2 2>&3)
    
    if [ $? -eq 0 ] && [ -n "$api_key" ]; then
        echo "export OPENAI_API_KEY=\"$api_key\"" >> /workdir/.keys
        
        whiptail --title "✅ KEY ADDED ✅" --msgbox "OpenAI API key has been connected!\n\nLLM CLI tool is now ready to use." 8 60
    fi
    show_api_keys_menu
}

# Function to install Playwright MCP
install_playwright_mcp() {
    if whiptail --title "🎭 PLAYWRIGHT SETUP 🎭" --yesno "┌─────────────────────────────────────────┐\n│  Adding Web Automation to your vibe...  │\n│                                         │\n│  🔧 This will install browser control  │\n│      tools for your coding session     │\n└─────────────────────────────────────────┘\n\n🚀 Add to your vibe?" 12 65; then
        echo ""
        echo -e "\033[1;33m⚡ ADDING PLAYWRIGHT TO YOUR VIBE... ⚡\033[0m"
        echo ""
        
        # Install playwright-mcp if not already installed
        if ! npm list -g playwright-mcp >/dev/null 2>&1; then
            npm install -g playwright-mcp
        fi
        
        claude mcp add --transport sse playwright http://127.0.0.1:7777/sse
        
        if [ $? -eq 0 ]; then
            whiptail --title "✅ TOOL ADDED ✅" --msgbox "┌─────────────────────────────────────────┐\n│  🎭 PLAYWRIGHT READY!                  │\n│                                         │\n│  ✓ Web automation tools loaded         │\n│  ✓ Browser control available           │\n│  ✓ Ready for your coding session       │\n└─────────────────────────────────────────┘" 10 65
        else
            whiptail --title "❌ SETUP FAILED ❌" --msgbox "┌─────────────────────────────────────────┐\n│  ⚠️  PLAYWRIGHT SETUP FAILED!         │\n│                                         │\n│  💥 Check system logs for errors       │\n│  🔧 Try adding the tool again          │\n└─────────────────────────────────────────┘" 10 65
        fi
    fi
    show_mcp_menu
}

# Function to setup Claude provider
setup_claude_provider() {
    # Check if Claude is available
    if command -v claude &> /dev/null; then
        if whiptail --title "🧠 CLAUDE CODE READY 🧠" --yesno "┌─────────────────────────────────────────┐\n│  🤖 CLAUDE CODE ASSISTANT DETECTED!   │\n│                                         │\n│  ✓ Interactive AI assistant ready      │\n│  ✓ Code generation & assistance        │\n│  ✓ Perfect for your coding session     │\n└─────────────────────────────────────────┘\n\n🚀 Start Claude Code now?" 12 65; then
            clear
            echo ""
            echo -e "\033[1;32m⚡ STARTING CLAUDE CODE... ⚡\033[0m"
            echo -e "\033[1;37mYour AI coding assistant is launching...\033[0m"
            echo ""
            exec claude
        fi
    else
        whiptail --title "❌ SETUP ISSUE ❌" --msgbox "┌─────────────────────────────────────────┐\n│  ⚠️  CLAUDE CODE NOT FOUND!           │\n│                                         │\n│  💥 Tool not properly installed        │\n│  🔧 Check your setup and try again     │\n└─────────────────────────────────────────┘" 10 65
    fi
    show_llm_menu
}

# Function to setup LLM CLI provider
setup_llm_provider() {
    # Check if LLM CLI is available
    if command -v llm &> /dev/null; then
        if whiptail --title "💬 LLM CLI READY 💬" --yesno "┌─────────────────────────────────────────┐\n│  🛠️  LLM COMMAND LINE TOOL DETECTED!   │\n│                                         │\n│  ✓ Fast command-line AI interactions   │\n│  ✓ Perfect for quick queries & tasks   │\n│  ✓ Ready for your coding workflow      │\n└─────────────────────────────────────────┘\n\n🚀 Start using LLM CLI now?" 12 65; then
            clear
            echo ""
            echo -e "\033[1;32m⚡ LLM CLI READY ⚡\033[0m"
            echo -e "\033[1;37mType '\033[1;33mllm\033[1;37m' followed by your question to get started\033[0m"
            echo -e "\033[1;37mExample: \033[1;33mllm 'explain this code'\033[1;37m\033[0m"
            echo ""
            return 0
        fi
    else
        whiptail --title "❌ SETUP ISSUE ❌" --msgbox "┌─────────────────────────────────────────┐\n│  ⚠️  LLM CLI NOT FOUND!               │\n│                                         │\n│  💥 Tool not properly installed        │\n│  🔧 Check your setup and try again     │\n└─────────────────────────────────────────┘" 10 65
    fi
    show_llm_menu
}

# Main execution
main() {
    # Show intro screen and wait for spacebar
    show_intro_screen
    
    # Show setup menu
    show_setup_menu
}

# Run the main function
main