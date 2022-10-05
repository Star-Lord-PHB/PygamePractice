from random import Random, randrange
import sys
import pygame 
import lib 
import data

pygame.init()

screen = pygame.display.set_mode((800, 600), pygame.RESIZABLE)
pygame.display.set_caption("game")
clock = pygame.time.Clock() 


text_font = pygame.font.Font(None, 50)

background_sky = pygame.Surface((screen.get_width(), screen.get_height() // 3 * 2))
background_sky.fill("white")
background_sky = lib.StaticPicture(background_sky, (screen.get_width(), screen.get_height() // 3 * 2))

background_ground = pygame.Surface((screen.get_width(), screen.get_height() // 3 + 1))
background_ground.fill("black")
background_ground = lib.StaticPicture(background_ground, (screen.get_width(), screen.get_height() // 3 + 1), topleft = (0, background_sky.image.get_height()))

background = pygame.sprite.Group()
background.add(background_ground)
background.add(background_sky)


title = lib.Text("Game", text_font, "lightblue", None, center = (screen.get_width() // 2, screen.get_height() // 3))
score_text = lib.ScoreText("0", text_font, "red", "lightblue", center = (screen.get_width() // 2, 20))
fail_text = lib.Text("Fail", text_font, "red", "grey", center = (screen.get_width() // 2, screen.get_height() // 3))

menu_texts = pygame.sprite.Group()
menu_texts.add(title)

game_active_texts = pygame.sprite.Group()
game_active_texts.add(score_text)

fail_texts = pygame.sprite.Group()
fail_texts.add(fail_text)


restart_game_button = lib.Button("Restart", text_font, "white", "grey", center = (screen.get_width() // 3, screen.get_height() // 3 * 2))

start_game_button = lib.Button("Start", text_font, "white", "grey", center = (screen.get_width() // 3, screen.get_height() // 3 * 2))

quit_game_button = lib.Button("Quit", text_font, "white", "grey", center = (screen.get_width() // 3 * 2, screen.get_height() // 3 * 2))

player = pygame.sprite.GroupSingle()
player.add(lib.Player("./satori.png", background_ground.rect.top, (50,50)))

maoyu_list = pygame.sprite.Group()

start_time = pygame.time.get_ticks()
score = 0
mouse_position = (0,0)


while True :

    if data.game_status == data.ACTIVE :
        for event in pygame.event.get() :
            if event.type == pygame.QUIT :
                pygame.quit()
                sys.exit()
            elif event.type == data.SPAN_MAOYU :
                if Random().randrange(0, 10) < 5 :
                    if Random().randrange(0, 3) == 2 :
                        maoyu_list.add(lib.Enemy("./maoyu.png", background_sky.image.get_height() - 150, 4, (50, 50)))
                    else :
                        maoyu_list.add(lib.Enemy("./maoyu.png", background_sky.image.get_height(), 4, (50, 50)))


        player.update()
        maoyu_list.update()

        if pygame.sprite.spritecollide(player.sprite, maoyu_list, False) :
            data.game_status = data.FAIL
                
        
        data.updateScore()
        game_active_texts.update()

        background.draw(screen)
        game_active_texts.draw(screen)
        player.draw(screen)
        maoyu_list.draw(screen)
        
    elif data.game_status == data.FAIL:
        for event in pygame.event.get() :
            if event.type == pygame.QUIT :
                pygame.quit()
                sys.exit()

        if restart_game_button.isClicked() :
            player.sprite.reset()
            maoyu_list.empty()
            data.game_status = data.ACTIVE
            data.resetScore()
        elif quit_game_button.isClicked() :
            pygame.quit() 
            sys.exit() 

        final_score_text = pygame.sprite.GroupSingle()
        final_score_text.add(lib.Text("Your Score: {}".format(data.score), text_font, "red", "lightblue", center = (screen.get_width() // 2, screen.get_height() // 2)))

        background.draw(screen)
        fail_texts.draw(screen)
        final_score_text.draw(screen)
        restart_game_button.draw(screen)
        quit_game_button.draw(screen)
    
    elif data.game_status == data.MENU :
        for event in pygame.event.get() :
            if event.type == pygame.QUIT :
                pygame.quit()
                sys.exit()

        if start_game_button.isClicked() :
            data.game_status = data.ACTIVE
            data.resetScore()
        elif quit_game_button.isClicked() :
            pygame.quit()
            sys.exit()
        

        background.draw(screen)
        # screen.blit(background_sky, background_sky_rect)
        # screen.blit(title_surface, title_surface_rect)
        menu_texts.draw(screen)
        quit_game_button.draw(screen)
        start_game_button.draw(screen)
    

    pygame.display.update()
    clock.tick(60)