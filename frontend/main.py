import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import requests
import time
from PIL import Image
import datetime 

server = "https://flappybirds.server-welt.com/py-api"

def call_backend():
    '''
    This function makes HTTP requests to a server at a specific URL to buy a new stock and save it. It returns the response in JSON format if the request is successful. Otherwise, it returns None.
    
    Parameters: 
    None
    
    Returns: 
    A JSON object if the request is successful, otherwise None.

    Possible Tests:
    Test call_backend() function by mocking the HTTP requests and checking that it returns the expected response.
    Check if the response by the HTTP request has the correct syntax
    '''

    response_buy = requests.get(server+'buy')
    print('Response zum Buy: ' + str(response_buy))

    response_save = requests.get(server+'saveChart')
    print('Response zum saveChart:' + str(response_save))

    if response_buy.status_code != 200 or response_save.status_code != 200:
        print('Buying a new stock and saving it failed!')
        return None
    
    return response_buy.json()

def create_chart(data):
    '''
    This function takes a list of data containing dates and prices and creates a line chart using the matplotlib library. The chart is displayed using Streamlit.
    
    Parameters: 
    A list of data in the format [['Date', 'Value'], [date_1, price_1], [date_2, price_2], ...].
    
    Returns: 
    None

    Possible Tests:
    Test this function by passing a valid list of data and verifying that it creates a chart.
    Check if the datetime is parsed correctly.
    '''
    # Convert the data list to a Pandas DataFrame
    df = pd.DataFrame(data, columns=['Date', 'Value'])

    # Convert the 'Date' column to datetime type
    df['Date'] = pd.to_datetime(df['Date'])

    plt.style.use('fivethirtyeight')    

    # Create the chart
    fig, ax = plt.subplots()
    ax.plot(df['Date'], df['Value'])
    
    image = Image.open('python_degens.png')
    st.image(image, use_column_width=True)
    st.write("# MSCI ESG Mirk Düller Fond")
    st.write("This is the Mirk Düller Fond *created by Python Degenerates Inc*. It's 100% controlled by a machine learning bot that listens to advices from r/wallstreetbets!")

    ax.xaxis.set_major_locator(plt.MaxNLocator(6))  # Set maximum number of tick labels
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))  # Format the tick labels as desired

    # Rotate x-axis tick labels for better visibility
    fig.autofmt_xdate()

    ax.set_xlabel("time")
    ax.set_ylabel("value")
    ax.grid(True)

    # Show the chart using Streamlit
    st.pyplot(fig)

def main():
    '''
    This is the main function that displays the Streamlit app. It first retrieves a list of data from a server using an HTTP GET request. If the request is successful, it passes the data to the create_chart() function to create a chart. It also provides a button to run the call_backend() function to buy a new stock and save it as a chart. The create_chart() function is then called again to display the updated chart.

    Parameters: 
    None

    Returns: 
    None

    Possible Tests:
    Test this function by running the Streamlit app and verifying that it retrieves and displays data correctly, and that the call_backend() function runs successfully and updates the chart.
    Or test this function by trying out the button and if the function call_backend() is called.
    '''
    st.set_page_config(page_title='Mirk Düller Fond', page_icon='python_degens.ico')

    last_buy_time = time.time()
    data = []

    # Get data list from server/backend
    url = server+'/getChart'

    response = requests.get(url)
    print('Response zum getChart:' + str(response))

    if response.status_code == 200:
        data = response.json()
    else:
        print('Error:', response)

    edited_data = {}
    for entry in data:
        date = entry[0]
        value = entry[1]

        # Check if the date already exists in the dictionary
        if date in edited_data:
            # If the value is higher than the existing value, update it
            if value > edited_data[date]:
                edited_data[date] = value
        else:
            # If the date doesn't exist, add it to the dictionary
            edited_data[date] = value

    # Convert the dictionary back to a list of lists
    data = [[date, value] for date, value in edited_data.items()]

    create_chart(data)

    if st.button('Run backend'):
        if time.time() - last_buy_time < 3600:  # 3600 seconds = 60 minutes
            st.write("Backend has already been executed at " + datetime.datetime.fromtimestamp(last_buy_time).strftime('%H:%M:%S') + " o'clock. The backend can only be executed once every hour.")
            return
        last_buy_time = time.now()
        data.append(call_backend())  # Call the Python function when the button is clicked
        create_chart(data)


if __name__ == "__main__":
    main()
