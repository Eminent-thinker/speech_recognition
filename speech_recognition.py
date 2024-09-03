import speech_recognition as sr

def recognize_speech_from_mic(recognizer, microphone):
    """Transcribe speech from recorded from `microphone`."""
    # check that recognizer and microphone arguments are appropriate type
    if not isinstance(recognizer, sr.Recognizer):
        raise TypeError("`recognizer` must be `Recognizer` instance")
    if not isinstance(microphone, sr.Microphone):
        raise TypeError("`microphone` must be `Microphone` instance")

    # adjust the recognizer sensitivity to ambient noise and record audio from the microphone
    with microphone as source:
        recognizer.adjust_for_ambient_noise(source)
        print("Listening...")
        audio = recognizer.listen(source)

    # initialize response
    response = {
        "success": True,
        "error": None,
        "transcription": None
    }

    try:
        # recognize speech using Google Web Speech API
        response["transcription"] = recognizer.recognize_google(audio)
    except sr.RequestError:
        # API was unreachable or unresponsive
        response["success"] = False
        response["error"] = "API unavailable"
    except sr.UnknownValueError:
        # speech was unintelligible
        response["error"] = "Unable to recognize speech"

    return response

if __name__ == "__main__":
    recognizer = sr.Recognizer()
    microphone = sr.Microphone()

    while True:
        print("Say something:")
        response = recognize_speech_from_mic(recognizer, microphone)
        
        if response["success"]:
            print("You said: {}".format(response["transcription"]))
        else:
            print("Error: {}".format(response["error"]))

        if response["transcription"] and response["transcription"].lower() == "quit":
            break
