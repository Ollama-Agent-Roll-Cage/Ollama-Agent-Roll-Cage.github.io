#!/usr/bin/env python3
import os
import sys
from rich.console import Console
from rich.markdown import Markdown
from rich.prompt import Prompt
from rich.panel import Panel
from typing import Dict, Any, Optional

console = Console()

class OARCCliBot:
    def __init__(self):
        self.commands = {
            'help': self.show_help,
            'about': self.show_about,
            'components': self.show_components,
            'agent': self.show_agent_info,
            'speech': self.show_speech_info,
            'docs': self.show_docs,
            'discord': self.show_discord,
            'clear': self.clear_screen,
            'exit': self.exit_bot,
            'quit': self.exit_bot,
            'version': self.show_version
        }
        
        # Knowledge base for natural language queries
        self.knowledge_base = {
            'agent': {
                'keywords': ['agent', 'what is agent', 'agent definition', 'agents'],
                'response': """An agent in OARC refers to the algorithmic logic that wraps a model and via iteration, 
generates the chain of thought output for the model.

Key aspects:
- Model Wrapping: Encapsulates LLM functionality
- Chain of Thought: Implements reasoning processes
- Action Space: Converts text to actionable programming logic
- Multi-Modal Support: Handles various input/output types
- Tool Integration: Connects with external services"""
            },
            'speech': {
                'keywords': ['speech', 'voice', 'audio', 'tts', 'stt', 'speech to text'],
                'response': """OARC's Speech-to-Speech Pipeline features:

• Silence removal preprocessing
• Smart user interruption handling
• Wake word detection system
• Voice activity detection
• Neural voice cloning capabilities
• Debate moderator mode
• LLM sentence chunking for TTS
• Real-time streaming support
• Multi-speaker management"""
            },
            'components': {
                'keywords': ['components', 'parts', 'modules', 'features'],
                'response': """OARC consists of several core components:

1. Modal Flags
   - TTS_FLAG: Text-to-Speech capability
   - STT_FLAG: Speech-to-Text processing
   - LLAVA_FLAG: Vision-language tasks

2. Models Configuration
   - Language models
   - Speech models
   - Vision models

3. Tool Integration
   - External APIs
   - Local services
   - Custom tools

4. Processing Pipeline
   - Speech preprocessing
   - Real-time streaming
   - Multi-modal fusion"""
            }
        }

    def find_best_response(self, query: str) -> Optional[str]:
        """Find the most relevant response from knowledge base for a natural language query"""
        query = query.lower()
        
        for topic, data in self.knowledge_base.items():
            if any(keyword in query for keyword in data['keywords']):
                return data['response']
        
        return None

    def show_help(self) -> str:
        return """Available Commands:
• help              Show this help message
• about             Learn about OARC
• components        List OARC components
• agent             What is an Agent?
• speech            Speech-to-Speech architecture
• docs              Get documentation links
• discord           Get Discord server link
• clear             Clear the terminal
• exit/quit         Close the CLI
• version           Show CLI version

You can also ask questions naturally about OARC!"""

    def show_about(self) -> str:
        return """Ollama Agent Roll Cage (OARC) is a Python-based framework combining:
• Ollama LLMs
• Coqui-TTS
• Keras classifiers
• LLaVA Vision
• Whisper Speech Recognition
• YOLOv8 Object Detection

Into a unified chatbot agent API for local, custom automation."""

    def show_components(self) -> str:
        return self.knowledge_base['components']['response']

    def show_agent_info(self) -> str:
        return self.knowledge_base['agent']['response']

    def show_speech_info(self) -> str:
        return self.knowledge_base['speech']['response']

    def show_docs(self) -> str:
        return """Documentation Links:
• What is an Agent?: https://github.com/Ollama-Agent-Roll-Cage/oarc/blob/master/docs/what_is_an_agent/what_is_an_agent.md
• Speech-to-Speech: https://github.com/Ollama-Agent-Roll-Cage/oarc/tree/master/docs/speech_to_speech
• AgentChef Docs: https://github.com/Leoleojames1/agentChef/tree/main/docs"""

    def show_discord(self) -> str:
        return "Join our Discord community: https://discord.gg/dAzSYcnpdF"

    def clear_screen(self) -> None:
        os.system('cls' if os.name == 'nt' else 'clear')
        console.print("[bold blue]OARC CLI v1.0.0[/bold blue] - Type 'help' for available commands")

    def exit_bot(self) -> None:
        console.print("\n[bold blue]Thank you for using OARC CLI! Goodbye! 👋[/bold blue]")
        sys.exit(0)

    def show_version(self) -> str:
        return """OARC CLI v1.0.0
Build: 2025.04.23
Platform: Python CLI
Mode: Interactive
Author: OARC Team"""

    def process_input(self, user_input: str) -> None:
        """Process user input - either command or natural language query"""
        user_input = user_input.lower().strip()
        
        if user_input == "":
            return
            
        if user_input in self.commands:
            result = self.commands[user_input]()
            if result:
                console.print(Panel(result, border_style="blue"))
        else:
            # Try to find a relevant response from knowledge base
            response = self.find_best_response(user_input)
            if response:
                console.print(Panel(response, border_style="green"))
            else:
                console.print(Panel(
                    "I'm not sure about that. Try asking about OARC agents, components, or speech capabilities. "
                    "Or type 'help' to see available commands.", 
                    border_style="yellow"
                ))

def main():
    bot = OARCCliBot()
    console.print(Panel("Welcome to OARC CLI! Type 'help' for available commands.", title="OARC CLI v1.0.0", border_style="blue"))
    
    while True:
        try:
            user_input = Prompt.ask("\n[blue]OARC>[/blue]")
            bot.process_input(user_input)
        except KeyboardInterrupt:
            console.print("\n[bold blue]Goodbye! 👋[/bold blue]")
            break
        except Exception as e:
            console.print(f"[red]An error occurred: {str(e)}[/red]")

if __name__ == "__main__":
    main()