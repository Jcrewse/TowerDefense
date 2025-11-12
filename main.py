import pygame as pg
import units
import consts
import util
import gui

# Initialize pygame module
# pg.init()
pg.font.init()

# Create pygame screen
screen = pg.display.set_mode((consts.SCREEN_WIDTH, consts.SCREEN_HEIGHT))
pg.display.set_caption('Tower Defense')

# Set background
background = pg.Surface((800,800))
background.fill(consts.BLACK)

# Game clock
clock = pg.time.Clock()

def game_loop():
    '''
    Main game loop function
    '''
    running = True
    wave_number = 1
    game_speed = 1

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
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
            # elif event.type == pg.KEYDOWN:
            #     if event.key == pg.K_1:
            #         tower.upgrade_damage()
            #     elif event.key == pg.K_2:
            #         tower.upgrade_attack_speed()
            elif interface.test_button.is_clicked(event):
                if tower.cash >= 10:
                    tower.upgrade_damage()
                    print("Damage upgraded!")
            elif interface.test_button2.is_clicked(event):
                if tower.cash >= 10:
                    tower.upgrade_attack_speed()
                    print("Attack speed upgraded!")

        # Spawn new wave if all enemies dead
        if not enemies:
            # for _ in range(consts.WAVE_PAUSE_TIME*consts.FPS):
            #     tower.update(screen, enemies)
            #     clock.tick(game_speed*consts.FPS)
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
                enemy.kill()
                tower.give_cash()

        # Check if tower is dead
        if tower.health <= 0:
            running = False

        pg.display.flip()
        clock.tick(int(game_speed*consts.FPS))


if __name__ == "__main__":
    game_loop()
                                                                               
