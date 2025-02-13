import pygame
import random


pygame.init()


width = 600
height = 750
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Space War")


clock = pygame.time.Clock()


BLACK = (0, 0, 0)
DARKBLUE = (10, 10, 50)
WHITE = (255, 255, 255)
YELLOW = (255, 255, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)

ship = pygame.image.load("C:/Users/Tweety/OneDrive/المستندات/work/ship 7.png")
ship_rect = ship.get_rect()
ship_rect.center = (width // 2, height - 100)


enemy1 = pygame.image.load("C:/Users/Tweety/OneDrive/المستندات/work/ship 6.png")
enemy_rect1 = enemy1.get_rect()
enemy_rect1.center = (random.randint(50, width - 50), 0)

enemy2 = pygame.image.load("C:/Users/Tweety/OneDrive/المستندات/work/ship 2.png")
enemy_rect2 = enemy2.get_rect()
enemy_rect2.center = (random.randint(50, width - 50), 0)


sound1 = pygame.mixer.Sound("C:/Users/Tweety/OneDrive/المستندات/work/sound.wav")
powerup_sound = pygame.mixer.Sound("C:/Users/Tweety/OneDrive/المستندات/work/sound3.wav")
pygame.mixer.music.load("C:/Users/Tweety/OneDrive/المستندات/work/sound2.wav")
pygame.mixer.music.play(loops=-1, start=0.0)


class Bullet:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, 5, 10)
        self.color = RED

    def update(self):
        self.rect.y -= 7

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.rect)


class EnemyBullet:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, 5, 10)
        self.color = WHITE

    def update(self):
        self.rect.y += 5

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.rect)


class PowerUp:
    def __init__(self, x, y, type_):
        self.rect = pygame.Rect(x, y, 30, 30)
        self.type = type_
        self.color = (0, 255, 0) if type_ == "life" else (255, 255, 0) if type_ == "speed" else (255, 0, 0)

    def update(self):
        self.rect.y += 2

    def draw(self, screen):
        pygame.draw.ellipse(screen, self.color, self.rect)


bullets = []
enemy_bullets = []
power_ups = []


score = 0
lives = 3
speed_boost = 1
rapid_fire = False
rapid_fire_timer = 0
power_up_timer = 0
shield_active = False
shield_timer = 0
score_multiplier = 1
score_multiplier_timer = 0


stars = [(random.randint(0, width), random.randint(0, height)) for _ in range(100)]

system_font = pygame.font.Font(None, 30)


