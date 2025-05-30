import sdl2.ext

class usecka:
    def __init__(self, x1, y1, x2, y2, f):
        self.x1 = x1
        self.y1 = y1
        self.x2 = x2
        self.y2 = y2
        self.f = f

    def kresli(self):
        dx = abs(self.x2 - self.x1)
        dy = abs(self.y2 - self.y1)

        dlzka = dx if dx > dy else dy

        if dlzka == 0:
            return

        deltax = (self.x2 - self.x1) / dlzka
        deltay = (self.y2 - self.y1) / dlzka

        x = self.x1
        y = self.y1
        for i in range(dlzka):
            pixle[int(y)][int(x)] = self.f
            x += deltax
            y += deltay

class kruznica:

    def __init__(self, stred, polomer, farba):
        self.stred = stred
        self.polomer = polomer
        self.farba = farba
        
    def kresli(self):
        x = self.polomer
        y = 0
        err = 0
        while x >= y:
            pixle[self.stred[1] + y][self.stred[0] + x] = self.farba
            pixle[self.stred[1] + x][self.stred[0] + y] = self.farba
            pixle[self.stred[1] + x][self.stred[0] - y] = self.farba
            pixle[self.stred[1] + y][self.stred[0] - x] = self.farba
            pixle[self.stred[1] - y][self.stred[0] - x] = self.farba
            pixle[self.stred[1] - x][self.stred[0] - y] = self.farba
            pixle[self.stred[1] - x][self.stred[0] + y] = self.farba
            pixle[self.stred[1] - y][self.stred[0] + x] = self.farba
            if err <= 0:
                y += 1
                err += 2 * y + 1
            if err > 0:
                x -= 1
                err -= 2 * x + 1

class bezier:
    def __init__(self, P0, P1, P2, P3, farba):
        self.P0 = P0
        self.P1 = P1
        self.P2 = P2
        self.P3 = P3
        self.farba = farba
            
    def kresli(self):
        """P0 je zaciatocny bod, P3 je koncovy bod, P1 a P2 su kontrolne body. Krivka je definovana vztahom:
           B(t) = (1-t)^3*P0 + 3*t*(1-t)^2*P1 + 3*t^2*(1-t)*P2 + t^3*P3 (t ide od 0 po 1 a predstavuje kde medzi bodmi P0 a P3 sa nachadzame)."""
        
        for t in frange(0, 1, 0.002):
            Bx = (1 - t) ** 3 * self.P0[0] + 3 * (1 - t) ** 2 * t * self.P1[0] + 3 * (1 - t) * t ** 2 * self.P2[0] + t ** 3 * self.P3[0]
            By = (1 - t) ** 3 * self.P0[1] + 3 * (1 - t) ** 2 * t * self.P1[1] + 3 * (1 - t) * t ** 2 * self.P2[1] + t ** 3 * self.P3[1]
            pixle[int(By)][int(Bx)] = self.farba

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
        v =usecka(self.x, self.y + self.v + 10, self.x + self.s, self.y+ self.v +10, (sdl2.ext.Color(220, 100, 50)))
        v.kresli();
    def odznacenie(self):
        v = usecka(self.x, self.y + self.v + 10, self.x + self.s, self.y+ self.v +10, (sdl2.ext.Color(255, 255, 255)))  
        v.kresli()

def frange(start, end=None, inc=None):
    "A range function, that does accept float increments..."

    if end == None:
        end = start + 0.0
        start = 0.0

    if inc == None:
        inc = 1.0

    L = []
    while 1:
        next = start + len(L) * inc
        if inc > 0 and next >= end:
            break
        elif inc < 0 and next <= end:
            break
        L.append(next)
        
    return L

# tlacidla funkcii
t1 = tlacidlo(30, 50, 52, 52, "487144-200.png")
t2 = tlacidlo(90, 50, 52, 52, "568205.png")
t3 = tlacidlo(150, 50, 52, 52, "97511-200.png")
t4 = tlacidlo(210, 50, 52, 52, "pngtree-black-edit-icon-image_1130448.jpg")
t5 = tlacidlo(270, 50, 52, 52, "new.png")

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

# inicializacia SDL2
sdl2.ext.init()

# vytvor a zobraz okno
window = sdl2.ext.Window("cvicenie pokus o vektorovy editor", size=(800, 600))
window.show()

