## Drones Agents
This document describes a multi-agent system designed to plan and monitor a fleet of drones used for package delivery. An overview of the various agents involved, their responsibilities, and the communication methods between them is provided.

## File Principali
- **weather_handler.py**: This module is utilized by the drone agents to call the language model (LLM moondream) and analyze images. It returns a Prolog predicate that provides weather information to the drones.

- **main.py**: This script serves as the main interface for the project. It is used both to call the chatbot assistant (LLM llama2), which provides information on initiated or past missions, and to test the LLM in relation to images.

## Configuration
The project includes a configuration file ('config.py') that contains settings necessary for its operation. These details should be modified according to specific needs, such as:
- **Path for images to analyze**: default ./images/
- **LLM for conversing or analyzing images**: default 'llama2' for conversing, 'moondream' analyzing images
- **Path where agent states will be saved**
  
To run the LLM locally you need to download the framework Ollama: https://ollama.com and download the chosen models.
Once the framework is running, if you want to use the llama2 and moondream models, run in the terminal:
- ollama run moondream
- ollama run llama2

## DALI
To execute the multi-agent system, it is necessary to download the DALI interpreter from the following link: https://github.com/AAAI-DISIM-UnivAQ/DALI and subsequently upload the files into the 'agents' folder within it.
