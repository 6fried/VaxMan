import pygame

black = (0, 0, 0)
white = (255, 255, 255)
blue = (0, 0, 255)
green = (0, 255, 0)
red = (255, 0, 0)
purple = (255, 0, 255)
yellow = (255, 255,   0)

class Wall(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height, color):
        pygame.sprite.Sprite.__init__(self)
        
        self.image = pygame.Surface([width, height])
        self.image.fill(color)
        
        self.rect = self.image.get_rect()
        self.rect.top = y
        self.rect.left = x

def setup_room_one(all_sprite_list):
    wall_list = pygame.sprite.RenderPlain()
    
    walls = [ [0,0,6,600],
              [0,0,600,6],
              [0,600,606,6],
              [600,0,6,606],
              [300,0,6,66],
              [60,60,186,6],
              [360,60,186,6],
              [60,120,66,6],
              [60,120,6,126],
              [180,120,246,6],
              [300,120,6,66],
              [480,120,66,6],
              [540,120,6,126],
              [120,180,126,6],
              [120,180,6,126],
              [360,180,126,6],
              [480,180,6,126],
              [180,240,6,126],
              [180,360,246,6],
              [420,240,6,126],
              [240,240,42,6],
              [324,240,42,6],
              [240,240,6,66],
              [240,300,126,6],
              [360,240,6,66],
              [0,300,66,6],
              [540,300,66,6],
              [60,360,66,6],
              [60,360,6,186],
              [480,360,66,6],
              [540,360,6,186],
              [120,420,366,6],
              [120,420,6,66],
              [480,420,6,66],
              [180,480,246,6],
              [300,480,6,66],
              [120,540,126,6],
              [360,540,126,6]
            ]

    for i in walls:
        wall = Wall(i[0], i[1], i[2], i[3], blue)
        wall_list.add(wall)
        all_sprite_list.add(wall)
    
    return wall_list

def setup_gate(all_sprite_list):
    gate = pygame.sprite.RenderPlain()
    gate.add(Wall(282, 242, 42, 2, white))
    all_sprite_list.add(gate)
    return gate

class Block(pygame.sprite.Sprite):
    def __init__(self, color, width, height):
        pygame.sprite.Sprite.__init__(self)
        
        self.image = pygame.Surface([width, height])
        self.image.fill(white)
        self.image.set_colorkey(white)
        pygame.draw.ellipse(self.image, color, [0, 0, width, height])
        
        self.rect = self.image.get_rect()

class Player(pygame.sprite.Sprite):
    vx = 0
    vy = 0
    
    def __init__(self, x, y, filename):
        pygame.sprite.Sprite.__init__(self)
        
        self.image = pygame.image.load(filename).convert()
        
        self.rect = self.image.get_rect()
        self.rect.top = y
        self.rect.left = x
        self.prev_x = x
        self.prev_y = y
        
    def prevdirection(self):
        self.prev_x = self.vx
        self.prev_y = self.vy

    def changespeed(self, x, y):
        self.vx+=x
        self.vy+=y
        
    def update(self, walls, gate):
        old_x=self.rect.left
        new_x=old_x+self.vx
        self.rect.left = new_x
        
        old_y=self.rect.top
        new_y=old_y+self.vy
        
        x_collide = pygame.sprite.spritecollide(self, walls, False)
        if x_collide:
            self.rect.left = old_x
        else:
            self.rect.top = new_y
            y_collide = pygame.sprite.spritecollide(self, walls, False)
            if y_collide:
                self.rect.top = old_y
        
        if gate != False:
            gate_hit = pygame.sprite.spritecollide(self, gate, False)
            if gate_hit:
                self.rect.left = old_x
                self.rect.top = old_y

class Ghost(Player):
    def __init__(self, x, y, filename, name):
        super().__init__(x, y, filename)
        self.name = name
        self.turn = 0
        self.steps = 0

    def changespeed(self,list,ghost,turn,steps,l):
        try:
            z=list[turn][2]
            if steps < z:
                self.vx=list[turn][0]
                self.vy=list[turn][1]
                steps+=1
            else:
                if turn < l:
                    turn+=1
                elif ghost == "clyde":
                    turn = 2
                else:
                    turn = 0
                self.vx=list[turn][0]
                self.vy=list[turn][1]
                steps = 0
            return [turn,steps]
        except IndexError:
            return [0,0]

Pinky_directions = [
[0,-30,4],
[15,0,9],
[0,15,11],
[-15,0,23],
[0,15,7],
[15,0,3],
[0,-15,3],
[15,0,19],
[0,15,3],
[15,0,3],
[0,15,3],
[15,0,3],
[0,-15,15],
[-15,0,7],
[0,15,3],
[-15,0,19],
[0,-15,11],
[15,0,9]
]

