# download.py
# Downloads YouTube video(s) and saves the audio.
# Python 3.9
# Windows/MacOS/Linux


import os
import json
from moviepy.editor import *
from pydub import AudioSegment
from pytube import YouTube, Channel, Playlist


def main():
	# Save paths.
	save_video_path = "./movie"
	save_mp3_path = "./audio"
	save_wav_path = "./wav"
	
	# Pre indexed and indexed channel json files.
	input_file = "ChillMusicLab.json"
	output_file = "ChillMusicLab_Explored.json"
	
	# File checks.
	if not os.path.exists(input_file) and not os.path.exists(output_file):
		print(f"Could not find input json {input_file}")
		exit(0)
		
	# Index the youtube channel (based on available playlists) and save the
	# indexed data. NOTE: going by playlists doesnt necessarily cover/index all
	# videos on the channel, only those found on playlists.
	if not os.path.exists(output_file):
		print("No index file exists. Using channel json file to index from playlist(s)")
	
		# Load initial data from json file.
		with open(input_file, "r") as f_in:
			data = json.load(f_in)

		output_data = index_from_playlists(
			data["playlist_urls"], data["channel_url"]
		)
		
		# Write extracted data to json file.
		with open(output_file, "w+") as f_out:
			json.dump(output_data, f_out, indent=4)
	
	# Read indexed data file.
	with open(output_file, "r") as f_index:
		indexed_data = json.load(f_index)
		
	# Iterate through each video.
	seen = set()
	for playlist in indexed_data["playlist"]:
		# For testing, only do 1 playlist (this one has about 12 songs). Can
		# Use this as an estimate on the storage needs.
		if playlist != "LoFi Hip-Hop Music":
			continue

		videos = indexed_data["playlist"][playlist]
		for video in videos:
			song_url = video["url"]
			song_name = video["song"]
			if song_url not in seen:
				seen.add(song_url)
				download_status = download_video(song_url, save_video_path)
				if download_status:
					full_path = os.path.join(save_video_path, song_name + ".mp4")
					convert2mp3(full_path)
					convert2wav(full_path.replace(".mp4", ".mp3"))

	# Exit the program.
	exit(0)
	
	
'''
	Given the YouTube channel url and the list of playlist urls associated with
	that channel, index the content from each playlist (and download if a save
	path/folder is provided).
	
	@param: playlist_urls (str), list of urls that point to the beginning of a
		playlist. It is assumed that these playlists are associated to the YouTube
		channel (url) passed in.
	@param: channel_url (str), url to the YouTube channel's home or video page.
	@param: save_path (str, Path) [Optional], folder path to download indexed
		content. Is None by default.
	@return: returns a dictionary containing the indexed content from playlist(s)
		assorciated to the channel (url) passed in.
'''
def index_from_playlists(playlist_urls, channel_url, save_path=None):
	# Channel info.
	channel = Channel(channel_url)
	channel_name = channel.channel_name
	
	# Return data.
	data = {
		"channel": channel_name,
		"url": channel_url,
		"playlist": {},
	}
	
	# Videos seen (reduce redundancy).
	seen = set()
	
	# Playlist info.
	for url in playlist_urls:
		# Playlist info.
		playlist = Playlist(url)
		playlist_title = playlist.title
		data["playlist"][playlist_title] = []
		print(f"Indexing playlist: {playlist_title}")
		
		for video in playlist.videos:
			try:
				# Song info.
				song_title = video.streams.get_highest_resolution().title
				song_url = video.watch_url
				
				if song_url not in seen:
					seen.add(song_url)
					print(f"\tIndexed {song_title}")
				
					# Download if a path has been specified.
					if save_path:
						print(f"Downloading {song_title}")
						video.streams.get_highest_resolution().download(
							os.path.join(save_path, playlist_title)
						)
				
				# Update return data.
				data["playlist"][playlist_title].append(
					{"song": song_title, "url": song_url}
				)
			except:
				print(f"\tUnable to index {video.watch_url}")
					
	print("Indexing complete")
	print(f"Indexed {len(seen)} songs")
		
	# Return the data.
	return data
	
	
'''
	Download a YouTube video from its url.
	
	@param: video_url (str), url of the video to download.
	@param: save_path (str, Path), folder path to download content to.
	@return: returns a boolean as to whether the video was able to be successfully
		downloaded.
'''
def download_video(video_url, save_path):
	try:
		yt = YouTube(video_url)
		yt.streams.get_highest_resolution().download(save_path)
		return True
	except:
		print(f"Unable to download {video_url}")
		return False
	
	
'''
	Extract and save mp3 audio from mp4 video.
	
	@param: mp4_video_path (str, Path), path to the source mp4 video file.
	@param: mp3_save_path (str, Path), path to the destination mp3 audio file.
		Is None by default.
	@return: returns nothing.
'''
def convert2mp3(mp4_video_path, mp3_save_path=None):
	# Verify the source file exists.
	if not os.path.exists(mp4_video_path):
		print(f"Target mp4 file {mp4_video_path} does not exist")
		return

	# If the destination mp3 path not defined, use the same path as the input
	# mp4 file.
	if mp3_save_path != None:
		output_path = mp3_save_path
	else:
		output_path = mp4_video_path.replace(".mp4", ".mp3")

	try:
		video = VideoFileClip(mp4_video_path)
		video.audio.write_audiofile(output_path)
	except:
		print(f"Failed to convert {mp4_video_path} to mp3")
	

'''
	Extract and save wav audio from mp3 audio.
	
	@param: mp3_video_path (str, Path), path to the source mp3 audio file.
	@param: wav_save_path (str, Path), path to the destination wav audio file.
		Is None by default.
	@return: returns nothing.
'''
def convert2wav(mp3_audio_path, wav_save_path=None):
	# Verify the source file exists.
	if not os.path.exists(mp3_audio_path):
		print(f"Target mp3 file {mp3_audio_path} does not exist")
		return

	# If the destination wav path not defined, use the same path as the input
	# mp3 file.
	if mp3_audio_path != None:
		output_path = wav_save_path
	else:
		output_path = mp3_audio_path.replace(".mp3", ".wav")

	try:
		sound = AudioSegment.from_mp3(mp3_audio_path)
		sound.export(output_path, format="wav")
	except:
		print(f"Failed to convert {mp3_audio_path} to wav")


if __name__ == '__main__':
	main()
