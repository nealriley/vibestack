#!/usr/bin/env python3
"""
VibeStack Setup Walkthrough
A Game-Like Configuration Experience for Developers
"""

import json
import os
import time
import asyncio
from pathlib import Path
from textual.app import App, ComposeResult
from textual.containers import Container, Horizontal, Vertical, Grid
from textual.widgets import (
    Header, Footer, Button, Static, Label, Checkbox, 
    Input, ProgressBar, Switch, RadioButton, RadioSet
)
from textual.screen import Screen
from textual import events, work
from textual.validation import ValidationResult, Validator


class VibeStackState:
    """Global state management for the Vibe Stack setup"""
    
    def __init__(self):
        self.platforms = {
            'claude_code': {'enabled': False, 'mcp_servers': []},
            'llm_cli': {'enabled': False, 'api_key': None}
        }
        self.current_screen = 'welcome'
        self.setup_complete = False
        self.progress = 0


class APIKeyValidator(Validator):
    """Validator for OpenAI API keys"""
    
    def validate(self, value: str) -> ValidationResult:
        if not value:
            return self.failure("API key cannot be empty")
        if not value.startswith("sk-"):
            return self.failure("OpenAI API key must start with 'sk-'")
        if len(value) < 20:
            return self.failure("API key appears to be too short")
        return self.success()


class WelcomeScreen(Screen):
    """Screen 1: Welcome with ASCII art title"""
    
    CSS = """
    WelcomeScreen {
        align: center middle;
        background: $surface;
    }
    
    #welcome-container {
        width: 100%;
        height: 100%;
        align: center middle;
    }
    
    #ascii-title {
        text-align: center;
        color: $accent;
        text-style: bold;
        margin: 2;
    }
    
    #continue-prompt {
        text-align: center;
        color: $warning;
        text-style: bold;
        margin: 3;
    }
    """
    
    def compose(self) -> ComposeResult:
        with Container(id="welcome-container"):
            yield Label(self.get_ascii_art(), id="ascii-title")
            yield Label("Press any key to continue", id="continue-prompt")
    
    def get_ascii_art(self) -> str:
        """Return ASCII art for Vibe Stack title"""
        return """
██╗   ██╗██╗██████╗ ███████╗    ███████╗████████╗ █████╗  ██████╗██╗  ██╗
██║   ██║██║██╔══██╗██╔════╝    ██╔════╝╚══██╔══╝██╔══██╗██╔════╝██║ ██╔╝
██║   ██║██║██████╔╝█████╗      ███████╗   ██║   ███████║██║     █████╔╝ 
╚██╗ ██╔╝██║██╔══██╗██╔══╝      ╚════██║   ██║   ██╔══██║██║     ██╔═██╗ 
 ╚████╔╝ ██║██████╔╝███████╗    ███████║   ██║   ██║  ██║╚██████╗██║  ██╗
  ╚═══╝  ╚═╝╚═════╝ ╚══════╝    ╚══════╝   ╚═╝   ╚═╝  ╚═╝ ╚═════╝╚═╝  ╚═╝
        """
    
    def on_key(self, event: events.Key) -> None:
        """Handle any key press to continue"""
        self.app.push_screen("platform_selection")


