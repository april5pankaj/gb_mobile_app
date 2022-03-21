import tkinter as tk
from tkinter import *
from PIL import Image, ImageTk
import tkinter.ttk as ttk
from datetime import datetime
from datetime import date
import os
import gc
import time
import json
import yaml
import yamlordereddictloader
from PIL import Image, ImageGrab
today = date.today()


def winscreen():
    global today

    with open("new_match_yaml_dump.yaml") as f:
        match_yaml = yaml.load(f, Loader=yamlordereddictloader.Loader)

    topws = tk.Tk()
    topws.title('Winner')
    imagew1 = Image.open('backgroundblur.jpg')
    tkw1_image = ImageTk.PhotoImage(imagew1)

    labelw1 = tk.Label(topws, image=tkw1_image)
    labelw1.pack()

    winner = tk.Label(topws)
    winner.place(relx=0.0, rely=0.04, height=100, width=1366)
    winner.configure(font="-family {Segoe UI Black} -size 54 -weight bold")
    winner.configure(background="black")
    winner.configure(foreground="gold")
    winner.configure(text='''Winner''')

    img = tk.PhotoImage(file="gullyball.png")
    logo = tk.Label(topws)
    logo.place(relx=0.05, rely=0.04, height=100, width=100)
    logo.configure(font="-family {Segoe UI Black} -size 24 -weight bold")
    logo.configure(background="black")
    logo.config(image=img)

    date = tk.Label(topws)
    date.place(relx=0.80, rely=0.125, height=30, width=300)
    date.configure(font="-family {Segoe UI Black} -size 12 -weight bold")
    date.configure(background="black")
    date.configure(foreground="white")
    d2 = today.strftime("%B %d, %Y")
    date.configure(text=str(d2))

    img1 = tk.PhotoImage(file="win1.png")
    trophy = tk.Label(topws)
    trophy.place(relx=0.16, rely=0.25, height=333, width=300)
    trophy.configure(font="-family {Segoe UI Black} -size 44 -weight bold")
    trophy.configure(background="pale turquoise")
    trophy.config(image=img1)

    team_member1 = tk.Label(topws)
    team_member1.place(relx=0.42, rely=0.25, height=75, width=560)
    team_member1.configure(font="-family {Segoe UI Black} -size 36 -weight bold")
    team_member1.configure(background="black")
    team_member1.configure(foreground="gold")
    wtm1 = 0
    if match_yaml['info']['outcome']['winner_team_id'] == 1:
        wtm1 = (match_yaml['info']['teams']['team1']['player1']['player_name']).upper()
    else:
        wtm1 = (match_yaml['info']['teams']['team2']['player1']['player_name']).upper()
    team_member1.configure(text=' ' + str(wtm1)[0:16])
    team_member1.configure(anchor='w')

    team_member2 = tk.Label(topws)
    team_member2.place(relx=0.42, rely=0.42, height=75, width=560)
    team_member2.configure(font="-family {Segoe UI Black} -size 36 -weight bold")
    team_member2.configure(background="black")
    team_member2.configure(foreground="gold")
    wtm2 = 0
    if match_yaml['info']['outcome']['winner_team_id'] == 1:
        wtm2 = (match_yaml['info']['teams']['team1']['player2']['player_name']).upper()
    else:
        wtm2 = (match_yaml['info']['teams']['team2']['player2']['player_name']).upper()
    team_member2.configure(text=' ' + str(wtm2)[0:16])
    team_member2.configure(anchor='w')

    team_member3 = tk.Label(topws)
    team_member3.place(relx=0.42, rely=0.59, height=75, width=560)
    team_member3.configure(font="-family {Segoe UI Black} -size 36 -weight bold")
    team_member3.configure(background="black")
    team_member3.configure(foreground="gold")
    wtm3 = 0
    if match_yaml['info']['outcome']['winner_team_id'] == 1:
        wtm3 = (match_yaml['info']['teams']['team1']['player3']['player_name']).upper()
    else:
        wtm3 = (match_yaml['info']['teams']['team2']['player3']['player_name']).upper()
    team_member3.configure(text=' ' + str(wtm3)[0:16])
    team_member3.configure(anchor='w')

    congrats = tk.Label(topws)
    congrats.place(relx=0.0, rely=0.83, height=50, width=1366)
    congrats.configure(font="-family {Segoe UI Black} -size 24 -weight bold")
    congrats.configure(background="black")
    congrats.configure(foreground="gold")
    congrats.configure(text='''Congratulations to the Winners..........''')

    topws.after(15000, topws.destroy)

    topws.mainloop()

winscreen()