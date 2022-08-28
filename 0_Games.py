import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import streamlit as st
from datetime import date
import time

########## First elements to define

# initial configuration for the page
st.set_page_config(page_title='Games',
                   page_icon='four_leaf_clover',
                   layout='centered',
                   initial_sidebar_state='expanded'
                   )

# Title
st.title('Welcome to the minigames on streamlit app!!! :four_leaf_clover: :heart: :game_die: :slot_machine: :tada:')

# more text
st.subheader('Have fun and enjoy the games :grin:')


st.markdown("""
            Hi! You have reached the games application built with Streamlit. On your left you will find some games
            to check the capabilities of the Streamlit library for Python.
            
            If you want, you are more than welcome to create more games and add them to the list. In the meantime, 
            you can play with the ones that are available and check the source code to see how they have been done.
            
            All these games have been developed only with Python using streamlit functionalities. Streamlit is an open
            source web development library which is commonly be used for developing quick reports and dashboards 
            and share them with others in a fast and easy way.
            
            This application can be hosted in several platform, such as native sharing streamlit platform, Heroku,
            AWS... to name some.
            
            You might encounter some bugs from time to time in this app but don't worry, they do not affect the normal
            functioning of it. If that happens, try to refresh the app since these bugs are caused by streamlit. Sometimes 
            the layout and the element positioning can be a bit unstable and have an undesired behaviour, however the
            app will continue running and you can still interact with it.
            
            With that being said, it is time for you to explore the app. :smile:
            """)

st.markdown('### Let the fun begin :rocket:')

