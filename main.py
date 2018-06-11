#
import pygame,random,sys,time
from pygame.locals import *
from settings import *


egg = pygame.image.load(egg_image_name)
funnel = pygame.image.load(funnel_image_name)
egg_rect = egg.get_rect()
funnel_rect = funnel.get_rect()
funnel_rect.top = funnel_pos_y
assert (funnel_rect.height + funnel_pos_y) < SCsize[1],'funnel is too big'
points = 0
eggs_on_screen = []
screen_rect = pygame.Rect(0,0,SCsize[0],SCsize[1])
assert (funnel_rect.height + funnel_pos_y) < SCsize[1],'funnel is too big'

def main():
    #make main
    global FPS,SCREEN,FPSCLOCK,funnel_rect,egg_rect,eggs_on_screen,points
    pygame.init()
    #stuff
    the_font = pygame.font.Font('freesansbold.ttf', 30)
    time_font = the_font
    point_font = the_font
    start_game_message_font = the_font
    start_game_message_obj = start_game_message_font.render(start_game_message, True, YELLOW)
    start_game_message_rect = start_game_message_obj.get_rect()
    start_game_message_rect.center = (round(SCsize[0] / 2), round(SCsize[1] / 2))
    game_won_message_font = the_font
    game_won_message_obj = game_won_message_font.render(game_won_message, True,BLUE)
    game_won_message_rect = game_won_message_obj.get_rect()
    game_won_message_rect.center = (round(SCsize[0] / 2), round(SCsize[1] / 4))
    game_lost_message_font = the_font
    game_lost_message_obj = game_lost_message_font.render(game_lost_message,True,BLACK)
    game_lost_message_rect = game_lost_message_obj.get_rect()
    game_lost_message_rect.center = (round(SCsize[0] / 2), round(SCsize[1] / 2))
    end_game_pointage_font = time_font
    end_game_time_font = time_font

    #/stuff
    FPSCLOCK = pygame.time.Clock()
    SCREEN = pygame.display.set_mode(SCsize)
    SCREEN.fill(BGcolor)
    pygame.display.set_caption(caption)
    SCREEN.blit(start_game_message_obj,start_game_message_rect.topleft)
    pygame.display.update()
    time.sleep(2)
    SCREEN.fill(WHITE)
    game_start_time = time.time()


    mouseposx = 0

    while True:

        time_obj = time_font.render('time: ' + str(round(time.time() - game_start_time,3)),True,BLACK)
        time_rect = time_obj.get_rect()
        point_obj = point_font.render('points: ' + str(points),True,BLACK)
        point_rect = point_obj.get_rect()
        time_rect.right = SCsize[0]
        SCREEN.fill(BGcolor)
        funnel_rect.centerx = mouseposx
        SCREEN.blit(funnel,funnel_rect.topleft)
        eggs_on_screen,eggs_caught = update_eggs(eggs_on_screen, SCsize)
        points += len(eggs_caught)

        for an_egg in eggs_on_screen:
            SCREEN.blit(an_egg.picture,an_egg.rect.topleft)
            an_egg.drop_egg_by(egg_drop_amount)

        SCREEN.blit(time_obj, time_rect.topleft)
        SCREEN.blit(point_obj, point_rect.topleft)

        for event in pygame.event.get():
            if (event.type == KEYUP and event.key == K_ESCAPE) or event.type == QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == MOUSEMOTION:
                mouseposx = event.pos[0]

        if points >= game_won_pointage_and_time[0] and time.time() - game_start_time <= game_won_pointage_and_time[1]:
            SCREEN.fill(WHITE)
            SCREEN.blit(game_won_message_obj,game_won_message_rect.topleft)
            end_game_pointage_obj = end_game_pointage_font.render('pointage: ' + str(points),True,BLACK)
            end_game_pointage_rect = end_game_pointage_obj.get_rect()
            end_game_pointage_rect.topright = (game_won_message_rect[0] + 20,game_won_message_rect.midbottom[1] + 20)
            SCREEN.blit(end_game_pointage_obj,end_game_pointage_rect.topleft)
            end_game_time_obj = end_game_time_font.render('time used:' + str(round(time.time() - game_start_time)),True,BLACK)
            end_game_time_rect = end_game_time_obj.get_rect()
            end_game_time_rect.topleft = (game_won_message_rect[0] + 250,game_won_message_rect.midbottom[1] + 20)
            SCREEN.blit(end_game_time_obj,end_game_time_rect.topleft)
            pygame.display.update()
            time.sleep(2)
            points = 0
            main()
        elif time.time() - game_start_time >= game_won_pointage_and_time[1]:
            SCREEN.fill(RED)
            SCREEN.blit(game_lost_message_obj,game_lost_message_rect.topleft)
            pygame.display.update()
            time.sleep(2)
            points = 0
            main()
        pygame.display.update()
        FPSCLOCK.tick(FPS)

class ball():
    def __init__(self,picture,SCsize,number):
        #THIS WILL DRAW AN EGG AT THE TOP OF THE SCREEN AT A RANDOM X POSITION
        self.screen = SCsize
        self.number = number
        self.picture = pygame.image.load(picture)
        self.rect = self.picture.get_rect()
        self.width = self.rect.width
        self.rect_top = - (self.number * self.rect.height)
        self.random_pos_x = random.randint(0,self.screen[0]-self.width)
        self.rect.topleft = (self.random_pos_x,self.rect_top)
    def drop_egg_by(self,amount):
        self.rect.top += amount

def update_eggs(eggs_list, screensize):
    number = 0
    eggs_caught = []
    try:
        if eggs_list[-1].rect.top >= screensize[1]:
            #del eggs[an_egg.index()]
            del eggs_list[:]
    except IndexError:
        pass
    while len(eggs_list) < 5:
        an_egg = ball('images/egg.jpg', screensize, number)
        eggs_list.append(an_egg)
        number += 1
    for egg2 in eggs_list:
        if egg2.rect.colliderect(funnel_rect):
            this_egg = eggs_list.pop(eggs_list.index(egg2))
            eggs_caught.append(this_egg)
    return [eggs_list,eggs_caught]

if __name__ == '__main__':
    main()



