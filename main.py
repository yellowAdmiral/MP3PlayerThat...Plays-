from tkinter import *
import os
import time
import pygame
from tkinter import filedialog
from mutagen.mp3 import MP3
import tkinter.ttk as ttk


root = Tk()
root.title('MP3 Player by Pranup')
root.iconbitmap('D:/python projects/MusicPlayer/img/icon.ico')
root.geometry("500x450")

#A List of all the songs in the player , it stores the entire address of a given song
global songlist
songlist = list()

#a global variable to know if the player is stopped
global stopped 
stopped = False
#initialize pygame mixer
pygame.mixer.init()

#create player control button images
prev_btn_img = PhotoImage(file='img/prev80.png')
next_btn_img = PhotoImage(file='img/next80.png')
play_btn_img = PhotoImage(file='img/play80.png')
pause_btn_img = PhotoImage(file='img/pause80.png')
stop_btn_img =  PhotoImage(file='img/stop80.png')
remove_btn_img = PhotoImage(file= 'img/removesong80.png')

#A variable to know if its the first instance 
global first
first = 1
#A global variable to know which song is playing 
global playingnow
playingnow = ''
#A global variable to know what the index of the current song is in the songlist
global playingnowindex
playingnowindex = 0
global textvar
textvar = StringVar()
#FUNCTIONS 

#Get Song length info
def play_time():
    global textvar
    global playingnow
    textvar.set(f'Now Playing - {playingnow}')
    #To keep only one loop running
    if stopped :
        return
    #Get time in seconds
    current_time = pygame.mixer.music.get_pos()/1000
    global paused
    #Throw temp label to get data
    #slider_label.config(text=f'Slider : {int(my_slider.get())} and Song pos : {int(current_time)} ')
    #Time in format Min:Sec
    converted_time = time.strftime('%M:%S', time.gmtime(current_time))
    #Get current playing song
    # cur_song = song_box.curselection()
    #Getting the next song 
    song = playingnow
    #Playing the song
    song = songlist[playingnowindex]
    #Load song with mutagen
    song_mut = MP3(song)
    #Get song length
    global song_length
    song_length = song_mut.info.length

    #Converting length format
    converted_length = time.strftime('%M:%S', time.gmtime(song_length))
    #Incrementing the current time 
    current_time += 1
    if int(my_slider.get()) == int(song_length) :
        status_bar.config(text=f'Time Elapsed : {converted_length}   ')
        next_song()
    elif paused :
        pass
    elif int(my_slider.get()) == int(current_time) :
        #Slider hasnt moved
        #updating the slider
        slider_position = int(song_length)
        my_slider.config(to=slider_position, value=int(current_time))
    else :
        #Slider has moved
        #updating the slider
        slider_position = int(song_length)
        my_slider.config(to=slider_position, value=int(my_slider.get()))
        converted_time = time.strftime('%M:%S', time.gmtime(int(my_slider.get())))
        #Print the time
        status_bar.config(text=f'Time Elapsed : {converted_time} of {converted_length}   ')
        next_time = int(my_slider.get())+1
        my_slider.config(value=next_time)
    #Print the time
    # status_bar.config(text=f'Time Elapsed : {converted_time} of {converted_length}   ')
    #Updating the slider position
    # my_slider.config(value=int(current_time))
    status_bar.after(1000,play_time)




#Addsong function
def add_song() :
    global songlist
    song = filedialog.askopenfilename(initialdir='audio/' , title='choose a song', filetypes=(("mp3 Files","*.mp3"), ))
    songlist.append(song)
    #Stripping the directory and .mp3 from the song name
    songnamewitext = os.path.basename(song)
    songname= os.path.splitext(songnamewitext)
    #add song to list box
    songlist.append(song)
    song_box.insert(END,songname[0])
    pass


#Add playlist function 
def add_playlist():
    playlist = f'{filedialog.askdirectory()}/'
    scandirectory(playlist)

#Scan a directory
path = 'D:/python projects/MusicPlayer/audio/'
def scandirectory(path) :
    global songlist
    for root, directories , file in os.walk(path) :
        for file in file:
            if(file.endswith('.mp3')) :
                temp = f'{path}{file}'
                songlist.append(temp)
                file = file.replace(".mp3","")
                song_box.insert(END,file)