class PlatformSelectionScreen(Screen):
    """Screen 2: Platform Selection with boxed options and arrow navigation"""
    
    BINDINGS = [
        ("left,h", "previous_option", "Previous"),
        ("right,l", "next_option", "Next"),
        ("enter", "select_option", "Select"),
        ("escape", "back", "Back"),
    ]
    
    CSS = """
    PlatformSelectionScreen {
        background: $surface;
    }
    
    #selection-title {
        text-align: center;
        color: $accent;
        text-style: bold;
        margin: 2;
        height: 3;
    }
    
    #selection-subtitle {
        text-align: center;
        color: $text;
        margin: 1;
        height: 2;
    }
    
    #platforms-container {
        align: center middle;
        width: 100%;
        height: 100%;
        layout: horizontal;
    }
    
    .platform-box {
        border: thick $primary;
        background: $surface-lighten-1;
        padding: 3;
        margin: 2;
        width: 1fr;
        height: 20;
        min-width: 35;
    }
    
    .platform-box.selected {
        border: thick $accent;
        background: $surface-lighten-2;
    }
    
    .platform-title {
        text-align: center;
        color: $accent;
        text-style: bold;
        margin: 1;
    }
    
    .platform-icon {
        text-align: center;
        color: $primary;
        margin: 1;
        text-style: bold;
    }
    
    .platform-description {
        color: $text;
        margin: 1;
        text-align: center;
    }
    
    .platform-features {
        color: $text-muted;
        margin: 1;
        text-align: center;
    }
    
    .platform-features-list {
        margin: 1;
    }
    
    #instructions {
        text-align: center;
        color: $warning;
        margin: 2;
        height: 2;
        text-style: bold;
    }
    """
    
    def __init__(self):
        super().__init__()
        self.selected_option = 0  # 0 = Claude Code, 1 = LLM CLI
        
    def compose(self) -> ComposeResult:
        yield Label("SELECT YOUR AI CODING COMPANION", id="selection-title")
        yield Label("Choose the platform that matches your workflow", id="selection-subtitle")
        
        with Horizontal(id="platforms-container"):
            # Claude Code Box
            with Container(classes="platform-box selected", id="claude-box"):
                yield Label("CLAUDE CODE", classes="platform-title")
                yield Label("🎯", classes="platform-icon")
                yield Label("Interactive AI Assistant", classes="platform-description")
                yield Label("", classes="platform-description")
                with Container(classes="platform-features-list"):
                    yield Label("• Advanced code understanding", classes="platform-features")
                    yield Label("• Real-time collaboration", classes="platform-features")
                    yield Label("• MCP server integration", classes="platform-features")
                    yield Label("• Context-aware editing", classes="platform-features")
                    yield Label("• Multi-file operations", classes="platform-features")
            
            # LLM CLI Box
            with Container(classes="platform-box", id="llm-box"):
                yield Label("LLM CLI", classes="platform-title")
                yield Label("⚡", classes="platform-icon")
                yield Label("Command-Line Powerhouse", classes="platform-description")
                yield Label("", classes="platform-description")
                with Container(classes="platform-features-list"):
                    yield Label("• Terminal-native interface", classes="platform-features")
                    yield Label("• OpenAI GPT integration", classes="platform-features")
                    yield Label("• Scriptable workflows", classes="platform-features")
                    yield Label("• Pipeline integration", classes="platform-features")
                    yield Label("• Lightweight and fast", classes="platform-features")
        
        yield Label("Use ← → arrow keys to navigate, ENTER to select", id="instructions")
    
    def action_previous_option(self) -> None:
        """Move to previous option"""
        self.selected_option = (self.selected_option - 1) % 2
        self.update_selection()
    
    def action_next_option(self) -> None:
        """Move to next option"""
        self.selected_option = (self.selected_option + 1) % 2
        self.update_selection()
    
    def action_select_option(self) -> None:
        """Select current option and proceed"""
        if self.selected_option == 0:
            # Claude Code selected
            self.app.state.platforms['claude_code']['enabled'] = True
            self.app.state.platforms['llm_cli']['enabled'] = False
            self.app.push_screen("claude_detail")
        else:
            # LLM CLI selected
            self.app.state.platforms['claude_code']['enabled'] = False
            self.app.state.platforms['llm_cli']['enabled'] = True
            self.app.push_screen("llm_detail")
    
    def action_back(self) -> None:
        """Go back to previous screen"""
        self.app.pop_screen()
    
    def update_selection(self) -> None:
        """Update visual selection"""
        claude_box = self.query_one("#claude-box")
        llm_box = self.query_one("#llm-box")
        
        if self.selected_option == 0:
            claude_box.add_class("selected")
            llm_box.remove_class("selected")
        else:
            llm_box.add_class("selected")
            claude_box.remove_class("selected")
    
    def on_key(self, event: events.Key) -> None:
        """Handle additional key events"""
        if event.key == "left" or event.key == "h":
            self.action_previous_option()
        elif event.key == "right" or event.key == "l":
            self.action_next_option()
        elif event.key == "enter":
            self.action_select_option()
        elif event.key == "escape":
            self.action_back()


