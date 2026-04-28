import pygame
import sys
from logic import GameLogic, WIDTH, HEIGHT

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

font = pygame.font.SysFont("Arial", 25)
big_font = pygame.font.SysFont("Arial", 50, bold=True)

pause_btn_rect = pygame.Rect(10, 10, 80, 35)
restart_btn_rect = pygame.Rect(10, 55, 80, 35)


def draw_overlay(title, subtitle):
    overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
    overlay.fill((0, 0, 0, 180))
    screen.blit(overlay, (0, 0))
    t_surf = big_font.render(title, True, (255, 255, 255))
    screen.blit(t_surf, t_surf.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 40)))
    s_surf = font.render(subtitle, True, (200, 200, 200))
    screen.blit(s_surf, s_surf.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 20)))


try:
    player_img = pygame.transform.scale(
        pygame.image.load("player.png").convert_alpha(), (40, 40))
    stat_plat_img = pygame.transform.scale(
        pygame.image.load("static_sat.png").convert_alpha(), (60, 15))
    moving_plat_img = pygame.transform.scale(
        pygame.image.load("moving_ufo.png").convert_alpha(), (60, 15))
    # ufo image section
except:
    player_img = stat_plat_img = moving_plat_img = None

game = GameLogic()
start_time = pygame.time.get_ticks()

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.MOUSEBUTTONDOWN:
            if pause_btn_rect.collidepoint(event.pos):
                if not game.game_over:
                    game.paused = not game.paused

            if (game.paused or game.game_over) and restart_btn_rect.collidepoint(event.pos):
                game.reset_game()
                start_time = pygame.time.get_ticks()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_p and not game.game_over:
                game.paused = not game.paused
            if event.key == pygame.K_r:
                game.reset_game()
                start_time = pygame.time.get_ticks()
            if event.key == pygame.K_SPACE and not game.paused and not game.game_over:
                if game.has_double_jump:
                    game.player_velocity = game.player_jump
                    game.has_double_jump = False

    keys = pygame.key.get_pressed()
    game.update(keys)

    screen.fill((250, 250, 250))

    for i, plat in enumerate(game.platforms):
        if stat_plat_img:
            img = moving_plat_img if game.platform_speeds[i] != 0 else stat_plat_img
            screen.blit(img, plat)
        else:
            color = (0, 0, 255) if game.platform_speeds[i] != 0 else (
                0, 255, 0)
            pygame.draw.rect(screen, color, plat)

    for p_data in game.powerups:
        pygame.draw.rect(screen, (255, 215, 0), p_data[0])

    if player_img:
        screen.blit(player_img, game.player_rect)
    else:
        pygame.draw.rect(screen, (255, 65, 70), game.player_rect)

    score_txt = font.render(f"Score: {game.score}", True, (0, 0, 0))
    screen.blit(score_txt, (WIDTH // 2 - 40, 20))
    if game.has_double_jump:
        dj_txt = font.render("Double Jump Ready!", True, (255, 165, 0))
        screen.blit(dj_txt, (10, HEIGHT - 30))

    pygame.draw.rect(screen, (150, 150, 150), pause_btn_rect)
    p_label = font.render("Pause", True, (255, 255, 255))
    screen.blit(p_label, (pause_btn_rect.x + 10, pause_btn_rect.y + 5))

    if game.paused or game.game_over:
        pygame.draw.rect(screen, (200, 50, 50), restart_btn_rect)
        r_label = font.render("Reset", True, (255, 255, 255))
        screen.blit(r_label, (restart_btn_rect.x + 10, restart_btn_rect.y + 5))

    if game.paused:
        draw_overlay("PAUSED", "Click 'Reset' or Press 'R' to restart")
    if game.game_over:
        draw_overlay(
            "GAME OVER", f"Score: {game.score}  Click 'Reset' or Press 'R' to restart")

    if pygame.time.get_ticks() - start_time > 1000:
        if game.player_rect.y > HEIGHT:
            game.game_over = True

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()
