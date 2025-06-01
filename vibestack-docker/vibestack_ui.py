#!/usr/bin/env python3
"""
VibeStack - Modern Terminal UI
A Textual-based interface for VibeStack configuration and management
"""

from textual.app import App, ComposeResult
from textual.containers import Container, Horizontal, Vertical
from textual.widgets import Header, Footer, Button, Static, Label
from textual.screen import Screen
from textual import events
import sys
import os
import asyncio


class VibeLogo(Static):
    """Custom widget for the VibeStack logo"""
    
    def compose(self) -> ComposeResult:
        yield Label("""
██╗   ██╗██╗██████╗ ███████╗███████╗████████╗ █████╗  ██████╗██╗  ██╗
██║   ██║██║██╔══██╗██╔════╝██╔════╝╚══██╔══╝██╔══██╗██╔════╝██║ ██╔╝
██║   ██║██║██████╔╝█████╗  ███████╗   ██║   ███████║██║     █████╔╝ 
╚██╗ ██╔╝██║██╔══██╗██╔══╝  ╚════██║   ██║   ██╔══██║██║     ██╔═██╗ 
 ╚████╔╝ ██║██████╔╝███████╗███████║   ██║   ██║  ██║╚██████╗██║  ██╗
  ╚═══╝  ╚═╝╚═════╝ ╚══════╝╚══════╝   ╚═╝   ╚═╝  ╚═╝ ╚═════╝╚═╝  ╚═╝
        """, id="logo")


class IntroScreen(Screen):
    """Welcome screen with logo and system status"""
    
    CSS = """
    IntroScreen {
        align: center middle;
        background: $surface;
    }
    
    #logo {
        text-align: center;
        color: $accent;
        text-style: bold;
        margin: 1;
        opacity: 0%;
    }
    
    #status-container {
        width: 60;
        height: 15;
        border: thick $primary;
        background: $surface-lighten-1;
        margin: 2;
        opacity: 0%;
    }
    
    #status-content {
        padding: 2;
        text-align: center;
    }
    
    #system-status {
        color: $success;
        text-style: bold;
        margin: 1;
    }
    
    #subtitle {
        color: $text-muted;
        margin: 1;
    }
    
    #continue-prompt {
        color: $warning;
        text-style: bold;
        margin: 2;
        opacity: 0%;
    }
    
    Button {
        margin: 1;
        min-width: 20;
    }
    """
    
    def compose(self) -> ComposeResult:
        yield VibeLogo()
        
        with Container(id="status-container"):
            with Vertical(id="status-content"):
                yield Label("⚡ SYSTEM INITIALIZATION COMPLETE ⚡", id="system-status")
                yield Label("Claude Code Terminal", id="subtitle1")
                yield Label("Powered by Anthropic AI", id="subtitle2")
                yield Label("STATUS: READY", id="ready-status")
                yield Label("[ PRESS ENTER TO CONTINUE ]", id="continue-prompt")
    
    def on_mount(self) -> None:
        """Start animations when screen mounts"""
        # Animate logo fade-in
        logo = self.query_one("#logo")
        logo.styles.animate("opacity", value=1.0, duration=1.5, delay=0.5)
        
        # Animate status container fade-in  
        status_container = self.query_one("#status-container")
        status_container.styles.animate("opacity", value=1.0, duration=1.5, delay=1.5)
        
        # Animate continue prompt fade-in
        continue_prompt = self.query_one("#continue-prompt")
        continue_prompt.styles.animate("opacity", value=1.0, duration=1.0, delay=3.5)
    
    def on_key(self, event: events.Key) -> None:
        if event.key == "enter":
            self.app.push_screen("setup")


class SetupScreen(Screen):
    """Main setup screen with configuration options"""
    
    CSS = """
    SetupScreen {
        background: $surface;
    }
    
    #setup-header {
        text-align: center;
        color: $accent;
        text-style: bold;
        margin: 1;
        padding: 1;
        border: thick $primary;
        background: $surface-lighten-1;
    }
    
    #menu-container {
        align: center middle;
        width: 80;
        height: 20;
        border: thick $primary;
        background: $surface-lighten-1;
        margin: 2;
    }
    
    #menu-content {
        padding: 2;
        width: 100%;
    }
    
    Button {
        width: 100%;
        margin: 1;
        height: 3;
        background: $primary;
        color: $text;
    }
    
    Button:hover {
        background: $primary-lighten-1;
        color: $text;
    }
    
    Button:focus {
        background: $accent;
        color: $text;
    }
    """
    
    def compose(self) -> ComposeResult:
        yield Header()
        
        yield Label("✨ CREATE YOUR VIBE CODING KIT ✨", id="setup-header")
        
        with Container(id="menu-container"):
            with Vertical(id="menu-content"):
                yield Button("🔑 Configure API Keys", id="api-keys", variant="primary")
                yield Button("🔧 Add MCP Tools", id="mcp-tools", variant="primary") 
                yield Button("🤖 Select LLM Tool", id="llm-tool", variant="primary")
                yield Button("🚀 Start Coding Session", id="start-session", variant="success")
        
        yield Footer()
    
    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "api-keys":
            self.app.push_screen("api-keys")
        elif event.button.id == "mcp-tools":
            self.app.push_screen("mcp-tools")
        elif event.button.id == "llm-tool":
            self.app.push_screen("llm-selection")
        elif event.button.id == "start-session":
            self.start_coding_session()
    
    def start_coding_session(self) -> None:
        self.app.exit(message="Starting coding session...")


