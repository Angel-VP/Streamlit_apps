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
from game_functions import full_rows, game_over, gain_table, row_candidates_to_fill, box_to_fill, pc_turn_f
    

########## First elements to define

# initial configuration for the pagee
st.set_page_config( page_title='TicTacToe',
                    page_icon=':o:',
                    layout='centered',
                    initial_sidebar_state='expanded'
                    )

# Title
st.title('Welcome to Tic Tac Toe game !')

st.subheader(':heavy_multiplication_x: :o: :heavy_multiplication_x: :o: :heavy_multiplication_x: :o:')

##############################
## session state variables 

if 'turn' not in st.session_state:
    st.session_state['turn'] = 0
    
if 'game_over' not in st.session_state:
    st.session_state['game_over'] = False
    
if 'submit' not in st.session_state:
    st.session_state['submit'] = False
    
if 'tl' not in st.session_state:
    st.session_state['tl'] = ''
if 'tc' not in st.session_state:
    st.session_state['tc'] = ''
if 'tr' not in st.session_state:
    st.session_state['tr'] = ''
if 'ml' not in st.session_state:
    st.session_state['ml'] = ''
if 'mc' not in st.session_state:
    st.session_state['mc'] = ''
if 'mr' not in st.session_state:
    st.session_state['mr'] = ''
if 'bl' not in st.session_state:
    st.session_state['bl'] = ''
if 'bc' not in st.session_state:
    st.session_state['bc'] = ''
if 'br' not in st.session_state:
    st.session_state['br'] = ''
    
if 'pl_win' not in st.session_state:
    st.session_state['pl_win'] = 0
if 'pc_win' not in st.session_state:
    st.session_state['pc_win'] = 0
    
#############################
## other formating variables

# spacing for symbols
space = '# ' + ' '.join(['&nbsp;' for e in range(0,5)])

##########################################
## Choose 'X' or 'O' to play and PC choicer

# # Player choice
# placeholder0 = st.empty()
# pick_XO = placeholder0.radio("Choose 'X' or 'O' to play:",['','X','O'], key='pick_XO', disabled=False )

# if pick_XO=='X' or pick_XO=='O':
#     pick_XO_2 = st.radio('You picked:', pick_XO, key='pick_XO_2', disabled=True)
#     placeholder0.empty()

# # option picked:
# opt = ['']+[pick_XO]

# # PC choice 
# if pick_XO=='X':
#     pc = 'O'
# elif pick_XO=='O':
#     pc = 'X'
# else:
#     pc = ''
    
    
#########################################################
## Game settings - Box Filler / Player Name / Difficulty

st.subheader('Game Options')

with st.form(key='columns_in_form'):
    c1, c2, c3 = st.columns(3)
    with c1:
        pick_XO = st.radio("Choose 'X' or 'O' to play ",['X','O'], key='pick_XO', disabled=st.session_state['submit'] )
        # option picked:
        opt = ['']+[pick_XO]
        # PC choice 
        if pick_XO=='X':
            pc = 'O'
        elif pick_XO=='O':
            pc = 'X'
        else:
            pc = ''
            
    with c2:
        player_name = st.text_input("Enter your Name ", value='Player', disabled=st.session_state['submit'])
    with c3:
        difficulty = st.radio("Choose difficulty ",['Easy','Hard'], key='difficulty', disabled=st.session_state['submit'] )

    submitButton = st.form_submit_button(label = 'Play')
    if submitButton and st.session_state['submit']==False and (pick_XO in ['X', 'O']):
        st.session_state['submit'] = True
        st.experimental_rerun()

######################
## Win Counter

st.subheader('Score Board')

sc1, sc2, sc3, sc4, sc5, sc6 = st.columns((3,10,1,4,10,1))
with sc2:
    text_score_pl = ("""<span style='color:blue;'> {} </span>""").format(str(st.session_state['pl_win']))
    st.markdown('## :bust_in_silhouette: ' + player_name + ':&nbsp; &nbsp;' + text_score_pl, 
                unsafe_allow_html=True)
    