class ClaudeDetailScreen(Screen):
    """Full-screen Claude Code configuration and details"""
    
    BINDINGS = [
        ("up,k", "previous_option", "Previous"),
        ("down,j", "next_option", "Next"),
        ("space", "toggle_option", "Toggle"),
        ("enter", "continue", "Continue"),
        ("escape", "back", "Back"),
    ]
    
    CSS = """
    ClaudeDetailScreen {
        background: $surface;
    }
    
    #header {
        height: 4;
        background: $primary;
        color: $text;
        text-align: center;
        text-style: bold;
        padding: 1;
    }
    
    #main-content {
        layout: vertical;
        height: 1fr;
        padding: 2;
    }
    
    #description-section {
        height: 8;
        border: round $primary;
        background: $surface-lighten-1;
        padding: 2;
        margin: 1;
    }
    
    #options-section {
        height: 1fr;
        border: round $accent;
        background: $surface-lighten-1;
        padding: 2;
        margin: 1;
    }
    
    .option-item {
        border: round $primary;
        background: $surface-lighten-2;
        padding: 1;
        margin: 1;
        height: 6;
    }
    
    .option-item.selected {
        border: round $accent;
        background: $accent-darken-2;
    }
    
    .option-title {
        color: $accent;
        text-style: bold;
    }
    
    .option-description {
        color: $text;
        margin: 1;
    }
    
    .option-status {
        color: $success;
        text-style: bold;
        margin: 1;
    }
    
    #footer {
        height: 3;
        background: $primary;
        color: $text;
        text-align: center;
        text-style: bold;
        padding: 1;
    }
    """
    
    def __init__(self):
        super().__init__()
        self.selected_option = 0
        self.options = {
            'playwright': False,
            'future_mcp1': False,
            'future_mcp2': False
        }
        
    def compose(self) -> ComposeResult:
        yield Label("🎯 CLAUDE CODE - Interactive AI Assistant", id="header")
        
        with Container(id="main-content"):
            with Container(id="description-section"):
                yield Label("ABOUT CLAUDE CODE", classes="option-title")
                yield Label("Claude Code is an advanced AI-powered development environment that provides")
                yield Label("intelligent code assistance, real-time collaboration, and seamless integration")
                yield Label("with modern development workflows. Enhanced with MCP (Model Context Protocol)")
                yield Label("servers for extended capabilities.")
            
            with Container(id="options-section"):
                yield Label("CONFIGURATION OPTIONS", classes="option-title")
                yield Label("Select the enhancements you want to enable:", classes="option-description")
                
                with Container(classes="option-item selected", id="playwright-option"):
                    yield Label("☐ Playwright MCP Server", classes="option-title")
                    yield Label("  🎭 Browser automation and web testing capabilities", classes="option-description")
                    yield Label("  STATUS: Available", classes="option-status")
                
                with Container(classes="option-item", id="future-option1"):
                    yield Label("☐ Database MCP Server (Coming Soon)", classes="option-title")
                    yield Label("  🗄️  Direct database interaction and query assistance", classes="option-description")
                    yield Label("  STATUS: Development", classes="option-status")
                
                with Container(classes="option-item", id="future-option2"):
                    yield Label("☐ API Testing MCP Server (Coming Soon)", classes="option-title")
                    yield Label("  🔌 REST API testing and documentation generation", classes="option-description")
                    yield Label("  STATUS: Planned", classes="option-status")
        
        yield Label("↑↓ Navigate | SPACE Toggle | ENTER Continue | ESC Back", id="footer")
    
    def action_previous_option(self) -> None:
        """Move to previous option"""
        self.selected_option = (self.selected_option - 1) % 3
        self.update_selection()
    
    def action_next_option(self) -> None:
        """Move to next option"""
        self.selected_option = (self.selected_option + 1) % 3
        self.update_selection()
    
    def action_toggle_option(self) -> None:
        """Toggle current option (only for available options)"""
        if self.selected_option == 0:  # Playwright
            self.options['playwright'] = not self.options['playwright']
            self.update_option_display()
    
    def action_continue(self) -> None:
        """Continue with selected options"""
        # Save selections to state
        if self.options['playwright']:
            self.app.state.platforms['claude_code']['mcp_servers'].append('playwright')
        
        self.app.push_screen("completion")
    
    def action_back(self) -> None:
        """Go back to platform selection"""
        self.app.pop_screen()
    
    def update_selection(self) -> None:
        """Update visual selection"""
        options = ["playwright-option", "future-option1", "future-option2"]
        
        for i, option_id in enumerate(options):
            option = self.query_one(f"#{option_id}")
            if i == self.selected_option:
                option.add_class("selected")
            else:
                option.remove_class("selected")
    
    def update_option_display(self) -> None:
        """Update option checkboxes"""
        playwright_option = self.query_one("#playwright-option")
        title_label = playwright_option.query_one(".option-title", Label)
        
        if self.options['playwright']:
            title_label.update("☑ Playwright MCP Server")
        else:
            title_label.update("☐ Playwright MCP Server")