# priprav pristup na kreslenie do okna (pozadie okna vyfarbi na bielo)
plocha = window.get_surface()
sdl2.ext.fill(plocha, sdl2.ext.Color(255, 255, 255))
window.refresh()

# pole na kreslenie
pixle = sdl2.ext.PixelView(plocha)

vytvaramKruznicu = False
vytvaramUsecku = False
vytvaramKrivku = False

p0, p1, p2, p3 = 0, 0, 0, 0
r0, r1, r2, r3 = 0, 0, 0, 0

usecky = []
kruznice = []
krivky = []

oznacena_funkcia = 0
navbar = 150
aktualna_r, aktualna_g, aktualna_b = 0, 0, 0


# jednoduchy event loop
running = True
while running:
    # spracuvaj eventy
    events = sdl2.ext.get_events()
    for event in events:
        # zoznam klaves pozri na: https://wiki.libsdl.org/SDL_Scancode


            #kreslenie usecky
        if oznacena_funkcia == 1 and event.motion.y > navbar:
            if event.type == sdl2.SDL_MOUSEBUTTONDOWN and event.button.button == sdl2.SDL_BUTTON_LEFT:
                u = usecka(event.motion.x, event.motion.y, event.motion.x, event.motion.y,sdl2.ext.Color(aktualna_r, aktualna_g, aktualna_b))  
                usecky.append(u)
                vytvaramUsecku = True

            
           #kreslenie kruznice
        if oznacena_funkcia == 2 and event.motion.y > navbar:
            if event.type == sdl2.SDL_MOUSEBUTTONDOWN and event.button.button == sdl2.SDL_BUTTON_LEFT:
                k = kruznica((event.motion.x, event.motion.y), 200, sdl2.ext.Color(aktualna_r, aktualna_g, aktualna_b))  
                kruznice.append(k)
                vytvaramKruznicu = True

        if oznacena_funkcia == 3 and event.motion.y > navbar:
           #kreslenie bezierovej krivky
            if event.type == sdl2.SDL_MOUSEBUTTONDOWN and event.button.button == sdl2.SDL_BUTTON_LEFT and p0 != 0 and p1 != 0 and p2 != 0 and p3 == 0:
                p3 = event.motion.x
                r3 = event.motion.y
                print("p3, r3: "+ str(p3), str(r3))
                print(" \n" )
                b = bezier((p0, r0), (p1, r1), (p2, r2), (p3, r3), sdl2.ext.Color(aktualna_r, aktualna_g, aktualna_b))  
                krivky.append(b)
                vytvaramKrivku = True
                
            if event.type == sdl2.SDL_MOUSEBUTTONDOWN and event.button.button == sdl2.SDL_BUTTON_LEFT and p0 != 0  and p1 != 0 and p2 == 0 and p3 == 0:
                p2 = event.motion.x
                r2 = event.motion.y
                print("p2, r2: " +str(p2), str(r2))
            if event.type == sdl2.SDL_MOUSEBUTTONDOWN and event.button.button == sdl2.SDL_BUTTON_LEFT and p0 != 0 and p1 == 0 and p2 == 0 and p3 == 0:
                p1 = event.motion.x
                r1 = event.motion.y
                print("p1, r1: " + str(p1), str(r1))
            if event.type == sdl2.SDL_MOUSEBUTTONDOWN and event.button.button == sdl2.SDL_BUTTON_LEFT and p0 == 0 and p1 == 0 and p2 == 0 and p3 == 0:
                p0 = event.motion.x
                r0 = event.motion.y
                print("p0, r0: " +str(p0), str(r0))

            #editacia usecky
        if oznacena_funkcia == 4 and usecky !=[]:
            usecky[-1].x2 = event.motion.x
            usecky[-1].y2 = event.motion.y
            sdl2.ext.fill(plocha, sdl2.ext.Color(255, 255, 255))
            if event.type == sdl2.SDL_MOUSEBUTTONDOWN:
                oznacena_funkcia = 0
            for u in usecky:
                u.kresli()
            for k in kruznice:
                k.kresli()
            for k in krivky:
                k.kresli()   
                
            #editacia kruznice