with sc4:
    st.markdown('## /' )
with sc5:
    text_score_pc = ("""<span style='color:red;'> {} </span>""").format(str(st.session_state['pc_win']))
    st.markdown('## :computer:  ' + 'PC' + ':&nbsp; &nbsp;' + text_score_pc, 
                unsafe_allow_html=True)

################################
## columns and row for the board

if (pick_XO=='X' or pick_XO=='O') and st.session_state['submit']:
    
    # top row
    ct1, line_v1, ct2, line_v2, ct3 = st.columns((10,1,10,1,10))
    # ct1, ct2, ct3 = st.columns(3)
    with ct1:
        if st.session_state['tl'] == '':
            TL = st.selectbox('', opt, key='TL', disabled=st.session_state['game_over'])
        else:
            # TL2 = st.selectbox('', st.session_state['tl'], key='TL2', disabled=True)
            if st.session_state['tl'] == 'X':
                st.markdown(space + ':heavy_multiplication_x:')
            else:
                st.markdown(space +  ':o:')
    
    # separation line
    with line_v1:
        
        img = Image.open('aux_files/line_v.jpg')
        st.image(img, width=2 )
        img.close()
    
    with ct2:
        if st.session_state['tc'] == '':
            TC = st.selectbox('', opt, key='TC', disabled=st.session_state['game_over'])
        else:
            # TC2 = st.selectbox('', st.session_state['tc'], key='TC2', disabled=True)
            if st.session_state['tc'] == 'X':
                st.markdown(space + ':heavy_multiplication_x:')
            else:
                st.markdown(space + ':o:')
    
    # separation line
    with line_v2:
        img = Image.open('aux_files/line_v.jpg')
        st.image(img, width=2 )
        img.close()
    
    with ct3:
        if st.session_state['tr'] == '':
            TR = st.selectbox('', opt, key='TR', disabled=st.session_state['game_over'])
        else:
            # TR2 = st.selectbox('', st.session_state['tr'], key='TR2', disabled=True)
            if st.session_state['tr'] == 'X':
                st.markdown(space + ':heavy_multiplication_x:')
            else:
                st.markdown(space + ':o:')
    
    
    # separation line
    img = Image.open('aux_files/line_h.jpg')
    st.image(img, width=703 )
    img.close()
    
    # middle row
    # cm1, cm2, cm3 = st.columns(3)
    cm1, line_v3, cm2, line_v4, cm3 = st.columns((10,1,10,1,10))
    with cm1:
        if st.session_state['ml'] == '':
            ML = st.selectbox('', opt, key='ML', disabled=st.session_state['game_over'])
        else:
            # ML2 = st.selectbox('', st.session_state['ml'], key='ML2', disabled=True)
            if st.session_state['ml'] == 'X':
                st.markdown(space + ':heavy_multiplication_x:')
            else:
                st.markdown(space + ':o:')
            
    # separation line
    with line_v3:
        img = Image.open('aux_files/line_v.jpg')
        st.image(img, width=2 )
        img.close()
            
    with cm2:
        if st.session_state['mc'] == '':
            MC = st.selectbox('', opt, key='MC', disabled=st.session_state['game_over'])
        else:
            # MC2 = st.selectbox('', st.session_state['mc'], key='MC2', disabled=True)
            if st.session_state['mc'] == 'X':
                st.markdown(space + ':heavy_multiplication_x:')
            else:
                st.markdown(space + ':o:')
                
    # separation line
    with line_v4:
        img = Image.open('aux_files/line_v.jpg')
        st.image(img, width=2 )
        img.close()    
    
    with cm3:
        if st.session_state['mr'] == '':
            MR = st.selectbox('', opt, key='MR', disabled=st.session_state['game_over'])
        else:
            # MR2 = st.selectbox('', st.session_state['mr'], key='MR2', disabled=True)
            if st.session_state['mr'] == 'X':
                st.markdown(space + ':heavy_multiplication_x:')
            else:
                st.markdown(space + ':o:')
            
    # separation line
    img = Image.open('aux_files/line_h.jpg')
    st.image(img, width=703 )
    img.close()
    
    # bottom row
    # cb1, cb2, cb3 = st.columns(3)
    cb1, line_v5, cb2, line_v6, cb3 = st.columns((10,1,10,1,10))
    with cb1:
        if st.session_state['bl'] == '':
            BL = st.selectbox('', opt, key='BL', disabled=st.session_state['game_over'])
        else:
            # BL2 = st.selectbox('', st.session_state['bl'], key='BL2', disabled=True)
            if st.session_state['bl'] == 'X':
                st.markdown(space + ':heavy_multiplication_x:')
            else:
                st.markdown(space + ':o:')
                
    # separation line
    with line_v5:
        img = Image.open('aux_files/line_v.jpg')
        st.image(img, width=2 )
        img.close()  
    
    with cb2:
        if st.session_state['bc'] == '':
            BC = st.selectbox('', opt, key='BC', disabled=st.session_state['game_over'])
        else:
            # BC2 = st.selectbox('', st.session_state['bc'], key='BC2', disabled=True)
            if st.session_state['bc'] == 'X':
                st.markdown(space + ':heavy_multiplication_x:')
            else:
                st.markdown(space + ':o:')
                
    # separation line
    with line_v6:
        img = Image.open('aux_files/line_v.jpg')
        st.image(img, width=2 )
        img.close()  
    
    with cb3:
        if st.session_state['br'] == '':
            BR = st.selectbox('', opt, key='BR', disabled=st.session_state['game_over'])
        else:
            # BR2 = st.selectbox('', st.session_state['br'], key='BR2', disabled=True)
            if st.session_state['br'] == 'X':
                st.markdown(space + ':heavy_multiplication_x:')
            else:
                st.markdown(space + ':o:')
        
