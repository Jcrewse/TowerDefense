import pygame as pg
import consts
import gui
import game_manager

# Initialize pygame module
pg.font.init()

# Create pygame screen
screen = pg.display.set_mode((consts.SCREEN_WIDTH, consts.SCREEN_HEIGHT))
pg.display.set_caption('Tower Defense')


def game_loop():
    '''main game loop'''
    clock = pg.time.Clock()

    # Create GameManager - centralized game state
    game = game_manager.GameManager(screen)

    # Create interface - pass the game manager instead of just tower
    interface = gui.Interface(game)
    ui = pg.sprite.Group(interface)

    # Spawn first wave
    game.start_game()

    while game.running:
        # Event handling
        for event in pg.event.get():
            if event.type == pg.constants.QUIT:
                game.running = False
            elif event.type == pg.constants.KEYDOWN:
                if event.key == pg.constants.K_SPACE:
                    game.toggle_pause()
                elif event.key == pg.constants.K_r and game.game_over:
                    game.reset_game()
                    interface = gui.Interface(game)
                    ui = pg.sprite.Group(interface)

            # Handle button clicks
            interface.dmg_button.handle_event(event)
            interface.spd_button.handle_event(event)
            interface.arm_button.handle_event(event)

        # Update game state
        game.update()
        ui.update()

        # Rendering
        screen.fill((0, 0, 0))
        game.draw()
        ui.draw(screen)

        # Draw pause/game over overlays
        if game.paused:
            _draw_pause_overlay(screen)
        elif game.game_over:
            _draw_game_over_overlay(screen, game.wave_number)

        pg.display.flip()
        clock.tick(consts.FPS)


def _draw_pause_overlay(screen):
    """Draw pause overlay"""
    font = pg.font.Font(None, 72)
    text = font.render("PAUSED", True, (255, 255, 255))
    text_rect = text.get_rect(
        center=(
            consts.SCREEN_WIDTH / 2,
            consts.SCREEN_HEIGHT / 2))

    # Semi-transparent overlay
    overlay = pg.Surface((consts.SCREEN_WIDTH, consts.SCREEN_HEIGHT))
    overlay.set_alpha(128)
    overlay.fill((0, 0, 0))
    screen.blit(overlay, (0, 0))
    screen.blit(text, text_rect)


def _draw_game_over_overlay(screen, wave_number):
    """Draw game over overlay"""
    font_large = pg.font.Font(None, 72)
    font_small = pg.font.Font(None, 36)

    game_over_text = font_large.render("GAME OVER", True, (255, 0, 0))
    wave_text = font_small.render(
        f"Reached Wave: {wave_number}", True, (255, 255, 255))
    restart_text = font_small.render(
        "Press R to Restart", True, (255, 255, 255))

    # Semi-transparent overlay
    overlay = pg.Surface((consts.SCREEN_WIDTH, consts.SCREEN_HEIGHT))
    overlay.set_alpha(192)
    overlay.fill((0, 0, 0))
    screen.blit(overlay, (0, 0))

    # Position text
    screen.blit(game_over_text,
                game_over_text.get_rect(center=(consts.SCREEN_WIDTH / 2, consts.SCREEN_HEIGHT / 2 - 60)))
    screen.blit(wave_text,
                wave_text.get_rect(center=(consts.SCREEN_WIDTH / 2, consts.SCREEN_HEIGHT / 2 + 20)))
    screen.blit(restart_text,
                restart_text.get_rect(center=(consts.SCREEN_WIDTH / 2, consts.SCREEN_HEIGHT / 2 + 120)))


if __name__ == "__main__":
    game_loop()
