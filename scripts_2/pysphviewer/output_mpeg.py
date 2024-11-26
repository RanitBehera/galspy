import os

FRAMES_DIR = "/mnt/home/student/cranit/RANIT/Repo/galspy/scripts_2/pysphviewer/media/frames"
os.chdir(FRAMES_DIR)
# os.system("ffmpeg -r 10 -i fr_%4d.png -vcodec mpeg4 -y ../movie.mp4 -vf \"scale=1080:1080\" -c:a copy -b:v 20M")
os.system("ffmpeg -r 10 -i fr_%4d.png -vcodec mpeg4 -y ../movie.mp4 -vf \"scale=1080:1080\" -c:a copy -b:v 20M")
print("SAVED")