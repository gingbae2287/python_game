import pygame
import time
from 똥피하기 import enemy
import random
import os
dir=os.getcwd()
os.chdir(dir+"/똥피하기")

pygame.init()  # pygame 초기화 (필수)

# 화면 크기 설정
screen_width=480  # 가로
screen_height=640 # 세로
screen=pygame.display.set_mode((screen_width,screen_height))

# 화면 타이틀 설정
pygame.display.set_caption("YB game") # 게임이름

# FPS
clock=pygame.time.Clock()

# 배경이미지 불러오기
# C:\Users\kingb\Desktop\coding\game\background.png
background=pygame.image.load("background.png")

# 캐릭터(스프라이트) 불러오기
character=pygame.image.load("character.png")
# character_size=character.get_rect().size # 이미지 크기(가로,세로) 구해옴
# character_width=character_size[0]
# character_height=character_size[1]
character_width,character_height=character.get_rect().size
character_x_pos=screen_width/2-character_width/2  #화면 가로 절반 위치-캐릭터가로 절반
character_y_pos=screen_height-character_height   # 화면 세로 가장 아래

# 캐릭터 움직일때
to_x=0
to_y=0
move_x=0.3
move_y=0.3

# 적
# enemy=pygame.image.load("enemy.png")
# enemy_width,enemy_height=enemy.get_rect().size
# enemy_x_pos=screen_width/2-enemy_width/2  #화면 가로 절반 위치-캐릭터가로 절반
# enemy_y_pos=screen_height/2-enemy_height   # 화면 세로 중간

# 적 여러개
enemy_list=[]

# 텍스트입력
game_font=pygame.font.Font(None, 20) # 폰트 객체 생성
total_time=0
start_ticks=pygame.time.get_ticks() # 시작 tick을 받아옴

# 피한 적 개수=점수
score=0

# 이벤트 루프 (실행중)
# event.get() 창 실행중 어떤 입력이나 동작들을 체크
running=True    # 실행중인가
while running:
    dt=clock.tick(30)   # 초당 프레임수
    elapsed_time=int((pygame.time.get_ticks()-start_ticks)/1000)  # 경과시간
    
    # 2초마다 적을 하나씩 생성
    if random.random()>1-0.0025*dt:
        enemy_list.append(enemy.Enemy(random.randrange(0,screen_width)))

    #print(str(clock.get_fps()))
    for event in pygame.event.get():
        if event.type==pygame.QUIT:   # 창을 닫는 x버튼시 발생 
            running=False
        
        if event.type==pygame.KEYDOWN:  # 키가 눌렸을때
            if event.key==pygame.K_LEFT:
                    to_x-=move_x
            elif event.key==pygame.K_RIGHT:
                to_x+=move_x
            elif event.key==pygame.K_UP:
                to_y-=move_y
            elif event.key==pygame.K_DOWN:
                to_y+=move_y

        if event.type==pygame.KEYUP:
            if event.key==pygame.K_LEFT:
                to_x+=move_x
            elif event.key==pygame.K_RIGHT:
                to_x-=move_x
            elif event.key==pygame.K_UP:
                to_y+=move_y
            elif event.key==pygame.K_DOWN:
                to_y-=move_y

    character_x_pos+=to_x*dt
    character_y_pos+=to_y*dt
    if character_x_pos<0:
        character_x_pos=0
    elif character_x_pos>screen_width-character_width:
        character_x_pos=screen_width-character_width
    if 0>character_y_pos:
        character_y_pos=0
    elif character_y_pos>screen_height-character_height:
        character_y_pos=screen_height-character_height



    #충돌처리
    character_rect=character.get_rect()
    character_rect.left=character_x_pos
    character_rect.top=character_y_pos

    # enemy_rect=enemy.get_rect()
    # enemy_rect.left=enemy_x_pos
    # enemy_rect.top=enemy_y_pos  

    # if character_rect.colliderect(enemy_rect):
    #     print("충돌")
    #     running=False

    # 배경( 배경을 젤 위에 blit 해야 다른거 안가림)
    # screen.fill((0,0,255))  # 배경 색상으로 채워넣기
    screen.blit(background,(0,0)) # 배경이미지 직접 넣기
    
    # 캐릭터
    screen.blit(character,(character_x_pos,character_y_pos))
    # screen.blit(enemy,(enemy_x_pos,enemy_y_pos))

    for i in range(len(enemy_list)):
        try:
            if character_rect.colliderect(enemy_list[i].enemy_rect):
                print("충돌")
                running=False
            if enemy_list[i].enemy_y_pos>640:
                del enemy_list[i]
                score+=1
                i=i-1
                continue
            else:
                enemy_list[i].move(dt)
                screen.blit(enemy_list[i].enemy,(enemy_list[i].enemy_x_pos,enemy_list[i].enemy_y_pos))
        except:
            pass


    # 시간 출력 초 단위로 표시
    timer=game_font.render("time: %4s"%int(elapsed_time),True, (255,0,0))
    screen.blit(timer, (screen_width-100,20))

    # 점수 출력
    score_print=game_font.render("score: %4s"%score,True,(255,0,0))
    screen.blit(score_print, (50,20))
    pygame.display.update() # 화면 업데이트(무한 호출필요)
    #time.sleep(0.001)

print(int(score))
pygame.time.delay(2000)

# 게임종료
pygame.quit()