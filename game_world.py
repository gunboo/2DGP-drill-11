from itertools import filterfalse
world = [[] for _ in range(4)]
collision_pairs = {} #빈 딕셔너리

def add_collision_pair(group, a, b):
    if group not in collision_pairs:
        collision_pairs[group] = [ [], [] ]
    if a:
        print(f'Adding {type(a)} to group {group}')  # 디버그 출력
        collision_pairs[group][0].append(a)
    if b:
        print(f'Adding {type(b)} to group {group}')  # 디버그 출력
        collision_pairs[group][1].append(b)
def add_object(o, depth = 0):
    world[depth].append(o)

def add_objects(ol, depth = 0):
    world[depth] += ol


def update():
    for layer in world:
        for o in layer:
            o.update()


def render():
    for layer in world:
        for o in layer:
            o.draw()
def remove_collision_object(o):
    for pairs in collision_pairs.values():
        if o in pairs[0]:
            pairs[0].remove(o) #0에 들어있다면 제거
        if o in pairs[1]:
            pairs[1].remove(o) #1에 들어있다면 제거

def remove_object(o):
    if has_object(o):  # 객체가 존재하는 경우에만 제거
        for layer in world:
            if o in layer:
                layer.remove(o)
                remove_collision_object(o)
                del o
                return
    else:
        print(f"Warning: Tried to remove non-existing object {o}")

    raise ValueError('Cannot delete non existing object')


def clear():
    for layer in world:
        layer.clear()

def has_object(o):
    for layer in world:
        if o in layer:
            return True  # 객체가 존재하면 True 반환
    return False  # 객체가 없으면 False 반환

# fill here
def collide(a, b):
    al,ab,ar,at = a.get_bb()
    bl,bb,br,bt = b.get_bb()

    if ar < bl: return False
    if al > br: return False
    if at < bb: return False
    if ab > bt: return False

    return True

def handle_collisions():
    for group, pairs in collision_pairs.items():
        for a in pairs[0]:
            for b in pairs[1]:
                if has_object(a) and has_object(b):  # 유효한 객체만 충돌 검사
                    if collide(a, b):
                        print(f'{group} collide')
                        a.handle_collision(group, b)
                        b.handle_collision(group, a)


    return None