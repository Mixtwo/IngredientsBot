import praw
import config
import time
import os
import re
from ingredients_methods import product_info_for

# Login
def bot_login():
	r = praw.Reddit(username = config.username, 
			password = config.password,
			client_id = config.client_id,
			client_secret = config.client_secret,
			user_agent = "skin bot test v0.1")

	return r

# extract img
def extract_img(url):
	word = ".jpg"
	img_url = re.match(r'(.*(.jpg|.jpeg|.gif|.png))', url).group(1)
	return img_url

# Runs the bot
def run_bot(r, comments_replied_to):
	print ("Obtaining 25 comments...")
	#TODO: change 'test' subreddit to 'skincareaddiction' subreddit when bot is live
	for comment in r.subreddit('test').comments(limit=25):
		if ("!ingredients" in comment.body or "!Ingredients" in comment.body) and comment.id not in comments_replied_to:
			print("String with !ingredients found!")
			print("Posted by: " + comment.author.name)
			print("Comment Body: " + comment.body)

			# disect comment body for query words between < > ? fo non-greedy
			search_terms = re.search(r'<(\w+( \w+)*)>', comment.body) #.group(1)

			if search_terms:
				search_terms = search_terms.group(1)

				############### implementation of ingredients_methods.py ##################

				product_info = product_info_for(search_terms)

				if product_info != None:
					product_list_str = ' '.join(product_info.ingredients)
					product_img = extract_img(product_info.img_url)
					print(product_info.brand)
					print(product_info.name)
					print(product_img)
					print(product_list_str)

					comment.reply("#####" + product_info.brand + " - " + product_info.name + "\n" + "#####[[Product Image]](" + product_img + ")" + "\n" + "---" + "\n" + "#####INGREDIENTS: " + "\n>" + product_list_str + "\n" + "\n" + "\n" + "---" + "\n" + "\n" + "^^| ^^If ^^you ^^would ^^like ^^to ^^use ^^me, ^^the ^^command ^^is: ^^**!ingredients** ^^**<detailed** ^^**product** ^^**name>** ^^| ^^Message ^^me ^^for ^^complaints ^^and ^^suggestions ^^|")

				else:

					comment.reply("Sorry, searching for [" + search_terms + "] produced no results.")

				###########################################################################

			else:
				comment.reply("Sorry, I seem to have issues with the summoning command. It should be **!ingredients <*your search terms*>**")

			print("Replied to comment " + comment.id)

			# save comment id to our comments replied to Id txt file
			comments_replied_to.append(comment.id)
			with open("comments_replied_to_ID.txt", "a") as f:
				f.write(comment.id + "\n")

	print ("Sleeping for 10 seconds...")		
	time.sleep(10)	

# Saves comment ID to a file
def get_saved_comment_IDs():
	if not os.path.isfile("comments_replied_to_ID.txt"):
		comments_replied_to_ID = []

	else:	
		with open("comments_replied_to_ID.txt", "r") as f:
			comments_replied_to_ID = f.read()
			comments_replied_to_ID = comments_replied_to_ID.split("\n")		
			# filter object needs to be turned into a list manually in python 3
			comments_replied_to_ID = list(filter(None, comments_replied_to_ID))

	return comments_replied_to_ID

# main
r = bot_login()
comments_replied_to = get_saved_comment_IDs()

while True:
	run_bot(r, comments_replied_to)
