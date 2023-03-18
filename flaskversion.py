import os
import pyttsx3
import ffmpeg
import flask
from flask import Flask, request
# use ffmpeg-python package not ffmpeg

app = Flask(__name__)

@app.route("/")
def index():
    engine = pyttsx3.init()
    engine.setProperty('rate', engine.getProperty('rate') - 90)
    city = request.args.get('city')
    engine.save_to_file(city, 'audio.mp3')
    engine.runAndWait()
    input_video = ffmpeg.input("base.mp4")
    added_audio = ffmpeg.input("audio.mp3").audio.filter('adelay', "13300|13300")
    merged_audio = ffmpeg.filter([input_video.audio, added_audio], 'amix')
    (ffmpeg
     .concat(input_video, merged_audio, v=1, a=1)
     .drawtext(text=city, x='(w-text_w)/2', y='(h-text_h)/2', fontsize=70, fontcolor='white',
               enable=f'between(t,{12},{15})')
     .output("output.mp4")
     .run(overwrite_output=True))
    # remove temporary file
    os.remove('audio.mp3')
    try:
        return flask.send_file("output.mp4")
    finally:
        pass

if __name__ == '__main__':
    app.run(host='localhost', port=8080)
