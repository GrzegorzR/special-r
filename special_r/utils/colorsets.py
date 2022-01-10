import xmltodict
from colour import Color

adobe_colors_file = 'data/colors.xml'

basic_custom_mechanical_keybors_gone_wrong = {'background': (73, 73, 71),
                                              'color_1': (248, 229, 238),
                                              'color_2': (144, 255, 220)}

blue_crystal_vienna = ['#00090D', '#025E73', '#05F2DB', '#027368', '#027353', '#00090D']
schiele_1 = ['#00010D', '#038C65', '#027353', '#8C623E', '#BFA799']
mech_keyboard = ['#F26671', '#F27EB4', '#D9AA71', '#F28066', '#261614']
nikifor_1 = ['#242526', '#023059', '#8FA6A1', '#5B7349', '#592D2D']
vienna_wom = ['#F2ECCE', '#F2B6B6', '#A665A1', '#734343', '#394144']
vienna_strips = ['#040FD9', '#0554F2', '#00C5D6', '#71FAA8', '#FF82BB']
to_zdjecie = ['#04738C', '#77A632', '#F2EDA2', '#F2DABD', '#A67C6D']
chinskie = ['#637353' ,'#D9C9BA' ,'#A64D2D' ,'#D9593D' ,'#D94436' ]

white = Color('white')
green = Color('green')

gray = '#4e5052'

def white_to_red(n):
    return [c.hex_l.upper() for c in white.range_to(red, n)]


def white_to_green(n):
    return [c.hex_l.upper() for c in white.range_to(green, n)]


def colors_range_hex(c0, c1, n):
    return [c.hex_l.upper() for c in c0.range_to(c1, n)]


def asd():
    with open(adobe_colors_file, 'r') as f:
        data = xmltodict.parse(f.read())
        print(data['colors']['palette'][0])
        colorsets_5 = 1
        pass
