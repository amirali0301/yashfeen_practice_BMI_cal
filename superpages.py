import streamlit as st

def main():
    st.title('Simple Greeting App')
    
    # Text input for user's name
    name = st.text_input('Enter your name:')
    
    # Check if name is provided
    if name:
        # Display greeting message
        st.write(f'Hello, {name}! Welcome to Streamlit.')

if __name__ == "__main__":
    main()
