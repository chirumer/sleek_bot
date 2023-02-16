#!/usr/bin/env python
# coding: utf-8

# In[1]:


from googletrans import Translator
translator = Translator()
import requests
import googlesearch_py
from youtube_search import YoutubeSearch

API_URL = "https://api-inference.huggingface.co/models/sshleifer/distilbart-cnn-12-6"
headers = {"Authorization": "Bearer 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"}

API_URL_CHAT = "https://api-inference.huggingface.co/models/microsoft/DialoGPT-medium"
headers_CHAT = {"Authorization": "Bearer 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"}

def converse_val(payload):
    response = requests.post(API_URL_CHAT, headers=headers_CHAT, json=payload)
    return response.json()

def query(payload):
    response = requests.post(API_URL, headers=headers, json=payload)
    return response.json()

input_text = ""
def chat(input_text):
    translator = Translator()
    inp = translator.translate(input_text, dest = "en").text
    if(inp[:14]=="summarize this"):
        output = query(inp[14:])
        output = "here is your summary :" + output[0]['summary_text']
    #print(inp)
    elif(inp.startswith("links for")):
        inp = inp[len('links for'):]
        s=''
        results = googlesearch_py.search(inp)
        for i in results[:5]:
            s+=i['url']+'\n'
        output = s
    elif(inp.startswith("videos for")):
        inp = inp[len("videos for"):]
        results = YoutubeSearch(inp, max_results=5).to_dict()
        results = ['https://youtube.com' + url['url_suffix'] for url in results]
        output = '\n'.join(results)
    else:
        #output = converse(Conversation(inp))
        output = converse_val(inp)
        print(output)
        output = output['conversation']['generated_responses'][0]
        print(output)
    return output


# In[12]:


from tkinter import *
 
# GUI
root = Tk()
root.title("Chatbot")
 
BG_GRAY = "#ABB2B9"
BG_COLOR = "#17202A"
TEXT_COLOR = "#EAECEE"
 
FONT = "Helvetica 14"
FONT_BOLD = "Helvetica 13 bold"
 
# Send function
def send():
    converse_chat = e.get()
    send = "You -> " + converse_chat
    txt.insert(END, "\n" + send)
    chatbot_chat = chat(converse_chat)
    txt.insert(END, "\n" + "Bot -> " + chatbot_chat)
 
    user = e.get().lower()
 
 
lable1 = Label(root, bg=BG_COLOR, fg=TEXT_COLOR, text="Noibot", font=FONT_BOLD, pady=10, width=20, height=1).grid(
    row=0)
 
txt = Text(root, bg=BG_COLOR, fg=TEXT_COLOR, font=FONT, width=60)
txt.grid(row=1, column=0, columnspan=2)
 
scrollbar = Scrollbar(txt)
scrollbar.place(relheight=1, relx=0.974)
 
e = Entry(root, bg="#2C3E50", fg=TEXT_COLOR, font=FONT, width=55)
e.grid(row=2, column=0)
 
send = Button(root, text="Send", font=FONT_BOLD, bg=BG_GRAY,
              command=send).grid(row=2, column=1)
 
root.mainloop()


# In[ ]:




