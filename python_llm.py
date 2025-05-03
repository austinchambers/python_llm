#!/usr/bin/env python
"""
LLM CLI Interface

A simple command-line interface for interacting with various LLMs (Claude, OpenAI, Mistral).
This script prompts the user for questions and displays responses.

Usage:
    python python_llm.py [--provider PROVIDER] [--model MODEL] [--api_key API_KEY]

Options:
    --provider PROVIDER    Specify provider to use (anthropic, openai, or mistral). Optional. Default anthropic
    --model MODEL          Specify model to use. Optional. If unspecified, uses default model for the given provider.
    --api_key API_KEY      The API Key to use to connect. If unspecified uses environment variable  
"""

import os
import sys
import argparse
import json
from typing import Dict, Any, Optional, List, Union
from dotenv import load_dotenv
import time
import anthropic
from anthropic.types import MessageParam
import openai
import mistralai.client 
from mistralai.client import MistralClient as MistralSDK

"""Global fixed parameters across all LLM providers"""
MAX_TOKENS = 2048

"""Base client class for LLM providers."""
class LLMClient:
    def __init__(self, api_key: str, model: str):
        """Initialize LLM client.    

        Args:
            api_key: API key
            model: Model to use
        """
        self.model = model
        self.api_key = api_key

    """Generate response from LLM."""
    def generate_response(self, messages: List[Dict[str, str]]) -> str:
        """
        Args:
            messages: List of message dictionaries with 'role' and 'content'
            
        Returns:
            str: The generated response
        """
        raise NotImplementedError("Subclasses must implement generate_response")


"""Anthropic client."""
class AnthropicClient(LLMClient):
    def __init__(self, api_key: str, model: str = "claude-3-7-sonnet-20250219"):
        super().__init__(api_key, model)
        self.client = anthropic.Anthropic(api_key=api_key)
        
    def generate_response(self, messages: List[Dict[str, str]]) -> str:
        # Convert our messages format to Anthropic's expected format
        anthropic_messages = []
        for message in messages:
            role = "user" if message["role"] == "user" else "assistant"
            anthropic_messages.append(MessageParam(role=role, content=message["content"]))
        
        try:
            response = self.client.messages.create(
                model=self.model,
                messages=anthropic_messages,
                max_tokens=MAX_TOKENS
            )
            return response.content[0].text
        except Exception as e:
            print(f"Error generating response: {e}")
            return f"Error: {str(e)}"


"""OpenAI client."""
class OpenAIClient(LLMClient):
    def __init__(self, api_key: str, model: str):
        super().__init__(api_key, model)
        self.client = openai.OpenAI(api_key=api_key)
        
    def generate_response(self, messages: List[Dict[str, str]]) -> str:
        # Format already compatible with OpenAI
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                max_tokens=MAX_TOKENS
            )
            return response.choices[0].message.content
        except Exception as e:
            print(f"Error generating response: {e}")
            return f"Error: {str(e)}"


"""Mistral client."""
class MistralClient(LLMClient):
    def __init__(self, api_key: str, model: str):
        super().__init__(api_key, model)
        self.client = MistralSDK(api_key=api_key)
        
    def generate_response(self, messages: List[Dict[str, str]]) -> str:
        try:
            chat_response = self.client.chat(
                model=self.model,
                messages=messages,
                max_tokens=MAX_TOKENS
            )
            return chat_response.choices[0].message.content
        except Exception as e:
            print(f"Error generating response: {e}")
            return f"Error: {str(e)}"


"""Manages conversation state and history."""
class ConversationManager:
    
    def __init__(self, llm_client: LLMClient):
        self.llm_client = llm_client
        self.conversation_history = []

    """Add a message to the conversation history."""
    def add_message(self, role: str, content: str):
        """Args: 
               role: Role of the message sender ('user' or 'assistant')
               content: Content of the message"""
        self.conversation_history.append({"role": role, "content": content})

    """Get response from LLM based on conversation history."""
    def get_response(self) -> str:
        response = self.llm_client.generate_response(self.conversation_history)
        self.add_message("assistant", response)
        return response

    """Clear conversation history."""    
    def clear_history(self):
        self.conversation_history = []

    """Save conversation history to a file."""
    def save_conversation(self, filename: str):
        with open(filename, 'w') as f:
            json.dump(self.conversation_history, f, indent=2)
        print(f"Conversation saved to {filename}")


"""Generate LLM client from standard arguments."""
def get_llm_client(provider: str, api_key: str, model: str) -> LLMClient:
    
    if provider.lower() == "anthropic":
        if model is None: model = "claude-3-7-sonnet-20250219"
        return AnthropicClient(api_key, model)
    elif provider.lower() == "openai":
        if model is None: model = "gpt-4"
        return OpenAIClient(api_key, model)
    elif provider.lower() == "mistral":
        if model is None: model = "mistral-large-latest"
        return MistralClient(api_key, model)
    else:
        raise ValueError(f"Unsupported provider: {provider}")


"""Program Main entry point."""
def main():
    parser = argparse.ArgumentParser(description="LLM CLI Interface")
    parser.add_argument("--provider", default="anthropic", choices=["anthropic", "openai", "mistral"], help="LLM provider to use")
    parser.add_argument("--model", help="Specify model to use for the designated provider")
    parser.add_argument("--save", help="Save conversation to specified file")
    args = parser.parse_args()
    
    # Load environment variables from .env file
    load_dotenv()
    
    # Get API key from environment variables
    api_key_env_var = f"{args.provider.upper()}_API_KEY"
    api_key = os.getenv(api_key_env_var)
    
    if not api_key:
        print(f"Error: {api_key_env_var} environment variable not set.")
        print(f"Please set {api_key_env_var} in your environment or .env file.")
        sys.exit(1)
    
    try:
        # Create LLM client
        llm_client = get_llm_client(args.provider, api_key, args.model)
        
        # Create conversation manager
        conversation = ConversationManager(llm_client)
        
        print(f"Welcome to the {args.provider.capitalize()} CLI Interface!")
        print(f"Using model: {llm_client.model}")
        print("Type 'exit', 'quit', or Ctrl+C to exit.")
        print("Type 'save <filename>' to save the conversation.")
        print("Type 'clear' to clear the conversation history.")
        print("------------------------------------------------")
        
        while True:
            try:
                # Get user input
                user_input = input("\nYou: ")
                
                # Check for special commands
                if user_input.lower() in ["exit", "quit"]:
                    break
                elif user_input.lower() == "clear":
                    conversation.clear_history()
                    print("Conversation history cleared.")
                    continue
                elif user_input.startswith("save "):
                    filename = user_input[5:].strip()
                    conversation.save_conversation(filename)
                    continue
                
                # Add user message to conversation
                conversation.add_message("user", user_input)
                
                # Indicate that the assistant is thinking
                print("\nAssistant: ", end="", flush=True)
                
                # Get response from assistant
                start_time = time.time()
                response = conversation.get_response()
                end_time = time.time()
                
                # Clear the "thinking" indicator and print the response
                print(f"\r{' ' * 50}\r", end="")
                print(f"Assistant: {response}")
                print(f"\n[Response time: {end_time - start_time:.2f}s]")
                
            except KeyboardInterrupt:
                print("\nExiting...")
                break
            except Exception as e:
                print(f"\nError: {e}")
        
        # Save conversation if specified
        if args.save:
            conversation.save_conversation(args.save)
    
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()