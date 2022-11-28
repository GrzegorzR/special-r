import os

def svg2png(dir_in):
    files_list = os.listdir(dir_in)
    for f in files_list:
        file_path = os.path.join(dir_in, f)
        cmd = 'inkscape --without-gui --export-dpi=300 --export-type=png {}'.format(file_path)
        print(cmd)
        os.system(cmd)


if __name__ == '__main__':
    svg2png('out/3/movie_scene/1')