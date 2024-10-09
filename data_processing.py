# -*- coding: utf-8 -*-
"""
Created on Sun Sep 10 15:17:29 2023

@author: becky
"""

import re
from datetime import datetime
from datetime import timedelta
import regex


# find_hands makes a list of hands
# INPUT: conjoined text data files
# OUTPUT: textual data divided into a list of poker hands

def find_hands(data):
    pattern1 = "PokerStars Hand"
    pattern2 = ".+PokerStars Hand"
    find_pattern1 = regex.match(pattern1, data)
    find_pattern2 = regex.match(pattern2, data)
    if find_pattern1:
        return True
    if find_pattern2:
        return True
    return False


# hand_structure divides each hand into relevant comoponents of the game
# INPUT: a textual account of a poker hand
# OUTPUT: a dictionary containing information relating to different aspects of a poker hand

def hand_structure(hand):
    
    game={"hand details":None, "table and button":None, "seats": None, 
          "blinds":None, "hole cards":None, "flop":None, "turn": None, "river":None, 
          "showdown":None, "summary":None}
    
    game["hand details"]=hand[0][:83]
    game["table and button"]=hand[1]
    
    game["seats"]=[]
    for line in hand[2:7]:
        if "Seat" in line:
            game["seats"].append(line)
    
    num_seats=len(game["seats"])
    
    blinds_start_index=hand.index(hand[2+num_seats])
    hole_cards_index=hand.index("*** HOLE CARDS ***")
    summary_index=hand.index("*** SUMMARY ***")
    
    game["blinds"]=hand[blinds_start_index:hole_cards_index]
    
    flop_line=[s for s in hand if "FLOP" in s]
    turn_line=[s for s in hand if "TURN" in s]
    river_line=[s for s in hand if "RIVER" in s]
    show_down_line=[s for s in hand if "SHOW DOWN" in s]
    
    
    if len(show_down_line)>0:
        show_down_index=hand.index(show_down_line[0])
        game["showdown"]=hand[show_down_index+1:summary_index]
        
    if len(river_line)>0:
        river_index=hand.index(river_line[0])
        if len(show_down_line)>0:
            river=hand[river_index:show_down_index]
        else:
            river=hand[river_index:summary_index]
        river[0]=river[0][14:]
        game["river"]=river
        
    if len(turn_line)>0:
        turn_index=hand.index(turn_line[0])
        if len(river_line)>0:
            turn=hand[turn_index:river_index]
        else:
            turn=hand[turn_index:summary_index]
        turn[0]=turn[0][13:]
        game["turn"]=turn
    
    if len(flop_line)>0:
        flop_index=hand.index(flop_line[0])
        if len(turn_line)>0:
            flop=hand[flop_index:turn_index]
        else:
            flop=hand[flop_index:summary_index]
        flop[0]=flop[0][12:]
        game["flop"]=flop
    
    game["summary"]=hand[summary_index+1:]
        
    return game



# Dictionary keys for the information to be extracted from each hand

hand_information = ["hand_table_name", "hand_datetime_start", "hand_number", "number_players", "positions", "winner_main_pot", "winner_side_pot1", "winner_side_pot2", "winner_side_pot3", "money_main_pot", "money_side_pot1", "money_side_pot2", "money_side_pot3"]

player_information = ["username", "type", "hands_recorded", "pfr_count", "pfr_count"]

play_information = ["username_play", "hand_number_play", "position_play", "starting_stack", "finishing_stack", "cards"]



# table_session_data extracts the relevant data relating to "tables"
# INPUT: a list of hands
# OUTPUT: information pertaining to a particular "table" (aka a session)

