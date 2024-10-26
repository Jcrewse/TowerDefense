import pygame, consts

class Interface:

    def __init__(self, screen, tower, wave_number):
        self.font = pygame.font.Font(None, 18)
        self.screen = screen
        self.tower = tower
        self.wave_number = wave_number

    def update(self):
        # Draw health bar (DOESNT MOVE YET)
        buff = 2
        healthbar_tray_pos = (consts.SCREEN_WIDTH/2 - consts.HEALTHBAR_SIZE/2, 50, consts.HEALTHBAR_SIZE, 20)
        healthbar_pos = (consts.SCREEN_WIDTH/2 - consts.HEALTHBAR_SIZE/2 + buff, 50 + buff, consts.HEALTHBAR_SIZE*(self.tower.health/self.tower.max_health) - 2*buff, 20 - 2*buff)
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
