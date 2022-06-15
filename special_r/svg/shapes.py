import drawSvg as draw




triangle_svg = draw.Path(stroke='red', transform='', stroke_width=2, fill='#222222', id='dd')
triangle_svg.M(50, -40).L(20, -100).L(0, -20)
triangle_svg.args['transform'] = ''

blob_svg = draw.Path( transform='', stroke_width=2, fill='#222222', id='dd')
d = "M12.8,-4.1C12.8,6.9,6.4,13.9,1,13.9C-4.5,13.9,-8.9,6.9,-8.9,-4.1C-8.9,-15.1,-4.5,-30.2,1,-30.2C6.4,-30.2,12.8,-15.1,12.8,-4.1Z"
blob_svg.args['d'] = d
