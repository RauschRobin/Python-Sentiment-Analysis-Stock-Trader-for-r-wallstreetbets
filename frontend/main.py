import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import requests
import time
from PIL import Image
import datetime 
import os

server = "https://flappybirds.server-welt.com/py-api/"
last_buy_time_file = "last_buy_time.txt"

def get_last_buy_time():
    '''
    This function reads the file last_buy_time.txt and extracts the last buy time. This is used to prevent spam attacks.

    Parameters: 
    None
    
    Returns: 
    float: The last buy time

    Possible Tests:
    set the last buy time and call this function. check if it is correct
    or set the file text to null and check if this function returns 0
    '''
    if os.path.exists(last_buy_time_file):
        with open(last_buy_time_file, "r") as file:
            return float(file.read())
    else:
        return 0

def set_last_buy_time(timestamp):
    '''
    This function sets the file last_buy_time.txt.

    Parameters: 
    float: timestamp
    
    Returns: 
    None

    Possible Tests:
    Check if this function actually set the file correctly by reading the file afterwards.
    Or test this by setting the parameter timestamp to something that is not parseable and see what happens
    '''
    with open(last_buy_time_file, "w") as file:
        file.write(str(timestamp))

def call_backend():
    '''
    This function makes a HTTP requests to a server at a specific URL to buy a new stock and save it. 
    
    Parameters: 
    None
    
    Returns: 
    None

    Possible Tests:
    Test call_backend() function by mocking/spying the HTTP requests and checking if it gets called.
    Check if the saveChart is called
    '''
    response_buy = requests.get(server+'buy', timeout=300)

    response_save = requests.get(server+'saveChart', timeout=20)

    if response_buy.status_code != 200 or response_save.status_code != 200:
        print('Buying a new stock and saving it failed!')
        print(str(response_buy.status_code) + " and " + str(response_save.status_code))
        return 
    
    print("Buying a new stock was successful!")
    return

def create_chart(data):
    '''
    This function takes a list of data containing dates and prices and creates a line chart using the matplotlib library. The chart is displayed using Streamlit. It also creates all the elements on the page. For example: It provides a button to run the call_backend() function to buy a new stock.
    
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
    st.write("This is the Mirk Düller Fond *created by Python Degenerates Inc*. It's 100% controlled by a machine learning bot that listens to advice from r/wallstreetbets!")

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
    This is the main function that displays the Streamlit app. It first retrieves a list of data from a server using an HTTP GET request. If the request is successful, it passes the data to the create_chart() function to create a chart.

    Parameters: 
    None

    Returns: 
    None

    Possible Tests:
    Integration Test: Run the Streamlit app and verify that it retrieves and displays data correctly, and that the call to create_chart() generates a chart without errors.
    HTTP Request Test: Mock the HTTP GET request to the server and simulate different response codes (e.g., 200, 404, 500) to ensure that the code handles different scenarios appropriately.
    '''
    last_buy_time = get_last_buy_time()
    st.set_page_config(page_title='Mirk Düller Fond', page_icon='python_degens.ico')
    data = []

    # Get data list from server/backend
    url = server+'getChart'

    response = requests.get(url)

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
            wait_time = 3600 - (time.time() - last_buy_time)
            wait_time_str = str(datetime.timedelta(seconds=wait_time)).split(".")[0]
            st.write("Backend has already been executed. Wait at least " + wait_time_str + ". The backend can only be executed once every hour.")            
            return
        last_buy_time = time.time()
        set_last_buy_time(last_buy_time)
        call_backend()  # Call the backend function when the button is clicked
        st.experimental_rerun() 


if __name__ == "__main__":
    main()
