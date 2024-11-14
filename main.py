
# Third party imports
import streamlit as st
from openai import OpenAI

# Local imports
from app.menue import pizzeria_menu
from app.oders_view import show_orders_page
from pizza_agent.system_prompt.building import build_agent_system_prompt
from calculation_and_validation.CalcAndValidate import check_response

st.set_page_config(page_title="Pizza Challenge", layout="wide")

def main_page():
    #-----------------------------------------------------#
    # NOT RELEVANT FOR THE CHALLENGE (this is only the ui)#
    #-----------------------------------------------------#
    
    # Set the title of the Streamlit app
    st.title("Pizza Challenge")

    # Initialize the OpenAI client with the API key from Streamlit secrets
    client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

    # Check if the OpenAI model is set in the session state; if not, set a default model
    if "openai_model" not in st.session_state:
        st.session_state["openai_model"] = "gpt-4o-mini"
    if "system_message" not in st.session_state:
        st.session_state["system_message"] = {"role": "system",
                                              "content": build_agent_system_prompt(pizzeria_menu)}

    # Check if the messages list is in the session state; if not, initialize it with a welcome message
    if "messages" not in st.session_state:
        st.session_state.messages = [
            # Remove system message from here
            {
                "role": "assistant",
                "content": "Hello, I am your pizza delivery assistant. How can I help you today?",
            }
        ]
    # Display each message in the chat interface
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            if message["role"] != "system":
                st.markdown(message["content"])
            
    #-----------------------------------------------------#
    # RELEVANT FOR THE CHALLENGE                          #
    #-----------------------------------------------------#
    
    # Capture user input from the chat input box 
    if prompt := st.chat_input("What do you wanna order?"):
        # Append the user's message to the session state messages
        st.session_state.messages.append({"role": "user", "content": prompt})
        
        # Display the user's message in the chat interface (not relevant for the challenge)
        with st.chat_message("user"):
            st.markdown(prompt)
            
        # Generate a response from the assistant using the OpenAI model
        with st.chat_message("assistant"):
            stream = client.chat.completions.create(
                model=st.session_state["openai_model"],
                messages=[st.session_state["system_message"]] + [
                    {"role": m["role"], "content": m["content"]}
                    for m in st.session_state.messages
                ],
                stream=True,
            )
            # Write the assistant's response to the chat interface (not relevant for the challenge)
            response = st.write_stream(stream)
        
        response = check_response(response)
        
        if "ERROR" in response:
            error_message = {"role": "assistant", "content": response}
            fix_message = {'role': 'user', 'content': 'Please fix the error in the response'}
            client.chat.completions.create(
                model=st.session_state["openai_model"],
                messages=st.session_state.messages + [error_message, fix_message],
            )
            response = check_response(response.choices[0].message.content)
        
        st.session_state.messages.append({"role": "assistant", "content": response})


#-----------------------------------------------------#
# NOT RELEVANT FOR THE CHALLENGE (this is only the ui)#
#-----------------------------------------------------#

# Add navigation in the sidebar
st.sidebar.title("Navigation")
page = st.sidebar.radio("Go to", ["Order Pizza", "View Orders"])

# Display menu in the sidebar
st.sidebar.header("Our Menu")

# Display pizzas
st.sidebar.subheader("Pizzas")
if isinstance(pizzeria_menu["pizzas"], list):
    for pizza in pizzeria_menu["pizzas"]:
        st.sidebar.text(f"- {pizza['name']}")
else:
    st.sidebar.write("No pizzas available at the moment.")

st.sidebar.write("---")

# Display toppings
st.sidebar.subheader("Extra Toppings")
if isinstance(pizzeria_menu["toppings"], list):
    for topping in pizzeria_menu["toppings"]:
        st.sidebar.text(f"- {topping['name']}")
else:
    st.sidebar.write("No toppings available at the moment.")

st.sidebar.write("---")

# Display sides
st.sidebar.subheader("Sides")
if isinstance(pizzeria_menu["sides"], list):
    for side in pizzeria_menu["sides"]:
        st.sidebar.text(f"- {side['name']}")
else:
    st.sidebar.write("No sides available at the moment.")
    
st.sidebar.write("---")

# Display drinks
st.sidebar.subheader("Drinks")
if isinstance(pizzeria_menu["drinks"], list):
    for drink in pizzeria_menu["drinks"]:
        st.sidebar.text(f"- {drink['name']}")
else:
    st.sidebar.write("No drinks available at the moment.")

    st.sidebar.write(f"- {drink['name']}")



if page == "Order Pizza":
    main_page()
elif page == "View Orders":
    show_orders_page()