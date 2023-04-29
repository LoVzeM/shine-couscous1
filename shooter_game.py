from pygame import *
from random import randint
mixer.init()
font.init()
mw = display.set_mode((700, 650))
display.set_caption('Space_Shooter')
BG = transform.scale(image.load('galaxy.jpg'), (700, 650))
win_txt = font.SysFont('Bauhaus 93', 70).render('YOU WIN', True, (10, 200, 10))
loose_txt = font.SysFont('Bauhaus 93', 70).render('YOU LOST', True, (200, 10, 10))
shot = mixer.Sound('fire.ogg')
kill = mixer.Sound('fire.ogg')
rocket_kill = mixer.Sound('inecraft_death.ogg')
mixer.music.load('inecraft_mutation.ogg')
mixer.music.load('fire.ogg')
mixer.music.play()
clock = time.Clock()
lost = 0
kills = 0

class GameSprite(sprite.Sprite):
    def __init__(self, x, y, w, h, pic, speed=0):
        super().__init__()
        self.image = transform.scale(image.load(pic), (w, h))
        self.rect = self.image.get_rect()
        self.speed = speed
        self.rect.x = x
        self.rect.y = y
    def reset(self):
        mw.blit(self.image, (self.rect.x, self.rect.y))

class Player(GameSprite):
    def update(self):
        keys = key.get_pressed()
        if keys[K_d] and self.rect.x < 650:
            self.rect.x += self.speed
        if keys[K_a] and self.rect.x > 0:
            self.rect.x -= self.speed
    def fire(self):
        bullets.add(Bullet(self.rect.centerx-5, self.rect.top, 10, 20, 'bullet.png', 5))
class Enemy(GameSprite):
    def update(self):
        global lost
        self.rect.y += self.speed
        if self.rect.y >= 650:
            self.kill()
            lost += 1
            enemies.add(Enemy(randint(10, 650), randint(-40, 0), 60, 40, 'ufo.png', randint(2, 5)))

class Asteroid(GameSprite):
    def update(self):
        self.rect.y += self.speed
        if self.rect.y >= 650:
            self.kill()
            asteroids.add(Enemy(randint(10, 650), randint(-40, 0), 60, 40, 'asteroid.png', randint(2, 5)))

class Bullet(GameSprite):
    def update(self):
        self.rect.y -= self.speed
        if self.rect.y <= 0:
            self.kill()

asteroids = sprite.Group()
bullets = sprite.Group()
enemies = sprite.Group()
rocket = Player(300, 580, 50, 70, 'rocket.png', 5)
for i in range(5):
    enemies.add(Enemy(randint(10, 650), randint(-40, 0), 60, 40, 'ufo.png', randint(2, 5)))
for i in range(2):
    asteroids.add(Asteroid(randint(10, 650), randint(-40, 0), 60, 40, 'asteroid.png',randint(2, 5)))    
run = True
finish = False

while run:
    for e in event.get():
        if e.type == QUIT:
            run = False
        if e.type == KEYDOWN:
            if e.key == K_SPACE:
                shot.play()
                rocket.fire()
    if not finish:
        lost_txt = font.SysFont('Showcard Gothic', 20).render('Lost:' + str(lost), True, (220, 220, 220))
        kills_txt = font.SysFont('Showcard Gothic', 20).render('Kills:' + str(kills), True, (220, 220, 220))
        mw.blit(BG, (0, 0))
        mw.blit(kills_txt, (10, 5))
        mw.blit(lost_txt, (10, 35))
        bullets.draw(mw)
        bullets.update()
        rocket.reset()
        rocket.update()
        enemies.draw(mw)
        enemies.update()
        asteroids.draw(mw)
        asteroids.update()

        if sprite.groupcollide(bullets, enemies, True, True): # обработка столкновений группы спрайтов с группой
            kill.play()
            enemies.add(Enemy(randint(10, 650), randint(-40, 0), 60, 40, 'ufo.png', randint(2, 5)))
            kills += 1
        if kills > 10:
            finish = True
            mw.blit(win_txt, (250, 200))
        if lost > 5:
            finish = True
            mw.blit(loose_txt, (250, 200))
        if sprite.spritecollide(rocket, enemies, False): # обработка столкновений одного спрайта с группой
            finish = True
            rocket_kill.play()
            mw.blit(loose_txt, (250, 200))
        if sprite.spritecollide(rocket, asteroids, False): 
            finish = True
            rocket_kill.play()
            mw.blit(loose_txt, (250, 200))    
    display.update()
    clock.tick(60)
