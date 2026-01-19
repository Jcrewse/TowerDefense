'''Units for TowerDefense'''
import pygame
import pygame.gfxdraw as gfxdraw
import consts
import math


class Tower:
    '''Class defining the tower'''

    def __init__(self, screen, health=100, regen=0.1,
                 damage=1, range=200, cooldown=30, cash=0):

        self.screen = screen                              # Game screen

        # Geometry
        self.pos = (consts.TOWER_X, consts.TOWER_Y)       # Tower position

        # Health
        self.health = health                              # Current health
        self.max_health = health                          # Maximum health
        self.regen = regen / consts.FPS                     # Current health regen

        # Attack stats
        self.damage = damage                              # Shot damage
        self.range = range                                # Shot range
        self.cooldown_count = cooldown                    # Shot current cooldown
        self.cooldown = cooldown                          # Shot cooldown max

        # Resources/scores
        self.cash = cash                                  # Current cash
        self.wave_number = 1                              # Current wave number

        # Lists
        self.projectiles = []                             # Projectile list
        self.targets = []                                 # Current targets list

        self.current_target = None

        # Tower surface for drawing
        self.surface = pygame.Surface(
            (consts.TOWER_SIZE, consts.TOWER_SIZE), pygame.SRCALPHA)

        # self.attack_sound = pygame.mixer.Sound('assets/sounds/shot_sound.wav')

    def update(self, enemies_group, projectiles_group):
        '''
        Updates tower for each frame
        '''
        if self.cooldown_count > 0:
            self.cooldown_count -= 1

        self._update_targets(enemies_group)

        if self.cooldown_count == 0 and self.current_target is not None:
            shot = Projectile(
                self.pos, self.current_target, speed=5, damage=self.damage)
            projectiles_group.add(shot)
            self.cooldown_count = self.cooldown
            # self.attack_sound.play()

    def _update_targets(self, enemies_group):
        '''
        Updates current targets list based on enemies in range
        '''
        if not self._valid_target(self.current_target):
            self.current_target = None

        # Acquire target if we don't have one
        if self.current_target is None:
            cx, cy = self.pos
            range_sq = self.range * self.range
            # Simple “closest to tower” selection
            best_enemy = None
            best_dist_sq = None
            for enemy in enemies_group:
                if getattr(enemy, "state",
                           "alive") != "alive" or enemy.health <= 0:
                    continue
                ex, ey = enemy.rect.center
                dx = ex - cx
                dy = ey - cy
                dist_sq = dx * dx + dy * dy
                if dist_sq <= range_sq and (
                        best_dist_sq is None or dist_sq < best_dist_sq):
                    best_dist_sq = dist_sq
                    best_enemy = enemy
            self.current_target = best_enemy

    def _valid_target(self, enemy):
        if enemy is None:
            return False
        if not enemy.alive():
            return False
        if getattr(enemy, "state", "alive") != "alive" or enemy.health <= 0:
            return False
        cx, cy = self.pos
        ex, ey = enemy.rect.center
        dx = ex - cx
        dy = ey - cy
        return dx * dx + dy * dy <= self.range * self.range

    def upgrade_damage(self):
        '''Upgrade tower damage'''
        print('Upgrading damage')
        upgrade_cost = 50 + self.damage * 2
        if self.cash >= upgrade_cost:
            self.cash -= upgrade_cost
            self.damage += 5

    def upgrade_speed(self):
        '''Upgrade tower speed (reduce cooldown)'''
        print('Upgrading speed')
        upgrade_cost = 50 + (self.cooldown * 3)
        if self.cash >= upgrade_cost and self.cooldown > 5:
            self.cash -= upgrade_cost
            self.cooldown -= 2

    def upgrade_armor(self):
        '''Upgrade tower armor (increase max health)'''
        print('Upgrading armor')
        upgrade_cost = 50 + (self.max_health * 2)
        if self.cash >= upgrade_cost:
            self.cash -= upgrade_cost
            self.max_health += 20
            self.health += 20  # also heal current health

###############################################################################
# RENDER FUNCTIONS
###############################################################################

    def draw(self, screen):
        '''Draw tower elements to screen surface'''
        pygame.draw.circle(screen, (0, 255, 0), self.pos, 20)
        #pygame.draw.circle(screen, (0, 100, 0), self.pos, self.range, 1)
        self._draw_range_circle(screen)
        
    def _draw_range_circle(self, screen):
        '''Draw the tower's range circle'''
        for angle in range(0, 360, 5):
            gfxdraw.arc(screen, int(self.pos[0]), int(self.pos[1]), self.range, angle, angle + 2, (0, 255, 0))


###############################################################################


