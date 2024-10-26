import random
import consts
import units

def spawn_enemies(number, tower):
    enemies = []
    for _ in range(number):
        rand_x = random.randint(-int(0.5*consts.SCREEN_WIDTH),
                                int(1.5*consts.SCREEN_WIDTH))
        rand_y = random.randint(-int(0.5*consts.SCREEN_HEIGHT),
                                int(1.5*consts.SCREEN_HEIGHT))
        enemy = units.Enemy(rand_x, rand_y)
        while in_spawn_range(enemy, tower):
            rand_x = random.randint(-int(0.5*consts.SCREEN_WIDTH),
                                    int(1.5*consts.SCREEN_WIDTH))
            rand_y = random.randint(-int(0.5*consts.SCREEN_HEIGHT),
                                    int(1.5*consts.SCREEN_HEIGHT))
            enemy = units.Enemy(rand_x, rand_y)
        enemies.append(units.Enemy(rand_x, rand_y))
    return enemies


def in_spawn_range(enemy, tower):
    return ((tower.pos[0] - enemy.x)**2+(tower.pos[1] - enemy.y)**2)**0.5 <= 400
