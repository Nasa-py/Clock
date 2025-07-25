import time
import datetime
import pygame
import os

def set_alarm(alarm_time, sound_file):
    print(f"The alarm is set for {alarm_time}".title())
    while True:
        now = datetime.datetime.now().strftime("%I:%M:%S")
        print(now)
        if now == alarm_time:
            print("---------------------- 🥱 Wake Up!!! 🥱 ----------------------")
            pygame.mixer.init()

            if not os.path.exists(sound_file):
                print("⚠️ Alarm sound file not found! Using default 'a.mp3'")
                sound_file = "a.mp3"

            pygame.mixer.music.load(sound_file)
            pygame.mixer.music.play()
            while pygame.mixer.music.get_busy():
                time.sleep(1)
            break 

        time.sleep(1)

if __name__ == "__main__":
    alarm = input("Enter the time you want to set (HH:MM:SS): ").strip()
  
    sound = input("Enter your choice of alarm tone (or press Enter for default): ").strip()

    if sound.lower() == "default" or sound == "":
        sound = "a.mp3"  

    set_alarm(alarm, sound)