#modules
import pygame as pg
import tkinter as tk
import tkinter.messagebox
from tkinter import filedialog
import tkinter.ttk as ttk
import os
import shutil as sh
import time
from mutagen.mp3 import MP3

paused = False
mute = False
sound = 0

def about_us():
	tkinter.messagebox.showinfo("About us","This is created by Surya Rakshit as a part of project")

def add_song():
	song =""
	song = tk.filedialog.askopenfilename(title="Choose a music file")
	if song != "":
		sh.copy(song,"E:/python/Projects/Audio Player/Songs")
		songmain = os.path.basename(song)
		playlist.insert(tk.END,songmain)

def delete_song():
	pass
def total_time():
	current_song = playlist.curselection()
	song = playlist.get(current_song)
	song = f'E:/python/Projects/Audio Player/Songs/{song}'

	song_mut = MP3(song)
	global song_length
	song_length = song_mut.info.length
	total_time = time.strftime('%M:%S',time.gmtime(song_length))
	TimeLabel["text"] = "Play Time : "+ total_time
	TotalTimeLabel["text"] = total_time
	

def play_time():
	current_time = pg.mixer.music.get_pos()//1000

	conv_time = time.strftime('%M:%S',time.gmtime(current_time))

	TimeElapsedLabel['text']=conv_time
	TimeElapsedLabel.after(1000,play_time)
	mover.config(value = current_time)

def play_music():
	global paused
	if paused==False:
			song = playlist.get(tk.ACTIVE)
			song= f"E:/python/Projects/Audio Player/Songs/{song}"
			pg.mixer.music.load(song)
			pg.mixer.music.play()
			status_bar['text']="Music is playing : "
			MusicLabel['text']="NOW PLAYING:"+ os.path.basename(song)
	else:
		pg.mixer.music.unpause()
		paused = False
		status_bar['text']="Music resumes"

	play_time()
	total_time()

	#updating Slider
	mover.config(to = int(song_length), value = 0 )

def stop_music():
	global paused
	pg.mixer.music.stop()
	paused = False
	status_bar['text']="Music stopped"
	MusicLabel['text']="NO MUSIC IS PLAYING: -------------------------------"
	TimeElapsedLabel['text']="--:--"
	TotalTimeLabel['text']="--:--"
	


def pause_music():
	global paused
	paused=True
	pg.mixer.music.pause()
	status_bar['text']="Music Paused"

def set_vol(val):
	global sound
	if(int(val)==0):
		pass
	else:
		sound=int(val)
	volume=int(val)/100
	pg.mixer.music.set_volume(volume)

def muteaudio():
	global mute
	if mute:
		pg.mixer.music.set_volume(sound/100)
		volume_control.set(sound)
		mute = False
		muteBtn['image']=mutephoto
		status_bar['text']="Unmuted"
	else:
		pg.mixer.music.set_volume(0)
		volume_control.set(0)
		mute = True
		muteBtn['image']=unmutephoto
		status_bar['text']="Muted"

#intializing mixer
pg.mixer.init()


#window
window = tk.Tk()
window.title("Audio Player")
window.geometry("800x500")
window.iconbitmap('icons.ico')

#Menu Bar and Cascade menus
menubar = tk.Menu(window)
window.config(menu=menubar)

submenu1 = tk.Menu(menubar,tearoff = 0)
menubar.add_cascade(label = "file", menu=submenu1)
submenu1.add_command(label = "Add Song to playlist", command = add_song)
submenu1.add_command(label = "Exit", command = window.destroy)

submenu2 = tk.Menu(menubar, tearoff = 0)
menubar.add_cascade(label = "Help", menu=submenu2)
submenu2.add_command(label = "About Us",command=about_us)


#pics for play icon
playps = tk.PhotoImage(file = r"play.png")
playphoto = playps.subsample(8,8)

#pics for stop icon
stopps = tk.PhotoImage(file=r"stop.png")
stopphoto = stopps.subsample(18,18)

#pics for pause icon
pauseps = tk.PhotoImage(file = r"pause.png")
pausephoto = pauseps.subsample(2,2)

#pics for mute button
muteps = tk.PhotoImage(file =r"mute.png")
mutephoto = muteps.subsample(30,30)

#pics for unmute Button
unmuteps = tk.PhotoImage(file =r"unmute.png")
unmutephoto = unmuteps.subsample(30,30)

#Buttons
playBtn = tk.Button(window,image=playphoto, command = play_music, borderwidth=0)
stopBtn = tk.Button(window,image=stopphoto, command = stop_music, borderwidth=0)
pauseBtn = tk.Button(window,image=pausephoto, command = pause_music, borderwidth=0)
muteBtn = tk.Button(window,image=mutephoto, command = muteaudio)

#lABELS
StartLabel = tk.Label(window,text = "MY MUSIC...MY RULES",font=('Arial Bold',10))
MusicLabel = tk.Label(window,text = "NO MUSIC IS PLAYING: -------------------------------",font=('Arial Bold',10))
TimeLabel = tk.Label(window,text = "Play Time --:--",font=('Arial Bold',10))
MyMusicLabel = tk.Label(window,text = "My Playlist",font=('Arial Bold',10))
TimeElapsedLabel = tk.Label(window,text = "--:--",font=('Arial Bold',10))
TotalTimeLabel = tk.Label(window,text = "--:--",font=('Arial Bold',10))

#Volume
volume_control = tk.Scale(window,from_=0,to=100,orient = tk.HORIZONTAL, command=set_vol)
volume_control.set(60)
pg.mixer.music.set_volume(0.6)

#Music Growing
mover = ttk.Scale(window, from_ = 0, to=200,orient= tk.HORIZONTAL, length =350)


#Status Bar making
status_bar = tk.Label(window,text="My audio Player...",bd = 2, relief = tk.SUNKEN, anchor = tk.W)

#Music Playlist
playlist = tk.Listbox(window,bg="Black",fg= "Green", width = 45, height =23, selectbackground="Gray",selectforeground = "White")
onlyfiles = [f for f in os.listdir("E:/python/Projects/Audio Player/Songs")]
for i in onlyfiles:
	songmain = os.path.basename(i)
	playlist.insert(tk.END,songmain)	



#Aligning
mover.place(x=77,y=260)
StartLabel.place(x=180,y=30)
MusicLabel.place(x=130, y= 70)
TimeLabel.place(x=200, y = 220)
playBtn.place(x=225,y=330)
stopBtn.place(x=75,y=330)
pauseBtn.place(x=375,y=330)
muteBtn.place(x=330,y=400)
volume_control.place(x=360,y=385)
playlist.place(x=490, y= 40)
MyMusicLabel.place(x=590,y=20)
TimeElapsedLabel.place(x=30,y=260)
TotalTimeLabel.place(x=450,y=260)
status_bar.pack(side = tk.BOTTOM, fill=tk.X)


window.mainloop()