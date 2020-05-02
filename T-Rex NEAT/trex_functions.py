import random
import neat

def collide(object1, object2):
    if (((((object2.hitbox[0] >= object1.hitbox[0]) and (object2.hitbox[0] <= object1.hitbox[0] + object1.hitbox[2])) or
         ((object2.hitbox[0] + object2.hitbox[2] >= object1.hitbox[0]) and (
                 object2.hitbox[0] + object2.hitbox[2] <= object1.hitbox[0] + object1.hitbox[2]))) and
            (((object2.hitbox[1] >= object1.hitbox[1]) and (
                    object2.hitbox[1] <= object1.hitbox[1] + object1.hitbox[3])) or
             ((object2.hitbox[1] + object2.hitbox[3] >= object1.hitbox[1]) and (
                     object2.hitbox[1] + object2.hitbox[3] <= object1.hitbox[1] + object1.hitbox[3])))) or
        ((((object1.hitbox[0] >= object2.hitbox[0]) and (object1.hitbox[0] <= object2.hitbox[0] + object2.hitbox[2])) or
          ((object1.hitbox[0] + object1.hitbox[2] >= object2.hitbox[0]) and (
                  object1.hitbox[0] + object1.hitbox[2] <= object2.hitbox[0] + object2.hitbox[2]))) and
         (((object1.hitbox[1] >= object2.hitbox[1]) and (
                 object1.hitbox[1] <= object2.hitbox[1] + object2.hitbox[3])) or
          ((object1.hitbox[1] + object1.hitbox[3] >= object2.hitbox[1]) and (
                  object1.hitbox[1] + object1.hitbox[3] <= object2.hitbox[1] + object2.hitbox[3]))))):
        return True
    else:
        return False

def elem_appears(elem_list, elem_class, elem_img_list, elem_y):
    elem_list.append(elem_class(elem_img_list[random.randint(0, len(elem_img_list)-1)], elem_y))
    return elem_list
