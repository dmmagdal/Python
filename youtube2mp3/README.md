# Download YouTube 2 MP3

Description: A simple program that downloads youtube videos and extracts their mp3 audio from them.


### Run the program

This program is designed to for indexing playlists from YouTube channels. It can download content from those indexed playlists as mp4 videos and convert them to mp3 or wav audio files. This is ideal for users who want to download playlists from YouTube containing music and OSTs. Be sure that you have adaquet space for the downloads.

1. Start by creating a rough index json file containing the YouTube channel's url (usally formatted `https://www.youtube.com/c/ChannelName/videos`) and the list of playlist urls from that channel you wish to be indexed (see `ChillMusicLab.json` as an example).
2. Create the docker image.

`docker build -t youtube2mp3 -f Dockerfile .`

3. Run the docker image in a container and mount a volume between the container and this current directory (again, be sure to have adaquet file storage available for your downloads).

`docker image a`


### What is going on in the background?

The docker container is going to run `download.py`. `download.py` is a script that will look first look for a fine indexed json file to load (here it's `ChillMusicLab_Explored.json`). If not such file exists, it will use the rough index file defined (`ChillMusicLab.json`) and iterate through each playlist to index its contents and save that to the respective json. Once the contents of the playlist have been indexed, the script will go through each playlist and download the videos as mp4 video files in a folder. The program will also extract the audio from those videos and save it in mp3 and wav formatted files.


### TODO

This program can be made a lot more extensible to allow for user input in the arguments other than relying on the hardcoded contents in `download.py` as well as some general file checking.
 - [] provide arguments for rough index json (ie `ChillMusicLab.json`) so that users can enter their own files.
 - [] provide arguments for fine index json (ie `ChillMusicLab_Explored.json`) so that users can enter their own files.
 - [] provide arguments for audio exporting (mp3, wav, both, or neither).
 - [] provide arguments for saving mp4 video if audio export arguments are defined as anything other than "neither".
 - [] add more error checking/handling for files.


### Resources

 - PyTube [GitHub](https://github.com/pytube/pytube)
 - PyTube [Documentation](https://pytube.io/en/latest/user/quickstart.html)
 - MoviePy [Documentation](https://zulko.github.io/moviepy/)
 - Pydub [Documentation](http://pydub.com/)
 - Convert mp4 to mp3 [Stack Overflow post] (https://stackoverflow.com/questions/55081352/how-to-convert-mp4-to-mp3-using-python)
 - Convert mp3 to wav [tutorial](https://pythonbasics.org/convert-mp3-to-wav/)
