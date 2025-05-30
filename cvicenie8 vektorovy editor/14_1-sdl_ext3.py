#!/usr/bin/python3

"""14_1-sdl_ext.py: pouzitie kniznice SDL prostrednictvom Python extensions - priklad event loop-u a reagovanie na stlacenie klavesy a pohyb mysi"""
__author__ = "Michal Vagac"
__email__ = "michal.vagac@gmail.com"

# https://www.libsdl.org/
# https://pypi.python.org/pypi/PySDL2/0.2.0
# https://github.com/syntonym/pysdl2/tree/master/examples
# http://pysdl2.readthedocs.io/en/latest/modules/sdl2ext.html

# LINUX:
#   apt-get install libsdl2-2.0-0
#   apt-get install libsdl2-image-2.0-0         # obrazky
#   apt-get install libsdl2-ttf-2.0-0           # font
#   pip3 install pysdl2
# WINDOWS:
#   pip3 install pysdl2 pysdl2-dll
#   manualna instalacia:
#       stiahnut spravnu Runtime Binary z adresy https://www.libsdl.org/download-2.0.php
#       niekde umiestnit subor SDL2.dll (napr. do adresara C:/test/ )
#       nastavit premennu prostredia (environment variables) PYSDL2_DLL_PATH na cestu k tomuto suboru (napr. C:/test/ )
#       po pridani premennej prostredia sa nezabudnite odhlasit/prihlasit (resp. restartovat pocitac)
#       ak to nebude fungovat, skuste druhu verziu Runtime Binary (64bit vs 32bit)

import sdl2.ext


def usecka(x1, y1, x2, y2, f):
    dx = abs(x2 - x1)
    dy = abs(y2 - y1)

    # if dx > dy:
    #     dlzka = dx
    # else:
    #     dlzka = dy
    dlzka = dx if dx > dy else dy
    #C/java: dlzka = dx > dy?dx:dy
    if dlzka == 0:
        return

    deltax = (x2 - x1) / dlzka
    deltay = (y2 - y1) / dlzka

    x = x1
    y = y1
    for i in range(dlzka):
        pixle[int(y)][int(x)] = f
        x += deltax
        y += deltay


# inicializacia SDL2
sdl2.ext.init()

# vytvor a zobraz okno
window = sdl2.ext.Window("Priklad Event Loop", size=(800, 600))
window.show()

# priprav pristup na kreslenie do okna (pozadie okna vyfarbi na bielo)
plocha = window.get_surface()
sdl2.ext.fill(plocha, sdl2.ext.Color(255, 255, 255))
window.refresh()

# pole na kreslenie
pixle = sdl2.ext.PixelView(plocha)

zac_x = None
zac_y = None

# jednoduchy event loop
running = True
while running:
    # spracuvaj eventy
    events = sdl2.ext.get_events()
    for event in events:
        # zoznam klaves pozri na: https://wiki.libsdl.org/SDL_Scancode
        if event.type == sdl2.SDL_MOUSEBUTTONDOWN and event.button.button == sdl2.SDL_BUTTON_LEFT:
            print(event.motion.x, event.motion.y)
            if zac_x is None or zac_y is None:
                # pamataj pociatocny vrchol
                zac_x = event.motion.x
                zac_y = event.motion.y
            else:
                # kresli ciaru
                usecka(zac_x, zac_y, event.motion.x, event.motion.y, sdl2.ext.Color(255, 0, 0))
                window.refresh()
                zac_x = None
                zac_y = None
        if event.type == sdl2.SDL_QUIT:             # event: quit
            running = False
            break

# uvolni alokovane zdroje
sdl2.ext.quit()

