# 공을 터뜨리면 작은공 두개로 쪼개짐. 총 4단계
# 공 크기별로 max_height이 존재.
# 중력가속도 설정후 공이 땅에 닿으면 각 크기별 고정속도로 변함
# 땅에서튀어오르는 속도= sqrt(2*g*max_height)

import pygame
import math
import random
import setting
screen_width=setting.screen_width
screen_height=setting.screen_height
g=setting.gravity   # 중력가속도
ball_x_vel=setting.ball_x_vel  # 공 x속도
class ball:
    def __init__(self,x,y,size=1,x_dir=1):
        self.size=size
        self.ball=pygame.image.load(f"image/pang{self.size}.png")
        self.w,self.h=self.ball.get_rect().size # 공 길이,높이
        self.max_h=screen_height/8*(self.size+1)    # 좌표상 최대 위치
        self.max=screen_height-self.h-self.max_h    # 최대 높이(계산용)
        self.x_pos=x
        self.y_pos=y
        if self.size==1:
            self.x=random.randrange(0,screen_width-self.w)
            self.y=self.max_h
        self.y_vel=-0.3  # 초기 y속도
        self.x_vel=ball_x_vel*x_dir    # x속도
        self.ball_rect=self.ball.get_rect()
    def move(self,dt):

        # 풍선 움직임
        self.x_pos+=self.x_vel*dt
        self.y_pos+=self.y_vel*dt
        self.y_vel+=g*dt

        if self.x_pos<0:
            self.x_pos=0
            self.x_vel=-self.x_vel
        elif self.x_pos>screen_width-self.w:
            self.x_pos=screen_width-self.w
            self.x_vel=-self.x_vel
        if self.y_pos>screen_height-self.h:
            self.y_pos=screen_height-self.h
            self.y_vel=-math.sqrt(2*g*self.max)
        elif self.y_pos<self.max_h:
            self.y_pos=self.max_h
            self.y_vel=0

        self.ball_rect.left=self.x_pos
        self.ball_rect.top=self.y_pos

    


