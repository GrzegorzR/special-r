ffmpeg -r 60 -i pym%04d.png -vcodec mpeg4 -y -b 15000k  pym_3.mp4
ffmpeg -r 60 -i 5/6/%04d.png -vcodec mpeg4 -y -b 64000k  5_6.mp4