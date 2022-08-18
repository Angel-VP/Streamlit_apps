import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import streamlit as st
from datetime import date
import time
import random
from PIL import Image
from game_functions import option_from_bet_type, player_win


########## First elements to define

# initial configuration for the pagee
st.set_page_config( page_title='Roulette',
                    page_icon=':ferris_wheel:',
                    layout='centered',
                    initial_sidebar_state='collapsed'
                    )

# Title
st.title('Welcome to the Roulette !')

# Subtitle
subheader_text = ':red_circle: :black_circle: :red_circle: :black_circle: :red_circle: :black_circle:'
st.markdown('#### ' + str(subheader_text) + ':green_heart:' + str(subheader_text) )

##############################
## session state variables 

if 'spin' not in st.session_state:
    st.session_state['spin'] = False
    
if 'player_amount' not in st.session_state:
    st.session_state['player_amount'] = 5000
    
    
##############################
## other local variables

possible_bets = ['', 'Single number', 'Double numbers', 'Three numbers', 'Four numbers', 
                 'Six numbers', 'Dozen', 'Column', '18 numbers', 'Red/Black', 'Odd/Even']

space = ' '.join(['&nbsp;' for e in range(0,10)])

# numbers in bet types
red_numbers = [1,3,5,7,9,12,14,16,18,19,21,23,25,27,30,32,34,36]
black_numbers = [2,4,6,8,10,11,13,15,17,20,22,24,26,28,29,31,33,35]
first_dozen = list(range(0,13))
second_dozen = list(range(13,25))
third_dozen = list(range(25,37))
first_column = list(np.arange(1, 35, 3, dtype=int))
second_column = list(np.arange(2, 36, 3, dtype=int))
third_column = list(np.arange(3, 37, 3, dtype=int))
first_18 = list(range(0,19))
second_18 =  list(range(19,37))
odd_numbers = list(np.arange(1, 37, 2, dtype=int))
even_numbers = list(np.arange(2, 38, 2, dtype=int))

# Dictionary to match bets with numbers within bets
dict_bets = {'First Dozen':first_dozen, 'Second Dozen':second_dozen, 'Third Dozen':third_dozen,
             'First Column':first_column, 'Second Column':second_column, 'Third Column':third_column,
             'From 1 to 18':first_18, 'From 19 to 36':second_18,
             'Red':red_numbers, 'Black':black_numbers,
             'Odd':odd_numbers, 'Even':even_numbers}

# bet odds
dict_odds = {'Single number':35, 'Double numbers':17, 'Three numbers':11, 'Four numbers':8, 'Six numbers':5, 
             'Dozen':2, 'Column':2, '18 numbers':1, 'Red/Black':1, 'Odd/Even':1}


##############################
## Game Board

# spacing
st.markdown('')
st.markdown('')

# croupier sentences
c1, c2, c3, c4 = st.columns((3,3,10,1))
with c2:
    st.image('aux_files/croupier.png', width=100)
    st.write('')
with c3:
    if st.session_state['spin'] == False: 
        st.markdown('&ndash; "Please place your bets to spin the wheel"')
        st.markdown('&ndash; "You can make up to 4 bets - Good luck!"')
    else: # when the wheel spins the croupier changes sentences
        st.markdown('The wheel is spinning!')
        st.markdown('&ndash; "And the result is..."')
    
