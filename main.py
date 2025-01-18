import random
from langchain_core.tools import tool
from langchain_ollama import ChatOllama
from langgraph.prebuilt import create_react_agent
from langgraph.checkpoint.memory import MemorySaver


# Tool to roll dice with the specified number of sides and dice
@tool(parse_docstring=True)
def roll_dice(num_dice: int, num_sides: int):
    """
    Rolls a specified number of dice, each with a specified number of sides.

    Args:
        num_dice (int): The number of dice to roll.
        num_sides (int): The number of sides on each die.

    Returns:
        str: A formatted string containing the result of each die roll.
    """
    if num_dice <= 0 or num_sides <= 0:
        raise ValueError("Both number of dice and number of sides must be positive integers.")

    rolls = [random.randint(1, num_sides) for _ in range(num_dice)]
    return f"Here are the results: {rolls}"


# Function to interact with the chatbot and ask questions
def ask_stuff(base_prompt: str, thread_id: str) -> str:
    """
    Sends a prompt to the chatbot and gets a response.

    Args:
        base_prompt (str): The user's input to ask the chatbot.
        thread_id (str): A unique identifier for the conversation thread.

    Returns:
        str: The chatbot's response.
    """
    print(f"Role description: {role_description}")
    print(f"Prompt to ask: {base_prompt}")

    # Prepare configuration and inputs for the model
    config = {"configurable": {"thread_id": thread_id}}
    inputs = {"messages": [("system", role_description), ("user", base_prompt)]}

    # Get response from the chatbot model
    ollama_response = print_stream(graph.stream(inputs, config=config, stream_mode="values"))

    print(f"Original Response from model: {ollama_response}")
    return ollama_response


# Function to process and print the response stream
def print_stream(stream):
    """
    Processes and prints the message from the model's response stream.

    Args:
        stream (iterable): The stream of messages from the chatbot.

    Returns:
        str: The content of the last message in the stream.
    """
    message = ""
    for s in stream:
        message = s["messages"][-1]
        if isinstance(message, tuple):
            print(message)
        else:
            message.pretty_print()
    return message.content


# Configuration settings
LLAMA_MODEL = "llama3.2"
role_description = (
    "You are a helpful chatbot. "
    "Here are the tools available to you, do not call the tools unless you need to. "
    "roll_dice: used to roll different types of dice."
)

# Initialize memory and tools
memory = MemorySaver()
tools = [roll_dice]

# Initialize the Ollama chatbot instance and agent
ollama_instance = ChatOllama(model=LLAMA_MODEL)
graph = create_react_agent(ollama_instance, tools=tools, checkpointer=memory)

# Main script to run the chatbot interaction
if __name__ == '__main__':
    thing_to_ask = input("What would you like to ask the chatbot?\r\n")

    while True:
        response = ask_stuff(thing_to_ask, "1")
        thing_to_ask = input(f"\r\n\r\nRESPONSE FROM MODEL: {response}\r\n")