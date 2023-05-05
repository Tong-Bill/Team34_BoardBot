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
        path = '/home/team34/ros_ws/src/baxter_tools/scripts/audio/'

        angry_list = [path+'angry-trump1.wav', path+'angry-trump2.wav', path+'angry-trump3.wav', path+'angry-trump4.wav', path+'angry-trump5.wav']
        list_value = random.randint(0,4)
        selected = angry_list[list_value]
        playsound('%s' % (selected))

def happy():
        path = '/home/team34/ros_ws/src/baxter_tools/scripts/audio/'
        # Phrases generated in (happy)Trump-TTS:
        # "I'll send you to sleep like I did with sleepy joe last night"
        # "I'm not a monopolist, I'm a winner."
        # "I will build a wall around my properties next!"
        # "I'm the best Monopoly player, nobody plays Monopoly better than me"
        # "The best thing about me is that I'm rich and famous"
        happy_list = [path+'happy-trump1.wav', path+'happy-trump2.wav', path+'happy-trump3.wav', path+'happy-trump4.wav', path+'happy-trump5.wav']
        list_value = random.randint(0,4)
        selected = happy_list[list_value]
        playsound('%s' % (selected))

def sad():
        path = '/home/team34/ros_ws/src/baxter_tools/scripts/audio/'
        # Phrases generated in (sad)Trump-TTS:
        # "This is the saddest game I've ever played"
        # "I CAN'T EVEN GET A BREANK IN A BOARD GAME."
        # "How about loaning me some money?"
        # "Everyone's out to get me today"
        # "I'm losing in life and in game, justice is dead."
        sad_list = [path+'sad-trump1.wav', path+'sad-trump2.wav', path+'sad-trump3.wav', path+'sad-trump4.wav', path+'sad-trump5.wav']
        list_value = random.randint(0,4)
        selected = sad_list[list_value]
        playsound('%s' % (selected))

def surprise():
        path = '/home/team34/ros_ws/src/baxter_tools/scripts/audio/'
        # Phrases generated in (surprise)Trump-TTS:
        # "Well that was an unexpected outcome. Unexpectedly stupid."
        # "What are you trying to do to me?"
        # "I didn't see that coming, neither did you."
        # "Looks like the tables have turned."
        # "I wish I had thought of that."
        surprise_list = [path+'surprise-trump1.wav', path+'surprise-trump2.wav', path+'surprise-trump3.wav', path+'surprise-trump4.wav', path+'surprise-trump5.wav']
        list_value = random.randint(0,4)
        selected = surprise_list[list_value]
        playsound('%s' % (selected))

def taunt():
        path = '/home/team34/ros_ws/src/baxter_tools/scripts/audio/'
        # I'm the king of the board. You're just a peasant.
        # I always win at Monopoly, it's just a fact.
        # You're a total loser! You can't even handle Monopoly!
        # You're a disaster, just like your game strategy.
        # I'm a billionaire in real life, so watch out on this board.
        # I'm a winner, and you're a loser. It's as simple as that.
        # I always win bigly, so don't even bother trying to beat me.
        # I'm owning this board like I own my hotels.
        taunt_list = [path+'taunt-trump1.wav', path+'taunt-trump2.wav', 
                    path+'taunt-trump3.wav', path+'taunt-trump4.wav', path+'taunt-trump5.wav', path+'taunt-trump6.wav', path+'taunt-trump7.wav', path+'taunt-trump8.wav']
        list_value = random.randint(0,7)
        selected = taunt_list[list_value]
        playsound('%s' % (selected))

def dialogue(value):
        path = '/home/team34/ros_ws/src/baxter_tools/scripts/audio/'
        # You want to buy the railroad huh?
        # Do you want to buy utility or not?
        # cards? You mean my credit card?
        # HEY! Sell your house first.
        # Which property will you mortgage?
        # What do you want to unmortgage?
        # Completed sets? You got none.
        # You got no properties
        dialogue_list = [path+'dialogue-trump1.wav', path+'dialogue-trump2.wav', path+'dialogue-trump3.wav',
        path+'dialogue-trump4.wav', path+'dialogue-trump5.wav', path+'dialogue-trump6.wav', path+'dialogue-trump7.wav', path+'dialogue-trump8.wav']
        selected = dialogue_list[value]
        playsound(selected)

def robotStart():
        global path
        playsound('/home/team34/ros_ws/src/baxter_tools/scripts/audio/start-trump1.wav')
def playerStart():
        global path
        playsound('/home/team34/ros_ws/src/baxter_tools/scripts/audio/start-trump2.wav')

def jail():
        path = '/home/team34/ros_ws/src/baxter_tools/scripts/audio/'
        # "I'm not going to jail, I'm too important for that. I have a get-out-of-jail-free card."
        playsound(path+'jail-trump1.wav')

def bankrupt():
        path = '/home/team34/ros_ws/src/baxter_tools/scripts/audio/'
        # "I'm bankrupt? No, fake news! My assets are tremendous, believe me."
        playsound(path+'bankrupt-trump1.wav')

def robotWin():
        path = '/home/team34/ros_ws/src/baxter_tools/scripts/audio/'
        # Come on, don't be a sore loser.
        playsound(path+'dialogue-trump9.wav')
        pass

def playerWin():
        path = '/home/team34/ros_ws/src/baxter_tools/scripts/audio/'
        # I would have won if there was a pay to win option.
        playsound(path+'dialogue-trump10.wav')
        pass
if __name__=="__main__":
        angry()
