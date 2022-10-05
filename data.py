import pygame


pygame.init()


score = 0
start_time = pygame.time.get_ticks()


ACTIVE = 1
MENU = 2
FAIL = 3
game_status = MENU


SPAN_MAOYU = pygame.USEREVENT + 1
pygame.time.set_timer(SPAN_MAOYU, 1000)



def updateScore() :
    global score
    score = (pygame.time.get_ticks() - start_time) // 100


def resetScore() :
    global score, start_time
    score = 0
    start_time = pygame.time.get_ticks()