#############################        
## update box selection state
if (pick_XO=='X' or pick_XO=='O') and st.session_state['submit']:
    if st.session_state['tl'] == '':
        if (TL=='X' or TL=='O'):
            st.session_state['tl'] = TL
            st.session_state['turn'] += 1
            st.experimental_rerun()
    
    if st.session_state['tc'] == '':
        if (TC=='X' or TC=='O'):
            st.session_state['tc'] = TC
            st.session_state['turn'] += 1
            st.experimental_rerun()
    
    if st.session_state['tr'] == '':    
        if (TR=='X' or TR=='O'):
            st.session_state['tr'] = TR
            st.session_state['turn'] += 1
            st.experimental_rerun()
            
    if st.session_state['ml'] == '':
        if (ML=='X' or ML=='O'):
            st.session_state['ml'] = ML
            st.session_state['turn'] += 1
            st.experimental_rerun()
    
    if st.session_state['mc'] == '':
        if (MC=='X' or MC=='O'):
            st.session_state['mc'] = MC
            st.session_state['turn'] += 1
            st.experimental_rerun()
    
    if st.session_state['mr'] == '':    
        if (MR=='X' or MR=='O'):
            st.session_state['mr'] = MR
            st.session_state['turn'] += 1
            st.experimental_rerun()
            
    if st.session_state['bl'] == '':
        if (BL=='X' or BL=='O'):
            st.session_state['bl'] = BL
            st.session_state['turn'] += 1
            st.experimental_rerun()
    
    if st.session_state['bc'] == '':
        if (BC=='X' or BC=='O'):
            st.session_state['bc'] = BC
            st.session_state['turn'] += 1
            st.experimental_rerun()
    
    if st.session_state['br'] == '':    
        if (BR=='X' or BR=='O'):
            st.session_state['br'] = BR
            st.session_state['turn'] += 1
            st.experimental_rerun()

##############
## game status

