import os
import sys
from pytube import YouTube
from youtubesearchpython import VideosSearch
from pydub import AudioSegment 

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
            print("part 1 done")
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
            print ("part 2 done")
        return self.names_list

    def merge(self):
        self.audio_duration = self.audio_duration * 1000
        try:
            for i in range(self.no_of_videos):
                sound1 = AudioSegment.from_file(self.names_list[i])
                print("Extracting sound from audio file...")
                extract = sound1[self.audio_duration:]
                if i == 0:
                    final_sound = extract
                else:
                    final_sound = final_sound.append(extract, crossfade=1500)
            final_sound.export(self.result_file_name, format="mp3")
            print("Mashup created successfully!")
        except Exception as e:
            print(f"An error occurred while creating the mashup: {e}")
        print("part 3 done")

    def cleanup(self):
        for i in range(self.no_of_videos):
            os.remove(self.names_list[i])
        print("part 4 done")
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