def table_session_data(hands_lists):
    hand=hands_lists[0]
    table_name = regex.findall(r"'([^']*)'", hand["table and button"])[0]
    
    blinds = (regex.findall("\(.+?\)", hand['hand details']))[0][1:-1].split("/")
    small_blind = int(blinds[0])
    big_blind = int(blinds[1])
    
    table_date_start = regex.findall('[0-9]{4}/[0-9]{2}/[0-9]{2}', hand["hand details"])[0]
    table_start_time = regex.findall('[0-9]{1,2}:[0-9]{2}:[0-9]{2}', hand["hand details"])
    
    table_start_time=table_start_time[0]
    
    if len(hands_lists)>1:
    
        table_date_end=regex.findall('[0-9]{4}/[0-9]{2}/[0-9]{2}', hands_lists[-1]["hand details"])[0]
        table_end_time = regex.findall('[0-9]{1,2}:[0-9]{2}:[0-9]{2}', hands_lists[-1]["hand details"])[0]

        datetime_str_start=table_date_start+" " + table_start_time
        datetime_start = datetime.strptime(datetime_str_start, '%Y/%m/%d %H:%M:%S')

        datetime_str_end=table_date_end+" " + table_end_time
        datetime_end=datetime.strptime(datetime_str_end, '%Y/%m/%d %H:%M:%S')

        duration2=(datetime_end-datetime_start)
        duration1=duration2.total_seconds()
        duration=round(duration1/60)*60
        duration=timedelta(seconds=duration)
    else:
        duration=0
        datetime_end=0

    return table_name, small_blind, big_blind, [str(datetime_start)],str(duration), len(hands_lists)



# hand_data extracts the relevant data relating to "hands"
# INPUT: a hand dictionary
# OUTPUT: relevant information about a  hand

def hand_data(hand):
    table=hand["table and button"]
    hand_d=hand["hand details"]
    
    hand_table_name = regex.findall(r"'([^']*)'", table)[0]
    
    hand_number = re.findall(r'(?<=\#).+?(?=\:)',hand_d)[0]
    
    hand_date = regex.findall('[0-9]{4}/[0-9]{2}/[0-9]{2}', hand_d)[0]
    hand_start_time = regex.findall('[0-9]{1,2}:[0-9]{2}:[0-9]{2}', hand_d)[0]
    hand_datetime_str=hand_date+" " + hand_start_time
    hand_datetime_start = datetime.strptime(hand_datetime_str, '%Y/%m/%d %H:%M:%S')
    
    
    seats_section=hand["seats"]
    seats= dict.fromkeys([1,2,3,4,5,6])
    for i in range(len(seats_section)):
        user=re.findall(r'(?<=\: ).+?(?=\()',seats_section[i])
        seat=int(seats_section[i][5])
        seats[seat]=user[0][:-1]
    
    number_players=len(seats_section)
    btn_seat=int(re.findall(r'(?<=\#).+?(?=\ i)',table)[0])
    
    if number_players==5:
        pos_key=['btn','sb','bb','utg','co']      # For the purposes of labelling positions, the 'co' (a late position) should                                       
    else:                                         # appear before the 'mp' (a middle position).
        pos_key=['btn','sb','bb','utg','mp','co'] # Otherwise the positions should appear in order beginning with the button.
    
    pos_val=[seats[btn_seat]]
    
    for j in range(1,6):
        if btn_seat+j<7:
            if seats[btn_seat+j] != None:
                pos_val.append(seats[btn_seat+j])
        else:
            if seats[btn_seat+j-6] != None:
                pos_val.append(seats[btn_seat+j-6])
    
    positions=dict(zip(pos_key, pos_val))
    
    winner_main_pot=None
    winner_side_pot1=None
    winner_side_pot2=None
    winner_side_pot3=None
    
    size_main_pot=None
    size_side_pot1=None
    size_side_pot2=None
    size_side_pot3=None
    
    keys=hand.keys()
    game_flat=[]
    for key in keys:
        if key!= "summary":
            if hand[key]!= None:
                game_flat+=hand[key]
                
    game=game_flat

    for item in game: 
        if regex.match(".+collected ", item):
            
            if regex.match(".+side pot-1", item):
                winner_side_pot1=item.split(' collected')[0]
                size_side_pot1=int(item.split(' collected ')[1].split(" from")[0])

            if regex.match(".+side pot-2", item):
                winner_side_pot2=item.split(' collected')[0]
                size_side_pot2=int(item.split(' collected ')[1].split(" from")[0])

            if regex.match(".+side pot-3", item):
                winner_side_pot3=item.split(' collected')[0]
                size_side_pot3=int(item.split(' collected ')[1].split(" from")[0])

            if regex.match(".+main", item):
                winner_main_pot=item.split(' collected ')[0]
                size_main_pot=int(item.split(' collected ')[1].split(" from")[0])
                
            else: 
                winner_main_pot=item.split(' collected ')[0]
                size_main_pot=int(item.split(' collected ')[1].split(" from")[0])

    return hand_table_name, str(hand_datetime_start), hand_number, number_players, positions, winner_main_pot, winner_side_pot1, winner_side_pot2, winner_side_pot3, size_main_pot, size_side_pot1, size_side_pot2, size_side_pot3
    

