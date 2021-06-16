#  보석(황금,다이아) 및 돌 생성
# 크기 랜덤, 크기별 가치
#  갈고리 회전
# 스페이스=>갈고리 발사
# 갈고리 충돌
# 보석 종류에 따른 갈고리 속도



import pygame
import os
import setting
import random
from object import *

# 화면설정
pygame.init()
screen_width=setting.screen_width
screen_height=setting.screen_height

# screen=pygame.display.set_mode((screen_width, screen_height))
# pygame.display.set_caption("Glod Miner")
fps=setting.fps
clock=pygame.time.Clock()

start_time= pygame.time.get_ticks() # 시작시간 tick
game_font=pygame.font.Font(None, 30)    #폰트객체

# 배경, 게임 이미지
current_path=os.path.dirname(__file__)
background=pygame.image.load(os.path.join(current_path, "images/background.png"))

# 게임 구동
running=True
tmp_time=game_play_time
# 집게 오브젝트 생성

claw=Claw(object_claw, (screen_width/2, 50))
# 처음에 오브젝트 3개 생성
object_group.add(object(random.randrange(1,101)))
object_group.add(object(random.randrange(1,101)))
object_group.add(object(random.randrange(1,101)))

while running:
    dt=clock.tick(fps)
# 이벤트발생
    for event in pygame.event.get():
        if event.type==pygame.QUIT:
            running=False
        
        if event.type==pygame.MOUSEBUTTONDOWN:
            claw.stop()
    screen.blit(background,(0,0))   # 배경
    # 시간,점수 표시
    score=claw.score
    time=game_play_time-int((pygame.time.get_ticks()-start_time)/1000)
    timer=game_font.render("time left: %4s"%time, True, (255,0,0))
    score_board=game_font.render("score: %4s"%score,True,(0,0,0))
    screen.blit(score_board, (50, 30))
    screen.blit(timer, (screen_width-150, 30))
    # 오브젝트 다루기
    if tmp_time-time==1:
        tmp_time=time
        # object_group=그룹 리스트
        if random.random()>len(object_group)/max_object_count:
            object_group.add(object(random.randrange(1,101)))
    object_group.draw(screen)
    claw.update(dt)
    claw.draw(screen)

    pygame.display.update()
    if time==0:
        running=False


print("최종 점수 :",score)
pygame.time.wait(2000)
pygame.quit()



