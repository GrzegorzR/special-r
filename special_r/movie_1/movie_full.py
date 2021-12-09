import os
import shutil

from special_r.movie_1.scene_1 import get_scene_1_obj
from special_r.movie_1.scene_2 import get_scene_2_obj
from special_r.movie_1.scene_3 import get_scene_3_obj, get_scene_3_2_obj, get_scene_3_3_obj
from special_r.movie_1.scene_5 import get_scene_5_obj, get_scene_5_2_obj
from special_r.movie_1.scene_6 import get_scene_6_obj
from special_r.movie_1.utils import make_movie

if __name__ == '__main__':
    s1 = get_scene_1_obj()
    s2 = get_scene_2_obj()

    s3 = get_scene_3_obj()
    s3_2 = get_scene_3_2_obj()
    s3_3 = get_scene_3_3_obj()

    s5 = get_scene_5_obj()
    s5_2 = get_scene_5_2_obj()

    s6 = get_scene_6_obj()
    out_dir = 'out/movie_1/test_123'
    if os.path.exists(out_dir):
        shutil.rmtree(out_dir)

    make_movie([s1, s6, s2, s3, s3_2, s3_3, s5, s5_2], out_dir)
