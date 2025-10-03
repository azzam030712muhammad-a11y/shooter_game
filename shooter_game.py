#Create your own shooter
from pygame import *
from random import randint

win_width = 700
win_height = 500

window = display.set_mode((win_width, win_height))
display.set_caption('Galaxy War')
background = transform.scale(image.load('Galaxy2.jpg'), (700, 500))

clock = time.Clock()
FPS = 60

font.init()
font1 = font.SysFont('Arial', 36)
font2 = font.SysFont('Arial', 80)
win = font2.render('YOU WIN!', True, (255, 255, 255))
lose = font2.render('YOU LOSE!', True, (255, 0, 0))

mixer.init()
mixer.music.load('space.ogg')
mixer.music.play()
fire_sound = mixer.Sound('fire.ogg')

#Atur volume
mixer.music.set_volume(0.2)

# Statistic
score = 0
lost = 0

life = 10

class GameSprite(sprite.Sprite):
    def __init__(self, sprite_image, sprite_x, sprite_y, size_x, size_y, sprite_speed):
        super().__init__()
        self.image = transform.scale(image.load(sprite_image), (size_x, size_y))
        self.speed = sprite_speed
        self.rect = self.image.get_rect()
        self.rect.x = sprite_x
        self.rect.y = sprite_y

    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

class Player(GameSprite):
    def update(self):
        key_pressed = key.get_pressed()
        if key_pressed[K_LEFT] and self.rect.x > 5:
            self.rect.x -= self.speed

        if key_pressed[K_RIGHT] and self.rect.x < 685:
            self.rect.x += self.speed

    def fire(self):
        bullet = Bullet('bullet.png', self.rect.centerx, self.rect.top, 15, 20, -20)
        bullets.add(bullet)


class Enemy(GameSprite):
    def update(self):
        self.rect.y += self.speed
        global lost
        if self.rect.y > win_height:
            self.rect.x = randint(80, win_height - 80)
            self.rect.y = 0
            lost = lost + 1

class Asteroids(GameSprite):
    def update(self):
        self.rect.y += self.speed
        
        if self.rect.y > win_height:
            self.rect.x = randint(80, win_height - 80)
            self.rect.y = 0
            

    
    
         
            
class Bullet(GameSprite):
    def update(self):
        self.rect.y += self.speed
        if self.rect.y < 0:
            self.kill()






#Instance Gamesprite
player = Player('spaceship3.png', win_width/2, win_height - 100, 80, 100, 15 )

#Instance Enemy
monsters = sprite.Group()
for i in range(1, 6):
    monster = Enemy('ufo2.png', randint(80, win_width - 80), -40, 80, 50, randint(1, 5))
    monsters.add(monster)

asteroids = sprite.Group()
for i in range(1, 3):
    asteroid = Asteroids('asteroid.png', randint(80, win_width - 80), -40, 80, 50, randint(1, 5))
    asteroids.add(asteroid)

bullets = sprite.Group()

finish = False
game = True
while game:

    if not finish:
 
        window.blit(background, (0, 0))

        #Tampilkan text score & missed
        text_score = font1.render("Score:" + str(score), 1, (255, 255, 255))
        text_missed = font1.render("Missed:" + str(lost), 1, (255, 255, 255))
        text_life = font1.render("Life:" + str(life), 1, (255, 255, 255))
        window.blit(text_score, (10, 20))
        window.blit(text_missed, (10, 60))
        window.blit(text_life, (10, 100))


        player.reset()
        player.update()

        monsters.draw(window)
        monsters.update()

        asteroids.draw(window)
        asteroids.update()

        bullets.update()
        bullets.draw(window)

        collides = sprite.groupcollide(monsters, bullets, True, True)

        for collide in collides:
            score = score + 1
            monster = Enemy('ufo2.png', randint(80, win_width - 80), -40, 80, 50, randint(1, 5))
            monsters.add(monster)

        # if sprite.spritecollide(player, monsters, False) or lost >= 3:
        #     finish = True
        #     window.blit(lose, (200, 200))

        if sprite.spritecollide(player, monsters, False) or sprite.spritecollide(player, asteroids, False):
            sprite.spritecollide(player, monsters, True)  
            sprite.spritecollide(player, asteroids, True)

            life = life - 1

        if life == 0 or lost >= 5:
            finish = True
            window.blit(lose, (200, 200))


        
        if score >= 10:
            finish = True
            window.blit(win, (200, 200))

        display.update()
        clock.tick(FPS)

    else:
        finish = False
        score = 0
        lost = 0
        for b in bullets:
            b.kill()

        for m in monsters:
            m.kill()

        time.delay(3000)

        for i in range(1, 6):
            monster = Enemy('ufo2.png', randint(80, win_width - 80), -40, 80, 50, randint(1, 5))
            monsters.add(monster)

    for e in event.get():
        if e.type == QUIT:
            game = False

        elif e.type == KEYDOWN:
            if e.key == K_SPACE:
                fire_sound.play()
                player.fire()

    # Jeda lopping sekitar 0,05 detik (50 Mili Second)
    time.delay(50)




    
    