#Play selected song
def play() :
    global first
    global stopped
    global playingnow
    global playingnowindex
    stopped = False
    if first == 1:
        first = 0
        index = song_box.curselection()
        song = songlist[index[0]]
        playingnow = song_box.get(index[0])
        playingnowindex = index[0]
        # song = f'D:/python projects/MusicPlayer/audio/{song}.mp3'
        play_btn.configure(image=pause_btn_img)
        pygame.mixer.music.load(song)
        pygame.mixer.music.play(loops=0)
    else :
        #pause the song
        global paused
        if paused :
            #unpause
            pygame.mixer.music.unpause()   
            paused = False 
            play_btn.configure(image=pause_btn_img)
            #pause
        elif paused != True :
            pygame.mixer.music.pause()
            paused = True
            play_btn.configure(image=play_btn_img)
    #Caalling the playtime 
    play_time()

    #updating the slider
    # slider_position = int(song_length)
    # my_slider.config(to=slider_position, value=0)
def playbyclick(x) :
    stop(1)
    play()
#Slider Function
def slide(x) :
    #slider_label.config(text= f'{int(my_slider.get())} of {int(song_length)}')
    global songlist
    index = song_box.curselection()
    song = songlist[index[0]]
    play_btn.configure(image=pause_btn_img)
    pygame.mixer.music.load(song)
    pygame.mixer.music.play(loops=0, start = int(my_slider.get()))

#Function for volume
def volume(x) :
    value = 1 - volume_slider.get()
    pygame.mixer.music.set_volume(value)


#stop the song that is playing
def stop(remove=0) :
    global first
    first = 1
    global playingnow
    playingnow = ''
    status_bar.config(text= '')
    my_slider.config(value=0)
    pygame.mixer.music.stop()
    play_btn.configure(image=play_btn_img)
    if remove == 0 :
        song_box.selection_clear(ACTIVE)
    else :
        pass
    #Clear the status bar
    status_bar.config(text= '')

    #Set stop variable to true
    global stopped
    stopped = True

#Play the next song in the playlist
def next_song() : 
    #Getting the current song index
    global paused
    global playingnow
    global songlist
    global playingnowindex
    next_one = song_box.curselection()
    status_bar.config(text= '')
    my_slider.config(value=0)
    if next_one[0] < song_box.size() -1 :
        #adding one tot the current index
        next_one = next_one[0] + 1
        #Getting the next song 
        song = songlist[next_one]
        playingnow = song_box.get(next_one)
        playingnowindex = next_one
        #Playing the song
        play_btn.configure(image=pause_btn_img)
        pygame.mixer.music.load(song)
        pygame.mixer.music.play(loops=0)
        #Clear Active bar in the listbox
        song_box.selection_clear(0,END)
        #setting pause
        paused = False
        #Activate new song bar
        song_box.activate(next_one)
        song_box.select_set(next_one,last = None)
    else :
        #adding one tot the current index
        next_one = 0
        #Getting the next song 
        song = song_box.get(next_one)
        playingnow = song_box.get(next_one)
        #Playing the song   
        song = f'D:/python projects/MusicPlayer/audio/{song}.mp3'   
        play_btn.configure(image=pause_btn_img)   
        pygame.mixer.music.load(song)   
        pygame.mixer.music.play(loops=0)
        #Clear Active bar in the listbox
        song_box.selection_clear(0,END)
        #setting pause
        paused = False
        #Activate new song bar
        song_box.activate(next_one)
        song_box.select_set(next_one,last = None)

