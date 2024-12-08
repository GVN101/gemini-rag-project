import streamlit as st
import requests

def main():
    st.set_page_config("Chat Data Source")
    st.header("IHRD BOT")
    
    # Hide Streamlit default styling
    hide_st_style = """
    <style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    </style>
    """
    st.markdown(hide_st_style, unsafe_allow_html=True)
    
    # User input
    user_question = st.text_input("Have a query on IHRD? ask")
    
    # Only make API call when user has entered a question
    if user_question:
        try:
            # Send POST request with JSON payload
            response = requests.post(
                "http://127.0.0.1:5000/get_data", 
                json={"question": user_question},
                timeout=10 
            )
            
            # Check response from the api
            if response.status_code == 200:
                data = response.json()
                if data.get('status') == 'success':
                    st.write("Reply: ", data.get('output', 'No response'))
                else:
                    st.error(f"Error: {data.get('error', 'Unknown error')}")
            else:
                st.error(f"Failed to fetch data. Status code: {response.status_code}")
        
        except requests.RequestException as e:
            st.error(f"Network error: {e}")
        except Exception as e:
            st.error(f"An unexpected error occurred: {e}")

if __name__ == "__main__":
    main()