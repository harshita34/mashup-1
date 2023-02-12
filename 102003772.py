import os
import sys
from pytube import YouTube
from youtubesearchpython import VideosSearch
import imageio
try:
    imageio.plugins.ffmpeg.download()
except:
    print("Install imageio==2.4.1")
    exit(1)
from moviepy.editor import *

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

    def create_mashup(self):
        try:
            self.search_videos()
            self.download_videos()
            self.merge()
            self.cleanup()
        except Exception as e:
            print(f"An error occurred while creating the mashup: {e}")

if __name__ == "__main__":
    if len(sys.argv) != 5:
        print("Sample input: python <program_name> <singer_name> <noOfVideos> <audioDuration> <resultFileName>")
        exit(1)
    else:
        singer_name = sys.argv[1]
        no_of_videos = int(sys.argv[2])
        audio_duration = int(sys.argv[3])
        result_file_name = sys.argv[4]
        video_mashup = VideoMashup(singer_name, no_of_videos, audio_duration, result_file_name)
        video_mashup.create_mashup()