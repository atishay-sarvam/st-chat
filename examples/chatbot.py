import streamlit as st
from streamlit_chat import message
import requests
import time

st.set_page_config(
    page_title="Streamlit Chat - Demo",
    page_icon=":robot:"
)

API_URL = "http://34.147.4.82:80/conversation"


import streamlit as st

access_code = st.text_input(
    label="Enter API Key",
    type="password",
)

while True:    
    if access_code:
        break
    else:
        print("sleepy")
        time.sleep(1)
headers = {"X-API-Key":access_code}



if 'generated' not in st.session_state:
    st.session_state['generated'] = []

if 'past' not in st.session_state:
    st.session_state['past'] = []
if 'session_id' not in st.session_state:
    st.session_state['session_id'] = ""


def query(payload):
	response = requests.post(API_URL, headers=headers, json=payload)
	return response.json()

def get_text():
    input_text = st.text_input("You: ","Hello, how are you?", key="input")
    return input_text 

user_input = get_text()
if user_input:
    output = query({
        "data": {
            "text": user_input,
    },"session_id":st.session_state['session_id']
    })

    st.session_state.past.append(user_input)
    st.session_state.session_id = output['session_id']
    print(output)
    st.session_state.generated.append(output["data"]['output'])

if st.session_state['generated']:

    for i in range(len(st.session_state['generated'])-1, -1, -1):
        message(st.session_state["generated"][i], key=str(i))
        message(st.session_state['past'][i], is_user=True, key=str(i) + '_user')

