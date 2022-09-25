import subprocess
from typing import Text
import pyttsx3
import operator
import speech_recognition as sr
import datetime
import wikipedia
import webbrowser
import os
import winshell
import pyjokes
import ctypes
import time
import smtplib, ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import getpass
import requests
from bs4 import BeautifulSoup
import bs4 as bs
from nltk.corpus import stopwords

engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)

assname = "Olivia"
count = 0

def speak(audio):
    engine.say(audio)
    engine.runAndWait()

def wishMe():
    hour = int(datetime.datetime.now().hour)
    if hour>= 0 and hour<12:
        print("Good Morning!")
        speak("Good Morning!")

    elif hour>= 12 and hour<18:
        print("Good Afternoon!")
        speak("Good Afternoon!")
  
    else:
        print("Good Evening!")
        speak("Good Evening!")

clear = lambda: os.system('cls')
clear()

def intro():
    print("I am your Assistant, " + assname)
    speak("I am your Assistant, " + assname)

def takeCommand():

    r = sr.Recognizer()
    r.pause_threshold
    with sr.Microphone() as source:
        r.adjust_for_ambient_noise(source, duration = 0.25)
        print("Listening...")
        audio = r.listen(source)

    try:
        print("Recognizing...")
        query = r.recognize_google(audio, language ='en')
        print(f"User said: {query}\n")

    except Exception as e:
        print(str(e))
        print("Unable to Recognize your voice.") 
        return "voice error"
    query = query.lower()
    return query

def getNote():
    print("What should i write?")
    speak("What should i write?")
    note = takeCommand()
    file = open(f'{assname}.txt', 'a')
    strTime = datetime.datetime.now().strftime("%Y/%m/%d\n%H:%M:%S")
    file.write(strTime)
    file.write(" :- ")
    file.write(note+"\n")
    subprocess.Popen(["notepad.exe", f"{assname}.txt"])

def showNote():
    speak("Showing Notes")
    file = open(f"{assname}.txt", "r")
    subprocess.Popen(["notepad.exe", f"{assname}.txt"])

def sendEmail():
    sender_email = input("Enter sender's E-mail: ")
    print("\n")
    password = getpass.getpass("Type sender's password and press enter")
    print("\n")
    receiver_email = input("Enter receiver's E-mail: ")
    print("\n")

    message = MIMEMultipart("alternative")
    message["Subject"] = input("Enter Subject of the E-mail: ")
    message["From"] = sender_email
    message["To"] = receiver_email
    text = input("Enter the E-mail to send:\n")
    part = MIMEText(text, "plain")
    message.attach(part)
    context = ssl.create_default_context()
    with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
        server.login(sender_email, password)
        server.sendmail(sender_email, receiver_email, message.as_string())

def corona_updates(query):
    url = 'https://www.worldometers.info/coronavirus/'
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'lxml')
    totalcases = soup.findAll('div', attrs =  {'class': 'maincounter-number'})
    total_cases = []
    for total in totalcases:
        total_cases.append(total.find('span').text)
    world_total = 'Total Coronavirus Cases: ' + total_cases[0]
    world_deaths = 'Total Deaths: ' + total_cases[1]
    world_recovered = 'Total Recovered: ' + total_cases[2]
    
    info = 'For more information visit: ' + 'https://www.worldometers.info/coronavirus/#countries'
    if 'world' in query:
        print('World Updates: ')
        print(world_total)
        print(world_deaths)
        print(world_recovered)
        print(info)
        speak('World Updates: ')
        speak(world_total)
        speak(world_deaths)
        speak(world_recovered)
    else:
        country = query
        url = 'https://www.worldometers.info/coronavirus/country/' + country.lower() + '/'
        page = requests.get(url)
        soup = BeautifulSoup(page.content, 'lxml')
        totalcases = soup.findAll('div', attrs =  {'class': 'maincounter-number'})
        total_cases = []
        for total in totalcases:
            total_cases.append(total.find('span').text)
        total = 'Total Coronavirus Cases: ' + total_cases[0]
        deaths = 'Total Deaths: ' + total_cases[1]
        recovered = 'Total Recovered: ' + total_cases[2]
        info = 'For more information visit: ' + url
        updates = country.capitalize() + ' Updates: '
        print(updates)
        print(total)
        print(deaths)
        print(recovered)
        print(info)
        speak(updates)
        speak(total)
        speak(deaths)
        speak(recovered)

def scrape_news():
    url = 'https://news.google.com/topstories?hl=en-IN&gl=IN&ceid=IN:en '
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')
    news = soup.findAll('h3', attrs = {'class':'ipQwMb ekueJc RD0gLb'})
    c=0
    for n in news:
        c = c+1
        print(f"{c}-->",n.text)
        speak(n.text)
    print('For more information visit: news.google.com')
    speak('For more information visit: news.google.com')

