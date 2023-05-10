# Author: Bill Tong
# Precursor to existing Trump.py file, deprecated with the introduction of the Trump voice

from gtts import gTTS
import os
import random

'''
Author: Bill Tong
Purpose: This file produces the voice over for game setup and provides TTS for social interaction while the game progresses.

Note: gTTS requires internet connection. Alternatives such as pyTTSx3 did not work as intended. Furthermore, features such as Voice recognition and OpenAI(for ChatGPT) did not work with python2.7
'''

def Angry():
	angry_list = ["I can't believe my luck is so bad. This game is rigged!","That's it, I'm done playing with you. You always cheat and ruin the game for everyone else!","I can't believe how unfair this game is! It's like everything is going against me!","I don't even want to talk to you right now. You're making me so angry with your constant greed and manipulation."]
	angry_option = random.randint(0,3)
	return angry_list[angry_option]

def Confused():
	confused_list = ["I don't understand, can you explain to me how that move is even possible?","I'm a bit lost here, can you walk me through your thought process on that move?","That move doesn't make sense to me, can we review the rules together and make sure we're on the same page?","I'm not sure I follow, can you clarify what you just did and why?"]
	confused_option = random.randint(0,3)
	return confused_list[confused_option]

def Happy():
	happy_list = ["Yes! Finally, luck is on my side!","I love Monopoly, it's always so exciting when things start going your way!","This game is so much fun, I'm having a blast playing with you!","I'm feeling really good about this game. I think I might have a shot at winning!"]
	happy_option = random.randint(0,3)
	return happy_list[happy_option]

def Neutral():
	neutral_list = ["I'm trying to concentrate here, so unless you want to be the next one bankrupt, be quiet.","I'm giving this game my full attention. Maybe you should do the same if you want to beat me.","I'm in the zone right now. Nothing can distract me from this game.","If you could refrain from talking for just a minute, that would be great. I need to focus on my next move."]
	neutral_option = random.randint(0,3)
	return neutral_list[neutral_option]

def Sad():
	sad_list = ["This game is just not going my way today. I feel like I can't catch a break.","I'm really struggling here. It seems like everyone else is doing better than me.","I'm not sure I'm enjoying this game anymore. It's hard to keep playing when things aren't going well.","Have mercy on me won't you?"]
	sad_option = random.randint(0,3)
	return sad_list[sad_option]

def Sassy():
	sassy_list = ["Haha, I can practically feel the envy radiating off of you! That move was a thing of beauty.","I'm not sure you're ready for the level of skill I just brought to the table with that move. I'm basically a monopoly master.","Looks like I've still got it! That move was a stroke of genius if I do say so myself.","You see that move? That's how it's done."]
	sassy_option = random.randint(0,3)
	return sassy_list[sassy_option]

def Surprise():
	surprise_list = ["I'm amazed by how quickly the tables can turn in this game. I was sure I had the upper hand!", "Wait, what? That's a game-changer! I didn't realize that was even possible.", "Wow, I didn't see that coming! You really caught me off guard!","I can't believe you just did that! That was so unexpected!"]
	surprise_option = random.randint(0,3)
	return surprise_list[surprise_option]

def Worried():
	worried_list = ["I'm starting to get concerned about your chances of winning.","I'm feeling a bit sorry for you, it seems like everything is going against you in this game.","I'm starting to think that we need to team up to help you get back in the game. It's no fun if someone loses too early!","I'm feeling a bit sorry for you right now. It can be tough when the game doesn't go your way."]
	worried_option = randint(0,3)
	return worried_list[worried_option]

def Run(state):
	if state == 1:
		speaker = gTTS(text=Angry(), lang="en", slow=False)
	elif state == 2:
		speaker = gTTS(text=Confused(), lang="en", slow=False)
	elif state == 3:
		speaker = gTTS(text=Happy(), lang="en", slow=False)
	elif state == 4:
		speaker = gTTS(text=Sad(), lang="en", slow=False)
	elif state == 5:
		speaker = gTTS(text=Sassy(), lang="en", slow=False)
	elif state == 6:
		speaker = gTTS(text=Surprise(), lang="en", slow=False)
	elif state == 7:
		speaker = gTTS(text=Worried(), lang="en", slow=False)
	# 0 state default for neutral
	elif state == 0:
		speaker = gTTS(text=Neutral(), lang="en", slow=False)

	speaker.save("tts.mp3")
	os.system("mpg321 tts.mp3")

# Voice over for game setup
def gameSetup():
	speaker = gTTS(text="Begin Setup. Choose a banker. A human is preferred. Each player starts with $1500. Please shuffle the Community Chest and Chance cards, and place them facedown in their designated areas. Choose a token. I will use my special token for easier gripping. Roll the dice. High roll goes first.", lang="en", slow=False)	
	speaker.save("dialogue.mp3")
	os.system("mpg321 dialogue.mp3")

# Voice over for turns and endgame
def generalDialogue(option):
	list = ["It's my turn.","It's your turn.","Looks like I'm out of money. You win! Would you like to play again?"]
	speaker = gTTS(text=list[option], lang="en", slow=False)
	speaker.save("general.mp3")
	os.system("mpg321 general.mp3")

if __name__ == "__main__":
	gameSetup()
