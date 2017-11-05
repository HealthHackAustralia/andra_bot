try:
    from robot import say_with_emotion
except:
    pass

EMOTION_SEQUENCE = [
    'animations/Stand/Gestures/Hey_7',
    'animations/Stand/Gestures/Explain_2',
    'Stand/Gestures/JointHands_2',
    'Stand/Gestures/WhatSThis_1',
    'Stand/Gestures/WhatSThis_3',
    'Stand/Gestures/IDontKnow_3',
]

if __name__ == '__main__':
    for emotion in EMOTION_SEQUENCE:
        _ = raw_input("Press any key to continue...")
        print(emotion)
        say_with_emotion('', emotion)
