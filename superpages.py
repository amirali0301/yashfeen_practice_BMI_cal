import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Create a function to generate a bar chart
def generate_bar_chart(data):
    plt.bar(data['Category'], data['Value'])
    plt.xlabel('Category')
    plt.ylabel('Value')
    plt.title('Bar Chart')
    st.pyplot()

# Main function to run the Streamlit app
def main():
    # Title for the app
    st.title('Simple Streamlit App')

    # Instructions for the user
    st.write('Enter some data to generate a bar chart.')

    # Input data
    category = st.text_input('Enter category:')
    value = st.number_input('Enter value:')

    # Add data to a pandas DataFrame
    data = pd.DataFrame({'Category': [category], 'Value': [value]})

    # Display the data
    st.write('Data Entered:')
    st.write(data)

    # Generate the bar chart
    generate_bar_chart(data)

# Run the main function
if __name__ == "__main__":
    main()