#        if oznacena_funkcia == 4 and kruznice != []:
 #           kruznice[-1].polomer = abs(event.motion.x - kruznice[-1].stred[0])
  #          sdl2.ext.fill(plocha, sdl2.ext.Color(255, 255, 255))
   #         if event.type == sdl2.SDL_MOUSEBUTTONDOWN:
    #            oznacena_funkcia = 0
     #       for u in usecky:
      #          u.kresli()
       #     for k in kruznice:
        #        k.kresli()
         #   for k in krivky:
          #      k.kresli()

          #editacia krivky







           
           # window.refresh()
            p0, p1, p2, p3 = 0, 0, 0, 0
            r0, r1, r2, r3 = 0, 0, 0, 0
                
            #kreslenie usecky
        if event.type == sdl2.SDL_MOUSEMOTION and vytvaramUsecku:
            usecky[-1].x2 = event.motion.x
            usecky[-1].y2 = event.motion.y
            sdl2.ext.fill(plocha, sdl2.ext.Color(255, 255, 255))
            t1.oznacenie()
            
            for u in usecky:
                u.kresli()
            for k in kruznice:
                k.kresli()
            for k in krivky:
                k.kresli()   
           # window.refresh()

            #kreslenie kruznice 
        if event.type == sdl2.SDL_MOUSEMOTION and vytvaramKruznicu:
            kruznice[-1].polomer = abs(event.motion.x - kruznice[-1].stred[0])
            sdl2.ext.fill(plocha, sdl2.ext.Color(255, 255, 255))
            t2.oznacenie()

            for u in usecky:
                u.kresli()
            for k in kruznice:
                k.kresli()
            for k in krivky:
                k.kresli()
            #window.refresh()


            #kreslenie bezierovej krivky

        if event.type == sdl2.SDL_MOUSEBUTTONDOWN and vytvaramKrivku:
            sdl2.ext.fill(plocha, sdl2.ext.Color(255, 255, 255))
            t3.oznacenie()

            for u in usecky:
                u.kresli()
            for k in kruznice:
                k.kresli()
            for k in krivky:
                k.kresli()             
           # window.refresh()
            p0, p1, p2, p3 = 0, 0, 0, 0
            r0, r1, r2, r3 = 0, 0, 0, 0

        if event.type == sdl2.SDL_MOUSEBUTTONDOWN:
            #vyber funkcie
            if t1.zasah(event.motion.x, event.motion.y):
                oznacena_funkcia = 1
                t1.oznacenie()
                t2.odznacenie()
                t3.odznacenie()
                t4.odznacenie()


            if t2.zasah(event.motion.x, event.motion.y):
                oznacena_funkcia = 2
                t1.odznacenie()
                t2.oznacenie()
                t3.odznacenie()
                t4.odznacenie()
                    
            if t3.zasah(event.motion.x, event.motion.y):
                oznacena_funkcia = 3
                t1.odznacenie()
                t2.odznacenie()
                t3.oznacenie()
                t4.odznacenie()

            if t4.zasah(event.motion.x, event.motion.y):
                oznacena_funkcia = 4
                t1.odznacenie()
                t2.odznacenie()
                t3.odznacenie()
                t4.oznacenie()
                    
            if t5.zasah(event.motion.x, event.motion.y):
                usecky = []
                kruznice = []
                krivky = []

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
                
        if event.type == sdl2.SDL_MOUSEBUTTONUP and event.button.button == sdl2.SDL_BUTTON_LEFT:
            vytvaramUsecku = False
            vytvaramKruznicu = False
            vytvaramKrivku = False
            
        if event.type == sdl2.SDL_QUIT:             # event: quit
            running = False
            break
        
        #tlacidla funkcii
    t1.kresli(0, 0, 0)
    t2.kresli(0, 0, 0)
    t3.kresli(0, 0, 0)
    t4.kresli(0, 0, 0)
    t5.kresli(0, 0, 0)
    
    #tlacidla farieb
    f1.kresli(f1_r, f1_g, f1_b)
    f2.kresli(f2_r, f2_g, f2_b)
    f3.kresli(f3_r, f3_g, f3_b)
    f4.kresli(f4_r, f4_g, f4_b)
    f5.kresli(f5_r, f5_g, f5_b)
    
    window.refresh()
# uvolni alokovane zdroje
sdl2.ext.quit()

