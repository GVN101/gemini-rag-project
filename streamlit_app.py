import streamlit as st
import requests
import re

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
    
    if user_question.strip():
        st.spinner("Fetching your answers...")
    # Only make API call when user has entered a question
    if user_question:
        try:
            # Send POST request with JSON payload
            response = requests.post(
                "http://127.0.0.1:5000/get_data", 
                json={"question": user_question},
                timeout=30
            )
            # Check response from the api
            if response.status_code == 200:
                data = response.json()
                print(data, "data")
                if data.get('status') == 'success':
                    st.markdown(data['output'], unsafe_allow_html=True)
                    image_urls = data['image_urls']
                    print("\n\n\n\n")
                    print(image_urls)
                    print("\n\n\n\n")
                    for url in image_urls:
                        st.image(url[:-1], caption="Image", use_column_width=True)
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