if (pick_XO=='X' or pick_XO=='O') and st.session_state['game_over'] == False and st.session_state['submit']:
    
    board = {'p1':st.session_state['tl'], 'p2':st.session_state['tc'], 'p3':st.session_state['tr'],
             'p4':st.session_state['ml'], 'p5':st.session_state['mc'], 'p6':st.session_state['mr'],
             'p7':st.session_state['bl'], 'p8':st.session_state['bc'], 'p9':st.session_state['br']}
    game_status = game_over(board, pick_XO, pc)
    
    if game_status != 0:
        st.session_state['game_over'] = True
        if game_status==1:
            st.session_state['pl_win'] += 1
            st.success('You win !!!! :tada:')
            st.balloons()
            time.sleep(2)
            st.experimental_rerun()
        elif game_status==2:
            st.session_state['pc_win'] += 1
            st.error('PC wins !!!! :tada:')
            st.balloons()
            time.sleep(2)
            st.experimental_rerun()
        else:
            st.info('It is a draw :no_mouth: ... Do yo want to play again?')
            time.sleep(2)
            st.experimental_rerun()
        
if st.session_state['game_over'] == True:
    
    board = {'p1':st.session_state['tl'], 'p2':st.session_state['tc'], 'p3':st.session_state['tr'],
             'p4':st.session_state['ml'], 'p5':st.session_state['mc'], 'p6':st.session_state['mr'],
             'p7':st.session_state['bl'], 'p8':st.session_state['bc'], 'p9':st.session_state['br']}
    
    game_status = game_over(board, pick_XO, pc)
    
    if game_status==1:
        st.success('You win !!!! :tada:')
    elif game_status==2:
        st.error('PC wins !!!! :tada:')
    else:
        st.info('It is a draw :no_mouth: ... Do yo want to play again?')

        

#############
## pc turn

if (pick_XO=='X' or pick_XO=='O') and st.session_state['game_over'] == False and st.session_state['submit']:
    
    if st.session_state['turn']%2 !=0:
        
        board = {'p1':st.session_state['tl'], 'p2':st.session_state['tc'], 'p3':st.session_state['tr'],
                 'p4':st.session_state['ml'], 'p5':st.session_state['mc'], 'p6':st.session_state['mr'],
                 'p7':st.session_state['bl'], 'p8':st.session_state['bc'], 'p9':st.session_state['br']}
        
        pc_turn = pc_turn_f(board, pick_XO, pc, difficulty)
        st.write(pc_turn)
        
        if pc_turn==1:
            st.session_state['tl'] = pc
            st.session_state['turn'] += 1
            st.experimental_rerun()
        elif pc_turn==2:
            st.session_state['tc'] = pc
            st.session_state['turn'] += 1
            st.experimental_rerun()
        elif pc_turn==3:
            st.session_state['tr'] = pc
            st.session_state['turn'] += 1
            st.experimental_rerun()
        elif pc_turn==4:
            st.session_state['ml'] = pc
            st.session_state['turn'] += 1
            st.experimental_rerun()
        elif pc_turn==5:
            st.session_state['mc'] = pc
            st.session_state['turn'] += 1
            st.experimental_rerun()
        elif pc_turn==6:
            st.session_state['mr'] = pc
            st.session_state['turn'] += 1
            st.experimental_rerun()
        elif pc_turn==7:
            st.session_state['bl'] = pc
            st.session_state['turn'] += 1
            st.experimental_rerun()
        elif pc_turn==8:
            st.session_state['bc'] = pc
            st.session_state['turn'] += 1
            st.experimental_rerun()
        elif pc_turn==9:
            st.session_state['br'] = pc
            st.session_state['turn'] += 1
            st.experimental_rerun()
        else:
            pass

# st.session_state

#########################
## clear game and restart

not_clear_seasion_keys = ['submit', 'pick_XO', 'pl_win', 'pc_win']

clear_1 = st.button('Play Again')
if clear_1:
    for key in st.session_state.keys():
        if key not in not_clear_seasion_keys:
            del st.session_state[key]
    st.experimental_rerun()
    

#########################
## clear game and restart

clear_2 = st.button('Restart & Change Configuration')
if clear_2:
    for key in st.session_state.keys():
        del st.session_state[key]
    st.experimental_rerun()








