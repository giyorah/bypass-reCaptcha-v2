import speech_recognition as sr
from houndify_creds import HOUNDIFY_CLIENT_ID, HOUNDIFY_CLIENT_KEY
from pydub import AudioSegment
from os import path, remove

def speech_rec_from_file(file_path, engine = 'google'):
    '''
    Speech Recognition from file.

    Args:
        file_path: Path to audio file. Either MP3 or (better yet) WAV.
        engine: a string, either 'google' or 'houndify'. Default is Google's.

    Returns:
        - A text string transcription of the given speech.
        - Duration of the audio track.

    Raises:
        FileError: Raises an exception if the given file has unsupported format.
        EngineNotSupported: Raises an exception if the selected engine is N/a.
    '''
    # input handling
    assert file_path != None, \
        "TypeError: speech_rec_from_file() missing required argument 'file_path' (pos 1)"
    assert file_path.lower().endswith('.wav') or file_path.lower().endswith('.mp3'), \
        "FileError: unsupported format"
    assert engine.lower() == 'google' or engine.lower() == 'houndify', \
        "EngineNotSupported: You must choose either Google or Houndify"
    
    # in case of mp3 - convert to WAV for the SR engine
    wavFilePath = file_path
    if file_path.lower().endswith('.mp3'):
        try:
            # create WAV from MP3
            sound = AudioSegment.from_mp3(file_path)
            wavFilePath = path.splitext(file_path)[0] + '.wav'
            sound.export(wavFilePath, format="wav")
            
        except Exception:
            exit(
                "[ERR] Please run program as administrator or download ffmpeg manually, "
                "https://blog.gregzaal.com/how-to-install-ffmpeg-on-windows/"
            )
    
    # get track's duration
    duration = AudioSegment.from_wav(wavFilePath).duration_seconds

    # load the WAV to memory
    payload = sr.AudioFile(wavFilePath)
    r = sr.Recognizer()
    with payload as source:
        audio_data = r.record(source)
    
    # send to cloud for recognition
    engine_ = engine.lower()
    if engine_ == 'google':
        text = r.recognize_google(audio_data)
    elif engine_ == 'houndify':
        text = r.recognize_houndify(audio_data, client_id=HOUNDIFY_CLIENT_ID, client_key=HOUNDIFY_CLIENT_KEY)
    
    # clean up
    remove(wavFilePath)

    return text, duration