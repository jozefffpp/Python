import sys
import sdl2
import sdl2.ext


# inicializacia SDL2
sdl2.ext.init()

# vytvor a zobraz okno
window = sdl2.ext.Window("Rastrovy editor Pupava", size=(800, 600))
window.show()

# priprav pristup na kreslenie do okna (pozadie okna vyfarbi na bielo)
plocha = window.get_surface()
sdl2.ext.fill(plocha, sdl2.ext.Color(255, 255, 255))
window.refresh()

pixle = sdl2.ext.PixelView(plocha)

class tlacidlo:
    def __init__(self, x, y, s, v, image = "null"):
        self.x = x
        self.y = y
        self.s = s
        self.v = v
        self.image = image

        #nacitaj obrazok
        if self.image != "null":
            self.obrazok = sdl2.ext.load_image(image)
            self.r = sdl2.SDL_Rect()
            self.r.x, self.r.y, self.r.w, self.r.h = self.x+1, self.y+1, self.s, self.v

    def kresli(self, rr, g, b):
        #nakresli ramik
        for xi in range(self.s):
            pixle[self.y][self.x+xi] = sdl2.ext.Color(rr, g, b)
            pixle[self.y+self.v][self.x+xi] = sdl2.ext.Color(rr, g, b)
        
        for yi in range(self.s):
            pixle[self.y+yi][self.x] = sdl2.ext.Color(rr, g, b)
            pixle[self.y+yi][self.x+self.s] = sdl2.ext.Color(rr, g, b)
            
        #nakresli obrazok
        if self.image != "null":
            sdl2.SDL_BlitSurface(self.obrazok, None, plocha, self.r)

    def zasah(self, x,  y):
        return x>self.x and y>self.y and x<self.x + self.s and y<self.y + self.v

    def obrazok(self, image):
        obrazok = sdl2.ext.load_image(image)

    def oznacenie(self):
        usecka(self.x, self.y + self.v + 10, self.x + self.s, self.y+ self.v +10, (sdl2.ext.Color(220, 100, 50)))

    def odznacenie(self):
        usecka(self.x, self.y + self.v + 10, self.x + self.s, self.y+ self.v +10, (sdl2.ext.Color(255, 255, 255)))

def usecka(x1, y1, x2, y2, f):
    dx = abs(x2- x1)
    dy = abs(y2-y1)

    dlzka = dx if dx > dy else dy
    if dlzka == 0:
        return

    deltax = (x2-x1)/ dlzka
    deltay = (y2-y1)/ dlzka
    x = x1
    y = y1

    for i in range(dlzka):
        pixle[int(y)][int(x)] = f
        x += deltax
        y += deltay


def obdlznik(x1, y1, x2, y2, f):
    dx = abs(x2- x1)
    dy = abs(y2-y1)
    dlzkax = x2-x1
    dlzkay = y2-y1
    
    x = x1 if x2 > x1 else x2
    y = y1 if y2 > y1 else y2
    #nakresli obdlznik
    for xi in range(dx):
        pixle[y][x+xi] = f
        pixle[y+dy][x+xi] = f
        
    for yi in range(dy):
        pixle[y+yi][x] = f
        pixle[y+yi][x+dx] = f
        
        
# tlacidla funkcii
t1 = tlacidlo(30, 50, 52, 52,  "Actions-draw-freehand-icon.png")
t2 = tlacidlo(90, 50, 52, 52,  "stiahnuť.png")
t3 = tlacidlo(150, 50, 52, 52,  "depositphotos_289745958-stock-illustration-rectangle-sketch-hand-drawing-black.jpg")
t4 = tlacidlo(210, 50, 52, 52, "new.png")

# tlacidla farieb
f1 = tlacidlo(720, 50, 52, 52)
f2 = tlacidlo(660, 50, 52, 52)
f3 = tlacidlo(600, 50, 52, 52)
f4 = tlacidlo(540, 50, 52, 52)
f5 = tlacidlo(480, 50, 52, 52)

#farby tlacidiel farieb
f1_r, f1_g, f1_b = 250, 100, 0
f2_r, f2_g, f2_b = 0, 100, 250
f3_r, f3_g, f3_b = 0, 250, 50
f4_r, f4_g, f4_b = 100, 10, 120
f5_r, f5_g, f5_b = 190, 140, 200


oznacena_funkcia = 0
zac_x = None
zac_y = None
navbar = 150
aktualna_r, aktualna_g, aktualna_b = 0, 0, 0 


