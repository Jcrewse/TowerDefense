'''Units for TowerDefense'''
import pygame
import consts


class Projectile:
    '''Class defining projectiles shot by the tower'''

    def __init__(self, pos, target, speed, damage):
        self.x = pos[0]
        self.y = pos[1]
        self.target = target
        self.speed = speed
        self.damage = damage
        self.direction = self.calculate_direction()

    def calculate_direction(self):
        '''Calculates direction from projectile to target'''
        dx = self.target.x - self.x
        dy = self.target.y - self.y
        distance = (dx**2 + dy**2)**0.5
        return dx/distance, dy/distance

    def move(self):
        '''Changes projectile position according to direction and speed'''
        self.x += self.direction[0]*self.speed
        self.y += self.direction[1]*self.speed

    def draw(self, surface):
        '''Draws projectile as a small circle'''
        pygame.draw.circle(surface, consts.WHITE,
                           (int(self.x), int(self.y)), 5)

    def has_hit_target(self):
        '''Returns True if distance between projectile position and target position
        is less than 5 (arbitrary selection, could refine)'''
        return ((self.target.x - self.x)**2 + (self.target.y - self.y)**2)**0.5 < 5

class Tower:
    '''Class defining the tower'''

    def __init__(self, screen, health=100, regen=0.5, damage=15, range=150, cooldown=25, cash=0):
        self.screen = screen                              # Game screen
        self.pos = (consts.TOWER_X, consts.TOWER_Y)       # Tower position
        self.health = health                              # Current health
        self.max_health = health                          # Maximum health
        self.damage = damage                              # Shot damage
        self.range = range                                # Shot range
        self.cooldown_count = cooldown                    # Shot current cooldown
        self.cooldown = cooldown                          # Shot cooldown max
        self.cash = cash                                  # Current cash
        self.regen = regen/consts.FPS                     # Current health regen
        self.projectiles = []                             # Projectile list

    def update(self, screen, enemies):
        '''
        Updates tower for each frame
        '''
        self.draw(screen)
        self.attack(enemies)
        self.update_projectiles()
        self.regenerate_health()
        self.cooldown_tick()

    def draw(self, surface):
        '''
        Draws tower
        '''
        # Draw tower
        pygame.draw.circle(surface,
                           consts.GREEN,
                           self.pos,
                           consts.TOWER_SIZE)

        # Draw range circle
        pygame.draw.circle(surface,
                           consts.GREEN,
                           self.pos,
                           self.range,
                           width=1)

    def attack(self, enemies):
        '''
        Targets enemies and shoots projectiles. 
        If cooldown is zero, cycle through current enemies list 
            If an enemy in range
                i.  Add projectile to projectiles list
                ii. Reset cooldown
        '''
        if self.cooldown_count == 0:
            for enemy in enemies:
                if self.in_range(enemy):
                    shot = Projectile(
                        self.pos, enemy, speed=10, damage=self.damage)
                    self.projectiles.append(shot)
                    self.cooldown_count = self.cooldown
                    break

    def update_projectiles(self):
        '''
        Updates all active projectiles
        '''
        for projectile in self.projectiles[:]:
            projectile.move()
            if projectile.has_hit_target():
                projectile.target.health -= projectile.damage
                self.projectiles.remove(projectile)
            else:
                projectile.draw(self.screen)

    def in_range(self, target):
        '''
        Returns True if target is within range of tower
        '''
        return ((target.x - self.pos[0])**2+(target.y - self.pos[1])**2)**0.5 <= self.range

    def cooldown_tick(self):
        '''
        If cooldown > 0, reduces current cooldown count by 1.
        '''
        if self.cooldown_count > 0:
            self.cooldown_count -= 1

    def regenerate_health(self):
        '''
        Increases health by regen amount
        '''
        if self.health < self.max_health:
            self.health += self.regen

    def take_damage(self, damage):
        '''
        Reduces tower health by damage amount.
        '''
        self.health -= damage/consts.FPS

    def give_cash(self):
        '''
        Increases tower cash by 1.
        '''
        self.cash += 1

    def upgrade_attack_speed(self):
        '''
        Upgrades tower attack speed (reduced cooldown)
        '''
        cost = 10
        if self.cash >= cost and self.cooldown > 1:
            self.cash -= cost
            self.cooldown -= 1

    def upgrade_damage(self):
        '''
        Upgrades tower attack damage
        '''
        cost = 10
        if self.cash >= cost:
            self.cash -= cost
            self.damage += 1

class Enemy:
    '''
    Class defining enemy
    '''

    def __init__(self, x, y, health=10, damage=5, speed=1):
        self.health = health
        self.damage = damage
        self.x = x
        self.y = y
        self.speed = speed

    def draw(self, surface):
        '''
        Draws enemy
        '''
        rect = (self.x - 10, self.y - 10, 20, 20)
        pygame.draw.rect(surface, (255, 0, 0), rect)

    def calculate_direction(self):
        '''
        Calculated direction from tower to enemy
        '''
        dx = consts.TOWER_X - self.x
        dy = consts.TOWER_Y - self.y
        dist = (dx**2 + dy**2)**0.5
        return dx/dist, dy/dist, dist

    def touching_tower(self):
        '''
        Returns True if within the distance of the tower size
        '''
        dx = consts.TOWER_X - self.x
        dy = consts.TOWER_Y - self.y
        dist = (dx**2 + dy**2)**0.5
        return dist <= consts.TOWER_SIZE

    def move(self):
        '''
        Moves enemy towards tower according to speed
        '''
        # Calculate direction to move
        direction = self.calculate_direction()

        # Check if against the tower
        if self.touching_tower():
            return
        else:
            self.x += direction[0]*self.speed
            self.y += direction[1]*self.speed

    def attack(self, tower):
        '''
        Attacks tower if touching it. Reducing tower health.
        '''
        if self.touching_tower():
            tower.take_damage(self.damage)
