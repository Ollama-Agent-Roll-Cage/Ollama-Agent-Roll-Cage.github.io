#!/usr/bin/env python3
import os
import sys
import argparse
from rich.console import Console
from rich.markdown import Markdown
from rich.prompt import Prompt
from rich.panel import Panel

console = Console()

def print_help():
    help_text = """
    OARC Butler CLI Commands:
    ------------------------
    /help       - Show this help message
    /quit       - Exit the program
    /about      - Learn about OARC
    /components - List OARC components
    /agent      - What is an Agent?
    /speech     - Speech-to-Speech architecture
    /docs       - Get documentation links
    /discord    - Get Discord invite link
    
    Just type your question normally for other queries!
    """
    console.print(Panel(help_text, title="Help", border_style="blue"))

def handle_command(command):
    commands = {
        '/help': lambda: print_help(),
        '/quit': lambda: sys.exit(0),
        '/about': lambda: print_info_panel("About OARC", 
            "Ollama Agent Roll Cage (OARC) is a Python-based framework combining the power of ollama LLMs, "
            "Coqui-TTS, Keras classifiers, LLaVA Vision, Whisper Speech Recognition, and YOLOv8 Object Detection "
            "into a unified chatbot agent API for local, custom automation."),
        '/components': lambda: print_info_panel("Core Components", 
            "• Modal Flags (TTS_FLAG, STT_FLAG, LLAVA_FLAG)\n"
            "• Models Configuration\n"
            "• Tool Integration\n"
            "• Speech Processing Pipeline"),
        '/agent': lambda: print_info_panel("What is an Agent?", 
            '"An agent refers to the algorithmic logic that wraps a model and via iteration, '
            'generates the chain of thought output for the model" — Borch'),
        '/speech': lambda: print_info_panel("Speech-to-Speech", 
            "OARC implements a sophisticated speech-to-speech pipeline with:\n"
            "• Silence removal preprocess\n"
            "• Smart user interrupt\n"
            "• Wake words\n"
            "• Debate moderator mode"),
        '/docs': lambda: print_info_panel("Documentation Links",
            "• [link=https://github.com/Ollama-Agent-Roll-Cage/oarc/blob/master/docs/what_is_an_agent/what_is_an_agent.md]What is an Agent?[/link]\n"
            "• [link=https://github.com/Ollama-Agent-Roll-Cage/oarc/tree/master/docs/speech_to_speech]Speech-to-Speech Documentation[/link]\n"
            "• [link=https://github.com/Leoleojames1/agentChef/tree/main/docs]AgentChef Documentation[/link]"),
        '/discord': lambda: print_info_panel("Discord", 
            "Join our Discord community: [link=https://discord.gg/dAzSYcnpdF]https://discord.gg/dAzSYcnpdF[/link]")
    }
    return commands.get(command, lambda: False)()

def print_info_panel(title, content):
    console.print(Panel(Markdown(content), title=title, border_style="blue"))
    return True

def main():
    console.print(Panel("Welcome to OARC Butler CLI! Type /help for available commands.", 
                       title="OARC Butler", border_style="blue"))
    
    while True:
        try:
            user_input = Prompt.ask("\n[blue]You[/blue]")
            
            if user_input.startswith('/'):
                if not handle_command(user_input.lower()):
                    console.print("[red]Unknown command. Type /help for available commands.[/red]")
            else:
                console.print("[red]Invalid input. Please use a valid command.[/red]")
                
        except KeyboardInterrupt:
            console.print("\nGoodbye! 👋")
            break
        except Exception as e:
            console.print(f"[red]An error occurred: {str(e)}[/red]")

if __name__ == "__main__":
    main()