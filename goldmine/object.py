import pygame
import os
import random
from setting import *
current_path=os.path.dirname(__file__)

# 색깔
RED=(255,0,0)
BLACK=(0,0,0)

# 변수
offset_of_claw=40 # 중심점으로 부터 집게 거리
LEFT=-1
RIGHT=1
STOP=0
COMEBACK=2
left_max_angle=170
right_max_angle=10
object_count=0  # 오브젝트수

# 그룹생성
object_group=pygame.sprite.Group()

pygame.display.init()
screen=pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Glod Miner")
# 오브젝트 이미지
# convert_alpha 는 투명한 부분을 제외한 이미지를 불러옴
object_gold=pygame.image.load(os.path.join(current_path,"images/gold.png")).convert_alpha()  # 큰금
object_stone=pygame.image.load(os.path.join(current_path,"images/stone.png")).convert_alpha()
object_dia=pygame.image.load(os.path.join(current_path,"images/diamond.png")).convert_alpha()
object_claw=pygame.image.load(os.path.join(current_path,"images/claw.png")).convert_alpha()

gold_w,gold_h=object_gold.get_rect().size
dia_w,dia_h=object_dia.get_rect().size
stone_w,stone_h=object_stone.get_rect().size
# sprite 2D 이미지들 관리
# 보석, 돌 오브젝트
class object(pygame.sprite.Sprite):
    # 랜덤 확률에따라 보석 종류 결정
    # 보석 종류에 따라 무게 및 크기 결정(=가치)
    # 위치는 충돌 안일어나게 랜덤
    def __init__(self,num):
        # 오브젝트  base설정
        super().__init__()
        if num<chance_of_gold:
            self.w=random.randrange(gold_w-15,gold_w+5)
            self.h=int(self.w*gold_h/gold_w)
            self.price=self.w
            self.weight=self.w/gold_w*2
            self.image=pygame.transform.scale(object_gold,(self.w,self.h))

        elif chance_of_gold<=num<chance_of_gold+chance_of_dia:
            self.w=random.randrange(dia_w-20,dia_w)
            self.h=int(self.w*dia_h/dia_w)
            self.price=self.w*8
            self.weight=self.w/dia_w*2
            self.image=pygame.transform.scale(object_dia,(self.w,self.h))
        elif num>=100-chance_of_stone:
            self.w=random.randrange(stone_w-20,stone_w+10)
            self.h=int(self.w*stone_h/stone_w)
            self.price=int(self.w/4)
            self.weight=self.w/stone_w*4
            self.image=pygame.transform.scale(object_stone,(self.w,self.h))
        while 1:
            # 서로 겹치지 않게 오브젝트 생성
            no_collision=True
            x=random.randrange(100,screen_width-100)
            y=random.randrange(150, screen_height-100)
            self.rect=self.image.get_rect(center=(x,y))
            for object in object_group:
                 if self.rect.colliderect(object.rect):
                     no_collision=False
                     continue
            if no_collision: break
    def set_position(self, x,y):
        self.rect.center=(x,y)
# 집게
class Claw(pygame.sprite.Sprite):
    def __init__(self,image,position):
        super().__init__()
        self.score=0    # 점수. 집게가 하나라 집게에 만듬
        self.image=image
        self.original_image=image
        self.rect=image.get_rect(center=position)
        self.line_speed=claw_speed    # 선 길이
        self.offset=pygame.math.Vector2(offset_of_claw,0) # 중심으로부터 떨어뜨리기
        self.position=position  # 위치
        self.direction=LEFT # 집게 이동방향
        self.angle_speed= claw_angle_speed  # 각속도
        self.angle=10   # 현재 각도
        self.grab=False
        self.grab_object=None
        self.grab_distance=None



    def update(self,dt):
        if self.direction==LEFT:
            self.angle+=self.angle_speed*dt
        elif self.direction==RIGHT:
            self.angle-=self.angle_speed*dt
        elif self.direction==STOP:
            self.offset.x+=self.line_speed*dt
            if self.grab==False:    # 물체 안잡혔을때 잡으면
                try:
                    for object in object_group:
                        #if self.rect.colliderect(object.rect):  # 직사각형 충돌확인
                        if pygame.sprite.collide_mask(self, object):        # 투명영역제외한 충돌확인
                            self.grab=True
                            self.line_speed=-(claw_speed/object.weight)
                            self.grab_object=object
                            self.grab_distance=(self.rect.center[0]-object.rect.center[0],self.rect.center[1]-object.rect.center[1])
                            break
                except:
                    pass

        if self.angle>left_max_angle:
            self.angle=left_max_angle
            self.direction=RIGHT
        elif self.angle<right_max_angle:
            self.angle=right_max_angle
            self.direction=LEFT


        elif self.rect.left<0 or self.rect.right>screen_width or self.rect.bottom > screen_height:
            self.line_speed=-claw_speed

        elif self.offset.x<offset_of_claw:  # 집게 돌아오고 나면
            self.offset.x=offset_of_claw
            self.line_speed=claw_speed
            self.direction=self.tmp_dir
            if self.grab==True:         # 잡힌 물체 있었으면 다시없에주기
                self.grab=False
                self.score+=self.grab_object.price
                object_group.remove(self.grab_object)
                del self.grab_object
                self.grab_object=None
                self.grab_distance=None
        if self.grab==True:
            self.grab_object.set_position(self.rect.center[0]-self.grab_distance[0],self.rect.center[1]-self.grab_distance[1])
        self.rotate()



        rect_center=self.position+self.offset
        # self.rect=self.image.get_rect(center=rect_center)

    # 집게 회전 함수
    def rotate(self):
        self.image=pygame.transform.rotozoom(self.original_image, -self.angle,1)
        offset_rotated=self.offset.rotate(self.angle)   # 벡터 rotate
        # 이미지 RECT 가 기존 RECT(LEFT,TOP)을 유지하고 있어서
        # new image의 center를 기존center랑 맞춰준다
        self.rect=self.image.get_rect(center=self.position+offset_rotated)
    
    def stop(self):
        if self.direction!=STOP:
            self.tmp_dir=self.direction
            self.direction=STOP
            


    def draw(self, screen):
        screen.blit(self.image, self.rect)
        pygame.draw.circle(screen,RED,self.position,3)
        pygame.draw.line(screen,BLACK, self.position, self.rect.center, 2)
        # new image의 center까지 선 그음
    




