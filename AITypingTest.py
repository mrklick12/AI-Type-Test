import tkinter as tk
import time
import random
import openai
import os
from dotenv import load_dotenv

# Loads the API from the .env file
load_dotenv()


# CHATGPT API KEY
openai.api_key = os.getenv("OPENAI_API_KEY")

# CHATGPT AI FUNCTIONS
def chatGPTtest(prompt):
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",  
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": prompt}
        ]
    )
    return response['choices'][0]['message']['content']
def tenRandomWords(cache=[]):

    user_input = "give me a random sentence without ANY puntuation, all lowercase, NO FULL STOPS that contains 10 words ONLY (no extra chat) and nothing else. Do not include any numbers or special characters in the sentence."
    response = chatGPTtest(user_input)
    return response 



# GLOBALS
fontType=("Bahnschrift SemiBold", 16)
wordsToBeTyped = tenRandomWords()
typing_complete = False
start_time = None
timer_running = False
textfile = "highscores10.txt"
extension = " - 10 Words"


def sortHighScores(): # sorts the highscores
    highScoreNumbers = [float(x) for x in highScoreListNumbers()]
    for n in range(len(highScoreNumbers)):
        for i in range(len(highScoreNumbers)-1):
            temp = 0
            if highScoreNumbers[i+1] > highScoreNumbers[i]:
                temp = highScoreNumbers[i]
                highScoreNumbers[i] = highScoreNumbers[i+1]
                highScoreNumbers[i+1] = temp
    return highScoreNumbers

def top5list(): # finds the top 5 scores

    highscores = highScoreListNumbers()
    n = len(highscores)
    for i in range(n):
        for j in range(0, n-i-1):
            if float(highscores[j]) < float(highscores[j+1]):
                temp = highscores[j]
                highscores[j] = highscores[j+1]
                highscores[j+1] = temp
    top5 = highscores[:5]  
    indices = []
    for score in top5:
        for i, x in enumerate(highScoreListNumbers()):
            if float(x) == float(score):
                indices.append(i)
                break
    
    return indices

def highScoreListNumbers(): # returns the highscore values (like the wpms)
    highscores = []
    highscoresTXT = open(textfile, "r")
    while True:
        content=highscoresTXT.readline()
        if not content:
            break
        highScoreNumbers=filter(str.isdecimal,content)
        numberContent="".join(highScoreNumbers)
        result = numberContent[:len(numberContent)-2] + "." + numberContent[len(numberContent)-2:]
        highscores.append(result)
    highscoresTXT.close()
    return highscores

def highScoreListNames():  # returns the highscore names as strings
    highscores = []
    highscoresTXT = open(textfile, "r")
    while True:
        content=highscoresTXT.readline()
        if not content:
            break
        highScoreNumbers=filter(str.isalpha,content)
        nameContent="".join(highScoreNumbers)
        highscores.append(nameContent)
    highscoresTXT.close()
    return highscores

def ifHighScoreReached(): # checks if the player reached the top 5 

    wpm = calculate_wpm()
    for i in range(5):
        if wpm > float(sortHighScores()[i]):
            print(str(wpm) + " : " + str(sortHighScores()[i]))
            highscoreEntry = tk.Entry(root, font=fontType)
            congratsMessage = tk.Label(root, text="Nice! You managed to make the top 5! Enter your name", font=fontType, fg="#1e2870")
            highscoreEntry.grid(column=1, row=13)
            congratsMessage.grid(column=1, row=12)
            def submitName():
                name = highscoreEntry.get()
                highscoresTXT = open(textfile, "a")
                highscoresTXT.write("\n" + name + ": " + str(wpm))
                highscoresTXT.close()
                highscoreEntry.destroy()
                highscoreEntryButton.destroy()
            highscoreEntryButton = tk.Button(root, text="Submit!", font=fontType, fg="#172f4a", command=submitName)
            highscoreEntryButton.grid(column=1, row=14)
            break

def displayHighscores(): # displays highscore leaderboard and includes refresh function of leaderboard
    listOfIndexes = top5list()

    P1 = tk.Label(text=highScoreListNames()[listOfIndexes[0]], fg="#e8b125", font=fontType)
    P2 = tk.Label(text=highScoreListNames()[listOfIndexes[1]], fg="#b5b2aa", font=fontType)
    P3 = tk.Label(text=highScoreListNames()[listOfIndexes[2]], fg="#CE8946", font=fontType)
    P4 = tk.Label(text=highScoreListNames()[listOfIndexes[3]], fg="black", font=fontType)
    P5 = tk.Label(text=highScoreListNames()[listOfIndexes[4]], fg="black", font=fontType)
    WPM1 = tk.Label(text=highScoreListNumbers()[listOfIndexes[0]], fg="#e8b125", font=fontType)
    WPM2 = tk.Label(text=highScoreListNumbers()[listOfIndexes[1]], fg="#b5b2aa", font=fontType)
    WPM3 = tk.Label(text=highScoreListNumbers()[listOfIndexes[2]], fg="#CE8946", font=fontType)
    WPM4 = tk.Label(text=highScoreListNumbers()[listOfIndexes[3]], fg="black", font=fontType)
    WPM5 = tk.Label(text=highScoreListNumbers()[listOfIndexes[4]], fg="black", font=fontType)

    P1.grid(column=1, row=6)
    P2.grid(column=1, row=7)
    P3.grid(column=1, row=8)
    P4.grid(column=1, row=9)
    P5.grid(column=1, row=10)
    WPM1.grid(column=2, row=6)
    WPM2.grid(column=2, row=7)
    WPM3.grid(column=2, row=8)
    WPM4.grid(column=2, row=9)
    WPM5.grid(column=2, row=10)
    def destroyHighscores():
        P1.destroy()
        P2.destroy()
        P3.destroy()
        P4.destroy()
        P5.destroy()
        WPM1.destroy()
        WPM2.destroy()
        WPM3.destroy()
        WPM4.destroy()
        WPM5.destroy()
        refreshButton.destroy()
        displayHighscores()

    refreshButton = tk.Button(text="Refresh", font=fontType, fg="#172f4a", command=destroyHighscores)
    refreshButton.grid(column=1, row=11)

