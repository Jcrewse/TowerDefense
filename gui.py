import pygame
import consts


class Interface(pygame.sprite.Sprite):
    '''Class defining the game interface'''

    def __init__(self, game_manager):
        super().__init__()
        self.font = pygame.font.Font(None, 24)
        self.game_manager = game_manager
        self.tower = game_manager.tower

        self.tower_stats_interface = TowerStatsInterface(self.tower)

        self.image = pygame.Surface(
            (consts.SCREEN_WIDTH, consts.SCREEN_HEIGHT), pygame.SRCALPHA)
        self.rect = self.image.get_rect(topleft=(0, 0))

        # Buttons now call game_manager upgrade methods
        self.dmg_button = Button(10, consts.SCREEN_HEIGHT - 50, 100, 30, text='DMG+',
                                 callback=game_manager.upgrade_tower_damage)
        self.spd_button = Button(120, consts.SCREEN_HEIGHT - 50, 100, 30, text='SPD+',
                                 callback=game_manager.upgrade_tower_speed)
        self.arm_button = Button(230, consts.SCREEN_HEIGHT - 50, 100, 30, text='ARM+',
                                 callback=game_manager.upgrade_tower_armor)

    def update(self):
        '''Update interface elements'''
        self.image.fill((0, 0, 0, 0))  # Clear with transparent

        # Draw health bar, scores, upgrade costs
        #self._draw_healthbar()
        #self._draw_scores()
        self.tower_stats_interface.update()
        

        # Draw buttons
        self.dmg_button.draw()
        self.spd_button.draw()
        self.arm_button.draw()

        # Blit buttons onto interface
        self.image.blit(self.dmg_button.image, self.dmg_button.rect)
        self.image.blit(self.spd_button.image, self.spd_button.rect)
        self.image.blit(self.arm_button.image, self.arm_button.rect)
        
        self.image.blit(self.tower_stats_interface.image, self.tower_stats_interface.rect)

    def _draw_healthbar(self):
        buff = 2
        healthbar_tray_pos = (consts.SCREEN_WIDTH / 2 - consts.HEALTHBAR_SIZE / 2,
                              50, consts.HEALTHBAR_SIZE, 20)
        healthbar_pos = (consts.SCREEN_WIDTH / 2 - consts.HEALTHBAR_SIZE / 2 + buff,
                         50 + buff,
                         consts.HEALTHBAR_SIZE *
                         (self.tower.health / self.tower.max_health) - 2 * buff,
                         20 - 2 * buff)
        pygame.draw.rect(self.image, (40, 40, 40), healthbar_tray_pos)
        pygame.draw.rect(self.image, (0, 128, 0), healthbar_pos)

    def _draw_scores(self):
        health_text = self.font.render(f'{round(self.tower.health)}/{self.tower.max_health}',
                                       True, consts.WHITE)
        cash_text = self.font.render(
            f'${self.game_manager.cash}', True, consts.WHITE)
        wave_text = self.font.render(
            f'Wave: {
                self.game_manager.wave_number}',
            True,
            consts.WHITE)

        self.image.blit(health_text, (consts.SCREEN_WIDTH / 2 - 25, 52))
        self.image.blit(cash_text, (consts.SCREEN_WIDTH / 2 + 40, 10))
        self.image.blit(wave_text, (consts.SCREEN_WIDTH / 2 - 100, 10))

    # def _draw_upgrade_costs(self):
    #     """Draw upgrade costs below buttons"""
    #     small_font = pygame.font.Font(None, 18)

    #     dmg_cost = 50 + self.tower.damage * 2
    #     spd_cost = 50 + (self.tower.cooldown * 3)
    #     arm_cost = 50 + (self.tower.max_health * 2)

    #     dmg_text = small_font.render(f'${dmg_cost}', True, consts.WHITE)
    #     spd_text = small_font.render(f'${spd_cost}', True, consts.WHITE)
    #     arm_text = small_font.render(f'${arm_cost}', True, consts.WHITE)

    #     self.image.blit(dmg_text, (10 + 35, 42))
    #     self.image.blit(spd_text, (120 + 35, 42))
    #     self.image.blit(arm_text, (230 + 35, 42))
    
class TowerStatsInterface(pygame.sprite.Sprite):
    '''Class defining the tower stats interface'''
    
    BOX_WIDTH = 200
    BOX_HEIGHT = 50

    def __init__(self, tower):
        super().__init__()
        self.font = pygame.font.Font(None, 24)
        self.tower = tower

        self.image = pygame.Surface(
            (self.BOX_WIDTH, self.BOX_HEIGHT), pygame.SRCALPHA)
        self.rect = self.image.get_rect(topleft=(consts.SCREEN_WIDTH/2 - self.BOX_WIDTH/2, 5))

    def update(self):
        '''Update tower stats interface elements'''
        self.image.fill((0, 0, 0))
        pygame.draw.rect(self.image, consts.BLACK, self.image.get_rect(), 2)

        # Draw tower stats
        self._draw_tower_stats()

    def _draw_tower_stats(self):
        health_text = self.font.render(f'Health: {self.tower.health}', True, consts.WHITE)
        score_text = self.font.render(f'Cash: {self.tower.cash}', True, consts.WHITE)

        self.image.blit(health_text, (100, 100))
        self.image.blit(score_text, (100, 140))


class Button(pygame.sprite.Sprite):
    """Simple rectangular button as a Sprite, with optional border + rounded corners."""

    def __init__(
        self, x, y, width, height,
        text='',
        text_color=consts.BLACK,
        button_color=consts.GREEN,
        callback=None,
        border_color=consts.BLACK,
        border_width=2,
        border_radius=10
    ):
        super().__init__()

        self.text = text
        self.text_color = text_color
        self.button_color = button_color
        self.callback = callback

        self.border_color = border_color
        self.border_width = border_width
        self.border_radius = border_radius

        self.font = pygame.font.Font(None, 24)

        # Use SRCALPHA so rounded corners can be transparent
        self.image = pygame.Surface((width, height), pygame.SRCALPHA).convert_alpha()
        self.rect = self.image.get_rect(topleft=(x, y))

        self.draw()

    def draw(self):
        """Render rounded rect button + border + text onto self.image."""
        self.image.fill((0, 0, 0, 0))  # fully transparent

        w, h = self.image.get_size()
        outer_rect = pygame.Rect(0, 0, w, h)

        # Clamp radius so it can't exceed half the smallest dimension
        r = max(0, min(self.border_radius, min(w, h) // 2))

        # 1) Border (outer)
        if self.border_width > 0:
            pygame.draw.rect(
                self.image,
                self.border_color,
                outer_rect,
                border_radius=r
            )

            # 2) Fill (inner), inset by border width
            inner = outer_rect.inflate(-2 * self.border_width, -2 * self.border_width)

            # Reduce radius for inner rect so corners line up nicely
            inner_r = max(0, r - self.border_width)

            pygame.draw.rect(
                self.image,
                self.button_color,
                inner,
                border_radius=inner_r
            )
        else:
            # No border: just fill
            pygame.draw.rect(
                self.image,
                self.button_color,
                outer_rect,
                border_radius=r
            )

        # 3) Text
        if self.text:
            text_surf = self.font.render(self.text, True, self.text_color)
            text_rect = text_surf.get_rect(center=outer_rect.center)
            self.image.blit(text_surf, text_rect)

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.rect.collidepoint(event.pos):
                if self.callback is not None:
                    self.callback()
                return True
        return False

    def update(self):
        """Update button if needed (e.g., hover effects)"""
        pass