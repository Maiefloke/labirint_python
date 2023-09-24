from pygame import *


'''Необхідні класи'''
 
#клас-батько для спрайтів
class GameSprite(sprite.Sprite):
    #конструктор класу
    def __init__(self, player_image, player_x, player_y, player_speed, width=65, haight=65):
        super().__init__()
        #кожен спрайт повинен зберігати властивість image - зображення
        self.image = transform.scale(image.load(player_image), (width, haight))
        self.speed = player_speed
        #кожен спрайт повинен зберігати властивість rect - прямокутник, в який він вписаний
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y
 
    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))


class Player(GameSprite):
    def update(self):
        keys = key.get_pressed()
        if keys[K_LEFT] and self.rect.x > 5:
            self.rect.x -= self.speed
        if keys[K_RIGHT] and self.rect.x < win_width - 80:
            self.rect.x += self.speed
        if keys[K_UP] and self.rect.y > 5:
            self.rect.y -= self.speed
        if keys[K_DOWN] and self.rect.y < win_height - 80:
            self.rect.y += self.speed


class Enemy(GameSprite):

    def update(self):
        if self.rect.x <= 170:
            self.direction = "right"

        if self.rect.x >= 600:
            self.direction = "left"

        if self.direction == "left":
            self.rect.x -= self.speed
        else:
            self.rect.x += self.speed

class Wall(sprite.Sprite):
    def __init__(self, color_1, color_2, color_3, wall_x, wall_y, wall_width, wall_haight):
        super().__init__()
        self.color_1 = color_1
        self.color_2 = color_2
        self.color_3 = color_3
        self.width = wall_width
        self.haight = wall_haight
        self.image = Surface((self.width, self.haight))
        self.image.fill((color_1, color_2, color_3))
        self.rect = self.image.get_rect()
        self.rect.x = wall_x
        self.rect.y = wall_y
    
    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))


#Ігрова сцена:
win_width = 700
win_height = 500
 
window = display.set_mode((win_width, win_height))
display.set_caption("Backroom")
background = transform.scale(image.load("bk.jfif"), (win_width, win_height))
 
#Персонажі гри:
player = Player('hero2.png', 30, win_height - 80, 10)
monster = Enemy('enemy2.png', win_width - 80, 280, 2)
final = GameSprite('exit.jfif', win_width - 120, win_height - 80, 0)
win = GameSprite('win.jfif', 50, 70, 0, 612, 344)


walls = [
    Wall(7, 242, 76, 0, 50, 500, 10),
    Wall(7, 242, 76, 150, 150, 10, 350),
    Wall(7, 242, 76, 250, 350, 500, 10),

]


game = True
clock = time.Clock()
FPS = 60
finish = False


#музика
mixer.init() # Створює музичний плеєр
mixer.music.load('mus.mp3') # завантажує музику
mixer.music.play() # зациклює і програє її
 
font.init()
f = font.Font(None, 70)
win_text = f.render("YOU WIN!!!", True, (255, 215, 0))
lose_text = f.render("YOU LOSE!!!", True, (100, 0, 0))

while game:
    for e in event.get():
        if e.type == QUIT:
            game = False

    window.blit(background,(0, 0))

    if finish != True:
        player.reset()
        monster.reset()
        final.reset()
        for wall in walls:
            wall.reset()

        player.update()
        monster.update()

    
    for w in walls:
        w.reset()
        if player.rect.colliderect(monster.rect) or player.rect.colliderect(w.rect):
            finish = True
            window.blit(lose_text, (200, 200))
            mixer.music.stop()
            
            
            

    if player.rect.colliderect(final.rect):
        finish = True
        window.blit(win_text, (200, 200))
        mixer.music.stop()

    display.update()
    clock.tick(FPS)