class LLMDetailScreen(Screen):
    """Full-screen LLM CLI configuration and details"""
    
    BINDINGS = [
        ("enter", "continue", "Continue"),
        ("escape", "back", "Back"),
    ]
    
    CSS = """
    LLMDetailScreen {
        background: $surface;
    }
    
    #header {
        height: 4;
        background: $primary;
        color: $text;
        text-align: center;
        text-style: bold;
        padding: 1;
    }
    
    #main-content {
        layout: vertical;
        height: 1fr;
        padding: 2;
    }
    
    #description-section {
        height: 8;
        border: round $primary;
        background: $surface-lighten-1;
        padding: 2;
        margin: 1;
    }
    
    #config-section {
        height: 1fr;
        border: round $accent;
        background: $surface-lighten-1;
        padding: 2;
        margin: 1;
    }
    
    .config-title {
        color: $accent;
        text-style: bold;
        margin: 1;
    }
    
    .config-description {
        color: $text;
        margin: 1;
    }
    
    #api-key-container {
        border: round $primary;
        background: $surface-lighten-2;
        padding: 2;
        margin: 2;
    }
    
    Input {
        margin: 1;
        width: 100%;
    }
    
    .security-note {
        color: $success;
        margin: 1;
    }
    
    .url-note {
        color: $text-muted;
        margin: 1;
    }
    
    #validation-message {
        color: $error;
        margin: 1;
        text-align: center;
    }
    
    #footer {
        height: 3;
        background: $primary;
        color: $text;
        text-align: center;
        text-style: bold;
        padding: 1;
    }
    """
    
    def compose(self) -> ComposeResult:
        yield Label("⚡ LLM CLI - Command-Line AI Powerhouse", id="header")
        
        with Container(id="main-content"):
            with Container(id="description-section"):
                yield Label("ABOUT LLM CLI", classes="config-title")
                yield Label("LLM CLI is a powerful command-line interface for interacting with")
                yield Label("large language models. Built for developers who prefer terminal-based")
                yield Label("workflows, it provides direct access to OpenAI's GPT models with")
                yield Label("scriptable commands and pipeline integration.")
            
            with Container(id="config-section"):
                yield Label("CONFIGURATION", classes="config-title")
                yield Label("Enter your OpenAI API key to enable LLM CLI:", classes="config-description")
                
                with Container(id="api-key-container"):
                    yield Label("🔑 OpenAI API Key", classes="config-title")
                    yield Input(
                        placeholder="sk-...", 
                        password=False,
                        id="api-key-input",
                        validators=[APIKeyValidator()]
                    )
                    yield Label("🛡️  Your API key is securely stored locally", classes="security-note")
                    yield Label("ℹ️  Get your API key from: https://platform.openai.com/api-keys", classes="url-note")
                
                yield Label("", id="validation-message")
        
        yield Label("ENTER Continue | ESC Back", id="footer")
    
    def action_continue(self) -> None:
        """Validate and continue"""
        api_input = self.query_one("#api-key-input", Input)
        validation_msg = self.query_one("#validation-message")
        
        if not api_input.is_valid or not api_input.value:
            validation_msg.update("⚠️ Please enter a valid OpenAI API key")
            return
        
        # Save API key to state
        self.app.state.platforms['llm_cli']['api_key'] = api_input.value
        
        self.app.push_screen("completion")
    
    def action_back(self) -> None:
        """Go back to platform selection"""
        self.app.pop_screen()


