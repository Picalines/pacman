import pygame
from pacmanhp import HP
from globals import *
from config import *
from Score import Score
from High_Score import HighScore


pygame.font.init()
pygame.mixer.init()

screen = pygame.display.set_mode(size)
font = pygame.font.SysFont('arial', 35, True)
play_act = pygame.image.load("res/btn_play_2.png")
play_d_act = pygame.image.load("res/btn_play_1.png")
exit_act = pygame.image.load("res/btn_exit_2.png")
exit_d_act = pygame.image.load("res/btn_exit_1.png")
High_act = pygame.image.load("res/btn_high_score_2.png")
High_d_act = pygame.image.load("res/btn_high_score_1.png")


def show_menu():
    from Menu import Button, h_scr
    show = False

    play_btn = Button(250, 200, play_act, play_d_act, main)
    high_score_btn = Button(250, 285, High_act, High_d_act, h_scr)
    exit_btn = Button(250, 370, exit_act, exit_d_act, quit)

    back_gr = pygame.image.load('res/DEEPSPACE.png')

    while not show:
        for ev in pygame.event.get():
            if ev.type == pygame.QUIT:
                show = True
        screen.blit(back_gr, (0, 0))
        play_btn.draw_button()
        high_score_btn.draw_button()
        exit_btn.draw_button()
        pygame.display.flip()
        pygame.time.wait(10)
    quit()


def main():
    from ghost import render_ghost_cage
    from tilemap import load_map_from_txt
    from Menu import authors
    clock = pygame.time.Clock()

    dead_curtain = pygame.Surface(size, pygame.SRCALPHA, 32)

    player = Pacman(screen, (32 * 9, 32 * 13))
    player_hp = HP(screen)
    player_h_score = HighScore(screen)
    player_score = Score(screen)
    corns = []
    tile_map = Tilemap(screen, (19, 19), (32, 32), pygame.image.load('tiles_sheet.png'))
    load_map_from_txt('map_data.txt', tile_map, screen, corns)

    poses = [((7 + x) * 32, 8 * 32) for x in (0, 1, 3, 4)]
    ghosts = []

    def reset():

        player.rebirth()
        i = 0
        Ghost.score_multiplier = 1
        ghosts.clear()
        for n in ghost_names:
            ghosts.append(Ghost(screen, poses[i], n))
            i += 1

    reset()

    screen.fill(black)
    tile_map.render()
    render_ghost_cage(screen, (32 * 7, 32 * (17 // 2)))
    authors("Davydova", "Kostenko", "Gil", "Gladkov", "Sasin")
    pygame.display.flip()

    pygame.mixer.music.load("res/music/defmus.wav")
    pygame.mixer.music.play(0, 0.0)

    start_music_endev = pygame.USEREVENT + 1
    pygame.mixer.music.set_endevent(start_music_endev)

    start_music_playing = True
    while start_music_playing:
        for event in pygame.event.get():
            if event.type == start_music_endev:
                start_music_playing = False

    game_over = False
    while not game_over:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True
                player_h_score.updt()
                add_score(-get_score())
        screen.fill(black)
        tile_map.render()

        if not player.dead:
            for c in corns:
                if player.rect.collidepoint(c.rect.center[0], c.rect.center[1]):
                    c.eat()
                    alleaten = True
                    for v in corns:
                        if not v.eaten:
                            alleaten = False
                            break
                    if alleaten:
                        reset()
                        load_map_from_txt('map_data.txt', tile_map, screen, corns)
                c.render()

            for g in ghosts:
                if g.rect.collidepoint(player.rect.center):
                    if not g.kill():
                        player.kill()
                        player_hp.count -= 1
                        break
                g.update()
                g.render()

        render_ghost_cage(screen, (32 * 7, 32 * (17 // 2)))

        if player.dead:
            dead_curtain.fill((0, 0, 0, (player.death_anim.current_sprite + 1) * 51))

        player.render()
        player_hp.render()
        player_score.render()
        player_h_score.render()

        authors("Davydova", "Kostenko", "Gil", "Gladkov", "Sasin")


        if player.dead and player.death_anim.current_sprite == 5:
            if player_hp.count > 0:
                reset()

            else:
                player_h_score.updt()
                add_score(-get_score())
                game_over = True

        pygame.display.flip()
        pygame.time.wait(tick_speed)
        set_dt(clock.tick(fps) / 1000.0)


if __name__ == '__main__':
    show_menu()
