from pico2d import *
import game_world
import game_framework

class Ball:
    image = None

    def __init__(self, x = 400, y = 300, velocity = 1):
        if Ball.image == None:
            Ball.image = load_image('ball21x21.png')
        self.x, self.y, self.velocity = x, y, velocity
        self.active = True

    def draw(self):
        self.image.draw(self.x, self.y)
        draw_rectangle(*self.get_bb())


    def update(self):
        if self.active:
            self.x += self.velocity * 100 * game_framework.frame_time
            if self.x < 25 or self.x > 1600 - 25:
                self.active = False
                game_world.remove_object(self)
        else:
            pass


    def get_bb(self):
        # fill here
        return self.x-10, self.y-10, self.x+10, self.y+10
        pass

    def handle_collision(self, group, other):
        if group == 'boy:ball':
            game_world.remove_object(self)
        elif group == 'ball:zombie' and self.active:
            print("Ball hit Zombie, removing Ball.")  # 디버깅 로그
            self.active = False
            game_world.remove_object(self)  # 충돌 후 즉시 게임 월드에서 제거