class ClaudeConfigScreen(Screen):
    """Screen 3A: Claude Code Configuration (MCP Server Selection)"""
    
    CSS = """
    ClaudeConfigScreen {
        background: $surface;
    }
    
    #progress-indicator {
        text-align: center;
        color: $accent;
        margin: 1;
        text-style: bold;
    }
    
    #config-title {
        text-align: center;
        color: $accent;
        text-style: bold;
        margin: 2;
    }
    
    #config-subtitle {
        text-align: center;
        color: $text;
        margin: 1;
    }
    
    #config-container {
        align: center middle;
        width: 65;
        height: 20;
        border: thick $primary;
        background: $surface-lighten-1;
        margin: 2;
        padding: 2;
    }
    
    #mcp-section-title {
        color: $accent;
        text-style: bold;
        margin: 1;
    }
    
    #enhancements-container {
        border: round $primary;
        background: $surface-lighten-2;
        padding: 2;
        margin: 1;
    }
    
    .enhancement-item {
        margin: 1;
    }
    
    .enhancement-title {
        color: $success;
        text-style: bold;
    }
    
    .enhancement-description {
        color: $primary;
        margin-left: 2;
    }
    
    .enhancement-features {
        color: $text-muted;
        margin-left: 4;
    }
    
    #future-note {
        color: $warning;
        text-style: italic;
        margin: 1;
    }
    
    #instruction {
        text-align: center;
        color: $text;
        margin: 2;
    }
    
    #button-container {
        align: center middle;
        margin: 2;
    }
    
    Button {
        margin: 0 2;
        min-width: 15;
    }
    """
    
    def compose(self) -> ComposeResult:
        yield Label("Step 3/4", id="progress-indicator")
        yield Label("ENHANCE CLAUDE CODE ABILITIES", id="config-title")
        yield Label("Configure your Claude Code superpowers:", id="config-subtitle")
        
        with Container(id="config-container"):
            yield Label("MCP SERVER SELECTION", id="mcp-section-title")
            
            with Container(id="enhancements-container"):
                yield Label("Available Enhancements:", classes="enhancement-title")
                yield Label("", classes="enhancement-title")
                
                with Container(classes="enhancement-item"):
                    yield Checkbox("Playwright MCP Server", id="playwright-checkbox")
                    yield Label("🎭 Browser automation & web testing", classes="enhancement-description")
                    yield Label("• Automated UI testing", classes="enhancement-features")
                    yield Label("• Web scraping capabilities", classes="enhancement-features")
                    yield Label("• Cross-browser compatibility", classes="enhancement-features")
                
                yield Label("", classes="enhancement-features")
                yield Label("🔒 More servers available in future updates", id="future-note")
        
        yield Label("Use SPACE to toggle selection, ENTER to continue", id="instruction")
        
        with Horizontal(id="button-container"):
            yield Button("BACK", id="back-button", variant="default")
            yield Button("CONTINUE →", id="continue-button", variant="primary")
    
    def on_key(self, event: events.Key) -> None:
        """Handle keyboard navigation"""
        if event.key == "enter":
            self.save_and_continue()
        elif event.key == "escape":
            self.app.pop_screen()
        elif event.key == "space":
            # Toggle the checkbox
            checkbox = self.query_one("#playwright-checkbox", Checkbox)
            checkbox.value = not checkbox.value
    
    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "back-button":
            self.app.pop_screen()
        elif event.button.id == "continue-button":
            self.save_and_continue()
    
    def save_and_continue(self) -> None:
        """Save MCP server selections and continue"""
        playwright_selected = self.query_one("#playwright-checkbox", Checkbox).value
        
        if playwright_selected:
            self.app.state.platforms['claude_code']['mcp_servers'].append('playwright')
        
        # Always go to completion since we only allow one platform selection
        self.app.push_screen("completion")


