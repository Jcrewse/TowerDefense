import random
import consts
import units

def spawn_wave(enemies_group, all_sprites_group, tower, count=20):
    for _ in range(count):
        # your current random spawn but using Enemy sprite
        rand_x = random.randint(-int(0.5*consts.SCREEN_WIDTH),
                                int(1.5*consts.SCREEN_WIDTH))
        rand_y = random.randint(-int(0.5*consts.SCREEN_HEIGHT),
                                int(1.5*consts.SCREEN_HEIGHT))
        enemy = units.Enemy(rand_x, rand_y)
        while in_spawn_range(enemy, tower):
            # re-roll until out of spawn range
            rand_x = random.randint(-int(0.5*consts.SCREEN_WIDTH),
                                    int(1.5*consts.SCREEN_WIDTH))
            rand_y = random.randint(-int(0.5*consts.SCREEN_HEIGHT),
                                    int(1.5*consts.SCREEN_HEIGHT))
            enemy.x, enemy.y = rand_x, rand_y
            enemy.rect.center = (rand_x, rand_y)
        enemies_group.add(enemy)
        all_sprites_group.add(enemy)


def in_spawn_range(enemy, tower):
    return ((tower.pos[0] - enemy.x)**2+(tower.pos[1] - enemy.y)**2)**0.5 <= 400
