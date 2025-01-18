# LangGraph-Demo

A simple demo to show how to use langgraph.

## Installation

Download Ollama and run llama3.2 locally first - https://ollama.com/blog/llama3

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install any dependencies using this command:

pip install -r /path/to/requirements.txt

## Use

By default, running will go into an endless loop of a CLI for a prompt for Llama3.2 after starting.

1) To change the model you're using, simply run another model in Ollama and change the LLAMA_MODEL variable.
2) To add new tools, use the same format as roll_dice and then add the function to tools. (make sure to add it to the system prompt)