# wheel spinner gif and roulette board
if st.session_state['spin'] == True:
    placeholder1 = st.empty()
    placeholder1.image('aux_files/roulette.gif')
    st.image('aux_files/roulette_board.jpg')
    time.sleep(5)
    placeholder1.empty()    
    
    wheel_result = random.randint(0,36)
    # evaluate player's wins/losses based on his bets
    win_lose = player_win(wheel_result, st.session_state['num_bets'], st.session_state, dict_bets, dict_odds)
    st.session_state['player_amount'] = st.session_state['player_amount'] + win_lose
    
    # show wheel result
    if wheel_result == 0:
        color='green'
    elif wheel_result not in red_numbers:
        color='black'
    else:
        color='red'   
    text_result = ("""<span style='color:{};'> {} </span>""").format(color,wheel_result)
    st.markdown('## ' + space + '"And the result is ... number &nbsp;' + text_result +'"', unsafe_allow_html=True)
    
    # show player's wins/loses
    if win_lose >= 0:
        color_2='darkgreen'
        text_2 = ('Congratulations, you have won +{}€ ! :tada: :confetti_ball: :balloon:').format(win_lose)
        text_result_2 = ("""<span style='color:{};'> {} </span>""").format(color_2,text_2)
        st.markdown('### ' + text_result_2 , unsafe_allow_html=True)
        placeholder2 = st.empty() 
        placeholder2.balloons()
        time.sleep(5)
        placeholder2.empty() 
    else:
        color_2='darkred'
        text_2 = ('Sorry, you have lost {}€').format(win_lose)
        text_result_2 = ("""<span style='color:{};'> {} </span>""").format(color_2,text_2)
        st.markdown('### ' + text_result_2 , unsafe_allow_html=True)
    
    st.session_state['spin'] = False
    
# roulette board
else:
    st.image('aux_files/roulette_board.jpg')
    
    
##################################
## Place bets & play again button

# Choose number of bets
cb1, cb2, cb3, cb4, cb5 = st.columns((10,5,10,3,10))
with cb1:
    st.number_input('Number of bets', min_value=1, max_value=4, value=1, step=1, key='num_bets')

with cb3:
    st.metric('You have left €:', st.session_state['player_amount'], delta=(st.session_state['player_amount']-5000), delta_color="normal", help='Start with 5.000€')

# play again button
not_clear_seasion_keys = ['player_amount','num_bets', 
                          'bet_1_type', 'bet_2_type', 'bet_3_type', 'bet_4_type',
                          'bet_1_select', 'bet_2_select', 'bet_3_select', 'bet_4_select',]

with cb5:
    clear_1 = st.button('Reset Bets')
    if clear_1:
        for key in st.session_state.keys():
            if key not in not_clear_seasion_keys:
                del st.session_state[key]
        st.experimental_rerun()

# separation line
img = Image.open('aux_files/line_h.jpg')
st.image(img, width=703 )
img.close()

#########################
## Bet configuration

