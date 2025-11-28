# Console Chatbot for Agentic Workflow

This project is a console-based chatbot designed to handle agentic workflows. It allows users to interact with various agents that can process tasks and manage workflows effectively.

## Project Structure

```
console-chatbot-agentic
├── src
│   ├── main.py                # Entry point of the chatbot application
│   ├── chatbot
│   │   ├── __init__.py        # Initializes the chatbot module
│   │   ├── console_interface.py # Handles user input and output in the console
│   │   └── chat_handler.py     # Manages conversation flow and processes user inputs
│   ├── agents
│   │   ├── __init__.py        # Initializes the agents module
│   │   ├── base_agent.py      # Base class for all agents
│   │   └── workflow_agent.py   # Handles workflows and coordinates tasks
│   ├── workflows
│   │   ├── __init__.py        # Initializes the workflows module
│   │   └── workflow_manager.py  # Manages execution of workflows
│   └── utils
│       ├── __init__.py        # Initializes the utils module
│       └── helpers.py         # Utility functions for various tasks
├── requirements.txt           # Lists project dependencies
├── config.py                  # Configuration settings for the chatbot
└── README.md                  # Project documentation
```

## Features

- **Interactive Console Interface**: Users can interact with the chatbot through a simple console interface.
- **Agentic Workflow Management**: The chatbot can manage complex workflows by coordinating multiple agents.
- **Extensible Architecture**: The design allows for easy addition of new agents and workflows.

## Installation

1. Clone the repository:
   ```
   git clone https://github.com/yourusername/console-chatbot-agentic.git
   cd console-chatbot-agentic
   ```

2. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```

## Usage

To start the chatbot, run the following command:
```
python src/main.py
```

Follow the prompts in the console to interact with the chatbot and manage workflows.

## Contributing

Contributions are welcome! Please open an issue or submit a pull request for any enhancements or bug fixes.

## License

This project is licensed under the MIT License. See the LICENSE file for more details.