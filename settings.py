level_map = [
    '                         ',
    '                 T       ',
    'P     V      f           ',
    'F       T     f     F    ',
    '                         ',
]
tile_size = 64
sizex = len(level_map[0])
if sizex > 15:
    sizex = 15
screen_width = tile_size * sizex
screeen_height = tile_size * len(level_map) * 2
fps = 60
