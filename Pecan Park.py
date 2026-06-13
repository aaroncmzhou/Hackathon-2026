import pygame as py
from random import randint, uniform

WIDTH, HEIGHT = 1500, 950
WALKSPEED = 5
JUMPPOWER = -15
screen = py.display.set_mode((WIDTH, HEIGHT))
confetti = []
confetti_end_time = 0
last_confetti_spawn_time = 0
global win
win = 0
py.display.set_caption("Pecan Park")

platforms = [
    [[500, 780, 70, 20], [550, 700, 950, 20], [600, 0, 900, 700]], #level 1
    [[700, 780, 50, 20], [500, 780, 50, 170], [550, 910, 50, 20]], #level 2
    [[0, 0, 1000, 750], [1300, 790, 25, 110], [0, 750, 1300, 150]], #level 3
    [[500, 800, 100, 150], [575, 775, 25, 25], [800, 780, 50, 20], [900, 700, 50, 20]], #level 4
    [[900, 800, 600, 150], [600, 700, 700, 20], [0, 700, 380, 20],], #level 5
    [[1100, 800, 600, 150], [600, 700, 700, 20], [550, 650, 20, 50], #level 6
     [480, 630, 20, 50], [410, 610, 20, 50], [320, 590, 20, 50], [0, 570, 220, 50], [1280, 660, 20, 40]], #level 6
    [[0, 750, 1300, 150]] #level 7
]
doors = [
    [550, 630, 50, 70], #level 1
    [700, 710, 50, 70], #level 2
    [1000, 680, 50, 70], #level 3
    [900, 630, 50, 70], #level 4
    [0, 630, 50, 70], #level 5
    [0, 500, 50, 70], #level 6
    [0, 680, 50, 70], #level 7
]
text = {
    "Get to the green door!" : (50, 500), # level 1
    "Stand on each other's heads to get on the platforms." : (500, 500), # level 2
    "CONSTRUCTION DRILL" : (350, 450), # level 3
    " " : (), # level 4
    "Wheeee" : (440, 500), # level 5
    "   " : (), # level 6
    "Both people jump while on each others heads-but not at the same time!" : (450, 500) # level 7
}
level_max_charges = [1.0, 1.0, 1.0, 1.0, 0.0, 1.0, 1.0]
level = 0
MAX_LEVELS = len(platforms)

py.init()
py.font.init()
font = py.font.SysFont(None, 36)

def load_next_level():
    """Loads the next level."""
    global level, confetti_end_time, win

    transition = py.Surface((WIDTH, HEIGHT))
    if level + 1 >= len(platforms):
        transition.fill((255, 127, 0))
    else:
        transition.fill((0, 0, 0))

    transparency = 0.0
    for frame in range(60):#60fps
        transparency += 4.25#4.25 = 255/60; I used this number because: 4.25 = total color limit / 60fps
        transition.set_alpha(min(int(transparency), 255))#cap at max opaqueness

        screen.fill((135, 206, 235))#normal blue background
        for plat in platforms[level]:
            py.draw.rect(screen, (100, 100, 100), py.Rect(plat[0], plat[1], plat[2], plat[3]))
        py.draw.rect(screen, (50, 255, 173), doors[level])
        player1.draw(screen, (255, 124, 5))
        player2.draw(screen, (71, 118, 137))
        if confetti:
            draw_confetti()
        draw_text()

        screen.blit(transition, (0, 0))#((0, 0))are the coordinites, it spans the entire screen, so it has to start at the orgin, (0, 0)
        py.display.flip()
        clock.tick(60)

    if level + 1 >= len(platforms):
        level = 0
        spawn_confetti()
        confetti_end_time = py.time.get_ticks()*1000
        win = 1
    else:
        level += 1 

    player1.max_charge = level_max_charges[level]
    player2.max_charge = level_max_charges[level]

        
    player1.pos = py.math.Vector2(250, 901)
    player1.rect.topleft = (player1.pos.x, player1.pos.y)
    player1.vel = py.math.Vector2(0, 0)
    
    player2.pos = py.math.Vector2(200, 901)
    player2.rect.topleft = (player2.pos.x, player2.pos.y)
    player2.vel = py.math.Vector2(0, 0)

    transparency = 255.0
    for frame in range(60):#again, 60fps
        transparency -= 4.25
        transition.set_alpha(max(int(transparency), 0))#cap at max transparency

        screen.fill((135, 206, 235))#normal blue background
        for plat in platforms[level]:
            py.draw.rect(screen, (100, 100, 100), py.Rect(plat[0], plat[1], plat[2], plat[3]))
        py.draw.rect(screen, (50, 255, 173), doors[level])
        player1.draw(screen, (255, 124, 5))
        player2.draw(screen, (71, 118, 137))
        if confetti:
            draw_confetti()
        draw_text()
            
        screen.blit(transition, (0, 0))
        py.display.flip()
        clock.tick(60)
    #py.event.clear()
    confetti_end_time = 0