# jednoduchy event loop
running = True
while running:
    
    # spracuvaj eventy
    events = sdl2.ext.get_events()
    for event in events:
        
        #kreslenie volnou rukou
        if event.type == sdl2.SDL_MOUSEMOTION and oznacena_funkcia == 1 and event.button.button == 1 and event.motion.y > navbar:      # event: mousemotion
            pixle[event.motion.y][event.motion.x] = sdl2.ext.Color(aktualna_r, aktualna_g, aktualna_b)     # najprv y, potom x !
            window.refresh()
            
        if event.type == sdl2.SDL_MOUSEBUTTONDOWN:

            #kreslenie usecky
            if oznacena_funkcia == 2 and event.motion.y > navbar:
                if zac_x == None or zac_y == None:
                    zac_x = event.motion.x
                    zac_y = event.motion.y
                else:
                    usecka(zac_x, zac_y, event.motion.x, event.motion.y, (sdl2.ext.Color(aktualna_r, aktualna_g, aktualna_b)))
                    window.refresh()

                    zac_x = None
                    zac_y = None

            if oznacena_funkcia == 3 and event.motion.y > navbar:
                #nakresli obdlznik
                if zac_x == None or zac_y == None:
                    zac_x = event.motion.x
                    zac_y = event.motion.y
                else:
                    obdlznik(zac_x, zac_y, event.motion.x, event.motion.y, (sdl2.ext.Color(aktualna_r, aktualna_g, aktualna_b)))
                    dx = event.motion.x

                    zac_x = None
                    zac_y = None
            
            #vyber funkcie
            if t1.zasah(event.motion.x, event.motion.y):
                oznacena_funkcia = 1
                t1.oznacenie()
                t2.odznacenie()
                t3.odznacenie()

            if t2.zasah(event.motion.x, event.motion.y):
                oznacena_funkcia = 2
                t1.odznacenie()
                t2.oznacenie()
                t3.odznacenie()
                
            if t3.zasah(event.motion.x, event.motion.y):
                oznacena_funkcia = 3
                t1.odznacenie()
                t2.odznacenie()
                t3.oznacenie()
                
            if t4.zasah(event.motion.x, event.motion.y):
                sdl2.ext.fill(plocha, sdl2.ext.Color(255, 255, 255))
                window.refresh()


            #vyber farby
            if f1.zasah(event.motion.x, event.motion.y):
                aktualna_r, aktualna_g, aktualna_b = f1_r, f1_g, f1_b
                f1.oznacenie()
                f2.odznacenie()
                f3.odznacenie()
                f4.odznacenie()
                f5.odznacenie()
                
            if f2.zasah(event.motion.x, event.motion.y):
                aktualna_r, aktualna_g, aktualna_b = f2_r, f2_g, f2_b
                f1.odznacenie()
                f2.oznacenie()
                f3.odznacenie()
                f4.odznacenie()
                f5.odznacenie()
                
            if f3.zasah(event.motion.x, event.motion.y):
                aktualna_r, aktualna_g, aktualna_b = f3_r, f3_g, f3_b
                f1.odznacenie()
                f2.odznacenie()
                f3.oznacenie()
                f4.odznacenie()
                f5.odznacenie()
                
            if f4.zasah(event.motion.x, event.motion.y):
                aktualna_r, aktualna_g, aktualna_b = f4_r, f4_g, f4_b
                f1.odznacenie()
                f2.odznacenie()
                f3.odznacenie()
                f4.oznacenie()
                f5.odznacenie()
                
            if f5.zasah(event.motion.x, event.motion.y):
                aktualna_r, aktualna_g, aktualna_b = f5_r, f5_g, f5_b
                f1.odznacenie()
                f2.odznacenie()
                f3.odznacenie()
                f4.odznacenie()
                f5.oznacenie()
                
          # event: quit
        if event.type == sdl2.SDL_QUIT:           
            running = False
            break

    #tlacidla funkcii
    t1.kresli(0, 0, 0)
    t2.kresli(0, 0, 0)
    t3.kresli(0, 0, 0)
    t4.kresli(0, 0, 0)

    #tlacidla farieb
    f1.kresli(f1_r, f1_g, f1_b)
    f2.kresli(f2_r, f2_g, f2_b)
    f3.kresli(f3_r, f3_g, f3_b)
    f4.kresli(f4_r, f4_g, f4_b)
    f5.kresli(f5_r, f5_g, f5_b)
    
    window.refresh()
# uvolni alokovane zdroje
sdl2.ext.quit()