running = True
while running:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:  # Shoot bullet when spacebar is pressed
                bullet = Bullet(ship_rect.centerx - 2, ship_rect.top)
                bullets.append(bullet)
                if rapid_fire:  # Shoot additional bullets in rapid fire mode
                    bullets.append(Bullet(ship_rect.centerx - 10, ship_rect.top))
                    bullets.append(Bullet(ship_rect.centerx + 6, ship_rect.top))


    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and ship_rect.left > 0:
        ship_rect.x -= 5 * speed_boost
    if keys[pygame.K_RIGHT] and ship_rect.right < width:
        ship_rect.x += 5 * speed_boost


    enemy_rect1.y += 3
    if enemy_rect1.top > height:
        enemy_rect1.center = (random.randint(50, width - 50), 0)

    enemy_rect2.y += 3
    if enemy_rect2.top > height:
        enemy_rect2.center = (random.randint(50, width - 50), 0)


    if random.randint(1, 100) == 1:  # Random chance to shoot
        enemy_bullets.append(EnemyBullet(enemy_rect1.centerx, enemy_rect1.bottom))
    if random.randint(1, 100) == 1:  # Random chance to shoot
        enemy_bullets.append(EnemyBullet(enemy_rect2.centerx, enemy_rect2.bottom))


    for bullet in bullets[:]:
        bullet.update()
        if bullet.rect.bottom < 0:
            bullets.remove(bullet)


    for bullet in enemy_bullets[:]:
        bullet.update()
        if bullet.rect.top > height:
            enemy_bullets.remove(bullet)


    for bullet in bullets[:]:
        if bullet.rect.colliderect(enemy_rect1):
            bullets.remove(bullet)
            enemy_rect1.center = (random.randint(50, width - 50), 0)
            sound1.play()
            score += 1 * score_multiplier

        if bullet.rect.colliderect(enemy_rect2):
            bullets.remove(bullet)
            enemy_rect2.center = (random.randint(50, width - 50), 0)
            sound1.play()
            score += 3 * score_multiplier


    if not shield_active:
        if ship_rect.colliderect(enemy_rect1):
            lives -= 1
            enemy_rect1.center = (random.randint(50, width - 50), 0)
            if lives <= 0:
                running = False

        if ship_rect.colliderect(enemy_rect2):
            lives -= 1
            enemy_rect2.center = (random.randint(50, width - 50), 0)
            if lives <= 0:
                running = False


    for bullet in enemy_bullets[:]:
        if bullet.rect.colliderect(ship_rect):
            enemy_bullets.remove(bullet)
            if not shield_active:
                lives -= 1
                if lives <= 0:
                    running = False


    power_up_timer += 1
    if power_up_timer >= 300:
        power_up_timer = 0
        new_powerup = PowerUp(random.randint(50, 550), 0, random.choice(["speed", "life", "rapid_fire", "shield", "score_multiplier"]))
        power_ups.append(new_powerup)


    for power_up in power_ups[:]:
        power_up.update()


        if ship_rect.colliderect(power_up.rect):
            powerup_sound.play()
            if power_up.type == "speed":
                speed_boost = 2
                pygame.time.set_timer(pygame.USEREVENT, 5000)
            elif power_up.type == "life":
                lives += 1
            elif power_up.type == "rapid_fire":
                rapid_fire = True
                rapid_fire_timer = 300
            elif power_up.type == "shield":
                shield_active = True
                shield_timer = 300
            elif power_up.type == "score_multiplier":
                score_multiplier = 2
                score_multiplier_timer = 300

            power_ups.remove(power_up)


        elif power_up.rect.top > height:
            power_ups.remove(power_up)


    if rapid_fire:
        rapid_fire_timer -= 1
        if rapid_fire_timer <= 0:
            rapid_fire = False

    if shield_active:
        shield_timer -= 1
        if shield_timer <= 0:
            shield_active = False

    if score_multiplier == 2:
        score_multiplier_timer -= 1
        if score_multiplier_timer <= 0:
            score_multiplier = 1


    screen.fill(DARKBLUE)


    for i, (x, y) in enumerate(stars):
        pygame.draw.circle(screen, WHITE, (x, y), 1)
        y += 1
        if y > height:
            y = 0 
        stars[i] = (x, y)


    pygame.draw.circle(screen, YELLOW, (550, 50), 50)


    score_text = system_font.render(f"Score: {score}", True, WHITE)
    lives_text = system_font.render(f"Lives: {lives}", True, WHITE)
    screen.blit(score_text, (10, 10))
    screen.blit(lives_text, (10, 40))


    screen.blit(ship, ship_rect)
    screen.blit(enemy1, enemy_rect1)
    screen.blit(enemy2, enemy_rect2)
    for bullet in bullets:
        bullet.draw(screen)
    for bullet in enemy_bullets:
        bullet.draw(screen)
    for power_up in power_ups:
        power_up.draw(screen)


    if shield_active:
        pygame.draw.circle(screen, GREEN, ship_rect.center, 30, 2)


    pygame.display.flip()


    clock.tick(60)


game_over_font = pygame.font.Font(None, 74)
game_over_text = game_over_font.render("GAME OVER", True, RED)
screen.blit(game_over_text, (width // 2 - 140, height // 2 - 40))
final_score_text = system_font.render(f"Final Score: {score}", True, WHITE)
screen.blit(final_score_text, (width // 2 - 80, height // 2 + 20))
pygame.display.flip()
pygame.time.wait(3000)


pygame.quit()