from pygame import*
from random import randint
from time import time as timer
'''Необходимые классы'''
font.init()
font1 = font.SysFont('Arial', 80)
win = font1.render('YOU WIN!', True, (255, 215, 0))
lose = font1.render('YOU LOSE!', True, (180, 0, 0))
font2 = font.SysFont('Arial', 36)

#kartinki
img_back = "galaxy.jpg"
img_hero = "rocket.png"
img_bullet = "bullet.png"
img_enemy = "ufo.png"
img_ast = "asteroid.png"
score = 0
lost = 0
goal = 10  
max_lost = 3 
life = 3
#класс-родитель для спрайтов
class GameSprite(sprite.Sprite):
    #конструктор
    def __init__(self, player_image, player_x, player_y, size_x, size_y, player_speed):
        super().__init__()
        # каждый спрайт должен хранить свойство image - изображение
        self.image = transform.scale(image.load(player_image), (size_x, size_y))
        self.speed = player_speed
        # каждый спрайт должен хранить свойство rect - прямоугольник, в который он вписан
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y

    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

#класс-наследник для спрайта-игрока 
class Player(GameSprite):
    def update(self):
        keys = key.get_pressed()
        if keys[K_LEFT] and self.rect.x > 5:
            self.rect.x -= self.speed
        if keys[K_RIGHT] and self.rect.x < win_width - 80:
            self.rect.x += self.speed
    #vistrel
    def fire(self):
        bullet = Bullet(img_bullet, self.rect.centerx, self.rect.top, 15, 20, -15)
        bullets.add(bullet)

#vrag
class Enemy(GameSprite):
    #dvizhenie vraga
    def update(self):
        self.rect.y += self.speed
        global lost
        #ischezaet esli doidet do konca
        if self.rect.y > win_height:
            self.rect.x + randint(80, win_width - 80)
            self.rect.y = 0
            lost = lost + 1

#pulya
class Bullet(GameSprite):
    #vragdvizh
    def update(self):
        self.rect.y += self.speed
        #ischezaet esli do konca 
        if self.rect.y < 0:
            self.kill()      

#Игровая сцена:
win_width = 700
win_height = 500
window = display.set_mode((win_width, win_height))
display.set_caption("Star Wars")
background = transform.scale(image.load("galaxy.jpg"), (win_width, win_height))

#Персонажи игры:
ship = Player('rocket.png', 5, win_height - 80,65,65, 15)

monsters = sprite.Group()
for i in range(1,6):
    monster = Enemy(img_enemy, randint(80, win_width - 80), -40, 80, 50, randint(1, 5))
    monsters.add(monster)
#asteroid
asteroids = sprite.Group()
for i in range(1, 3):
    asteroid = Enemy(img_ast, randint(30, win_height - 30), -40, 80, 50, randint(1,7))
    asteroids.add(asteroid)

bullets = sprite.Group()

#peremennaya
finish = False
#osnovnoicikl
run = True

rel_time = False 

num_fire = 0 

while run:
    #sobitie
    for e in event.get():
        if e.type == QUIT:
            run = False
        #sobitie probel
        elif e.type == KEYDOWN:
            if e.key == K_SPACE:
                #proveryaem
                if num_fire < 5 and rel_time == False:
                    num_fire = num_fire + 1
                    # fire_sound.play
                    ship.fire()

                if num_fire >= 5 and rel_time == False : #маленькийбабиджонмаленькийбабиджон
                    last_time = timer() #ктоподскажеткторасскажет
                    rel_time = True #гдежеонгдежеон
                
    
    if not finish:
        #obnovlyaem fon
        window.blit(background,(0,0))

        #pishem tekst
        text = font2.render("Счет: " +str(score), 1, (255, 255, 255))
        window.blit(text, (10, 20))
        text_lose = font2.render("Пропущено: " + str(lost), 1, (255, 255, 255))
        window.blit(text_lose, (10, 50))

        #proizvodim dvizhenie
        ship.update()
        monsters.update()
        asteroids.update()
        bullets.update()

        #obnovlyaem
        ship.reset()
        monsters.draw(window)
        asteroids.draw(window)
        bullets.draw(window)
        
        #perezarydka
        if rel_time == True:
            now_time = timer() #hthfhx

            if now_time - last_time < 3: #pokaneproidet3sek
                reload = font2.render('Перезаряжаюсь', 1, (150, 0, 0))
                window.blit(reload, (260, 460))
            else:
                num_fire = 0 #obnulyaem
                rel_time = False #sbrasivaem

        #proverkastolknpuli
        collides = sprite.groupcollide(monsters, bullets, True, True)
        for c in collides:
            #tambovskiybaron
            score = score + 1
            monster = Enemy(img_enemy, randint(80, win_width - 80), -40, 80, 50, randint(1, 5))
            monsters.add(monster)

        #eslispraitkosnulsa
        if sprite.spritecollide(ship, monsters, False) or sprite.spritecollide(ship, asteroids, False):
            sprite.spritecollide(ship,monsters, True)
            sprite.spritecollide(ship, asteroids, True)
            life = life -1
    
        #sliv
        if life == 0 or lost >= max_lost:
            finish = True #esliviproigrali
            window.blit(lose, (200, 200))

        #proverkawin
        if score >= goal:
            finish = True
            window.blit(win, (200, 200))
        
  

        #cvet
        if life == 3:
            life_color = (0, 150, 0)
        if life == 2:
            life_color = (150, 150, 0)
        if life == 1:
            life_color = (150, 0, 0)
        
        text_life = font1.render(str(life), 1, life_color)
        window.blit(text_life, (650, 10))

        display.update()

    #bonus
    else:
        finish = False
        score = 0
        lost = 0
        num_fire = 0
        life = 3
        for b in bullets:
            b.kill()
        for m in monsters:
            m.kill()
        for a in asteroids:
            a.kill()

        time.delay(3000) 
        for i in range(1, 6):
            monster = Enemy(img_enemy, randint(80, win_width - 80), -40, 80, 50, randint(1,5))
            monsters.add(monster)
        for i in range(1, 3):
            asteroid = Enemy(img_ast, randint(30, win_width - 30), -40, 80, 50, randint(1, 7))
            asteroids.add(asteroid)

    time.delay(50)

