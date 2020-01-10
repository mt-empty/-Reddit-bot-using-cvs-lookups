import praw
import time
import re
import pandas
import config
import game_config


def bot_login():
    print("logging in")
    reddit_account = praw.Reddit(username=config.username,
                                 password=config.password,
                                 client_id=config.client_id,
                                 client_secret=config.client_secret,
                                 user_agent="cvs lookup to reddit table")
    print("logged in as", config.username)
    return reddit_account


def run_bot(r, comments_replied):
    """
    Sanitizes input if valid
    
    Args:
        r (object): a reddit reddit instance
        comments_replied (string): the reply comment
    """

    for comment in r.subreddit('test').comments(limit=155):

        key_words = re.findall(game_config.regex, comment.body)
        # print(key_words)

        if key_words and comment.id not in comments_replied: # and comment.author != r.user.me():

            bot_reply = ""

            for key_word in key_words:
                try:
                    print("found a match")

                    # throws an error if there is more than one coma
                    key, version = key_word.split(",")

                    print("key:", key, "---", "version:", version)

                    key = key.strip()
                    version = version.strip().replace(' ', '')

                    header_list, keys_properties = get_data(key, version)
                    bot_reply += format_data(header_list, keys_properties)
                    print("bot reply:\n", bot_reply)
                except Exception as er:
                    print("Error:", er)
                    comments_replied.append(comment.id)
                    pass  # no entry in data or more than one coma or some other reason

            if bot_reply:
                comment.reply(bot_reply)
                comments_replied.append(comment.id)
                print("replied")

                with open("comments_replied.txt", "a") as f:
                    f.write(comment.id+"\n")


def get_data(keys, version):
    """
    returns data for a given keys and version
    
    Args:
        keys (list): a list of strings consisting of keyswords
        version (string): game version
    
    Returns:
        [list]: header list and key properties
    """

    files = game_config.files
    keys_properties = []

    if " vs " in keys:
        keys = keys.split(" vs ")
        keys = [k.strip() for k in keys]
    else:
        keys = [keys]

    for f in files:
        data = pandas.read_csv('{}\{}'.format(version, f))
        for key in keys:
            values = data[data.iloc[:, 0].str.match(
                key, case=False)].values.tolist()

            if values:
                values = values[0]
                keys_properties.append(values)  # check the first row only

        print(keys_properties)

        if len(keys_properties) == len(keys):
            header_list = data.columns.values.tolist()
            return header_list, keys_properties


def format_data(header_list, keys_properties):
    """
    formats the data into a reddit supported table
    
    Args:
        header_list (list): list of headers from the csv file
        keys_properties (list): the properties of each key
    
    Returns:
        string: the final replay
    """
    num_col = len(keys_properties)
    col_sep = "|---"

    keys_properties = comparison_format(keys_properties)

    bot_reply = ""
    for i, header_item in enumerate(header_list):
        if i == 1:
            bot_reply += "---" + col_sep*num_col + "\n"
        bot_reply += header_item + keys_properties[i] + "\n"

    bot_reply += "\n\n"

    assert isinstance(bot_reply, str), "should be a string"
    return bot_reply


def comparison_format(keys_properties):
    """
    returns a nicely formated table
    
    Args:
        keys_properties (strings): row information(non headers)
    
    Returns:
        list: row information(non headers)
    """
    row_properties = [""] * len(keys_properties[0])

    for key in keys_properties:
        for i, prop in enumerate(key):
            row_properties[i] = str(row_properties[i]) + "|" + str(prop)
    return row_properties


def get_saved_comments():
    """
    returns a list of user ids

    Returns:
        list: list of user ids
    """
    with open("comments_replied.txt", 'r') as f:
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

        print("sleeping for 5 seconds")  # sleep to prevent request limit
        time.sleep(5)
