import pygame as pg
import random
import consts
import units

class GameManager:
    '''Centralized game state manager'''
    def __init__(self, screen):
        self.screen = screen

        # Game state
        self.running = True
        self.paused = False
        self.game_over = False
        
        # Resources/scores
        self.cash = 100
        self.wave_number = 0
        
        # Sprite groups
        self.enemies = pg.sprite.Group()
        self.projectiles = pg.sprite.Group()
        self.all_sprites = pg.sprite.Group()
        
        # Tower
        self.tower = units.Tower(
            screen,
            cash = self.cash
        )
        
        # Wave management
        self.last_wave_time = pg.time.get_ticks()
        self.wave_interval_ms = int(consts.WAVE_INTERVAL*1000)
        self.wave_pause_ms = int(consts.WAVE_PAUSE_TIME*1000)
        self.waiting_for_next_wave = False


    def update(self):
        '''Main update loop. Called every frame'''
        
        if self.paused or self.game_over:
            return
    
        # Update all game entities
        self._update_entities()
        
        # Check for wave spawning
        self._check_wave_spawning()
        
        # Process collisions and interactions
        self._process_interactions()
        
        # Check win/lose conditions
        self._check_game_state()
        
        # Sync tower cash with game manager
        self.tower.cash = self.cash
    
    
    def _update_entities(self):
        """Update all game entities"""
        self.enemies.update()
        self.projectiles.update()
        self.tower.update(self.enemies, self.projectiles)
    
        
    def _check_wave_spawning(self):
        """Handle wave spawning logic"""
        now = pg.time.get_ticks()
        time_since_wave = now - self.last_wave_time
        
        # Check if we should spawn a new wave
        if len(self.enemies) == 0:
            if not self.waiting_for_next_wave:
                # All enemies cleared, start waiting period
                self.waiting_for_next_wave = True
                self.last_wave_time = now
            elif time_since_wave >= self.wave_pause_ms:
                # Pause period over, spawn new wave
                self._spawn_next_wave()
                self.waiting_for_next_wave = False
                self.last_wave_time = now
    
                
    def _spawn_next_wave(self):
        """Spawn the next wave of enemies"""
        self.wave_number += 1
        enemy_count = 20 + self.wave_number * 5
        
        print(f"Spawning wave {self.wave_number} with {enemy_count} enemies")
        
        self._spawn_wave(self.enemies, self.all_sprites, self.tower, count = enemy_count)
    
        
    def _spawn_wave(self, enemies_group, all_sprites_group, tower, count=20):
        '''Spawns a wave of enemies around the tower, avoiding spawn range'''
        for _ in range(count):
            # your current random spawn but using Enemy sprite
            rand_x = random.randint(-int(0.5*consts.SCREEN_WIDTH),
                                    int(1.5*consts.SCREEN_WIDTH))
            rand_y = random.randint(-int(0.5*consts.SCREEN_HEIGHT),
                                    int(1.5*consts.SCREEN_HEIGHT))
            enemy = units.Enemy(rand_x, rand_y)
            while ((tower.pos[0] - enemy.x)**2+(tower.pos[1] - enemy.y)**2)**0.5 <= 400:
                # re-roll until out of spawn range
                rand_x = random.randint(-int(0.5*consts.SCREEN_WIDTH),
                                        int(1.5*consts.SCREEN_WIDTH))
                rand_y = random.randint(-int(0.5*consts.SCREEN_HEIGHT),
                                        int(1.5*consts.SCREEN_HEIGHT))
                enemy.x, enemy.y = rand_x, rand_y
                enemy.rect.center = (rand_x, rand_y)
            enemies_group.add(enemy)
            all_sprites_group.add(enemy)
    
            
    def _process_interactions(self):
        """Handle interactions between game entities"""
        # Check for enemies attacking the tower
        for enemy in self.enemies:
            if enemy.state == 'alive' and enemy.touching_tower():
                self._enemy_attack_tower(enemy)
        
        # Clean up dead enemies and award cash
        for enemy in list(self.enemies):
            if enemy.state == 'dead' or not enemy.alive():
                self._handle_enemy_death(enemy)


    def _enemy_attack_tower(self, enemy):
        """Handle enemy attacking the tower"""
        self.tower.health -= enemy.damage
        
        
    def _handle_enemy_death(self, enemy):
        """Handle enemy death - award cash and score"""
        # Award cash for kill (before they're removed)
        if hasattr(enemy, 'health') and enemy.health <= 0:
            self.cash += enemy.bounty
        
    
    def _check_game_state(self):
        """Check for game over conditions"""
        if self.tower.health <= 0:
            self.game_over = True
            print("GAME OVER - Tower Destroyed!")
    
    
    def toggle_pause(self):
        """Toggle pause state"""
        self.paused = not self.paused
    
    
    def reset_game(self):
        """Reset the game to initial state"""
        self.__init__(self.screen)

    
    def upgrade_tower_damage(self):
        """Upgrade tower damage if player has enough cash"""
        upgrade_cost = 50 + self.tower.damage * 2
        
        if self.cash >= upgrade_cost:
            self.cash -= upgrade_cost
            self.tower.damage += 5
            print(f"Damage upgraded to {self.tower.damage}. Remaining cash: ${self.cash}")
            return True
        else:
            print(f"Not enough cash! Need ${upgrade_cost}, have ${self.cash}")
            return False
    
    
    def upgrade_tower_speed(self):
        """Upgrade tower attack speed if player has enough cash"""
        upgrade_cost = 50 + (self.tower.cooldown * 3)
        
        if self.cash >= upgrade_cost and self.tower.cooldown > 5:
            self.cash -= upgrade_cost
            self.tower.cooldown -= 2
            print(f"Speed upgraded! Cooldown: {self.tower.cooldown}. Remaining cash: ${self.cash}")
            return True
        else:
            if self.tower.cooldown <= 5:
                print("Speed already at maximum!")
            else:
                print(f"Not enough cash! Need ${upgrade_cost}, have ${self.cash}")
            return False
    
    
    def upgrade_tower_armor(self):
        """Upgrade tower armor (max health) if player has enough cash"""
        upgrade_cost = 50 + (self.tower.max_health * 2)
        
        if self.cash >= upgrade_cost:
            self.cash -= upgrade_cost
            self.tower.max_health += 20
            self.tower.health += 20
            print(f"Armor upgraded! Max health: {self.tower.max_health}. Remaining cash: ${self.cash}")
            return True
        else:
            print(f"Not enough cash! Need ${upgrade_cost}, have ${self.cash}")
            return False
    
    
    def draw(self):
        """Draw all game entities"""
        self.enemies.draw(self.screen)
        self.projectiles.draw(self.screen)
        self.tower.draw(self.screen)