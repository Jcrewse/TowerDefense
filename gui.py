import pygame, consts

class Interface:

    def __init__(self, screen, tower, wave_number):
        self.font = pygame.font.Font(None, 18)
        self.screen = screen
        self.tower = tower
        self.wave_number = wave_number
        #self.test_button = Button(10, 750, 100, 30, text='DMG')

    def update(self):
        # Draw health bar
        buff = 2
        healthbar_tray_pos = (consts.SCREEN_WIDTH/2 - consts.HEALTHBAR_SIZE/2, 
                              50, consts.HEALTHBAR_SIZE, 20)
        healthbar_pos = (consts.SCREEN_WIDTH/2 - consts.HEALTHBAR_SIZE/2 +buff, 50 + buff, consts.HEALTHBAR_SIZE*(self.tower.health/self.tower.max_health) - 2*buff, 20 - 2*buff)
        pygame.draw.rect(self.screen, (40,40,40), healthbar_tray_pos)
        pygame.draw.rect(self.screen, (0,128,0), healthbar_pos)
        
        # Display scores
        health_text = self.font.render(f'{round(self.tower.health)}/{self.tower.max_health}', True, consts.WHITE)
        cash_text = self.font.render(f'${self.tower.cash}', True, consts.WHITE)
        wave_text = self.font.render(f'Wave number: {self.wave_number}', True, consts.WHITE)
        self.screen.blit(health_text, (consts.SCREEN_WIDTH/2 - 25, 52))
        self.screen.blit(cash_text, (consts.SCREEN_WIDTH/2 + 40, 10))
        self.screen.blit(wave_text, (consts.SCREEN_WIDTH/2 - 100, 10))

        # Display combat stats
        combat_left_pos = 150
        damage_text = self.font.render(f'Damage: {self.tower.damage}', True, consts.WHITE)
        attack_speed_text = self.font.render(f'Attack Speed: {1/self.tower.cooldown}/s', True, consts.WHITE)
        self.screen.blit(damage_text, (consts.SCREEN_WIDTH - combat_left_pos, 20))
        self.screen.blit(attack_speed_text, (consts.SCREEN_WIDTH - combat_left_pos, 35))
        
        # Draw a button
        self.test_button = Button(10, 750, 100, 30, text=f'DMG+')
        self.test_button.draw(self.screen)
        self.test_button2 = Button(120, 750, 100, 30, text=f'SPD+')
        self.test_button2.draw(self.screen)
        
class Button:
    '''Class defining a simple rectangular button'''
    
    def __init__(self, x, y, width, height, text='', text_color=consts.BLACK, button_color=consts.GREEN):
        self.rect = pygame.Rect(x, y, width, height)
        self.color = button_color
        self.text = text
        self.text_color = text_color
        self.font = pygame.font.Font(None, 24)

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.rect)
        if self.text:
            text_surf = self.font.render(self.text, True, self.text_color)
            text_rect = text_surf.get_rect(center=self.rect.center)
            screen.blit(text_surf, text_rect)

    def is_clicked(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                return True
        return False
