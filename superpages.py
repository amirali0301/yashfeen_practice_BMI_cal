import streamlit as st

def main():
    st.title('love app')
    
    # Text input for user's name
    name = st.text_input('Enter your thark:')
    
    # Check if name is provided
    if name:
        # Display greeting message
        st.write(f'chor dy, {name} ki jan ukhar ly kch zindgi me.')

if __name__ == "__main__":
    main()
