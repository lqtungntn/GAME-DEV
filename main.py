import pygame
import os
import random

pygame.font.init()
pygame.mixer.init()

WIDTH, HEIGHT = 960, 600
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('HIT ZOMBIE!!!')
FPS = 60
MAP = pygame.transform.scale(pygame.image.load(
    os.path.join('Assets', 'Night.png')), (WIDTH, HEIGHT))
MOUSE = pygame.transform.scale(pygame.image.load(
    os.path.join('Assets', 'Mouse', 'Hammer.png')), (40, 75))
HIT_IMAGE = pygame.transform.scale(pygame.image.load(
    os.path.join('Assets', 'Hit.png')), (50, 50))
FONT = pygame.font.SysFont('comicsans', 40)
hit_mixer = pygame.mixer.Sound('Sound\\Hit.wav')
bg_mixer = pygame.mixer.Sound('Sound\\background.mp3')
hit_mixer.set_volume(0.25)
hit, miss = 0, 0
BOARD = [225, 125]
RANDOM = 0
TOMBSTONE_LIST = []
POW_LIST = []
CHECK = [False for i in range(0, 45)]
frame_count = 0
mouse_delay_count = 0
eventx, eventy = 0, 0
onHit = False
DeadList = [0 for i in range(0, 45)]
class Zombie(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.appear = []
        self.appear.append(pygame.image.load('Assets\\Zombie\\Zombie_1.png'))
        self.appear.append(pygame.image.load('Assets\\Zombie\\Zombie_2.png'))
        self.appear.append(pygame.image.load('Assets\\Zombie\\Zombie_3.png'))
        self.appear.append(pygame.image.load('Assets\\Zombie\\Zombie_4.png'))
        self.appear.append(pygame.image.load('Assets\\Zombie\\Zombie_5.png'))
        self.appear.append(pygame.image.load('Assets\\Zombie\\Zombie_6.png'))
        self.appear.append(pygame.image.load('Assets\\Zombie\\Zombie_7.png'))
        self.appear.append(pygame.image.load('Assets\\Zombie\\Zombie_8.png'))
        self.dead = []
        self.dead.append(pygame.image.load('Assets\\Zombie\\Zombie_Dead_1.png'))
        self.dead.append(pygame.image.load('Assets\\Zombie\\Zombie_Dead_2.png'))
        self.dead.append(pygame.image.load('Assets\\Zombie\\Zombie_Dead_3.png'))
        self.dead.append(pygame.image.load('Assets\\Zombie\\Zombie_Dead_4.png'))
        self.dead.append(pygame.image.load('Assets\\Zombie\\Zombie_Dead_5.png'))
        self.dead.append(pygame.image.load('Assets\\Zombie\\Zombie_Dead_6.png'))

    def update_appear(self, frame):
        return self.appear[frame]

    def update_dead(self, frame):
        return self.dead[frame]
def draw_mouse_cursor():
    global mouse_delay_count
    global MOUSE
    mouse_copy = MOUSE.copy()
    if mouse_delay_count > 0:
        if mouse_delay_count > FPS // 4:
            mouse_copy = pygame.transform.rotate(mouse_copy, 6 * (FPS // 2 - mouse_delay_count))
        else:
            mouse_copy = pygame.transform.rotate(mouse_copy, 6 * (mouse_delay_count))
        mouse_delay_count -= 1
    mx, my = pygame.mouse.get_pos()
    WIN.blit(mouse_copy, (mx, my))


def draw_pow(pos):
    hit_image_copy = HIT_IMAGE.copy()
    WIN.blit(hit_image_copy, pos)

def draw_tomestone(pos):
    tombstone_copy = Zombie()
    pic_pos = WIN.blit(tombstone_copy.update_appear(7), pos)
    if pic_pos.collidepoint(eventx, eventy):
        return True
    return False

def draw_appear_zombie(pos, frame):
    zombie_copy = Zombie()
    WIN.blit(zombie_copy.update_appear(int(frame)), pos)

def draw_dead_zombie(pos, frame):
    zombie_copy = Zombie()
    WIN.blit(zombie_copy.update_dead(int(frame)), pos)

def draw_background():
    global hit, miss, onHit
    # draw map
    WIN.blit(MAP, (0, 0))
    # draw hit counter
    hit_text = FONT.render("HIT: " + str(hit), 1, (255, 0, 0)) # red
    WIN.blit(hit_text, (10, 10))
    # draw miss counter
    miss_text = FONT.render("MISS: " + str(miss), 1, (255, 0, 0)) # red
    WIN.blit(miss_text, (10, 60))

    DEL_LIST = []
    hit_image = False

    for idx in range(len(TOMBSTONE_LIST)):
        if TOMBSTONE_LIST[idx][1] <= 60 and TOMBSTONE_LIST[idx][1] > 0:
            TOMBSTONE_LIST[idx][1] -= 1
            if DeadList[idx] > 0:
                draw_dead_zombie([BOARD[0] + (TOMBSTONE_LIST[idx][0] % 9)*75, BOARD[1] + (TOMBSTONE_LIST[idx][0] // 9)*75], (6 / FPS) * (FPS - DeadList[idx]))
                DeadList[idx] -= 1
            elif DeadList[idx] == 0:
                draw_appear_zombie([BOARD[0] + (TOMBSTONE_LIST[idx][0] % 9) * 75, BOARD[1] + (TOMBSTONE_LIST[idx][0] // 9) * 75], (8 / FPS) * (TOMBSTONE_LIST[idx][1] - 1))
        elif TOMBSTONE_LIST[idx][1] != 0 and TOMBSTONE_LIST[idx][2]:
            if TOMBSTONE_LIST[idx][1] <= 300:
                check_hit = draw_tomestone([BOARD[0] + (TOMBSTONE_LIST[idx][0] % 9)*75, BOARD[1] + (TOMBSTONE_LIST[idx][0] // 9)*75])
                if check_hit:
                    TOMBSTONE_LIST[idx][2] = False
                    hit_image = True
                    POW_LIST.append([[eventx, eventy], FPS])
                    DeadList[idx] = FPS
                    TOMBSTONE_LIST[idx][1] = FPS + 1
            else:
                draw_appear_zombie([BOARD[0] + (TOMBSTONE_LIST[idx][0] % 9)*75, BOARD[1] + (TOMBSTONE_LIST[idx][0] // 9)*75], (8 / FPS) * (360 - TOMBSTONE_LIST[idx][1]))
            TOMBSTONE_LIST[idx][1] -= 1
        elif TOMBSTONE_LIST[idx][1] <= 0:
            DEL_LIST.append(idx)
        elif TOMBSTONE_LIST[idx][2] == False:
            TOMBSTONE_LIST[idx][1] -= 1


    for idx in DEL_LIST:
        CHECK[TOMBSTONE_LIST[idx][0]] = False
        del TOMBSTONE_LIST[idx]

    DEL_POW = []
    for idx in range(len(POW_LIST)):
        POW_LIST[idx][1] -= 1
        draw_pow(POW_LIST[idx][0])
        if (POW_LIST[idx][1] <= 0):
            DEL_POW.append(idx)

    for idx in DEL_POW:
        if (idx < len(POW_LIST)):
            del POW_LIST[idx]

    if onHit:
        if hit_image:
            hit += 1
        else:
            miss += 1
        onHit = False

    # draw mouse cursor
    draw_mouse_cursor()

    pygame.display.update()

def main():
    global frame_count
    global mouse_delay_count
    global eventx, eventy, onHit
    run = True
    bg_mixer.play(-1)
    clock = pygame.time.Clock()
    pygame.mouse.set_visible(False)

    while run:
        #input
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.MOUSEBUTTONUP and event.button == 1 and mouse_delay_count == 0:
                mouse_delay_count = FPS // 2
                eventx, eventy = event.pos
                onHit = True
                hit_mixer.play()

        #update
        frame_count += 1
        if frame_count % (FPS // 2) == 0:
            RANDOM = random.randint(0, 44)
            while ((CHECK[RANDOM]) and (CHECK.count(False) != 0)):
                RANDOM = random.randint(0, 44)
            CHECK[RANDOM] = True
            TOMBSTONE_LIST.append([RANDOM, 360, True])
        elif frame_count == FPS:
            frame_count = 0
        draw_background()

if __name__ == "__main__":
    pygame.init()
    main()
    pygame.quit()