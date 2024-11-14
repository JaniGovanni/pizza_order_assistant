from typing import Dict
from langchain_core.output_parsers import JsonOutputParser
from calculation_and_validation.validation.json_data import validate_json_data
from calculation_and_validation.process_items.pizza import process_pizza_order
from calculation_and_validation.process_items.sides import process_side_order
from calculation_and_validation.process_items.drinks import process_drink_order
from calculation_and_validation.Saving import save_order
from app.menue import pizzeria_menu

import re
import json

def extract_and_parse_json(text):
    # If input is already a dict, return it as is
    if isinstance(text, dict):
        return text
        
    # Find JSON-like structure between curly braces
    json_match = re.search(r'\{.*\}', text, re.DOTALL)
    if json_match:
        json_str = json_match.group()
        try:
            return json.loads(json_str)
        except json.JSONDecodeError:
            return None
    return None

def calculate_order_price(json_data: Dict, menu: Dict) -> Dict | str:
    try:
        validate_json_data(json_data)
        
        # Process pizzas
        total = 0
        for pizza in json_data.get("order_items", []):
            pizza_result = process_pizza_order(pizza, menu)
            total += pizza_result["total"]
        
        # Process sides
        for side in json_data.get("sides", []):
            side_result = process_side_order(side, menu)
            total += side_result["price"]
        
        # Process drinks
        for drink in json_data.get("drinks", []):
            drink_result = process_drink_order(drink, menu)
            total += drink_result["price"]
        
        # Update the total price in the original JSON
        json_data["total_price"] = round(total, 2)
        return json_data
        
    except ValueError as e:
        return str(e)


def check_response(response):
    # try to parse response, if it fails order is not finished
    try:
        json_data = extract_and_parse_json(response)
        # was an order-finished response, now calculate the price and check the format
        json_data = calculate_order_price(json_data, pizzeria_menu)
        try:
            # try to parse again, if it fails, the format of the json was not valid
            json_with_validation = extract_and_parse_json(json_data)
            save_order(json_with_validation)
            return "Your order has been processed successfully, Thank you for your order!"
        except Exception:
            return json_data
    except Exception:
        return response