import tkinter.messagebox
from tkinter import *
import gtts
import pandas
import random
import io
import pygame
import threading

# -----COLOUR PALATE----#
TEAL = "#B1DDC6"
TITLE = ("Ariel", 40, "italic")
WORD = ("Ariel", 60, "bold")
window = tkinter.Tk()
TEMP = ""

# ----------------------------Files---------------------------------#

data_frame = pandas.read_csv("../FlashCardApp/data/french_words.csv")
FRENCH = data_frame.French.to_list()


# ----------------------------French Handle--------------------------#

def french():
    global FRENCH
    if len(FRENCH) != 0:
        right_button.config(state=DISABLED)
        cross_button.config(state=DISABLED)
        canvas.itemconfig(canvas_image, image=green_card_img)
        canvas.itemconfig(card_title, text="French")
        french_choice = random.choice(FRENCH)
        canvas.itemconfig(word_title, text=f"{french_choice}")
        global TEMP
        TEMP = french_choice

        # Thread
        threading.Thread(target=speak_and_play, args=(french_choice, 'fr')).start()

        window.after(5000, change_image)
    else:
        tkinter.messagebox.showinfo(title="Oops", message="No more words available")


# ----- FUNCTION TO CHANGE IMAGE ----- #
def change_image():
    canvas.itemconfig(canvas_image, image=white_card_img)
    english()


# -----------------------------English Handle------------------------#

def english():
    right_button.config(state=NORMAL)
    cross_button.config(state=NORMAL)
    eng = data_frame[data_frame["French"] == TEMP].English.iloc[0]
    threading.Thread(target=speak_and_play, args=(eng,'en')).start()
    canvas.itemconfig(card_title, text="English")
    canvas.itemconfig(word_title, text=f"{eng}")
    threading.Thread(target=speak_and_play, args=(eng, 'en')).start()


# --------------Translate----------------------#

def speak_and_play(text, lang):
    tts = gtts.gTTS(text, lang=lang)
    audio_data = io.BytesIO()
    tts.write_to_fp(audio_data)
    # Reset the BytesIO object's position to the beginning
    audio_data.seek(0)

    # Initialize pygame mixer
    pygame.mixer.init()

    # Load the audio data into pygame mixer
    pygame.mixer.music.load(audio_data, "mp3")
    pygame.mixer.music.play()

    # Keep the program running until the audio finishes playing
    while pygame.mixer.music.get_busy():
        pygame.time.Clock().tick(10)


# ----------------------------Remove-----------------------------------#
def right():
    global FRENCH
    FRENCH.remove(TEMP)
    french()


# -------------------------Shuffle-------------------------------------#
def cross():
    french()


# -------------------------------UI---------------------------------#
window.title("Flash Card")
window.config(padx=50, pady=50, bg=TEAL)

canvas = tkinter.Canvas(width=800, height=526, bg=TEAL, highlightthickness=0)

# greenCard
green_card_img = tkinter.PhotoImage(file="../FlashCardApp/images/card_back.png")
canvas_image = canvas.create_image(400, 263, image="")
canvas.grid(column=0, row=0, columnspan=2)

# whiteCard
white_card_img = tkinter.PhotoImage(file="../FlashCardApp/images/card_front.png")

card_title = canvas.create_text(400, 150, text="", font=TITLE)
word_title = canvas.create_text(400, 263, text="trouve", font=WORD)

cross_image = tkinter.PhotoImage(file="../FlashCardApp/images/wrong.png")
cross_button = tkinter.Button(image=cross_image, highlightthickness=0, command=cross)
cross_button.grid(row=1, column=0)

right_image = tkinter.PhotoImage(file="../FlashCardApp/images/right.png")
right_button = tkinter.Button(image=right_image, highlightthickness=0, command=right)
right_button.grid(row=1, column=1)

game_on = True
# while game_on:
french()

window.mainloop()
