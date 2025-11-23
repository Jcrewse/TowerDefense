import pygame, consts

class Interface(pygame.sprite.Sprite):
    '''Class defining the game interface'''
    
    def __init__(self, tower):
        super().__init__()
        self.font = pygame.font.Font(None, 24)
        self.tower = tower
        
        self.image = pygame.Surface((consts.SCREEN_WIDTH, consts.SCREEN_HEIGHT), pygame.SRCALPHA)
        self.rect = self.image.get_rect(topleft=(0, 0))
        
        self.dmg_button = Button(10, 10, 100, 30, text='DMG+', callback=tower.upgrade_damage)
        self.spd_button = Button(120, 10, 100, 30, text='SPD+', callback=tower.upgrade_speed)
        self.arm_button = Button(230, 10, 100, 30, text='ARM+', callback=tower.upgrade_armor)
        

    def update(self):
        '''Update interface elements'''
        self.image.fill((0, 0, 0, 0))  # Clear with transparent
        
        self._draw_healthbar()
        self._draw_scores()
        
        self.dmg_button.draw()
        self.spd_button.draw()
        
        self.image.blit(self.dmg_button.image, self.dmg_button.rect)
        self.image.blit(self.spd_button.image, self.spd_button.rect)
        self.image.blit(self.arm_button.image, self.arm_button.rect)

        
    def _draw_healthbar(self):
        buff = 2
        healthbar_tray_pos = (consts.SCREEN_WIDTH/2 - consts.HEALTHBAR_SIZE/2, 
                              50, consts.HEALTHBAR_SIZE, 20)
        healthbar_pos = (consts.SCREEN_WIDTH/2 - consts.HEALTHBAR_SIZE/2 +buff,
                         50 + buff, 
                         consts.HEALTHBAR_SIZE*(self.tower.health/self.tower.max_health) - 2*buff,
                         20 - 2*buff)
        pygame.draw.rect(self.image, (40,40,40), healthbar_tray_pos)
        pygame.draw.rect(self.image, (0,128,0), healthbar_pos)
    
    def _draw_scores(self):
        health_text = self.font.render(f'{round(self.tower.health)}/{self.tower.max_health}', True, consts.WHITE)
        cash_text = self.font.render(f'${self.tower.cash}', True, consts.WHITE)
        wave_text = self.font.render(f'Wave number: {self.tower.wave_number}', True, consts.WHITE)
        self.image.blit(health_text, (consts.SCREEN_WIDTH/2 - 25, 52))
        self.image.blit(cash_text, (consts.SCREEN_WIDTH/2 + 40, 10))
        self.image.blit(wave_text, (consts.SCREEN_WIDTH/2 - 100, 10))

class Button(pygame.sprite.Sprite):
    """Simple rectangular button as a Sprite."""

    def __init__(self, x, y, width, height,
        text='', text_color=consts.BLACK, button_color=consts.GREEN, callback=None):
        super().__init__()

        self.text = text
        self.text_color = text_color
        self.button_color = button_color
        self.font = pygame.font.Font(None, 24)
        self.callback = callback

        # Sprite visuals
        self.image = pygame.Surface((width, height))
        self.rect = self.image.get_rect(topleft=(x, y))

        self.draw()

    def draw(self):
        """Render the button rectangle + text onto self.image."""
        self.image.fill(self.button_color)
        if self.text:
            text_surf = self.font.render(self.text, True, self.text_color)
            text_rect = text_surf.get_rect(
                center=(self.image.get_width() // 2, self.image.get_height() // 2)
            )
            self.image.blit(text_surf, text_rect)

    def handle_event(self, event):
        """Return True if clicked; run callback if provided."""
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                if self.callback is not None:
                    self.callback()
                    print(f'Button "{self.text}" clicked.')
                return True
        return False

    def update(self):
        """Optional: put hover / pressed visual logic here if you want."""
        pass