class Enemy(pygame.sprite.Sprite):
    '''
    Class defining enemies using pygame sprite system
    '''

    def __init__(self, x, y, health=1, damage=1, speed=1, bounty=1):
        super().__init__()
        self.state = 'alive'
        self.health = health
        self.death_timer = 0
        self.death_duration = 30
        self.damage = damage
        self.x = x
        self.y = y
        self.speed = speed
        self.bounty = bounty

        self.base_image = pygame.Surface((20, 20), pygame.SRCALPHA)
        # pygame.draw.polygon(
        #     self.base_image,
        #     (255, 255, 255),
        #     [(16, 10), (10, 5), (10, 15)]  # little arrow tip on the right side
        # )
        pygame.draw.rect(self.base_image, (255, 0, 0), (0, 0, 20, 20))
        self.image = self.base_image.copy()
        self.rect = self.image.get_rect(center=(self.x, self.y))

    def update(self):
        '''
        Updates enemy each frame
        '''
        if self.state == 'alive':
            self._move()
        elif self.state == 'dying':
            self._animate_death()

        if self.health <= 0 and self.state == 'alive':
            self.state = 'dying'
            self.death_timer = 0

        if self.state == 'dead':
            self.kill()

    def _move(self):
        '''Moves enemy towards tower'''
        if self.state != 'alive':
            return

        # Calculate direction to move
        direction = self._calculate_direction()

        self.image = pygame.transform.rotate(
            self.base_image, math.degrees(math.atan2(-direction[1], direction[0])))

        # Check if against the tower
        if self.touching_tower():
            return
        else:
            self.x += direction[0] * self.speed
            self.y += direction[1] * self.speed
            self.rect.center = (self.x, self.y)

    def touching_tower(self):
        '''
        Returns True if within the distance of the tower size
        '''
        dx = consts.TOWER_X - self.x
        dy = consts.TOWER_Y - self.y
        dist = (dx**2 + dy**2)**0.5
        return dist <= consts.TOWER_SIZE

    def _animate_death(self):
        '''Animates enemy death'''
        # Advance timer
        self.death_timer += 1

        # Calculate fade-out alpha
        alpha = max(0, 255 * (1 - self.death_timer / self.death_duration))

        # Start with the base image
        temp_image = self.base_image.copy()

        # Apply alpha/transparency to it
        temp_image.set_alpha(int(alpha))

        # Now rotate it to face the tower
        angle = math.degrees(
            math.atan2(-(consts.TOWER_Y - self.y), (consts.TOWER_X - self.x)))
        self.image = pygame.transform.rotate(temp_image, angle)

        # Update rect to keep it centered (rotation changes size)
        self.rect = self.image.get_rect(center=(self.x, self.y))

        if self.death_timer >= self.death_duration:
            self.state = "dead"

    def _calculate_direction(self):
        '''
        Calculated direction from tower to enemy
        '''
        dx = consts.TOWER_X - self.x
        dy = consts.TOWER_Y - self.y
        dist = (dx**2 + dy**2)**0.5
        return dx / dist, dy / dist, dist


###############################################################################

class Projectile(pygame.sprite.Sprite):
    '''Class defining projectiles shot by the tower'''

    def __init__(self, pos, target, speed=5, damage=10):
        super().__init__()
        self.image = pygame.Surface((6, 6))
        pygame.draw.circle(self.image, (255, 255, 0), (3, 3), 3)
        self.rect = self.image.get_rect(center=pos)
        self.target = target
        self.speed = speed
        self.damage = damage

        # New: store velocity and whether we're still homing
        self.vx = 0.0
        self.vy = 0.0
        self.tracking = True

    def update(self):
        '''Moves projectile towards target (while alive), then flies straight'''
        # If we're still tracking, try to home in on the target
        if self.tracking:
            if not self._alive_target():
                # Target is gone: stop tracking but keep current velocity
                self.tracking = False
            else:
                tx, ty = self.target.rect.center
                x, y = self.rect.center
                dx = tx - x
                dy = ty - y
                dist_sq = dx * dx + dy * dy

                # Hit detection
                if dist_sq <= 25:  # hit radius (~5 px)
                    self.target.health -= self.damage
                    self.kill()
                    return

                dist = math.sqrt(dist_sq)
                if dist == 0:
                    self.kill()
                    return

                # Update velocity to home in on target
                self.vx = self.speed * dx / dist
                self.vy = self.speed * dy / dist

        # Move using current velocity
        self.rect.x += self.vx
        self.rect.y += self.vy

        # Kill projectile once it goes off-screen (with a small margin)
        x, y = self.rect.center
        if (x < -50 or x > consts.SCREEN_WIDTH + 50 or
                y < -50 or y > consts.SCREEN_HEIGHT + 50):
            self.kill()

    def _alive_target(self):
        '''Target still exists in the game'''
        return (
            self.target is not None and
            self.target.alive()
        )
