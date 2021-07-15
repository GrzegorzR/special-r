import xmltodict

adobe_colors_file = 'data/colors.xml'

basic_custom_mechanical_keybors_gone_wrong = {'background': (73, 73, 71),
                                              'color_1': (248, 229, 238),
                                              'color_2': (144, 255, 220)}

blue_crystal_vienna = ['#00090D', '#025E73', '#05F2DB', '#027368', '#027353', '#00090D']
schiele_1 = ['#00010D', '#038C65', '#027353', '#8C623E', '#BFA799']


def asd():
    with open(adobe_colors_file, 'r') as f:
        data = xmltodict.parse(f.read())
        print(data['colors']['palette'][0])
        colorsets_5 = 1
        pass
