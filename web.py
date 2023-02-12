import streamlit as st
import os
from email import encoders
import smtplib, ssl
from pytube import YouTube
from youtubesearchpython import VideosSearch
import imageio
try:
    imageio.plugins.ffmpeg.download()
except:
    print("Instal imageio==2.4.1")
    exit(1)
from moviepy.editor import *
import zipfile
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

PASSWORD = st.secrets["PASSWORD"]


class VideoMashup:
    def __init__(self, singer_name, no_of_videos, audio_duration, result_file_name):
        self.singer_name = singer_name
        self.no_of_videos = no_of_videos
        self.audio_duration = audio_duration
        self.result_file_name = result_file_name
        self.res = []
        self.names_list = []

    def search_videos(self):
        videos_search = VideosSearch(self.singer_name, limit=self.no_of_videos)
        for i in range(self.no_of_videos):
            self.res.append(videos_search.result()['result'][i]['link'])
        return self.res

    def download_videos(self):
        for i in range(self.no_of_videos):
            try:
                yt = YouTube(self.res[i])
                video = yt.streams.filter(only_audio=True).first()
                destination =''
                out_file = video.download(output_path=destination)
                base, ext = os.path.splitext(out_file)
                new_file = base + '.mp3'
                self.names_list.append(new_file)
                os.rename(out_file, new_file)
                print(yt.title + " has been successfully downloaded.")
            except Exception as e:
                print(f"An error occurred while downloading the video: {e}") 
        return self.names_list
    
    def merge(self):
        final_clip = concatenate_audioclips([AudioFileClip(name).subclip(0,self.audio_duration) for name in self.names_list])
        final_clip.write_audiofile(self.result_file_name)
        final_clip.close()
        return
   

    def cleanup(self):
        for i in range(self.no_of_videos):
            os.remove(self.names_list[i])
            os.remove(self.result_file_name)
            os.remove(self.result_file_name + '.zip')

    def zipAudio(self):
        zip_file = self.result_file_name + '.zip'
        with zipfile.ZipFile(zip_file, 'w') as myzip:
            myzip.write(self.result_file_name)
        return

    def create_mashup(self):
        try:
            self.search_videos()
            self.download_videos()
            self.merge()
            self.zipAudio()
            self.cleanup()
            
        except Exception as e:
            print(f"An error occurred while creating the mashup: {e}")



def send_email(email, output_file):
    port = 465  
    smtp_server = "smtp.gmail.com"
    sender_email = "vshukla_be20@thapar.edu" 
    receiver_email = email 

    message = MIMEMultipart()
    message["From"] = sender_email
    message["To"] = receiver_email
    message["Subject"] = "Final Mashup as requested"
    message.attach(MIMEText("Please find the attached zip file.", "plain"))
    zip_file = os.getcwd() + '/' + output_file + ".zip"
    
    part = MIMEBase('application', "octet-stream")
    part.set_payload( open(zip_file,"rb").read() )   
    encoders.encode_base64(part)
    part.add_header(
        "Content-Disposition",
        f"attachment; filename={output_file+'.zip'}",
    )
    message.attach(part)
    text = message.as_string()
    context = ssl.create_default_context()
    with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
        server.login(sender_email, PASSWORD)
        server.sendmail(sender_email, receiver_email, text)

st.title("Video Mashup")
st.title("Vibhav Shukla - 102003772")
st.write("Enter the details to create a mashup")

form = st.form(key='my_form')
singer_name = form.text_input("Enter the singer name")
no_of_videos = form.number_input("Enter the number of videos", min_value=1, max_value=20, value=10)
audio_duration = form.number_input("Enter the audio duration", min_value=1, max_value=100, value=10)
result_file_name = form.text_input("Enter the result file name")
receiever_email = form.text_input("Enter the receiever email")
submit = form.form_submit_button(label='Submit')

if submit:
    video_mashup = VideoMashup(singer_name, no_of_videos, audio_duration, result_file_name)
    video_mashup.create_mashup()
    st.write("Mashup created successfully")
    send_email(receiever_email, result_file_name)