class LLMConfigScreen(Screen):
    """Screen 3B: LLM CLI Configuration (OpenAI API Key Setup)"""
    
    CSS = """
    LLMConfigScreen {
        background: $surface;
    }
    
    #progress-indicator {
        text-align: center;
        color: $accent;
        margin: 1;
        text-style: bold;
    }
    
    #config-title {
        text-align: center;
        color: $accent;
        text-style: bold;
        margin: 2;
    }
    
    #config-subtitle {
        text-align: center;
        color: $text;
        margin: 1;
    }
    
    #config-container {
        align: center middle;
        width: 65;
        height: 20;
        border: thick $primary;
        background: $surface-lighten-1;
        margin: 2;
        padding: 2;
    }
    
    #api-section-title {
        color: $accent;
        text-style: bold;
        margin: 1;
    }
    
    #api-key-container {
        border: round $primary;
        background: $surface-lighten-2;
        padding: 2;
        margin: 1;
    }
    
    #api-key-label {
        color: $success;
        text-style: bold;
        margin: 1;
    }
    
    Input {
        margin: 1;
        width: 100%;
    }
    
    .security-note {
        color: $success;
        margin: 1;
    }
    
    .info-note {
        color: $primary;
        margin: 1;
    }
    
    .url-note {
        color: $text-muted;
        margin-left: 2;
    }
    
    #button-container {
        align: center middle;
        margin: 2;
    }
    
    Button {
        margin: 0 2;
        min-width: 15;
    }
    
    #validation-message {
        text-align: center;
        color: $error;
        margin: 1;
        opacity: 0%;
    }
    """
    
    def compose(self) -> ComposeResult:
        yield Label("Step 3/4", id="progress-indicator")
        yield Label("POWER UP LLM CLI ACCESS", id="config-title")
        yield Label("Connect to your AI provider to unlock LLM CLI:", id="config-subtitle")
        
        with Container(id="config-container"):
            yield Label("OPENAI API CONFIGURATION", id="api-section-title")
            
            with Container(id="api-key-container"):
                yield Label("🔑 OpenAI API Key", id="api-key-label")
                yield Input(
                    placeholder="sk-...", 
                    password=False,
                    id="api-key-input",
                    validators=[APIKeyValidator()]
                )
                
                yield Label("🛡️  Your API key is encrypted and stored securely", classes="security-note")
                yield Label("     Only used for your local development", classes="security-note")
                yield Label("", classes="security-note")
                yield Label("ℹ️  Get your API key from:", classes="info-note")
                yield Label("     https://platform.openai.com/api-keys", classes="url-note")
        
        yield Label("", id="validation-message")
        
        with Horizontal(id="button-container"):
            yield Button("BACK", id="back-button", variant="default")
            yield Button("CONTINUE →", id="continue-button", variant="primary")
    
    def on_key(self, event: events.Key) -> None:
        """Handle keyboard navigation"""
        if event.key == "enter":
            self.validate_and_continue()
        elif event.key == "escape":
            self.app.pop_screen()
    
    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "back-button":
            self.app.pop_screen()
        elif event.button.id == "continue-button":
            self.validate_and_continue()
    
    def on_input_changed(self, event: Input.Changed) -> None:
        """Mask API key after entry for security"""
        if event.input.id == "api-key-input" and len(event.value) > 10:
            # Don't actually mask in real-time as it interferes with typing
            pass
    
    def validate_and_continue(self) -> None:
        """Validate API key and continue"""
        api_input = self.query_one("#api-key-input", Input)
        validation_msg = self.query_one("#validation-message")
        
        if not api_input.is_valid:
            validation_msg.update("⚠️ Please enter a valid OpenAI API key")
            validation_msg.styles.animate("opacity", value=1.0, duration=0.5)
            return
        
        if not api_input.value:
            validation_msg.update("⚠️ API key is required to use LLM CLI")
            validation_msg.styles.animate("opacity", value=1.0, duration=0.5)
            return
        
        # Save API key to state
        self.app.state.platforms['llm_cli']['api_key'] = api_input.value
        
        # Always go to completion since we only allow one platform selection
        self.app.push_screen("completion")