# player_data_update extracts relevant player data from each hand
# INPUT: a hand
# OUTPUT: each player's statistics from this hand

def player_data_update(hand):
    user_list=[]
    user_list_dict=[]
    user_info_keys=["username",'type','vpip','pfr']
    
    for i in range(6):
        line=hand[2+i]
        if line[:4]=='Seat':
            user=re.findall(r'(?<=\: ).+?(?=\()',line)
            if len(user)>0:
                user_list.append(user[0][:-1])
    
    hole_cards=hand.index("*** HOLE CARDS ***\n")
    hero_in=hand[hole_cards+1]
    
    flop=[s for s in hand if "FLOP" in s]
    summary_index=hand.index("*** SUMMARY ***\n")
    
    if len(flop)==0:
        pre_flop=hand[hole_cards+2:summary_index]
    else:
        flop_index=hand.index(flop[0])
        pre_flop=hand[hole_cards+2:flop_index]
    
    for user in user_list:
        user_info=[]
        pattern=".+"+user
        if regex.match(pattern, hero_in):
            user_info.extend([user, "hero"])
        else:
            user_info.extend([user, "villain"])
           
        pre_flop_bet=[s for s in pre_flop if user in s]
            
        if regex.match(".+calls", " ".join(pre_flop_bet)):
            user_info.append(True)
        else:
            if regex.match(".+raises", " ".join(pre_flop_bet)):
                user_info.append(True)
            else:
                user_info.append(False)
                

        for bet in pre_flop_bet:
            if regex.match(".+raises", bet):
                user_info.append(True)
            else:
                user_info.append(False)
                
        user_dict=dict(zip(user_info_keys, user_info))
        user_list_dict.append(user_dict)
        
    return user_list_dict
    

# player_data compiles into dictionary of dictionaries of player information
# INPUT: a list of lists of hands grouped by table
# OUTPUT: compiles together all of a player's statistics

def player_data(list_list_hands):
    dict_player_dict={}
    
    for i in range(len(list_list_hands)):
        list_hands=list_list_hands[i]
        
        for hand in list_hands:
            info=player_data_update(hand)
            
            for dictionary in info:
                user=dictionary['username']
                if user not in dict_player_dict.keys():
                    dict_player_dict[user]={"type":dictionary['type'], "hands_recorded":1, "vpip_count":int(dictionary['vpip']), "pfr_count":int(dictionary['pfr'])}
                else:
                    dict_player_dict[user]["hands_recorded"]=dict_player_dict[user]["hands_recorded"]+1
                    dict_player_dict[user]["vpip_count"]=dict_player_dict[user]["vpip_count"]+int(dictionary['vpip'])
                    dict_player_dict[user]["pfr_count"]=dict_player_dict[user]["pfr_count"]+int(dictionary['pfr'])
    
    return dict_player_dict
    

# end_stack computes the amount of chips a player has at the end of a hand
# INPUT: player statistics
# OUTPUT: number of chips in a player's stack at the end of a hand

