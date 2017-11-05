# Note : I hate Python2.7 but the NAO (naoqi) SDK is only distributed for this Python version ...

import qi
from naoqi import ALProxy # Works with Python 2.7.10 only!
from vision_definitions import *
from PIL import Image # Install Pillow
from json import loads
from os.path import basename
from os import getcwd
from time import sleep
from sys import stderr
import numpy as np

IP, PORT = "XX.XXX.XXX.XXX", 9559

speech_proxy = ALProxy("ALTextToSpeech", IP, PORT)
animated_speech_proxy = ALProxy("ALAnimatedSpeech", IP, PORT)
camera_proxy = ALProxy("ALVideoDevice", IP, PORT)
audio_proxy = ALProxy("ALAudioRecorder", IP, PORT)

with open('NAO_animations.json') as fh:
    NAO_ANIMATIONS = [T[1] for T in loads(fh.read())]

def say_with_emotion(message, emotion):
    if False:
        assert emotion in NAO_ANIMATIONS, (emotion, NAO_ANIMATIONS)

    stderr.write('Running')
    animated_speech_proxy.say(
        '^start({emotion}) {message} ^wait({emotion})"'.format(
            emotion=emotion,
            message=message,
        ),
    )

if False:
    for animation in NAO_ANIMATIONS[::-1]:
        sleep(1)
        say_with_emotion(basename(animation), animation)

def get_microphone():
    try:
        print getcwd()
        print audio_proxy.stopMicrophonesRecording()
        print audio_proxy.startMicrophonesRecording('/home/nao/audio.wav', 'wav', 16000, [1, 0, 0, 0])
        sleep(1)
        print audio_proxy.stopMicrophonesRecording()
        open('/home/nao/audio.wav')
    except RuntimeError, e:
        #print audio_proxy.stopMicrophonesRecording()
        print str(e)
        raise

#get_microphone()

def main(debug=False):
    if debug:
        speech_proxy.say('DEBUG')

    video_client, resolution, color_space, fps = 'python_GVMG', kQVGA, kRGBColorSpace, 2
    video_client_id = camera_proxy.subscribe(video_client, resolution, color_space, fps)

    try:
        for i in range(0, 1):
            nao_image = camera_proxy.getImageRemote(video_client_id)

            # Get the image size and pixel array.
            image_width = nao_image[0]
            image_height = nao_image[1]
            array = nao_image[6]

              # Create a PIL Image from our pixel array.
            im = Image.fromstring("RGB", (image_width, image_height), array)

              # Save the image.
            image_filepath = "camera_{0}.png".format(i)
            im.save(image_filepath, "PNG")
    except Exception, e:
        camera_proxy.unsubscribe(video_client)
        print str(e)
        animated_speech_proxy.say('Error, Bertrand')

if __name__ == '__main__':
    main()