class ApiKeysScreen(Screen):
    """API Keys configuration screen"""
    
    CSS = """
    ApiKeysScreen {
        background: $surface;
    }
    
    #api-header {
        text-align: center;
        color: $accent;
        text-style: bold;
        margin: 1;
        padding: 1;
        border: thick $primary;
        background: $surface-lighten-1;
    }
    
    #api-container {
        align: center middle;
        width: 60;
        height: 15;
        border: thick $primary;
        background: $surface-lighten-1;
        margin: 2;
    }
    
    #api-content {
        padding: 2;
        width: 100%;
    }
    
    Button {
        width: 100%;
        margin: 1;
        height: 3;
    }
    """
    
    def compose(self) -> ComposeResult:
        yield Header()
        
        yield Label("🔑 API KEYS CONFIG 🔑", id="api-header")
        
        with Container(id="api-container"):
            with Vertical(id="api-content"):
                yield Button("🧠 Anthropic API Key (Claude)", id="anthropic-key", variant="primary")
                yield Button("🔌 OpenAI API Key", id="openai-key", variant="primary")
                yield Button("← Back to Setup", id="back", variant="default")
        
        yield Footer()
    
    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "back":
            self.app.pop_screen()
        elif event.button.id == "anthropic-key":
            # TODO: Implement API key input dialog
            self.notify("Anthropic API key configuration coming soon!")
        elif event.button.id == "openai-key":
            # TODO: Implement API key input dialog
            self.notify("OpenAI API key configuration coming soon!")


class MCPToolsScreen(Screen):
    """MCP Tools configuration screen"""
    
    CSS = """
    MCPToolsScreen {
        background: $surface;
    }
    
    #mcp-header {
        text-align: center;
        color: $accent;
        text-style: bold;
        margin: 1;
        padding: 1;
        border: thick $primary;
        background: $surface-lighten-1;
    }
    
    #mcp-container {
        align: center middle;
        width: 60;
        height: 12;
        border: thick $primary;
        background: $surface-lighten-1;
        margin: 2;
    }
    
    #mcp-content {
        padding: 2;
        width: 100%;
    }
    
    Button {
        width: 100%;
        margin: 1;
        height: 3;
    }
    """
    
    def compose(self) -> ComposeResult:
        yield Header()
        
        yield Label("🔧 ENHANCE YOUR TOOLKIT 🔧", id="mcp-header")
        
        with Container(id="mcp-container"):
            with Vertical(id="mcp-content"):
                yield Button("🎭 Playwright (Web Automation)", id="playwright", variant="primary")
                yield Button("← Back to Setup", id="back", variant="default")
        
        yield Footer()
    
    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "back":
            self.app.pop_screen()
        elif event.button.id == "playwright":
            # TODO: Implement Playwright MCP setup
            self.notify("Playwright MCP setup coming soon!")


class LLMSelectionScreen(Screen):
    """LLM Tool selection screen"""
    
    CSS = """
    LLMSelectionScreen {
        background: $surface;
    }
    
    #llm-header {
        text-align: center;
        color: $accent;
        text-style: bold;
        margin: 1;
        padding: 1;
        border: thick $primary;
        background: $surface-lighten-1;
    }
    
    #llm-container {
        align: center middle;
        width: 60;
        height: 15;
        border: thick $primary;
        background: $surface-lighten-1;
        margin: 2;
    }
    
    #llm-content {
        padding: 2;
        width: 100%;
    }
    
    Button {
        width: 100%;
        margin: 1;
        height: 3;
    }
    """
    
    def compose(self) -> ComposeResult:
        yield Header()
        
        yield Label("🤖 LLM TOOL SELECTOR 🤖", id="llm-header")
        
        with Container(id="llm-container"):
            with Vertical(id="llm-content"):
                yield Button("🧠 Claude Code (Interactive Assistant)", id="claude-code", variant="primary")
                yield Button("💬 LLM CLI (Command Line Tool)", id="llm-cli", variant="primary")
                yield Button("← Back to Setup", id="back", variant="default")
        
        yield Footer()
    
    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "back":
            self.app.pop_screen()
        elif event.button.id == "claude-code":
            self.app.exit(message="Starting Claude Code...")
        elif event.button.id == "llm-cli":
            self.notify("LLM CLI ready! Type 'llm' followed by your question.")


class VibeStackApp(App):
    """Main VibeStack application"""
    
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
        "intro": IntroScreen,
        "setup": SetupScreen,
        "api-keys": ApiKeysScreen,
        "mcp-tools": MCPToolsScreen,
        "llm-selection": LLMSelectionScreen,
    }
    
    def on_mount(self) -> None:
        self.title = "VibeStack"
        self.sub_title = "Modern AI Development Environment"
        self.push_screen("intro")


def main():
    """Entry point for the VibeStack UI"""
    app = VibeStackApp()
    result = app.run()
    
    # Handle exit messages
    if hasattr(app, '_exit_message'):
        print(f"\n{app._exit_message}")
        if "Claude Code" in app._exit_message:
            os.system("claude")
        elif "coding session" in app._exit_message.lower():
            print("Your tools are ready! Type 'claude' or 'llm' to begin")


if __name__ == "__main__":
    main()