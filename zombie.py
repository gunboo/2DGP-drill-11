import random
import math
import game_framework
import game_world

from pico2d import *

# zombie Run Speed
PIXEL_PER_METER = (10.0 / 0.3)  # 10 pixel 30 cm
RUN_SPEED_KMPH = 10.0  # Km / Hour
RUN_SPEED_MPM = (RUN_SPEED_KMPH * 1000.0 / 60.0)
RUN_SPEED_MPS = (RUN_SPEED_MPM / 60.0)
RUN_SPEED_PPS = (RUN_SPEED_MPS * PIXEL_PER_METER)

# zombie Action Speed
TIME_PER_ACTION = 0.5
ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
FRAMES_PER_ACTION = 10.0

animation_names = ['Walk']

class Zombie:
    images = None

    def load_images(self):
        if Zombie.images == None:
            Zombie.images = {}
            for name in animation_names:
                Zombie.images[name] = [load_image("./zombie/"+ name + " (%d)" % i + ".png") for i in range(1, 11)]

    def __init__(self):
        self.x, self.y = random.randint(1600-800, 1600), 150
        self.size = (200, 200)
        self.load_images()
        self.frame = random.randint(0, 9)
        self.dir = random.choice([-1,1])
        self.hit_count = 0

    def update(self):
        self.frame = (self.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % FRAMES_PER_ACTION
        self.x += RUN_SPEED_PPS * self.dir * game_framework.frame_time
        if self.x > 1600:
            self.dir = -1
        elif self.x < 800:
            self.dir = 1
        self.x = clamp(800, self.x, 1600)
        pass


    def draw(self):
        draw_rectangle(*self.get_bb())
        if self.dir < 0:
            Zombie.images['Walk'][int(self.frame)].composite_draw(0, 'h', self.x, self.y, self.size[0], self.size[1])
        else:
            Zombie.images['Walk'][int(self.frame)].draw(self.x, self.y, self.size[0], self.size[1])

    def handle_event(self, event):
        pass

    def handle_collision(self, group, other):
        if group == 'boy:zombie':
            print("Game Over! Boy collided with Zombie.")
            game_framework.quit()  # 게임 종료
        elif group == 'ball:zombie' and other.active:
            print(f"Zombie {id(self)} hit by Ball! Current hit count: {self.hit_count}")
            self.hit_count += 1
            if self.hit_count == 1:
                self.resize()  # 첫 충돌: 크기 감소
            elif self.hit_count >= 2:
                print(f"Zombie {id(self)} removed after 2 hits")
                game_world.remove_object(self)  # 두 번째 충돌: 좀비 제거


    def resize(self):
        self.size= (self.size[0] // 2, self.size[1] // 2)

    def get_bb(self):
        return  self.x - 50, self.y - 100, self.x + 50, self.y + 100