#Play previous song
def previous_song() :
    #Getting the current song index
    global paused
    global playingnow
    global playingnowindex
    next_one = song_box.curselection()
    status_bar.config(text= '')
    my_slider.config(value=0)
    #adding one to the current index
    if next_one[0] != 0:
        next_one = next_one[0] - 1
        #Getting the next song 
        song = songlist[next_one]
        playingnow = song_box.get(next_one)
        playingnowindex = next_one
        #Playing the song
        play_btn.configure(image=pause_btn_img)
        pygame.mixer.music.load(song)
        pygame.mixer.music.play(loops=0)
        #Clear Active bar in the listbox
        song_box.selection_clear(0,END)
        #setting pause
        paused = False
        #Activate new song bar
        song_box.activate(next_one)
        song_box.select_set(next_one,last = None)
    else :
        next_one = song_box.size()-1
        #Getting the next song 
        song = songlist[next_one]
        playingnow = song_box.get(next_one)
        playingnowindex = next_one
        #Playing the song
        play_btn.configure(image=pause_btn_img)
        pygame.mixer.music.load(song)
        pygame.mixer.music.play(loops=0)
        #Clear Active bar in the listbox
        song_box.selection_clear(0,END)
        #setting pause
        paused = False
        #Activate new song bar
        song_box.activate(next_one)
        song_box.select_set(next_one,last = None)

#Delete song from playlist 
def remove() :
    global playingnow
    global playingnowindex
    global songlist
    selection = song_box.curselection()
    if playingnow == song_box.get(ACTIVE) :
        song_box.delete(ANCHOR)
        print("removed",songlist[selection[0]])
        del songlist[selection[0]]
        stop()
    else :
        song_box.delete(ANCHOR)
        print("removed",songlist[selection[0]])
        del songlist[selection[0]]
def removeall():
    global songlist
    song_box.delete(0,END)
    songlist.clear()
    stop()
    pass
#Create global pause variable
global paused 
paused = False

#create a new frame 
master_frame = Frame(root)
master_frame.pack(pady=20)

#Create a frame for volume
volume_frame = LabelFrame(master_frame , text='Volume')
volume_frame.grid(row=0,column=1)
#create playlist box
song_box = Listbox(master_frame, bg="black" , fg = "lightgreen" ,width="60", selectbackground="gray" , selectforeground="black")
song_box.grid(row=0,column=0)

#Scan the directory to fill it with songs
scandirectory(path)

#create player control frames
controls_frame = Frame(master_frame)
controls_frame.grid(row=1, column=0, pady=20)

#player control buttons
prev_btn = Button(controls_frame, image = prev_btn_img, borderwidth= 0, padx= 5, command = previous_song)
next_btn = Button(controls_frame, image = next_btn_img, borderwidth= 0, padx= 5 , command=next_song)
play_btn = Button(controls_frame, image = play_btn_img, borderwidth= 0, padx= 5, command= play)
remove_btn = Button(controls_frame, image = remove_btn_img, borderwidth= 0, padx= 5, command = remove)
stop_btn = Button(controls_frame, image = stop_btn_img, borderwidth= 0, padx = 5 , command = stop)
NowPlaying = Label(root,textvariable=textvar,pady=10)
#Layout of the buttons 
prev_btn.grid(row=1, column=0)
next_btn.grid(row=1, column=4)
play_btn.grid(row=1, column=2)
remove_btn.grid(row=1, column=1)
stop_btn.grid(row=1, column=3)
NowPlaying.pack()
#create menu
my_menu= Menu(root)
root.config(menu=my_menu)

#add  song menu
add_song_menu = Menu(my_menu)
my_menu.add_cascade(label="Add Songs", menu=add_song_menu)
add_song_menu.add_command(label="Add New song", command = add_song)
add_song_menu.add_command(label="Add a new playlist", command = add_playlist)
remove_all = Menu(my_menu)
my_menu.add_cascade(label="Remove All Songs",menu=remove_all)
remove_all.add_command(label="Remove all songs", command = removeall)

#create a status bar
status_bar = Label(root, text='', bd=1, relief=GROOVE , anchor = E)
status_bar.pack(fill = X,side=BOTTOM , ipady=2)

#Create a slider for song duration
my_slider = ttk.Scale(master_frame, from_=0 , to = 100, orient=HORIZONTAL, value=0, command = slide ,length=360)
my_slider.grid(row=2 ,column=0, pady=10)

#Create slider for volume
volume_slider = ttk.Scale(volume_frame, from_=0 , to = 1, orient=VERTICAL, value=0.3, command = volume ,length=125)
volume_slider.pack()


#Create slider label
# slider_label = Label(root, text = '0')
# slider_label.pack(pady=10)


song_box.bind('<Double-1>', playbyclick)
root.mainloop()