def draw_text():
    """Draws level text."""
    all_sentences = list(text.keys())
    all_positions = list(text.values())
    if level < len(all_sentences):
        if all_sentences[level].strip() != "":
            text_surface = font.render(all_sentences[level], True, (255, 255, 255))
            text_rect = text_surface.get_rect(topleft=all_positions[level])
            screen.blit(text_surface, text_rect)
    if not win:
        counter_surface = font.render("Level " + str(level + 1), True, (255, 255, 255))
        counter_rect = counter_surface.get_rect(topleft=(5, 5))
        screen.blit(counter_surface, counter_rect)
    else:
        counter_surface = font.render("All Levels Complete!", True, (255, 127, 0))
        counter_rect = counter_surface.get_rect(topleft=(5, 5))
        screen.blit(counter_surface, counter_rect)

def spawn_confetti(number_of_confetti=1500):
    """Create a burst of confetti particles."""
    #confetti.clear()
    for _ in range(number_of_confetti):
        # spawn from near top of the result panel / center-ish
        x = randint(80, WIDTH - 80)
        y = randint(-100, -10)
        vx = uniform(-2.5, 2.5)
        vy = uniform(1.0, 4.0)
        size = randint(4, 8)
        color = (
            randint(80, 255),
            randint(80, 255),
            randint(80, 255)
        )
        confetti.append({"x": x, "y": y, "vx": vx, "vy": vy, "size": size, "color": color})

def update_confetti():
    """Move particles and apply simple gravity."""
    for p in confetti[:]:
        p["x"] += p["vx"]
        p["y"] += p["vy"]
        p["vy"] += 0.08  # gravity
        p["vx"] *= 0.99  # tiny air resistance
        if p["y"] >= HEIGHT:
            confetti.remove(p)

def draw_confetti():
    for p in confetti:
        py.draw.rect(
            screen,
            p["color"],
            py.Rect(int(p["x"]), int(p["y"]), p["size"], p["size"])
        )

