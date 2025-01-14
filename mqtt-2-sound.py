#!/usr/bin/python3
from paho.mqtt import client as mqtt
import yaml
import pygame
import os

config_f = open('config.yaml')
config = yaml.safe_load(config_f)
config_f.close()

# set up the mixer at 44100 frequency, with 16 signed bits per sample, 1 channel, with a 2048 sample buffer
pygame.mixer.init(44100, -16, 1, 2048)

currently_playing_file = ""


def on_message(obj, user, msg):
    print ("Received %s on topic %s" % (msg.payload, msg.topic))
    if msg.topic == 'door/inner/opened/username':
        # Set volume to 50% for this clip
        play("audio/%s_announce.ogg" % msg.payload, 0.5)
    elif msg.topic == 'door/outer/buzzer':
        play("audio/buzzer.ogg")
    elif msg.topic == 'door/outer/opened/username':
        play("audio/outer_door_opened.ogg")
    elif msg.topic == 'door/inner/doorbell':
        play("audio/doorbell.ogg")
    elif msg.topic == 'DahuaVTO/BackKeyLight/Event':
        play("audio/doorbell.ogg")        


def play(filename,level = 1.0):
    global currently_playing_file
    if os.path.isfile(filename):
        if (not pygame.mixer.music.get_busy()) or (currently_playing_file is not filename):
            print ("Playing %s" % filename)
            currently_playing_file = filename
            pygame.mixer.music.load(filename)
            pygame.mixer.music.set_volume(level)
            pygame.mixer.music.play()


mqttc = mqtt.Client(config['mqtt']['name'])
mqttc.connect(config['mqtt']['server'], 1883, 60)

mqttc.subscribe("door/outer/buzzer")
mqttc.subscribe("door/outer/opened/username")

mqttc.subscribe("door/inner/doorbell")
mqttc.subscribe("door/inner/opened/username")

mqttc.subscribe("DahuaVTO/BackKeyLight/Event")

mqttc.on_message = on_message

while mqttc.loop(timeout=100) == 0:
    pass