def end_stack(hand, username, starting_stack):
    
    hole_cards_index=hand.index("*** HOLE CARDS ***\n")
    summary_index=hand.index("*** SUMMARY ***\n")
    summary=hand[summary_index:]
    
    blind_line=[s for s in hand if " small blind " in s]
    flop_line=[s for s in hand if "FLOP" in s]
    turn_line=[s for s in hand if "TURN" in s]
    river_line=[s for s in hand if "RIVER" in s]
    show_down_line=[s for s in hand if "SHOW DOWN" in s]
    
    game=[summary]
    
    if len(show_down_line)>0:
        show_down_index=hand.index(show_down_line[0])
        show_down=hand[show_down_index:summary_index]
        game.insert(0,show_down)
        
    if len(river_line)>0:
        river_index=hand.index(river_line[0])
        if len(show_down_line)>0:
            river=hand[river_index:show_down_index]
        else:
            river=hand[river_index:summary_index]
        game.insert(0,river)
        
    if len(turn_line)>0:
        turn_index=hand.index(turn_line[0])
        if len(river_line)>0:
            turn=hand[turn_index:river_index]
        else:
            turn=hand[turn_index:summary_index]
        game.insert(0,turn)
    
    if len(flop_line)>0:
        flop_index=hand.index(flop_line[0])
        if len(turn_line)>0:
            flop=hand[flop_index:turn_index]
        else:
            flop=hand[flop_index:summary_index]
        game.insert(0,flop)
        
    if len(flop_line)>0:
        hole_cards=hand[hole_cards_index:flop_index]
    else:
        hole_cards=hand[hole_cards_index:summary_index]
    game.insert(0,hole_cards)
    
    blinds=hand[hand.index(blind_line[0]):hole_cards_index]
    game.insert(0,blinds)
    
    total_bet=0
    winnings=0
    returned=0
    
    for part in game:
        bet=0
        for line in part:
            if "returned" in line:
                if username in line:
                    returned+=int(line.split("(")[1].split(")")[0])
            if username+": " in line:
                line=line.split(username+": ")[1]
                if "posts" in line or "raises" in line or "bets" in line:
                    bet=int(re.findall(r'\d+', line)[-1])
                if "calls" in line:
                    bet+=int(re.findall(r'\d+', line)[-1])
                    
        total_bet+=bet
   
    for line in summary:
        if username in line:
            if "won" in line or "collected" in line:
                winnings=int(re.findall(r'\d+', line)[-1])
                finishing_stack=winnings+starting_stack-total_bet+returned
            elif "lost" in line or "folded" in line or "mucked" in line:
                finishing_stack=starting_stack-total_bet+returned
                
    
    
    return finishing_stack

# play_info is a list of dictionaries containing information about a player's play in each hand, with usernames as keys.
# INPUT: hand and player information
# OUTPUT: information about how a player played a hand (e.g. their position and starting and ending stacks)

def play_data(hand,hand_info, player_info):
    hand_number=hand_info['hand_number']
    hand_datetime=hand_info['hand_datetime_start']
    position_list=list(hand_info['positions'].keys())
    user_list=list(hand_info['positions'].values())
    
    starting_stacks=[]
    
    
    hole_cards=hand.index("*** HOLE CARDS ***\n")
    intro=hand[:hole_cards]
    
    
    for user in user_list:
        for line in intro:
            if "Seat" in line:
                if user in line:
                    chips=line.split('(')[1].split(" in")[0]
                    starting_stacks.append(int(chips))
    
    hero_cards=hand[hole_cards+1][-7:-2]
    hero=[player for player in player_info if player['type']=='hero'][0]['username']
    
    play_dictionary={}
    play_dictionary=play_dictionary.fromkeys(user_list, None)
    play_dictionary[hero]=[hero_cards]
    
    summary=hand.index("*** SUMMARY ***\n")
    summary=hand[summary:]
    
    for user in user_list:
        for line in summary:
            if user in line:
                if "showed" in line:
                    cards=line.split("[")[1].split("]")[0]
                    play_dictionary[user]=cards.split(" ")
                else:
                    play_dictionary[user]=[]
    
    x=0
    while x<len(user_list):
        for key in play_dictionary:
            
            play_dictionary[key]=[hand_number, hand_datetime,position_list[x],starting_stacks[x]]+[play_dictionary[key]]
            x+=1
            
    for user in user_list:
        final_stack=end_stack(hand, user, play_dictionary[user][-2])
        
        play_dictionary[user].insert(-1,final_stack)
        
    return play_dictionary


