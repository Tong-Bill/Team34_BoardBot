# Author: Bill TOng
# Replaces the depricated expressions.py file, used for invoking trump voice
import random
from playsound import playsound

def angry():
	# Phrases generated in (angry)Trump-TTS:
	# "This game is rigged, just like the election"
	# "I'm losing? Who said that? fake news!"
	# "STOP THE GAME, STOP THE GAME."
	# "I demand a recount of the dice roll!"
	# "Why isn't my small loan showing up?"

	angry_list = ['angry-trump1.wav', 'angry-trump2.wav', 'angry-trump3.wav', 'angry-trump4.wav', 'angry-trump5.wav']
	list_value = random.randint(0,4)
	selected = angry_list[list_value]
	playsound('%s' % (selected))

def happy():
	# Phrases generated in (happy)Trump-TTS:
	# "I'll send you to sleep like I did with sleepy joe last night"
	# "I'm not a monopolist, I'm a winner."
	# "I will build a wall around my properties next!"
	# "I'm the best Monopoly player, nobody plays Monopoly better than me"
	# "The best thing about me is that I'm rich and famous"
	happy_list = ['happy-trump1.wav', 'happy-trump2.wav', 'happy-trump3.wav', 'happy-trump4.wav', 'happy-trump5.wav']
	list_value = random.randint(0,4)
	selected = happy_list[list_value]
	playsound('%s' % (selected))

def sad():
	# Phrases generated in (sad)Trump-TTS:
	# "This is the saddest game I've ever played"
	# "I CAN'T EVEN GET A BREANK IN A BOARD GAME."
	# "How about loaning me some money?"
	# "Everyone's out to get me today"
	# "I'm losing in life and in game, justice is dead."
	sad_list = ['sad-trump1.wav', 'sad-trump2.wav', 'sad-trump3.wav', 'sad-trump4.wav', 'sad-trump5.wav']
	list_value = random.randint(0,4)
	selected = sad_list[list_value]
	playsound('%s' % (selected))

def surprise():
	# Phrases generated in (surprise)Trump-TTS:
	# "Well that was an unexpected outcome. Unexpectedly stupid."
	# "What are you trying to do to me?"
	# "I didn't see that coming, neither did you."
	# "Looks like the tables have turned."
	# "I wish I had thought of that."
	surprise_list = ['surprise-trump1.wav', 'surprise-trump2.wav', 'surprise-trump3.wav', 'surprise-trump4.wav', 'surprise-trump5.wav']
	list_value = random.randint(0,4)
	selected = sad_list[list_value]
	playsound('%s' % (selected))

def robotStart():
	playsound('start-trump1.wav')
def playerStart():
	playsound('start-trump2.wav')

def jail():
	# "I'm not going to jail, I'm too important for that. I have a get-out-of-jail-free card."
	playsound('jail-trump1.wav')

def bankrupt():
	# "I'm bankrupt? No, fake news! My assets are tremendous, believe me."
	playsound('bankrupt-trump1.wav')

if __name__=="__main__":
	angry()