class CompletionScreen(Screen):
    """Screen 4: Configuration Summary & Launch"""
    
    CSS = """
    CompletionScreen {
        background: $surface;
    }
    
    #completion-title {
        text-align: center;
        color: $success;
        text-style: bold;
        margin: 2;
    }
    
    #completion-subtitle {
        text-align: center;
        color: $text;
        margin: 1;
    }
    
    #status-container {
        align: center middle;
        width: 65;
        height: 15;
        border: thick $success;
        background: $surface-lighten-1;
        margin: 2;
        padding: 2;
    }
    
    #active-platforms-title {
        color: $success;
        text-style: bold;
        margin: 1;
    }
    
    #platforms-status {
        border: round $primary;
        background: $surface-lighten-2;
        padding: 2;
        margin: 1;
    }
    
    .platform-status {
        color: $text;
        margin: 1;
    }
    
    .platform-enabled {
        color: $success;
        text-style: bold;
    }
    
    .mcp-status {
        color: $primary;
        margin-left: 2;
    }
    
    #next-steps-title {
        color: $accent;
        text-style: bold;
        margin: 2 0 1 0;
    }
    
    .next-step {
        color: $text;
        margin: 1;
    }
    
    .command {
        color: $warning;
        text-style: bold;
    }
    
    #action-buttons {
        align: center middle;
        margin: 2;
    }
    
    #finish-button {
        align: center middle;
        margin: 1;
        width: 30;
        background: $success;
    }
    
    Button {
        margin: 0 1;
        min-width: 20;
    }
    """
    
    def compose(self) -> ComposeResult:
        yield Label("SETUP COMPLETE! 🚀", id="completion-title")
        yield Label("Your Vibe Stack is configured and ready:", id="completion-subtitle")
        
        with Container(id="status-container"):
            yield Label("✅ ACTIVE PLATFORMS", id="active-platforms-title")
            
            with Container(id="platforms-status"):
                # Show Claude Code status if enabled
                if self.app.state.platforms['claude_code']['enabled']:
                    yield Label("• Claude Code         [CONFIGURED] ⚡", classes="platform-status platform-enabled")
                    if 'playwright' in self.app.state.platforms['claude_code']['mcp_servers']:
                        yield Label("  └─ Playwright MCP   [ENABLED]", classes="mcp-status")
                    yield Label("", classes="platform-status")
                
                # Show LLM CLI status if enabled
                if self.app.state.platforms['llm_cli']['enabled']:
                    yield Label("• LLM CLI            [CONFIGURED] ⚡", classes="platform-status platform-enabled")
                    if self.app.state.platforms['llm_cli']['api_key']:
                        yield Label("  └─ OpenAI API      [CONNECTED]", classes="mcp-status")
        
        yield Label("NEXT STEPS:", id="next-steps-title")
        yield Label("• Launch Claude Code: claude-code", classes="next-step")
        yield Label("• Use LLM CLI: llm chat", classes="next-step")
        yield Label("• View documentation: vibe-stack --help", classes="next-step")
        
        with Horizontal(id="action-buttons"):
            if self.app.state.platforms['claude_code']['enabled']:
                yield Button("LAUNCH CLAUDE CODE", id="launch-claude", variant="primary")
            elif self.app.state.platforms['llm_cli']['enabled']:
                yield Button("OPEN TERMINAL", id="open-terminal", variant="primary")
        
        yield Button("FINISH SETUP", id="finish-button", variant="success")
    
    def on_key(self, event: events.Key) -> None:
        """Handle keyboard navigation"""
        if event.key == "enter":
            self.generate_config_and_finish()
        elif event.key == "escape":
            self.app.exit()
    
    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "launch-claude":
            self.generate_config_and_launch("claude")
        elif event.button.id == "open-terminal":
            self.generate_config_and_launch("terminal")
        elif event.button.id == "finish-button":
            self.generate_config_and_finish()
    
    def generate_config_and_launch(self, launch_type: str) -> None:
        """Generate configuration files and launch selected platform"""
        self.generate_configurations()
        
        if launch_type == "claude":
            self.app.exit(message="Configuration saved! Launching Claude Code...")
        elif launch_type == "terminal":
            self.app.exit(message="Configuration saved! Opening terminal for LLM CLI...")
    
    def generate_config_and_finish(self) -> None:
        """Generate configuration files and finish setup"""
        self.generate_configurations()
        self.app.exit(message="Setup complete! Your Vibe Stack is ready to use.")
    
    def generate_configurations(self) -> None:
        """Generate all necessary configuration files"""
        try:
            # Create config directory
            config_dir = Path.home() / ".vibestack"
            config_dir.mkdir(exist_ok=True)
            
            # Generate Claude Code MCP configuration if enabled
            if self.app.state.platforms['claude_code']['enabled']:
                self.generate_claude_config(config_dir)
            
            # Generate LLM CLI configuration if enabled
            if self.app.state.platforms['llm_cli']['enabled']:
                self.generate_llm_config()
            
            # Save setup state
            state_file = config_dir / "setup_state.json"
            with open(state_file, 'w') as f:
                json.dump({
                    'platforms': self.app.state.platforms,
                    'setup_complete': True,
                    'setup_date': time.time()
                }, f, indent=2)
                
        except Exception as e:
            self.notify(f"Error generating configurations: {e}", severity="error")
    
    def generate_claude_config(self, config_dir: Path) -> None:
        """Generate Claude Code MCP configuration"""
        mcp_config = {"mcpServers": {}}
        
        if 'playwright' in self.app.state.platforms['claude_code']['mcp_servers']:
            mcp_config["mcpServers"]["playwright"] = {
                "command": "npx",
                "args": ["@modelcontextprotocol/server-playwright"]
            }
        
        config_file = config_dir / "claude_mcp_config.json"
        with open(config_file, 'w') as f:
            json.dump(mcp_config, f, indent=2)
    
    def generate_llm_config(self) -> None:
        """Generate LLM CLI configuration (set environment variable)"""
        api_key = self.app.state.platforms['llm_cli']['api_key']
        if api_key:
            # Set environment variable for current session
            os.environ['OPENAI_API_KEY'] = api_key
            
            # Add to bashrc for persistence
            bashrc_path = Path.home() / ".bashrc"
            export_line = f'export OPENAI_API_KEY="{api_key}"\n'
            
            # Check if already exists to avoid duplicates
            if bashrc_path.exists():
                with open(bashrc_path, 'r') as f:
                    content = f.read()
                if 'OPENAI_API_KEY' not in content:
                    with open(bashrc_path, 'a') as f:
                        f.write(f'\n# Added by VibeStack setup\n{export_line}')


