# import pywhatkit
from neuralintents import GenericAssistant
import speech_recognition
import pyttsx3 as tts
from quote import quote
import streamlit as st
from random_word import RandomWords
import warnings


warnings.filterwarnings("ignore")


def local_css(file_name):
    with open(file_name) as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)


def remote_css(url):
    st.markdown(f'<link href="{url}" rel="stylesheet">', unsafe_allow_html=True)


def icon(icon_name):
    st.markdown(f'<i class="material-icons">{icon_name}</i>', unsafe_allow_html=True)


local_css("style.css")
remote_css('https://fonts.googleapis.com/icon?family=Material+Icons')

st.markdown("<h1 style='text-align: ; color: #FFFAFA;'>Your virtual intelligence assistant</h1>",
            unsafe_allow_html=True)
st.markdown("<h3 style='text-align: ; color: #FFFAFA;'>Click and Say hello!</h3>", unsafe_allow_html=True)
st.info("she's able to do the fllowing: \n - Play Songs. \n - say a wisdom. \n - create todo list. \n - create note. \n - show the todo list. ")
submitButton = st.button("Play")

if submitButton:
    recognizer = speech_recognition.Recognizer()
    speaker = tts.init()
    voices = speaker.getProperty('voices')
    speaker.setProperty('voice', voices[1].id)
    speaker.setProperty('rate', 150)

    todo_list = []


    def create_note():
        global recognizer
        speaker.say('What do you want to write in your notes?')
        speaker.runAndWait()

        done = False

        while not done:
            try:
                with speech_recognition.Microphone() as mic:
                    recognizer.adjust_for_ambient_noise(mic, duration=0.2)
                    audio = recognizer.listen(mic)
                    note = recognizer.recognize_google(audio)
                    note = note.lower()

                    speaker.say("Choose a filename!")
                    speaker.runAndWait()
                    recognizer.adjust_for_ambient_noise(mic, duration=0.2)
                    audio = recognizer.listen(mic)

                    filename = recognizer.recognize_google(audio)
                    filename = filename.lower()

                with open(f"{filename}.text", 'w') as f:
                    f.write(note)
                    done = True
                    speaker.say(f"I successfully created the note {filename}")
                    speaker.runAndWait()
            except speech_recognition.UnknownValueError:
                recognizer = speech_recognition.Recognizer()
                speaker.say("I did not understand you! Please try again")
                speaker.runAndWait()


    def add_todo():
        global recognizer

        speaker.say("What to do do you want to add?")
        speaker.runAndWait()
        done = False

        while not done:
            try:
                with speech_recognition.Microphone() as mic:
                    recognizer.adjust_for_ambient_noise(mic, duration=0.2)
                    audio = recognizer.listen(mic)

                    item = recognizer.recognize_google(audio)
                    item = item.lower()
                    todo_list.append(item)
                    done = True

                    speaker.say(f"I added {item} to the to do list!")
                    speaker.runAndWait()

            except speech_recognition.UnknownValueError:
                recognizer = speech_recognition.Recognizer()
                speaker.say("I did not understand. Please try again")
                speaker.runAndWait()


    def show_todo():
        speaker.say("The item on your to do list are the following")
        for item in todo_list:
            speaker.say(item)
        speaker.runAndWait()


    def hello():
        speaker.say("hello what can i do for you?")
        speaker.runAndWait()


    def quotes():
        print("quote")
        r = RandomWords()
        w = r.get_random_word()

        res = quote(w, limit=1)
        for i in range(len(res)):
            speaker.say("here's a wisdom for today")
            st.info(" a wisdom for today: \n" + res[i]['quote'])
            speaker.say(res[i]['quote'])
            speaker.runAndWait()


    def hate_words():
        global recognizer
        speaker.say("but i love u")
        speaker.runAndWait()
        done = False

        while not done:
            try:
                with speech_recognition.Microphone() as mic:
                    recognizer.adjust_for_ambient_noise(mic, duration=0.2)
                    audio = recognizer.listen(mic)

                    words = recognizer.recognize_google(audio)
                    words = words.lower()
                    speaker.runAndWait()
                    done = True

            except speech_recognition.UnknownValueError:
                recognizer = speech_recognition.Recognizer()
                speaker.say("I did not understand. Please try again")
                speaker.runAndWait()


    def love_words():

        print("love")
        global recognizer
        speaker.say("you're amazing")
        speaker.runAndWait()
        done = False
        while not done:
            try:
                with speech_recognition.Microphone() as mic:
                    recognizer.adjust_for_ambient_noise(mic, duration=0.2)
                    audio = recognizer.listen(mic)

                    word = recognizer.recognize_google(audio)
                    word = word.lower()
                    speaker.runAndWait()
                    done = True

            except speech_recognition.UnknownValueError:
                recognizer = speech_recognition.Recognizer()
                speaker.say("I did not understand. Please try again")
                speaker.runAndWait()


    def play_songs():

        global recognizer

        speaker.say("What do you want to hear?")
        speaker.runAndWait()
        done = False

        while not done:
            try:
                with speech_recognition.Microphone() as mic:
                    recognizer.adjust_for_ambient_noise(mic, duration=0.2)
                    audio = recognizer.listen(mic)

                    song = recognizer.recognize_google(audio)
                    song = song.lower()
                    speaker.say('playing' + song)
                    # pywhatkit.playonyt(song)
                    speaker.runAndWait()
                    done = True

            except speech_recognition.UnknownValueError:
                recognizer = speech_recognition.Recognizer()
                speaker.say("I did not understand. Please try again")
                speaker.runAndWait()

    def quit():
        speaker.say("Bye")
        speaker.runAndWait()
        st.stop()

    mappings = {
            "greeting": hello,
            "create_note": create_note,
            "add_todo": add_todo,
            "show_todo": show_todo,
            "quotes": quotes,
            "play_songs": play_songs,
            "love_words": love_words,
            "hate_words": hate_words,
            "exit": quit}

    assistent = GenericAssistant('intents.json', intent_methods=mappings)
    assistent.train_model()




    while True:
        try:
            with speech_recognition.Microphone() as mic:
                recognizer.adjust_for_ambient_noise(mic, duration=0.2)
                audio = recognizer.listen(mic)
                message = recognizer.recognize_google(audio)
                message = message.lower()

            assistent.request(message)

        except speech_recognition.UnknownValueError:
            recognizer = speech_recognition.Recognizer()
# st.error("please try again")

else:
    pass
