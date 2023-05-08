import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import requests
import json

def main():
    st.title("MSCI ESG - Mirk Düller Fond")

    # Get data list from server/backend
    '''
    url = 'http://116.203.41.47:PORT'
    params = {'key1': 'value1', 'key2': 'value2'}
    headers = {'Authorization': 'Bearer <access_token>'}

    response = requests.get(url, params=params, headers=headers)

    if response.status_code == 200:
        data = response.json()
        # do something with the data
    else:
        print('Error:', response.status_code)
    '''
    data = [('2023-04-26 18:08:12', 2000), ('2023-04-27 19:08:12', 1000), ('2023-04-28 19:08:12', 2300)]

    # Convert the data list to a Pandas DataFrame
    df = pd.DataFrame(data, columns=['Date', 'Price'])

    # Convert the 'Date' column to datetime type
    df['Date'] = pd.to_datetime(df['Date'])

    # Create the chart
    fig, ax = plt.subplots()
    ax.plot(df['Date'], df['Price'])

    # Show the chart using Streamlit
    st.pyplot(fig)


if __name__ == "__main__":
    main()