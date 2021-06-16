# 공 터뜨리는게임

import pygame
import os
import ball
import setting
dir=os.getcwd()
os.chdir(dir+"/풍선pang")


pygame.init()

# 화면 크기 설정
screen_width=setting.screen_width
screen_height=setting.screen_height
screen=pygame.display.set_mode((screen_width,screen_height))

# 화면 타이틀 설정
pygame.display.set_caption("pang")

# FPS 섷정
clock=pygame.time.Clock()
fps=setting.fps

#시간 출력
game_font=pygame.font.Font(None, 20) # 폰트 객체 생성
total_time=0
start_ticks=pygame.time.get_ticks() # 시작 tick을 받아옴

background=pygame.image.load("image/background.png")

# 캐릭터 설정
character=pygame.image.load("image/character.png")
character_width,character_height=character.get_rect().size
character_x_pos=screen_width/2-character_width/2  #화면 가로 절반 위치-캐릭터가로 절반
character_y_pos=screen_height-character_height   # 화면 세로 가장 아래
cha_move_x=0
cha_vel=setting.character_velocity       # 캐릭터 이동 속도
character_rect=character.get_rect()


pang_g=setting.gravity  # 중력가속도


pang_list=[]
pang_list.append(ball.ball(0,0,1,1)) # 초기 공 생성


# 무기
weapon=pygame.image.load("image/weapon.png")
weapon_width,weapon_height=weapon.get_rect().size
weapon_rect=weapon.get_rect()
weapon_x_pos=-5
weapon_y_pos=screen_height+10
weapon_rect.left=weapon_x_pos   # 무기 충돌 좌표
weapon_rect.top=weapon_y_pos
weapon_speed=setting.weapon_speed
weapon_visible=False


running=True
while running:
    # 초당프레임
    dt=clock.tick(fps)

    # 이벤트 동작
    for event in pygame.event.get():
        if event.type==pygame.QUIT:
            running=False
            break

        # 방향키 입력
        if event.type==pygame.KEYDOWN:
            if event.key==pygame.K_LEFT:
                cha_move_x-=cha_vel
            elif event.key==pygame.K_RIGHT:
                cha_move_x+=cha_vel
            elif event.key==pygame.K_SPACE: # 무기 발사
                pass
        
        if event.type==pygame.KEYUP:
            if event.key==pygame.K_LEFT:
                cha_move_x+=cha_vel
            elif event.key==pygame.K_RIGHT:
                cha_move_x-=cha_vel
            elif event.key==pygame.K_SPACE:
                if weapon_visible==False:
                    weapon_visible=True
                    weapon_x_pos=character_x_pos+character_width/2-weapon_width/2
                    weapon_y_pos=character_y_pos-character_height/2

    screen.blit(background,(0,0))  # 배경( 맨처음)
    # 캐릭터 움직임
    character_x_pos+=cha_move_x*dt
    if character_x_pos<0:
        character_x_pos=0
    elif character_x_pos>screen_width-character_width:
        character_x_pos=screen_width-character_width
    # 캐릭터 충돌처리
    character_rect.left=character_x_pos
    character_rect.top=character_y_pos

    # 무기 동작
    if weapon_visible:
        screen.blit(weapon,(weapon_x_pos,weapon_y_pos))
        weapon_y_pos-=weapon_speed*dt
        weapon_rect.left=weapon_x_pos   # 무기 충돌 좌표
        weapon_rect.top=weapon_y_pos
        if weapon_y_pos<0:
            weapon_visible=False
    else:
        weapon_rect.left=-5   # 무기 충돌 좌표 숨기기
        weapon_rect.top=screen_height+10

    # 캐릭터 표시
    screen.blit(character,(character_x_pos, character_y_pos))


    # 공 동작
    if not pang_list:
        print("Clear")
        running=False
        break
    for i in range(len(pang_list)):
        # 캐릭터와 충돌
        if character_rect.colliderect(pang_list[i].ball_rect):
            print("Game Over")
            running=False
            break
        elif weapon_rect.colliderect(pang_list[i].ball_rect):
            weapon_visible=False
            if pang_list[i].size==4:
                del pang_list[i]
                break
                # if i<len(pang_list):
                #     i-=1
            else:
                pang_list.append(ball.ball(pang_list[i].x_pos, pang_list[i].y_pos,pang_list[i].size+1,-1))
                pang_list.append(ball.ball(pang_list[i].x_pos, pang_list[i].y_pos,pang_list[i].size+1,1))
                del pang_list[i]
                i-=1
        else:
            pang_list[i].move(dt)
            screen.blit(pang_list[i].ball, (pang_list[i].x_pos,pang_list[i].y_pos))
        # 무기와 충돌

    elapsed_time=100-int((pygame.time.get_ticks()-start_ticks)/1000)  # 경과시간
    timer=game_font.render("time: %4s"%int(elapsed_time),True, (255,0,0))
    screen.blit(timer, (20,20))
    if elapsed_time==0:
        running=False
        print("Time Over")


    #screen.blit(pang[0], (pang_x_pos,pang_y_pos))




    pygame.display.update()

    


            



pygame.time.delay(1000)
pygame.quit()