Blinky_directions = [
[0,-15,4],
[15,0,9],
[0,15,11],
[15,0,3],
[0,15,7],
[-15,0,11],
[0,15,3],
[15,0,15],
[0,-15,15],
[15,0,3],
[0,-15,11],
[-15,0,3],
[0,-15,11],
[-15,0,3],
[0,-15,3],
[-15,0,7],
[0,-15,3],
[15,0,15],
[0,15,15],
[-15,0,3],
[0,15,3],
[-15,0,3],
[0,-15,7],
[-15,0,3],
[0,15,7],
[-15,0,11],
[0,-15,7],
[15,0,5]
]

Inky_directions = [
[30,0,2],
[0,-15,4],
[15,0,10],
[0,15,7],
[15,0,3],
[0,-15,3],
[15,0,3],
[0,-15,15],
[-15,0,15],
[0,15,3],
[15,0,15],
[0,15,11],
[-15,0,3],
[0,-15,7],
[-15,0,11],
[0,15,3],
[-15,0,11],
[0,15,7],
[-15,0,3],
[0,-15,3],
[-15,0,3],
[0,-15,15],
[15,0,15],
[0,15,3],
[-15,0,15],
[0,15,11],
[15,0,3],
[0,-15,11],
[15,0,11],
[0,15,3],
[15,0,1],
]

Clyde_directions = [
[-30,0,2],
[0,-15,4],
[15,0,5],
[0,15,7],
[-15,0,11],
[0,-15,7],
[-15,0,3],
[0,15,7],
[-15,0,7],
[0,15,15],
[15,0,15],
[0,-15,3],
[-15,0,11],
[0,-15,7],
[15,0,3],
[0,-15,11],
[15,0,9],
]

pl = len(Pinky_directions)-1
bl = len(Blinky_directions)-1
il = len(Inky_directions)-1
cl = len(Clyde_directions)-1



pygame.init()
screen = pygame.display.set_mode([606, 606])
pygame.display.set_caption('Pacman')

background = pygame.Surface(screen.get_size())
background = background.convert()
background.fill(black)

clock = pygame.time.Clock()

font = pygame.font.SysFont(None, 24)

DUPLICATE = pygame.USEREVENT + 1
pygame.time.set_timer(DUPLICATE, 30000)


w = 303-16  # Width
p_h = (7*60)+19  # Pacman height
m_h = (4*60)+19  # Monster height
b_h = (3*60)+19  # Binky height
i_w = 303-16-32  # Inky width
c_w = 303+(32-16)  # Clyde width


