import Car_Detection.visualize
import os
import sys
from pygame import mixer # Load the required library
from gtts import gTTS

def say_done():
    mytext = 'annotating is done'
    language = 'en'
    myobj = gTTS(text=mytext, lang=language, slow=False) 
    myobj.save("done.mp3") 
    mixer.init()
    mixer.music.load("done.mp3")
    mixer.music.play()




if __name__ == "__main__":
    imgs=os.listdir('../'+sys.argv[1])
    imgpath='../'+sys.argv[1]
    for img in imgs:
        visualize.annotate(imgpath+'/'+img,sys.argv[1])
        print('finished image ',img)
    say_done()