def calculate_wpm(): # calculates the words per minute
    total_chars = len(wordsToBeTyped)  
    total_words = total_chars / 5  
    elapsed_time_minutes = (time.time() - start_time) / 60  
    wpm = total_words / elapsed_time_minutes  
    return round(wpm, 2) 

def otherWordButtons(): # creates buttons for other word length including their function with ChatGPT
    
    def updateMessageBox25():
        userInput25 = "give me a random sentence without ANY puntuation, all lowercase, NO FULL STOPS, that contains 25 words ONLY (no extra chat) and nothing else. Do not include any numbers or special characters in the sentence."
        respond = chatGPTtest(userInput25)
        global wordsToBeTyped
        global textfile
        global extension
        wordsToBeTyped = respond
        textfile = "highscores25.txt"
        extension = " - 25 Words"
    def updateMessageBox10():
        userInput10 = "give me a random sentence without ANY puntuation, all lowercase, NO FULL STOPS, that contains 10 words ONLY (no extra chat) and nothing else. Do not include any numbers or special characters in the sentence."
        respond = chatGPTtest(userInput10)
        global wordsToBeTyped
        global textfile
        global extension
        wordsToBeTyped = respond
        textfile = "highscores10.txt"
        extension = " - 10 Words"


    tenWordButton = tk.Button(text="10 Words", font=fontType, fg="#737d8c", command=updateMessageBox10)
    twentyFiveWordButton = tk.Button(text="25 Words", font=fontType, fg="#737d8c", command=updateMessageBox25)

    tenWordButton.grid(column=2, row=2)
    twentyFiveWordButton.grid(column=3, row=2)


def update_timer(): # updates the timer
    global timer_running, start_time
    if timer_running:
        elapsed_time = time.time() - start_time
        elapsed_time = round(elapsed_time, 1)
        timerLabel.config(text=f"Time: {elapsed_time} seconds")
        root.after(100, update_timer)

def check_typing(): # checks to see if user is typing, also updates the text with GREEN for correct spelling and RED for incorrect spelling
    global typing_complete, start_time, timer_running
    if typing_complete:
        return

    typed = typingBox.get()
    if len(typed) > 0 and start_time is None:
        start_time = time.time()
        timer_running = True
        update_timer()  
    
    messageToType.delete(1.0, tk.END)
    for i in range(len(typed)):
        if i < len(wordsToBeTyped) and typed[i] == wordsToBeTyped[i]:
            messageToType.insert(tk.END, typed[i], 'green')
        else:
            messageToType.insert(tk.END,wordsToBeTyped[i], 'red')
    if len(typed) < len(wordsToBeTyped):
        messageToType.insert(tk.END, wordsToBeTyped[len(typed):], 'black')
    messageToType.tag_config('green', foreground='green')
    messageToType.tag_config('red', foreground='red')


    if typed == wordsToBeTyped:
        end_time = time.time()
        typing_complete = True
        timer_running = False 
        elapsed_time = end_time - start_time
        
        elapsed_time = round(elapsed_time, 1)
        finalTime = tk.Label(text=f"Completed in {elapsed_time} seconds with a WPM of {calculate_wpm()}", fg="blue")
        displayHighscores()
        ifHighScoreReached()
        finalTime.grid(column=1, row=4)

        highscoresLabel = tk.Label(text="Highscores" + extension, fg="blue", font=(fontType,28, "bold"))
        highscoresLabel.grid(column=1, row=5)

    else:
        root.after(10, check_typing)

# END OF FUNCTIONS





# Tkinter Window Creation
root = tk.Tk()
root.title("Typing Game")
root.iconbitmap("keyboard.ico")



typingBox = tk.Entry(width=100, font=("Bahnschrift SemiBold", 14))
messageToType = tk.Text(root, height=3, wrap="word", width=len(wordsToBeTyped)-3, font=("Bahnschrift SemiBold", 14))
timerLabel = tk.Label(root, text="Time: 0 seconds", fg="red",font=("Bahnschrift SemiBold", 10))

typingBox.grid(column=1, row=2)
messageToType.grid(column=1, row=0, sticky="nsew")
timerLabel.grid(column=1, row=3)
    
otherWordButtons()
check_typing()




root.mainloop()