if st.session_state['player_amount'] > 0:
    # Bets - Row 1  
    cr1, cr2 = st.columns(2)
    # Bet number 1
    if st.session_state['num_bets']>=1:
        with cr1:  
            st.markdown('### **Bet nº 1**')
            checkbox_val = st.checkbox("Confirm Bet", value=False, key='check_1', disabled=False)
            B1 = st.selectbox('Bet Type', possible_bets, key='bet_1_type', disabled=st.session_state['check_1'])
            if B1 != '':
                list_select_1 = option_from_bet_type(B1)
                B1_2 = st.selectbox('Select your option',list_select_1, key='bet_1_select', disabled=st.session_state['check_1'])
            else:
                pass
            bet_val_1 = st.slider(label='Amount to bet €', min_value=0, max_value=st.session_state['player_amount'], 
                                  step=100, key='bet_1_amount', disabled=st.session_state['check_1'])
    
    # Bet number 2
    if st.session_state['num_bets']>=2:
        with cr2:
            st.markdown('### **Bet nº 2**')
            checkbox_val = st.checkbox("Confirm Bet", value=False, key='check_2', disabled=False)
            B2 = st.selectbox('Bet Type', possible_bets, key='bet_2_type', disabled=st.session_state['check_2'])
            if B2 != '':
                list_select_2 = option_from_bet_type(B2)
                B2_2 = st.selectbox('Select your option',list_select_2, key='bet_2_select', disabled=st.session_state['check_2'])
            else:
                pass
            bet_val_2 = st.slider(label='Amount to bet €', min_value=0, max_value=st.session_state['player_amount'], 
                                  step=100, key='bet_2_amount', disabled=st.session_state['check_2'])
        
           
    # separation line
    if st.session_state['num_bets']>=3:
        img = Image.open('aux_files/line_h.jpg')
        st.image(img, width=703 )
        img.close() 
            
    # Bets - Row 2
    cr3, cr4 = st.columns(2)
    # Bet number 3
    if st.session_state['num_bets']>=3:
        with cr3:  
            st.markdown('### **Bet nº 3**')
            checkbox_val = st.checkbox("Confirm Bet", value=False, key='check_3', disabled=False)
            B3 = st.selectbox('Bet Type', possible_bets, key='bet_3_type', disabled=st.session_state['check_3'])
            if B3 != '':
                list_select_3 = option_from_bet_type(B3)
                B1_3 = st.selectbox('Select your option',list_select_3, key='bet_3_select', disabled=st.session_state['check_3'])
            else:
                pass
            bet_val_3 = st.slider(label='Amount to bet €', min_value=0, max_value=st.session_state['player_amount'], 
                                  step=100, key='bet_3_amount', disabled=st.session_state['check_3'])
    
    # Bet number 4
    with cr4:
        if st.session_state['num_bets']>=4:
            st.markdown('### **Bet nº 4**')
            checkbox_val = st.checkbox("Confirm Bet", value=False, key='check_4', disabled=False)
            B4 = st.selectbox('Bet Type', possible_bets, key='bet_4_type', disabled=st.session_state['check_4'])
            if B4 != '':
                list_select_4 = option_from_bet_type(B4)
                B4_2 = st.selectbox('Select your option',list_select_4, key='bet_4_select', disabled=st.session_state['check_4'])
            else:
                pass
            bet_val_4 = st.slider(label='Amount to bet €', min_value=0, max_value=st.session_state['player_amount'], 
                                  step=100, key='bet_4_amount', disabled=st.session_state['check_4'])

else:
    st.markdown('### **Game Over**')

# separation line
img = Image.open('aux_files/line_h.jpg')
st.image(img, width=703 )
img.close() 

###################################
## Conditions to spin the wheel

if st.session_state['player_amount'] > 0:
    i = 1
    check_boxes=[]
    missing_values=[]
    amount_values=[]
    amount_zeros=[]
    while i<=st.session_state['num_bets']:
        check_boxes.append(st.session_state[('check_{}').format(i)])
        missing_values.append(st.session_state[('bet_{}_type').format(i)])
        amount_values.append(st.session_state[('bet_{}_amount').format(i)])
        if st.session_state[('bet_{}_amount').format(i)] > 0:
            amount_zeros.append(True)
        else:
            amount_zeros.append(False)
        i=i+1
    
    # spin wheel
    button_spin = st.button('Spin the roulette')
    if button_spin==True:
        if np.prod(check_boxes)==0:
            st.error('Some bets are not confirmed')
        elif '' in missing_values:
            st.error('Some bets are not correctly placed')
        elif sum(amount_values) > st.session_state['player_amount']:
            st.error('The amount at stake is greater than the amount available')
        elif np.prod(amount_zeros)==0:
            st.error('Some bets have an amount of 0')
        else:
            st.session_state['spin'] = True
            st.experimental_rerun()
        st.session_state['spin'] = False
    st.session_state['spin'] = False
    
else:
    pass


#########################
## clear game and restart

clear_2 = st.button('Clear game & Restart')
if clear_2:
    for key in st.session_state.keys():
        del st.session_state[key]
    st.experimental_rerun()

###################################
## Roulette Bets & Payouts Table
st.markdown('#### Roulette Bets & Payouts')
df = pd.DataFrame({'Bets':possible_bets[1:], 'Payouts':['35:1','17:1','11:1','8:1','5:1', '2:1', '2:1', '1:1', '1:1', '1:1']})
# CSS to inject contained in a string
hide_table_row_index = """
            <style>
            thead tr th:first-child {display:none}
            tbody th {display:none}
            </style>
            """
# Inject CSS with Markdown
st.markdown(hide_table_row_index, unsafe_allow_html=True)
st.table(df)