def get_operator_fn(op):
    return {
        '+' : operator.add,
        '-' : operator.sub,
        'x' : operator.mul,
        'divided' :operator.__truediv__,
        'Mod' : operator.mod,
        'mod' : operator.mod,
        '**' : operator.xor,
        }[op]

def eval_binary_expr(op1, oper, op2):
    op1,op2 = int(op1), int(op2)
    return get_operator_fn(oper)(op1, op2)

if __name__ == '__main__':
    wishMe()
    intro()
    
    print(f"Say \"Hi {assname}\" to use me")
    speak(f"Say \"Hi {assname}\" to use me")
    wake1 = f'hey {assname.lower()}'
    wake2 = f'hi {assname.lower()}'
    wake3 = f'ok {assname.lower()}'
    
    query = takeCommand()
    
    if query.count(wake1) > 0 or query.count(wake2) > 0 or query.count(wake3) > 0 :
        print(f"{assname} at your service.")
        speak(f"{assname} at your service.")
        print("How may I help you?")
        speak("How may I help you?")
    
    while True:

        query = takeCommand()

        if "don't listen" in query or "stop listening" in query:
            speak(f"Thank you for using me, say \"Hi {assname}\" to wake me up")
            while True:
                query = takeCommand()
                if query.count(wake1) > 0 or query.count(wake2) > 0 or query.count(wake3) > 0 :
                    print(f"{assname} at your service.")
                    speak(f"{assname} at your service.")
                    print("How may I help you?")
                    speak("How may I help you?")
                    break

        elif 'wikipedia' in query:
            speak('Searching Wikipedia...')
            query = query.replace("wikipedia", "")
            results = wikipedia.summary(query, sentences = 3)
            speak("According to Wikipedia")
            print(results)
            speak(results)

        elif 'youtube' in query:
            print("Here you go to Youtube\n")
            speak("Here you go to Youtube\n")
            webbrowser.open("https://www.youtube.com/")
        
        elif 'chrome' in query:
            print("Here you go to Google Chrome\n")
            speak("Here you go to Google Chrome\n")
            os.system("chrome")
        
        elif 'google' in query :
            print("Here you go to Google\n")
            speak("Here you go to Google\n")
            webbrowser.open("https://www.google.com/")
        
        elif "time" in query or "what is the time" in query or "tell me the time" in query:
            strTime = datetime.datetime.now().strftime("%H:%M:%S")
            print(f"The time is {strTime}")
            speak(f"The time is {strTime}")
        
        elif 'mozilla' in query or 'firefox' in query:
            print("Here you go to Mozilla Firefox\n")
            speak("Here you go to Mozilla Firefox\n")
            os.system("firefox")
        
        elif 'dev' in query or 'dev cpp' in query or 'dev c plus plus' in query:
            print("Here you go to Dev C++\n")
            speak("Here you go to Dev C plus plus\n")
            os.system("devcpp")
        
        elif 'edge' in query or 'internet explorer' in query:
            print("Here you go to Microsoft Edge\n")
            speak("Here you go to Microsoft Edge\n")
            os.system("msedge")
        
        elif 'vlc' in query:
            print("Here you go to VLC Media Player\n")
            speak("Here you go to VLC Media Player\n")
            os.system("vlc")
        
        elif 'zoom' in query:
            print("Here you go to ZOOM Cloud Meetings\n")
            speak("Here you go to ZOOM Cloud Meetings\n")
            os.system("zoom")
        
        elif 'atom' in query:
            print("Here you go to Atom Text editor\n")
            speak("Here you go to Atom Text editor\n")
            os.system("atom")
        
        elif 'vs' in query or 'visual studio' in query:
            print("Here you go to Visual Studio Code\n")
            speak("Here you go to Visual Studio Code\n")
            os.system("Code")
        
        elif "where is" in query:
            query = query.replace("where is", "")
            location = query
            speak("Locating: "+location)
            webbrowser.open("https://www.google.com/maps/search/" + location + "")
        
        elif "weather" in query or "tell me the weather" in query:
            base_url = "https://www.google.com/search?q=weather+"
            speak(" City name ")
            print("City name : ")
            city_name = takeCommand()
            complete_url = base_url +  city_name 
            webbrowser.open(complete_url)
        
        elif 'play' in query:
            query = query.replace("play", "")
            speak("Playing "+query)
            url = "https://www.youtube.com/results?search_query="+query
            webbrowser.open(url)

        elif 'covid' in query or 'covid-19' in query or 'coronavirus' in query or 'corona' in query:
            words = query.split(' ')
            corona_updates(words[-1])
        
        elif 'search' in query or 'define' in query or 'what is' in query or 'what are' in query or 'what do you mean by' in query or 'what is the meaning of' in query or 'what are the meaning of' in query or 'who is' in query:
            query = query.replace("search", "")
            query = query.replace("define", "")
            query = query.replace("what is", "")
            query = query.replace("what are", "")
            query = query.replace("what do you mean by", "")
            query = query.replace("what is the meaning of", "")
            query = query.replace("what are the meaning of", "")
            query = query.replace("who is", "")
            webbrowser.open("https://www.google.com/search?q="+query)
        
        elif "calculate" in query:
            query = query.replace("calculate", "")
            print(eval_binary_expr(*(query.split())))
            speak(eval_binary_expr(*(query.split())))

        elif 'exit' in query or 'thank you close now' in query or 'stop' in query:
            speak("Thanks for giving me your time")
            exit()
        
        elif "send" in query or "send an email" in query or "send email" in query or "email" in query:
            sendEmail()
            print("E-mail sent successfully")
            speak("E-mail sent successfully")
            
        elif 'tell me a joke' in query:
            s = pyjokes.get_joke()
            print(s)
            speak(s)

        elif 'news' in query or 'tell me the news' in query or 'what is the news today' in query:
            scrape_news()

        elif "write a note" in query or "make a note" in query:
            getNote()
            print("Note Saved!")
            speak("Note Saved!")

        elif "show note" in query or "show my notes" in query:
            showNote()

        elif assname.lower() in query:
            wishMe()
            speak(f"{assname} at your service")
            speak("How can I help you?")
        
        elif "morning" in query:
            speak("A warm Good Morning!")
            speak("How are you?")

        elif "afternoon" in query or "after noon" in query:
            speak("Good Afternoon to you too")
            speak("How may I help you?")

        elif "night" in query:
            speak("Good Night!")
            exit()
        
        elif 'change background' in query:
            ctypes.windll.user32.SystemParametersInfoW(20,0,"Location of wallpaper",0)
            speak("Background changed succesfully")

        elif 'lock' in query:
                print("locking the device")
                speak("locking the device")
                ctypes.windll.user32.LockWorkStation()
        
        elif 'shutdown' in query or 'shut down' in query or 'turn off' in query:
                speak("Hold On a Sec ! Your system is on its way to shut down")
                subprocess.call(['shutdown', '/s'])
                
        elif 'empty recycle bin' in query:
            winshell.recycle_bin().empty(confirm = False, show_progress = False, sound = True)
            print("Recycle Bin Emptied")
            speak("Recycle Bin Emptied")
        
        elif "restart" in query:
            subprocess.call(["shutdown", "/r"])
            
        elif "hibernate" in query or "sleep" in query or "hibernation" in query:
            print("Hibernating")
            speak("Hibernating")
            subprocess.call(["shutdown", "/h"])
        
        elif "log off" in query or "sign out" in query or "sign off" in query:
            speak("Make sure all the application are closed before sign-out")
            time.sleep(5)
            subprocess.call(["shutdown", "/l"])
            
        # most asked question from google Assistant

        elif "who are you" in query or "what are you" in query or "tell me about yourself" in query or "features" in query:
            print(f"I am {assname}, your Personal AI Assistant. I can do many things, and I am learning more. ")
            speak(f"I am {assname}, your Personal AI Assistant. I can do many things, and I am learning more. ")
            print("You can ask me to do things like stream music, check the news, hear out python jokes, Browse Web, send e-mails, watch videos in YouTube,\n Shutting down, sleeping mode, logging off and restarting PC, making Notes, Weather Report, know date and time, open zoom meetings,\n use atom text editor, visual studio code,   open VLC media player, track locations, use Simple Calculator, and Empty Recycle Bin.")
            speak("You can ask me to do things like stream music, check the news, hear out python jokes, Browse Web, send e-mails, watch videos in YouTube, Shutting down, sleeping mode, logging off and restarting PC, making Notes, Weather Report, know date and time, open zoom meetings, use atom text editor, visual studio code,   open VLC media player, track locations, use Simple Calculator, and Empty Recycle Bin.")

        elif 'love' in query:
            speak("It is 7th sense that destroy all other senses")

        elif "will you be my gf" in query or "will you be my girlfriend" in query or "will you be my girl friend" in query:
            speak("I'm not sure about, may be you should give me some time")
        
        elif "how are you" in query:
            speak("I'm fine, glad you asked me that")
            speak("How are you?")
        
        elif 'i am fine' in query or "i am good" in query:
            speak("It's good to know that your fine")