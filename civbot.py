import praw
import config 
import time
#import requests
#import wikia
import re
#import csv
import pandas


def bot_login():
    print("logging in")
    reddit_account = praw.Reddit(username = config.username,
                password = config.password,
                client_id = config.client_id,
                client_secret = config.client_secret,
                user_agent = "cvs lookup to reddit table" )
    print("logged in")
    return reddit_account


def run_bot(r,comments_replied):

    for comment in r.subreddit('test').comments(limit=155):
        
        key_words = re.findall(r"\{A-Za-z5-6,\}", comment.body)  # capital A-Z, small a-z and numbers form 5-6 since civ 5 and 6 and finally a coma
        #print(key_words)

        
        if key_words and comment.id not in comments_replied:# and comment.author != r.user.me():
            
            bot_reply = ""

            for key_word in key_words:                
                try:
                    print("found a match")      # todo: if it finds a match that is not valid, it should save the comment id and skip it the next time as this will make it check endlessly

                    key, version = key_word.split(",") # Error if there is more than one coma

                    print("key:", key, "---", "version:", version)


                    key = key.strip()
                    version = version.strip().replace(' ', '')
                
                    header_list, keys_properties = get_datas(key, version)
                    bot_reply += format_datas(header_list, keys_properties) 
                    print("bot reply:\n",bot_reply)
                except Exception as er:
                    print("Error:", er)
                    pass #no entry in data or more than one coma or some other reason

            if bot_reply:
                comment.reply(bot_reply)
                comments_replied.append(comment.id) # make this line a function
                print("replied")

                with open("comments_replied.txt","a") as f:
                    f.write(comment.id+"\n")

def get_data(key,version):
    """
    returns the data for a key 
    
    Args:
        key (string): a string such as Assyria
    
    Returns:
        list : data associated to the key, else false if none
    """ 
    
    files = ['civs.csv', 'units.csv']

    for f in files:
        data = pandas.read_csv('{}\{}'.format(version, f))
        keys_properties = data[data.iloc[:,0].str.match(key, case=False)].values.tolist()    #  check the first row only 
        print(keys_properties)

        if keys_properties:
            header_list =  data.columns.values.tolist()
            return header_list, keys_properties


def format_data(header_list, keys_properties):
    """
    formats the data into a reddit supported table

    """
    bot_reply = ""
    for i in range(len(header_list)):
        if i == 1:
            bot_reply += "---|---\n"
        bot_reply += header_list[i] + "|"+ str(keys_properties[0][i]) + "\n"

    bot_reply += "\n\n"
        
    assert isinstance(bot_reply, str),"should be a string"
    return bot_reply

#######################
def get_datas(keys,version):
    """
    returns the data for a key 
    
    Args:
        key (string): a string such as Assyria
    
    Returns:
        list : data associated to the key, else false if none
    """ 
    
    files = ['civs.csv', 'units.csv']
    keys_properties = []

    if " vs " in keys:
        keys = keys.split(" vs ")
        keys = [ k.strip() for k in keys ]
    else:
        keys = [keys]


    for f in files:
        data = pandas.read_csv('{}\{}'.format(version, f))
        for key in keys:
            values = data[data.iloc[:,0].str.match(key, case=False)].values.tolist()
            
            if values:
                values = values[0]
                keys_properties.append(values)    #  check the first row only 

        print(keys_properties)

        if len(keys_properties) == len(keys):
            header_list =  data.columns.values.tolist()
            return header_list, keys_properties


def format_datas(header_list, keys_properties):
    """
    foramts the data into a reddit supported table

    """
    num_col = len(keys_properties) + 1
    col_sep = "|---"

    keys_properties = comparison_format(keys_properties)
    

    bot_reply = ""
    for i,header_item in enumerate(header_list):
        if i == 1:
            bot_reply += "---" + col_sep*num_col + "\n"
        bot_reply += header_item + keys_properties[i] + "\n"

    bot_reply += "\n\n"
        
    assert isinstance(bot_reply, str),"should be a string"
    return bot_reply

def comparison_format(keys_properties):
    new_list = [""] * len(keys_properties[0])

    for key in keys_properties:
        for i, prop in enumerate(key):
            new_list[i] = str(new_list[i]) + "|" + str(prop)
    return new_list

def get_saved_comments():
    """
    returns a list of user ids
    
    Returns:
        list: list of user ids
    """
    with open("comments_replied.txt",'r') as f:
        comments_replied = f.read()
        comments_replied = comments_replied.split("\n")
        comments_replied = list(filter(None, comments_replied))

    
    return comments_replied 



if __name__ == "__main__":
    
    reddit_account = bot_login()
    comments_replied = get_saved_comments()
    while True:
        run_bot(reddit_account, comments_replied)
        #stall = input("continue?\n")

        print("sleeping for 5 seconds") # sleep to prevent request limit
        time.sleep(5)
