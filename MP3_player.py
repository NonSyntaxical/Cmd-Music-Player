import os
import json
import random
import subprocess
from difflib import SequenceMatcher
import time

cur_dir = os.getcwd()

mp3_player_path = None

#List's
mp3_songs = {}
mp3_json = {"Path": f"{mp3_player_path}"}

def compare_contrast():
    global mvp
    song_keys = []
    the_specific_song_in_question = input("\nType the song name (Please be somewhat accurate to what you named the mp3)\ninput?: ")

    songs = mp3_songs.keys()

    mvp = None
    overall_points = 0.0

    for song in songs:
        song_key_usable = song

        song_keys.append(song_key_usable)
                
        #transition
        song_path = mp3_songs.get(f"{song}")

        print(f"\nDEBUG:{song}, {song_path}, {song_keys}\n")

        Compa = SequenceMatcher(None, the_specific_song_in_question, song).ratio()
                    
        if Compa > overall_points:
            overall_points = Compa
            mvp = song_path
                    
        else:
            pass

def save_mp3path(extract):
    global mp3_player_path

    file = f"{cur_dir}\\MP3_Path_Save.json"

    try:
        with open(file=file, mode="w") as file:
            print(f"\nDEBUG: {extract} \n")
            if extract == None:
                json.dump(mp3_json, file)

            else:
                mp3_json.update({"Path": f"{extract}"})
                json.dump(mp3_json, file)

    except:
        print("Saving the file has failed.")

def load_mp3path():
    global info_extract, mp3_json, mp3_player_path
    
    file_to_load = f"{cur_dir}\\MP3_Path_Save.json"

    try:
        with open(file=file_to_load, mode="r") as file:
            load_save = json.load(file)
            info_extract = load_save.get("Path")
            mp3_player_path = info_extract

            if info_extract in (None, "None", "null"):
                mp3_player_path = input("Whats the path to your mp3 folder? (Give a exact Path): ")
                print(f"\nDEBUG: {mp3_player_path} \n")
                mp3_json.update({"Path": f"{mp3_player_path}"})

                save_mp3path(mp3_player_path)
            
            else:
                print(f"Your MP3 Path: {info_extract}\n")

    except FileNotFoundError:
        print("Save File Not Found")
        mp3_player_path = input("Whats the path to your mp3 folder? (Give a exact Path): ")
        print(f"DEBUG: {mp3_player_path}")
        mp3_json.update({"Path": f"{mp3_player_path}"})

        save_mp3path(mp3_player_path)
    
    except:
        print("Critical Error in trying to read the save file.")

load_mp3path()

#For loops for searching and appening MP3's 
def mp3_search():
    mp3_songs.clear()
    print("Finding mp3 files...\n")
    try:
        for dirpath, dirnames, filenames in os.walk(f"{mp3_player_path}"):

            try:
                for file in filenames:
                    extension_extract = os.path.splitext(file)[1]

                    print(f"file, {file}")

                    if extension_extract.lower()  == ".mp3":

                        the_complete_PATH = os.path.join(dirpath, file)

                        file_culled = os.path.splitext(file)[0]

                        mp3_songs.update({f"{file_culled}": f"{the_complete_PATH}"})
                        print("Successfully appended! \n")

                    else:
                        pass

            except:
                print("Critical Error... \n")
                return
            
        mp3_options()
            
    except:
        print("Critical Error... \n")
        return

#mp3 options
def mp3_options():
        global ran_flag_shuffler
        ran_flag_shuffler = False

        reseter = input("[1] Want to RESET your playlist Path? (Hit anykey for NO.): \ninput?: ")

        if reseter.strip() == "1":
            reseter_the_second = input("\nWhat do you want to change it too? (Give a exact Path): ")

            mp3_json.update({"Path": f"{reseter_the_second}"})
            print("Restarting file, Open the file after restart...")
            save_mp3path(reseter_the_second)
            time.sleep(3)
            return
        
        else:
            pass

        shuffler = input("\n[2] Want to SCHUFFLE your playlist? (Hit anykey for NO.): \ninput?: ")

        if shuffler.strip()  == "2":
            ran_flag_shuffler = True
            print("Successfuly Shuffled MP3 list.")

        else:
            pass
        
        run = input("\n[3] Want to PLAY your playlist (Hit anykey for NO.)?: \ninput?: ")

        if run.strip()  == "3":
            for song in mp3_songs:
                subprocess.run("cls", shell=True)
                usable_song = mp3_songs.get(song)

                if ran_flag_shuffler == False:
                    subprocess.run(["ffplay", "-nodisp", "-autoexit", usable_song])

                else:
                    path = random.choice(list(mp3_songs.values())) 
                    subprocess.run(["ffplay", "-nodisp", "-autoexit", path])

        else:
            pass
        
        run_specific = input("\n[4] Want to RUN a specific song? (Hit anykey for NO.): \ninput?: ")
        
        if run_specific.strip() == "4":
            compare_contrast()

            subprocess.run(["ffplay", "-nodisp", "-autoexit", mvp])

        else:
            pass
        
        run_specific_loop = input("\n[5] Want to play a specific song on loop? (Hit anykey for NO.): \n")

        if run_specific_loop == "5":
            compare_contrast()

            while True:
                subprocess.run(["ffplay", "-nodisp", "-autoexit", mvp])

        else:
            print("Restart...") 
            mp3_search()


mp3_search()