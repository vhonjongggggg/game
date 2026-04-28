import pygame
import random

WIDTH = 400
HEIGHT = 600


class GameLogic:
    def __init__(self):

        self.gravity = 0.5
        self.player_jump = -13
        self.platform_width = 60
        self.platform_height = 15
        self.min_speed = 2
        self.max_speed = 5
        self.powerups = []
        self.paused = False
        self.game_over = False
        self.has_double_jump = False
        self.reset_game()

    def reset_game(self):
        self.player_rect = pygame.Rect(WIDTH // 2 - 15, HEIGHT - 150, 30, 30)
        self.player_velocity = 0
        self.score = 0
        self.platforms = []
        self.platform_speeds = []
        self.powerups = []
        self.game_over = False
        self.paused = False
        self.has_double_jump = False

        # starting platform
        start_platform = pygame.Rect(
            WIDTH // 2 - self.platform_width // 2, HEIGHT - 50, self.platform_width, self.platform_height)
        self.platforms.append(start_platform)
        self.platform_speeds.append(0)

        # randomize platforms
        for i in range(7):
            p = pygame.Rect(random.randint(0, WIDTH - self.platform_width),
                            i * (HEIGHT // 7), self.platform_width, self.platform_height)
            self.platforms.append(p)
            if random.random() < 0.2:
                self.platform_speeds.append(random.randint(
                    self.min_speed, self.max_speed) * random.choice([-1, 1]))
            else:
                self.platform_speeds.append(0)

    def update(self, keys):

        if self.paused or self.game_over:
            return

        if keys[pygame.K_LEFT]:
            self.player_rect.x -= 7
        if keys[pygame.K_RIGHT]:
            self.player_rect.x += 7

        if self.player_rect.x > WIDTH:
            self.player_rect.x = -30
        elif self.player_rect.x < -30:
            self.player_rect.x = WIDTH

        self.player_velocity += self.gravity
        self.player_rect.y += self.player_velocity

        for i in range(len(self.platforms)):
            if self.platform_speeds[i] != 0:
                self.platforms[i].x += self.platform_speeds[i]

                for p_data in self.powerups:
                    if p_data[1] == i:
                        p_data[0].x += self.platform_speeds[i]

                # platform bounce to edge
                if self.platforms[i].right > WIDTH or self.platforms[i].left < 0:
                    self.platform_speeds[i] *= -1

        # for collecting powerup
        for p_data in self.powerups[:]:
            if self.player_rect.colliderect(p_data[0]):
                self.has_double_jump = True
                self.powerups.remove(p_data)

        if self.player_velocity > 0:
            for p in self.platforms:
                if self.player_rect.colliderect(p):
                    if self.player_rect.bottom < p.centery + 10:
                        self.player_rect.bottom = p.top
                        self.player_velocity = self.player_jump

        # scrolling
        if self.player_rect.y < HEIGHT // 2:
            diff = (HEIGHT // 2) - self.player_rect.y
            self.player_rect.y = HEIGHT // 2

            for i in range(len(self.platforms)):
                self.platforms[i].y += diff

                if self.platforms[i].y > HEIGHT:
                    self.platforms[i].y = 0
                    self.platforms[i].x = random.randint(
                        0, WIDTH - self.platform_width)
                    self.score += 10

                    # spawn chance of ufo
                    if random.random() < 0.2:
                        self.platform_speeds[i] = random.randint(
                            self.min_speed, self.max_speed) * random.choice([-1, 1])
                    else:
                        self.platform_speeds[i] = 0

                    # spawn of power ups
                    if random.random() < 0.15:
                        new_rect = pygame.Rect(
                            self.platforms[i].x + 20, self.platforms[i].y - 25, 20, 20)
                        self.powerups.append([new_rect, i])

            for p_data in self.powerups[:]:
                p_data[0].y += diff
                if p_data[0].y > HEIGHT:
                    self.powerups.remove(p_data)
