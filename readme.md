# Pizza Ordering System

This project is a small challenge that I had to prepare for a job interview. The task was to build an AI agent that can handle incoming orders for a pizzeria and adds it in a structured format as a json file to a specific folder. 

The JSON data should follow this schema:

```json
{
  "customer": {
    "name": "Customer Name",
    "phone": "Customer Phone Number",
    "address": "Customer Address",
  },
  "order_items": [
    {
      "pizza_name": "Pizza Name",
      "size": "Size (e.g., Small, Medium, Large)",
      "toppings": [
        "Topping 1",
        "Topping 2",
        "Topping 3"
      ]
    }
  ],
  "side": ["Side 1", "Side 2"],
  "drink": ["Drink 1", "Drink 2"],
  "total_price": 22.00,
  "special_instructions": "Any special instructions or notes"
}
```

During the conversation with the user, the agent should follow a predefined sequence of steps:
1. Greet the customer and ask for their name
2. Ask for the pizza type, size and toppings
3. Ask for a side and a drink
4. Ask for the delivery address and a phone number
5. Calculate the total price
6. Show an order confirmation to the customer (as a chat message) after he gave all the information.
7. Save the order to the [orders](./app/orders/) folder as a json file.


## Core Features

- AI Agent that handles the incoming orders, and outputs them in a structured format
- Real-time price calculation, seperated from the LLM (because LLMs are not good at math)
- Validation of the agent output to be sure that it fits the JSON schema
- JSON-based order storage
- Streamlit web interface

## System Components

### 1. Chat Agent
- Carefully designed system prompt to guide the agent through the order process
- Step-by-step order collection
- Input validation against the menu
- You can find the system prompt in [pizza_agent/system_prompt/building.py](./pizza_agent/system_prompt/building.py)


### 2. Order Processing
- JSON format validation
- Price calculation (seperated from the LLM)
- Menu item verification


## How to run the project

### Create a virtual environment

```bash
python -m venv .venv
```

### Install dependencies

```bash
pip install -r requirements.txt
```

### Add your OpenAI key

Paste your OPEN_API_KEY in the .streamli/secrets.toml file:

OPENAI_API_KEY = "sk-proj-1234..."

### Run the app

```bash
streamlit run main.py
```