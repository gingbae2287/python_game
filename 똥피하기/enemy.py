# enemy.py
import pygame
# import game1

class Enemy:
    y_acc=0.0005
    y_vel=0
    enemy_end=False
    def __init__(self,x_pos):
        self.enemy=pygame.image.load("enemy.png")
        self.enemy_width,self.enemy_height=self.enemy.get_rect().size
        self.enemy_x_pos=x_pos
        self.enemy_rect=self.enemy.get_rect()
        if self.enemy_x_pos<0:
            self.enemy_x_pos=0
        elif self.enemy_x_pos>480-self.enemy_width:
            self.enemy_x_pos=480-self.enemy_width
        self.enemy_y_pos=-self.enemy_height
    def move(self,dt):
        if not self.enemy_end:
            self.enemy_y_pos+=self.y_vel*dt
            self.y_vel+=self.y_acc*dt
            self.enemy_rect.left=self.enemy_x_pos
            self.enemy_rect.top=self.enemy_y_pos  
        if self.enemy_y_pos>640:
            self.enemy_end=True

    def __del__(Self):
        pass