def start_game():
    all_sprites_list = pygame.sprite.RenderPlain()
    block_list = pygame.sprite.RenderPlain()
    monsta_list = pygame.sprite.RenderPlain()
    player_collide = pygame.sprite.RenderPlain()
    wall_list = setup_room_one(all_sprites_list)
    gate = setup_gate(all_sprites_list)

    p_turn = 0
    p_steps = 0

    b_turn = 0
    b_steps = 0

    i_turn = 0
    i_steps = 0

    c_turn = 0
    c_steps = 0

    player = Player(w, p_h, "images/Pacman.png")
    all_sprites_list.add(player)
    player_collide.add(player)
    
    Blinky=Ghost( w, b_h, "images/Blinky.png", "Blinky")
    monsta_list.add(Blinky)
    all_sprites_list.add(Blinky)

    Pinky=Ghost( w, m_h, "images/Pinky.png", "Pinky")
    monsta_list.add(Pinky)
    all_sprites_list.add(Pinky)
    
    Inky=Ghost( i_w, m_h, "images/Inky.png" , "Inky")
    monsta_list.add(Inky)
    all_sprites_list.add(Inky)
    
    Clyde=Ghost( c_w, m_h, "images/Clyde.png" , "Clyde")
    monsta_list.add(Clyde)
    all_sprites_list.add(Clyde)

    for row in range(19):
        for column in range(19):
            if (row in [7, 8]) and (column in [8, 9, 10]):
                continue
            else:
                block = Block(yellow, 4, 4)
                
                block.rect.x = (30 * column + 6) + 26
                block.rect.y = (30 * row + 6) + 26
                
                b_collide = pygame.sprite.spritecollide(block, wall_list, False)
                p_collide = pygame.sprite.spritecollide(block, player_collide, False)
                if b_collide or p_collide:
                    continue
                else:
                    block_list.add(block)
                    all_sprites_list.add(block)

    block_lenght = len(block_list)
    
    score = 0
    
    done = False
    
    while not done:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    player.changespeed(-30,0)
                if event.key == pygame.K_RIGHT:
                    player.changespeed(30,0)
                if event.key == pygame.K_UP:
                    player.changespeed(0,-30)
                if event.key == pygame.K_DOWN:
                    player.changespeed(0,30)

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT:
                    player.changespeed(30,0)
                if event.key == pygame.K_RIGHT:
                    player.changespeed(-30,0)
                if event.key == pygame.K_UP:
                    player.changespeed(0,30)
                if event.key == pygame.K_DOWN:
                    player.changespeed(0,-30)

            if event.type == DUPLICATE:
                for ghost in monsta_list:
                    if ghost.name == "Blinky":
                        clone = Ghost( w, b_h, "images/Blinky.png", "Blinky")
                        monsta_list.add(clone)
                        all_sprites_list.add(clone)
                    elif ghost.name == "Pinky":
                        clone = Ghost(w, m_h, "images/Pinky.png", "Pinky")
                        monsta_list.add(clone)
                        all_sprites_list.add(clone)
                    elif ghost.name == "Inky":
                        clone = Ghost(i_w, m_h, "images/Inky.png", "Inky")
                        monsta_list.add(clone)
                        all_sprites_list.add(clone)
                    elif ghost.name == "Clyde":
                        clone = Ghost(c_w, m_h, "images/Clyde.png", "Clyde")
                        monsta_list.add(clone)
                        all_sprites_list.add(clone)

        player.update(wall_list, gate)

        for ghost in monsta_list:
            if ghost.name == "Blinky":
                blinky_speed = ghost.changespeed(Blinky_directions,False,ghost.turn,ghost.steps,bl)
                ghost.turn = blinky_speed[0]
                ghost.steps = blinky_speed[1]
                ghost.changespeed(Blinky_directions,False,ghost.turn,ghost.steps,bl)
                ghost.update(wall_list,False)

            elif ghost.name == "Pinky":
                pinky_speed = ghost.changespeed(Pinky_directions, False, ghost.turn, ghost.steps, pl)
                ghost.turn = pinky_speed[0]
                ghost.steps = pinky_speed[1]
                ghost.changespeed(Pinky_directions,False,ghost.turn,ghost.steps,pl)
                ghost.update(wall_list,False)

            elif ghost.name == "Inky":
                inky_speed = ghost.changespeed(Inky_directions,False,ghost.turn,ghost.steps,il)
                ghost.turn = inky_speed[0]
                ghost.steps = inky_speed[1]
                ghost.changespeed(Inky_directions,False,ghost.turn,ghost.steps,il)
                ghost.update(wall_list,False)

            elif ghost.name == "Clyde":
                clyde_speed = ghost.changespeed(Clyde_directions,"clyde",ghost.turn,ghost.steps,cl)
                ghost.turn = clyde_speed[0]
                ghost.steps = clyde_speed[1]
                ghost.changespeed(Clyde_directions,"clyde",ghost.turn,ghost.steps,cl)
                ghost.update(wall_list,False)

        blocks_hit_list = pygame.sprite.spritecollide(player, block_list, True)
        
        if len(blocks_hit_list) > 0:
            score += len(blocks_hit_list)
                
        screen.fill(black)
        wall_list.draw(screen)
        gate.draw(screen)
        all_sprites_list.draw(screen)
        
        score_text = font.render("Score: " + str(score) + "/" + str(block_lenght), True, white)
        screen.blit(score_text, [10, 10])

        if score == block_lenght:
            do_next("Congratulations, you won!",145,all_sprites_list,block_list,monsta_list,player_collide,wall_list,gate)
        

        pygame.sprite.spritecollide(player, monsta_list, True)
        if len(monsta_list) > 32 or len(monsta_list) == 0:
            do_next("Game Over",235,all_sprites_list,block_list,monsta_list,player_collide,wall_list,gate)

        pygame.display.flip()

        clock.tick(10)

def do_next(message,x,all_sprites_list,block_list,monsta_list,player_collide,wall_list,gate):
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
              pygame.quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                if event.key == pygame.K_RETURN:
                    del all_sprites_list
                    del block_list
                    del monsta_list
                    del player_collide
                    del wall_list
                    del gate
                    start_game()

        w = pygame.Surface((400,200))
        w.set_alpha(10)
        w.fill((128,128,128))
        screen.blit(w, (100,200))

        text1=font.render(message, True, white)
        screen.blit(text1, [x, 233])

        text2=font.render("To play again, press ENTER.", True, white)
        screen.blit(text2, [135, 303])
        text3=font.render("To quit, press ESCAPE.", True, white)
        screen.blit(text3, [165, 333])

        pygame.display.flip()

        clock.tick(10)


start_game()
pygame.quit()