class Player(py.sprite.Sprite):
    def __init__(self, start_x, start_y):
        super().__init__()
        self.image = py.Surface((25, 25))
        self.rect = self.image.get_rect()
        self.speed = WALKSPEED
        self.gravity = 0.8
        self.jump_power = JUMPPOWER

        self.pos = py.math.Vector2(start_x, start_y)
        self.vel = py.math.Vector2(0, 0)
        self.charge = 0.0
        self.max_charge = 1.0
        self.rect.topleft = (self.pos.x, self.pos.y)
        self.on_ground = False
        self.was_on_ground = False

    def handle_collisions(self, axis, other_player=None):
        current_platforms = platforms[level]
        for plat in current_platforms:
            tile_rect = py.Rect(plat[0], plat[1], plat[2], plat[3])
            self.collide_with_rect(tile_rect, axis)

        boundaries = [
            py.Rect(0, 927, 1500, 50),   #floor
            py.Rect(-5, 0, 5, 950),      #left
            py.Rect(1500, 0, 5, 950)     #right
        ]
        for boundary in boundaries:
            self.collide_with_rect(boundary, axis)
        if other_player:
            self.collide_with_rect(other_player.rect, axis)

    def collide_with_rect(self, tile_rect, axis):
        if self.rect.colliderect(tile_rect):
            if axis == 'x':
                if self.vel.x > 0:
                    self.rect.right = tile_rect.left
                elif self.vel.x < 0:
                    self.rect.left = tile_rect.right
                self.pos.x = self.rect.x
            if axis == 'y':
                if self.vel.y > 0:
                    self.rect.bottom = tile_rect.top
                    self.vel.y = 0
                    self.on_ground = True
                elif self.vel.y < 0:
                    self.rect.top = tile_rect.bottom
                    self.vel.y = 0
                self.pos.y = self.rect.y

    def update(self, arrows, other_player=None):
        keys = py.key.get_pressed()
        
        if arrows:
            self.vel.x = (keys[py.K_RIGHT] - keys[py.K_LEFT]) * self.speed
            jump_pressed = keys[py.K_UP]
            charge_pressed = keys[py.K_DOWN]
        else:
            self.vel.x = (keys[py.K_d] - keys[py.K_a]) * self.speed
            jump_pressed = keys[py.K_w]
            charge_pressed = keys[py.K_s]


        self.pos.x += self.vel.x
        self.rect.x = round(self.pos.x)
        self.handle_collisions("x", other_player)

        if jump_pressed and self.on_ground:
            self.vel.y = self.jump_power
            self.on_ground = False
        if charge_pressed:
            self.charge = min(self.charge + 0.1, self.max_charge)
            self.speed *= 0.5
        elif keys[py.K_LEFT] or keys[py.K_RIGHT]:
            self.speed += self.charge
            self.charge = max(self.charge - 0.07, 0.0)
        else:
            self.speed = 5
            
        self.vel.y += self.gravity
        self.pos.y += self.vel.y
        self.rect.y = round(self.pos.y)
        
        
        self.was_on_ground = self.on_ground
        self.was_velocity = self.vel.y
        self.on_ground = False
        self.handle_collisions("y", other_player)

        if self.on_ground and not self.was_on_ground and self.was_velocity > 1.0:
            land.play()

    def draw(self, surface, player_color):
        py.draw.rect(surface, player_color, self.rect)


clock = py.time.Clock()

py.mixer.music.load("denis-pavlov-music-game-music-puzzle-strategy-arcade-technology-301226.mp3")
py.mixer.music.play(-1, 0.0)

land = py.mixer.Sound("Stone_hit6.ogg")

player1 = Player(100, 300)
player2 = Player(200, 300)

running = True
while running:
    for event in py.event.get():
        if event.type == py.QUIT:
            running = False
        if event.type == py.MOUSEBUTTONDOWN and win:
            spawn_confetti()
    mouse_buttons = py.mouse.get_pressed()
    now = py.time.get_ticks()
    if win:
        if now - last_confetti_spawn_time >= 500:
            spawn_confetti(number_of_confetti=200)
            last_confetti_spawn_time = now

    player1.update(arrows=True, other_player=player2)
    player2.update(arrows=False, other_player=player1)

    current_door = doors[level]
    if player1.rect.colliderect(current_door) or player2.rect.colliderect(current_door):
        load_next_level()

    screen.fill((135, 206, 235))

    py.draw.rect(screen, (50, 255, 173), doors[level])
    
    # FIXED: This uses the list directly to create the rectangle
    for plat in platforms[level]:
        py.draw.rect(screen, (100, 100, 100), py.Rect(plat[0], plat[1], plat[2], plat[3]))

    #py.draw.rect(screen, (250, 236, 198), py.Rect(0, 930, 1500, 50))

    player1.draw(screen, (255, 124, 5))
    player2.draw(screen, (71, 118, 137))
    draw_text()
    if confetti:
        update_confetti()
        draw_confetti()
    py.display.flip()
    clock.tick(60)

py.quit()
exit()