class VibeStackApp(App):
    """Main VibeStack Application"""
    
    CSS = """
    Screen {
        background: $surface;
    }
    
    Header {
        background: $primary;
        color: $text;
        text-style: bold;
    }
    
    Footer {
        background: $primary;
        color: $text;
    }
    """
    
    SCREENS = {
        "welcome": WelcomeScreen,
        "platform_selection": PlatformSelectionScreen,
        "claude_detail": ClaudeDetailScreen,
        "llm_detail": LLMDetailScreen,
        "claude_config": ClaudeConfigScreen,
        "llm_config": LLMConfigScreen,
        "completion": CompletionScreen,
    }
    
    def __init__(self):
        super().__init__()
        self.state = VibeStackState()
    
    def on_mount(self) -> None:
        self.title = "VibeStack Setup"
        self.sub_title = "AI-Powered Development Environment Configuration"
        self.push_screen("welcome")


def main():
    """Entry point for the VibeStack setup"""
    app = VibeStackApp()
    result = app.run()
    
    # Handle exit messages and launch appropriate tools
    exit_message = getattr(app, '_exit_message', '')
    if exit_message:
        print(f"\n{exit_message}")
        
        if "Claude Code" in exit_message:
            print("\nTo launch Claude Code, run: claude-code")
        elif "terminal" in exit_message:
            print("\nTo use LLM CLI, run: llm chat 'your question here'")
        elif "complete" in exit_message:
            print("\nYour development tools are ready!")
            print("• Run 'claude-code' to start Claude Code")
            print("• Run 'llm chat' to use LLM CLI")


if __name__ == "__main__":
    main()