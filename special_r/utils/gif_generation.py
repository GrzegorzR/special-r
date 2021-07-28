import os
import ffmpeg
import ffmpy


def gen_mp4(imgs_dir, out_file):
    (
        ffmpeg
            .input('{}/*.png'.format(imgs_dir), pattern_type='glob', framerate=60)
            .output('{}'.format(out_file))
            .run()
    )


def mp4_to_gif(input_mp4, output_gif, frame_rate=15, scale=250):
    ff = ffmpy.FFmpeg(
        inputs={input_mp4: None},
        outputs={output_gif: '-r {} -vf "scale={}:-1,split[s0][s1];[s0]palettegen[p];[s1][p]paletteuse"'
                             .format(str(frame_rate), str(scale))})

    ff.run()

def gif_to_webp(input_gif, output_webp):
    os.system('gif2webp {} -o {}'.format(input_gif, output_webp))


if __name__ == '__main__':

    #gen_mp4('out/pym_7', 'out/pym_7.mp4')
    mp4_to_gif('out/pym_7_6.mp4', 'out/pym_7_6.gif', 20, 400)
    #gif_to_webp('out/pym_4.gif', 'out/pym_4.webp')
