import time
import arcade

from Player import Player
from ground import Ground ,Box
from enemy import Enemy

class Game(arcade.Window):
    def __init__(self):
        self.w = 1000
        self.h =700
        self.gravity = 0.1
        super().__init__(self.w,self.h, "Platform Game")
        self.background_image= arcade.load_texture("th.jpg")

        self.t1 = time.time()

        self.key = arcade.Sprite(":resources:images/items/keyGreen.png")
        self.key.center_x = 100
        self.key.center_y = 600
        self.key.width = 50
        self.key.height = 50
        
        self.lock = arcade.Sprite(":resources:images/tiles/lockRed.png")
        self.lock.center_x = 900
        self.lock.center_y = 130
        self.lock.width = 50
        self.lock.height = 50

        self.me = Player()
        self.ground_list = arcade.SpriteList()
        self.enemy_list = arcade.SpriteList()
        
        for i in range (0, 1000,120):
            ground= Ground(i, 40)
            self.ground_list.append(ground)

        for i in range (100, 500, 80):
            box= Box(i, 530)
            self.ground_list.append(box)

        for i in range (500, 700,80):
            box= Box(i, 270)
            self.ground_list.append(box)




        self.my_physics_engine = arcade.PhysicsEnginePlatformer(self.me, self.ground_list,gravity_constant=self.gravity)
        
        self.enemy_physics_engine_list = []


    def on_draw(self):
        arcade.start_render()
        arcade.draw_lrwh_rectangle_textured(0, 0, self.w, self.h,self.background_image)
        
        try:
            self.key.draw()

        except:
            pass  

        self.lock.draw()

        self.me.draw()
        for ground in self.ground_list:
            ground.draw()

        for enemy in self.enemy_list:
            enemy.draw()

    def on_update(self, delta_time:float):
        self.t2 = time.time()

        try:
            if arcade.check_for_collision(self.me, self.key):
                self.me.pocket.append(self.key)
                del self.key

        except:
            pass        
        
        if arcade.check_for_collision(self.me,self.lock) and len(self.me.pocket) == 1 :
            self.lock.texture = arcade.load_texture(":resources:images/items/gold_2.png")



        if self.t2 - self.t1 > 5 :
            new_enemy = Enemy()
            self.enemy_list.append(new_enemy)
            self.enemy_physics_engine_list.append(arcade.PhysicsEnginePlatformer(new_enemy, self.ground_list,gravity_constant=self.gravity))
            self.t1 = time.time()

        self.my_physics_engine.update()

        for item in self.enemy_physics_engine_list:
            item.update()
           
        for enemy in self.enemy_list:
           enemy.update_animation()
        
        self.me.update_animation()
        


    def on_key_press(self, key, modifiers):
        
        if key == arcade.key.LEFT:
            self.me.change_x = -1 * self.me.speed
        
        elif key == arcade.key.RIGHT:
            self.me.change_x = 1 *self.me.speed

        elif key == arcade.key.UP:
           if self.my_physics_engine.can_jump():
             self.me.change_y = 10

    def on_key_release(self, key, modifiers):
        self.me.change_x = 0

game=Game()
arcade.run()