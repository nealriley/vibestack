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
        echo "█                                                        █" | lolcat
        echo "█          ⚡ SYSTEM INITIALIZATION COMPLETE ⚡          █" | lolcat
        echo "█                                                        █" | lolcat
        echo "█                 Claude Code Terminal                   █" | lolcat
        echo "█              Powered by Anthropic AI                   █" | lolcat
        echo "█                                                        █" | lolcat
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
    echo -e "\033[1;37m              [ PRESS \033[1;33mSPACE\033[1;37m TO ENTER SETUP ]\033[0m"
    echo ""
    
    # Wait for spacebar press
    while true; do
        read -rsn1 key
        if [[ "$key" == " " ]]; then
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
        echo "║                      ⚙️  SETUP  ⚙️                       ║" | lolcat  
        echo "╚══════════════════════════════════════════════════════════╝" | lolcat
    else
        echo -e "\033[1;36m╔══════════════════════════════════════════════════════════╗\033[0m"
        echo -e "\033[1;36m║                      ⚙️  SETUP  ⚙️                       ║\033[0m"
        echo -e "\033[1;36m╚══════════════════════════════════════════════════════════╝\033[0m"
    fi
    echo ""
    
    local choice
    choice=$(whiptail --title "⚙️ VIBESTACK SETUP ⚙️" --menu "█ Select Configuration Module █" 15 65 4 \
        "1" "🔧 MCP Servers Module" \
        "2" "🤖 AI Provider Configuration" \
        "3" "🚀 Launch Combat Mode" \
        3>&1 1>&2 2>&3)
    
    case $choice in
        1)
            show_mcp_menu
            ;;
        2)
            show_llm_menu
            ;;
        3)
            echo ""
            echo -e "\033[1;32m⚡ ENTERING COMBAT MODE... ⚡\033[0m"
            echo -e "\033[1;37mType '\033[1;33mclaude\033[1;37m' to engage Claude Code AI Assistant\033[0m"
            echo ""
            return 0
            ;;
        *)
            echo ""
            echo -e "\033[1;32m⚡ SETUP COMPLETE ⚡\033[0m"
            echo -e "\033[1;37mType '\033[1;33mclaude\033[1;37m' to engage Claude Code AI Assistant\033[0m"
            echo ""
            return 0
            ;;
    esac
}

# Function to show MCP servers menu
show_mcp_menu() {
    local choice
    choice=$(whiptail --title "🔧 MCP SERVERS MODULE 🔧" --menu "█ Select Server Installation █" 15 65 4 \
        "1" "🎭 Playwright (Web Automation Engine)" \
        "2" "← Return to Setup Hub" \
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
    choice=$(whiptail --title "🤖 AI PROVIDER CONFIG 🤖" --menu "█ Select AI Combat Unit █" 15 65 4 \
        "1" "🧠 Claude (Anthropic Neural Core)" \
        "2" "← Return to Setup Hub" \
        3>&1 1>&2 2>&3)
    
    case $choice in
        1)
            setup_claude_provider
            ;;
        2)
            show_setup_menu
            ;;
        *)
            show_setup_menu
            ;;
    esac
}

# Function to install Playwright MCP
install_playwright_mcp() {
    if whiptail --title "🎭 PLAYWRIGHT INSTALLATION 🎭" --yesno "┌─────────────────────────────────────────┐\n│  Installing Web Automation Engine...   │\n│                                         │\n│  ⚠️  This will deploy combat-grade     │\n│      browser automation systems        │\n└─────────────────────────────────────────┘\n\n💀 Continue with installation?" 12 65; then
        echo ""
        echo -e "\033[1;33m⚡ DEPLOYING PLAYWRIGHT ENGINE... ⚡\033[0m"
        echo ""
        
        # Install playwright-mcp if not already installed
        if ! npm list -g playwright-mcp >/dev/null 2>&1; then
            npm install -g playwright-mcp
        fi
        
        # Add the MCP connection to Claude (this was moved from Dockerfile)
        claude mcp add --transport sse playwright http://127.0.0.1:7777/sse
        
        if [ $? -eq 0 ]; then
            whiptail --title "✅ MISSION SUCCESS ✅" --msgbox "┌─────────────────────────────────────────┐\n│  🎭 PLAYWRIGHT ENGINE DEPLOYED!       │\n│                                         │\n│  ✓ Web automation systems online       │\n│  ✓ Combat-ready browser control        │\n│  ✓ AI integration established          │\n└─────────────────────────────────────────┘" 10 65
        else
            whiptail --title "❌ MISSION FAILED ❌" --msgbox "┌─────────────────────────────────────────┐\n│  ⚠️  ENGINE DEPLOYMENT FAILED!        │\n│                                         │\n│  💥 Check system logs for errors       │\n│  🔧 Retry installation if needed       │\n└─────────────────────────────────────────┘" 10 65
        fi
    fi
    show_mcp_menu
}

# Function to setup Claude provider
setup_claude_provider() {
    # Check if Claude is available
    if command -v claude &> /dev/null; then
        if whiptail --title "🧠 CLAUDE NEURAL CORE 🧠" --yesno "┌─────────────────────────────────────────┐\n│  🤖 AI COMBAT UNIT DETECTED!          │\n│                                         │\n│  ✓ Claude Code systems operational     │\n│  ✓ Anthropic neural networks active    │\n│  ✓ Ready for immediate deployment      │\n└─────────────────────────────────────────┘\n\n🚀 Deploy Claude Code now?" 12 65; then
            clear
            echo ""
            echo -e "\033[1;32m⚡ DEPLOYING CLAUDE NEURAL CORE... ⚡\033[0m"
            echo -e "\033[1;37mAI systems coming online...\033[0m"
            echo ""
            exec claude
        fi
    else
        whiptail --title "❌ NEURAL CORE ERROR ❌" --msgbox "┌─────────────────────────────────────────┐\n│  ⚠️  CLAUDE CORE NOT DETECTED!        │\n│                                         │\n│  💥 AI systems not properly installed  │\n│  🔧 Check installation and retry       │\n└─────────────────────────────────────────┘" 10 65
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