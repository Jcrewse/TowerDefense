import pygame
import units
import consts
import util
import gui

# Initialize pygame module
# pygame.init()
pygame.font.init()

# Create pygame screen
screen = pygame.display.set_mode((consts.SCREEN_WIDTH, consts.SCREEN_HEIGHT))
pygame.display.set_caption('Tower Defense')

# Game clock
clock = pygame.time.Clock()


def game_loop():
    '''
    Main game loop function
    '''
    running = True
    wave_number = 1

    # Initialize tower
    tower = units.Tower(screen)

    # Initialize first wave
    initial_enemies = 10
    enemies = util.spawn_enemies(initial_enemies, tower)

    # Initialize GUI
    interface = gui.Interface(screen, tower, wave_number)

    # Run the game
    while running:
        screen.fill(consts.BLACK)

        # Update GUI
        interface.update()

        # Check for inputs
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    tower.upgrade_damage()
                elif event.key == pygame.K_2:
                    tower.upgrade_attack_speed()

        # Spawn new wave if all enemies dead
        if not enemies:
            for _ in range(consts.WAVE_PAUSE_TIME*consts.FPS):
                tower.update(screen, enemies)
                clock.tick(consts.FPS)
            wave_enemies = initial_enemies + int(1.01*wave_number)
            enemies = util.spawn_enemies(wave_enemies, tower)
            wave_number += 1

        # Update tower
        tower.update(screen, enemies)

        # Draw enemies, move, attack
        for enemy in enemies.copy():
            if enemy.health > 0:
                enemy.draw(screen)
                enemy.move()
                enemy.attack(tower)
            else:
                enemies.remove(enemy)
                tower.give_cash()

        # Check if tower is dead
        if tower.health <= 0:
            running = False

        pygame.display.flip()
        clock.tick(consts.FPS)


if __name__ == "__main__":
    game_loop()
