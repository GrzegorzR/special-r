import imageio


from os.path import join as join_path
from os import listdir

from PIL import Image

def make_gif(input_dir, output_file):
    images = []
    filenames = [join_path(input_dir, im_name) for im_name in listdir(input_dir)]
    filenames = sorted(filenames)[:50]
    img, *imgs = [Image.open(f) for f in filenames]
    img.save(fp=output_file, format='GIF', append_images=imgs,
             save_all=True, duration=10, loop=0)

if __name__ == '__main__':
    make_gif('gif_1', 'gif_1.gif')