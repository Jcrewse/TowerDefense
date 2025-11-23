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

def game_loop():
    running = True
    clock = pg.time.Clock()
    
    #Groups
    enemies = pg.sprite.Group()
    projectiles = pg.sprite.Group()
    all_sprites = pg.sprite.Group()
    
    # Create Tower
    tower = units.Tower(screen, consts.TOWER_X, consts.TOWER_Y, range=400)
    
    # Create interface
    interface = gui.Interface(tower)
    ui = pg.sprite.Group(interface)
    
    # Wave set up
    util.spawn_wave(enemies, all_sprites, tower, count=20)
    WAVE_INTERVAL_MS = int(consts.WAVE_INTERVAL * 1000)  # milliseconds
    last_wave_time = pg.time.get_ticks()
    
    while running:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False
    
            interface.dmg_button.handle_event(event)
            interface.spd_button.handle_event(event)
            interface.arm_button.handle_event(event)

        now = pg.time.get_ticks()
        if now - last_wave_time >= WAVE_INTERVAL_MS and len(enemies) == 0:
            tower.wave_number += 1
            util.spawn_wave(enemies, all_sprites, tower, count=20 + tower.wave_number * 5)
            last_wave_time = now

        # Update enemies and projectiles
        enemies.update()
        projectiles.update()
        ui.update()

        # Update tower
        tower.update(enemies, projectiles)

        # Rendering
        screen.fill((0, 0, 0))
        enemies.draw(screen)
        projectiles.draw(screen)
        tower.draw(screen)
        ui.draw(screen)

        pg.display.flip()
        clock.tick(consts.FPS)

if __name__ == "__main__":
    game_loop()
                                                                               
