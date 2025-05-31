#!/bin/bash

# VibeStack Interactive Startup Menu
# This script provides an interactive menu system for VibeStack

# Function to display VibeStack logo
show_logo() {
    clear
    echo ""
    
    # Check if lolcat is available, otherwise use basic colors
    if command -v lolcat &> /dev/null; then
        figlet -f small "Welcome toooo" 
        figlet -f big "Vibestack" | lolcat
    else
        # Fallback with ANSI colors
        echo -e "\033[1;35m$(figlet -f big 'Welcome to')\033[0m"
        echo -e "\033[1;36m$(figlet -f big 'VibeStack')\033[0m"
    fi
    echo ""
}

# Function to show main menu
show_main_menu() {
    local choice
    choice=$(whiptail --title "VibeStack Main Menu" --menu "Choose an option:" 15 60 4 \
        "1" "Install MCP Servers" \
        "2" "LLM Providers" \
        "3" "Exit to Shell" \
        3>&1 1>&2 2>&3)
    
    case $choice in
        1)
            show_mcp_menu
            ;;
        2)
            show_llm_menu
            ;;
        3)
            echo "Welcome to VibeStack! Type 'claude' to start Claude Code."
            return 0
            ;;
        *)
            echo "Welcome to VibeStack! Type 'claude' to start Claude Code."
            return 0
            ;;
    esac
}

# Function to show MCP servers menu
show_mcp_menu() {
    local choice
    choice=$(whiptail --title "MCP Servers" --menu "Choose an MCP server to install:" 15 60 4 \
        "1" "Playwright (Web automation)" \
        "2" "Back to Main Menu" \
        3>&1 1>&2 2>&3)
    
    case $choice in
        1)
            install_playwright_mcp
            ;;
        2)
            show_main_menu
            ;;
        *)
            show_main_menu
            ;;
    esac
}

# Function to show LLM providers menu
show_llm_menu() {
    local choice
    choice=$(whiptail --title "LLM Providers" --menu "Choose an LLM provider:" 15 60 4 \
        "1" "Claude (Anthropic)" \
        "2" "Back to Main Menu" \
        3>&1 1>&2 2>&3)
    
    case $choice in
        1)
            setup_claude_provider
            ;;
        2)
            show_main_menu
            ;;
        *)
            show_main_menu
            ;;
    esac
}

# Function to install Playwright MCP
install_playwright_mcp() {
    if whiptail --title "Install Playwright MCP" --yesno "This will install Playwright MCP server for web automation.\n\nContinue?" 10 60; then
        echo "Installing Playwright MCP server..."
        
        # Install playwright-mcp if not already installed
        if ! npm list -g playwright-mcp >/dev/null 2>&1; then
            npm install -g playwright-mcp
        fi
        
        # Add the MCP connection to Claude (this was moved from Dockerfile)
        claude mcp add --transport sse playwright http://127.0.0.1:7777/sse
        
        if [ $? -eq 0 ]; then
            whiptail --title "Success" --msgbox "Playwright MCP server has been successfully installed and configured!" 8 60
        else
            whiptail --title "Error" --msgbox "Failed to install Playwright MCP server. Please check the logs." 8 60
        fi
    fi
    show_mcp_menu
}

# Function to setup Claude provider
setup_claude_provider() {
    # Check if Claude is available
    if command -v claude &> /dev/null; then
        if whiptail --title "Claude Provider" --yesno "Claude Code is available!\n\nWould you like to start Claude Code now?" 10 60; then
            clear
            echo "Starting Claude Code..."
            exec claude
        fi
    else
        whiptail --title "Error" --msgbox "Claude Code is not properly installed. Please check the installation." 8 60
    fi
    show_llm_menu
}

# Main execution
main() {
    # Show logo first
    show_logo
    
    echo "Hello there" 
    
    # Show main menu
    show_main_menu
}

# Run the main function
main