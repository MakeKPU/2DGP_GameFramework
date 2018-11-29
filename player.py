from pico2d import *
from static import *

import stage_scene
import mainframe
from bullet import Bullet
import game_world

# Action Speed
TIME_PER_ACTION = 0.4
ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
FRAMES_PER_ACTION = 7

# Move Speed
# 추후 변경 가능하도록 해야함

class Player:
    image = None
    data = None
    def __init__(self):
        # position
        self.x = 250
        self.y = 50
        self.dirX = 0
        self.dirY = 0
        self.velocityX = 0
        self.velocityY = 0
        # status
        self.deadcheck = False
        self.turncheck = False
        # key
        self.pushLcheck = False
        self.pushRcheck = False
        self.pushAttcheck = False
        # collider
        self.collideCheck = False
        # frame
        self.frameID = 0
        self.frame = 0
        self.reformframe = 0
        # bullet
        #self.bullet = []
        # time
        self.BulletTime = 0
        self.BulletDelay = 0.15
        # speed
        self.moveSpeed = 20
        # image
        if Player.image == None:
            Player.image = load_image(os.path.join(os.getcwd(), 'resources', 'player', 'player.png'))
        if Player.data == None:
            self.initializeData()
        # player abilities
        self.hp = 100
        self.bomb = 3
        self.parsingID = '1'

        # modify
        self.parsingDataSet(self.parsingID)
        self.Modify_Abilities()

    def initializeData(self):
        Player.data = {
            'posion': [],
            'megica': [],
            # bullet
            # 불렛 갯수 사이각 각도, 속도, 이미지 타입, 불릿 타입, 사이즈
            # 나중에 데미지도 (맨 뒤에)
            '1': [1, 70, 'SmallCircle', 'RotateOnce', 4, 4, 1],
            '2': [3, 90, 'SmallMiss', 'RotateOnce', 2.7, 2.7, 1],
            '3': [3, 130, 'Rug', 'RotateOnce', 2, 2, 2],
            '4': [3, 70, 'GreenWeak', 'RotateOnce', 2, 2, 3],
            '5': [3, 70, 'PurpleWeak', 'RotateOnce', 2.5, 2.5, 3],
            '6': [5, 80, 'GreenNormal', 'RotateOnce', 2, 2, 4],
            '7': [5, 80, 'PurpleNormal', 'RotateOnce', 1.75, 1.75, 4],
            '8': [3, 100, 'GreenStrong', 'RotateOnce', 2, 2, 5],
            '9': [3, 100, 'PurpleStrong', 'RotateOnce', 1.75, 1.75, 5],
            '10': [1, 150, 'PurpleMax', 'RotateOnce', 3, 3, 6],
            '11': [3, 90, 'ExplodeMiss', 'Anim', 4, 4, 8],
            '12': [5, 100, 'BlueCircle', '', 1.25, 1.25, 6],
            '13': [1, 175, 'Eagle', 'RotateOnce', 3, 3, 15]
        }

    def get_rect(self):
        return self.x - 10, self.y - 20, self.x + 10, self.y + 20

    def handle_events(self, event):
        # 이동 구현
        # 키를 눌렀다면?
        if event.type == SDL_KEYDOWN:
            self.Move_State_DownKey(event.key)
            self.Attack_State_DownKey(event.key)
        # 키를 떼었다면?
        elif event.type == SDL_KEYUP:
            self.Move_State_UpKey(event.key)
            self.Attack_State_UpKey(event.key)

        # 동시에 눌렸을때는 그자리에 있는 스프라이트를 재생한다.
        if(self.pushLcheck == True) and (self.pushRcheck == True):
            self.turncheck = False

    # Key Input process
    # Move DownKey
    def Move_State_DownKey(self, key_state):
        if key_state == SDLK_UP:
            self.velocityY += self.moveSpeedPixelPerSecond
        elif key_state == SDLK_DOWN:
            self.velocityY -= self.moveSpeedPixelPerSecond
        # 좌
        elif key_state == SDLK_LEFT:
            # pushRcheck가 켜져있다는 뜻은 동시에 눌리고 있다는 뜻이므로
            # 누른 키의 반대쪽 키가 눌리지 않았을때 키에 알맞는 스프라이트를 재생한다.
            if self.pushRcheck == False:
                self.turncheck = False
                self.frameID = 1
                self.frame = 0
                self.reformframe = 6
                self.turncheck = True
            #
            self.velocityX -= self.moveSpeedPixelPerSecond
            self.pushLcheck = True
        # 우
        elif key_state == SDLK_RIGHT:
            # pushLcheck가 켜져있다는 뜻은 동시에 눌리고 있다는 뜻이므로
            # 누른 키의 반대쪽 키가 눌리지 않았을때 키에 알맞는 스프라이트를 재생한다.
            if self.pushLcheck == False:
                self.turncheck = False
                self.frameID = 2
                self.frame = 0
                self.reformframe = 6
                self.turncheck = True
            #
            self.velocityX += self.moveSpeedPixelPerSecond
            self.pushRcheck = True

        self.dirX = clamp(-1, self.velocityX, 1)
    # Move UpKey
    def Move_State_UpKey(self, key_state):
        if key_state == SDLK_UP:
            self.velocityY -= self.moveSpeedPixelPerSecond
        elif key_state == SDLK_DOWN:
            self.velocityY += self.moveSpeedPixelPerSecond
        # 좌
        elif key_state == SDLK_LEFT:
            # pushRcheck가 켜져있다는 뜻은 키를 뗌과 동시에 반대키가 눌리고 있다는 뜻이므로
            # 뗀 키의 반대쪽 키가 눌리고 있을때 키에 알맞는 스프라이트를 재생한다.
            if self.pushRcheck == True:
                self.turncheck = True
                self.frameID = 2
                self.frame = 0
                self.reformframe = 6
                self.turncheck = True
            else:
                self.turncheck = False
            #
            self.velocityX += self.moveSpeedPixelPerSecond
            self.dirX += 1
            self.pushLcheck = False
        # 우
        elif key_state == SDLK_RIGHT:
            # pushLcheck가 켜져있다는 뜻은 키를 뗌과 동시에 반대키가 눌리고 있다는 뜻이므로
            # 뗀 키의 반대쪽 키가 눌리고 있을때 키에 알맞는 스프라이트를 재생한다.
            if self.pushLcheck == True:
                self.turncheck = True
                self.frameID = 1
                self.frame = 0
                self.reformframe = 6
                self.turncheck = True
            else:
                self.turncheck = False
            #
            self.velocityX -= self.moveSpeedPixelPerSecond
            self.dirX -= 1
            self.pushRcheck = False
    # Att DownKey
    def Attack_State_DownKey(self, key_state):
        if key_state == SDLK_s:
            self.pushAttcheck = True
    # Att UpKey
    def Attack_State_UpKey(self, key_state):
        if key_state == SDLK_s:
            self.pushAttcheck = False

    def parsingDataSet(self, parsingID):
        # 불렛 갯수 /사이각 각도/, 속도, 이미지 타입, 불릿 타입, 사이즈
        self.parsingID = parsingID
        self.bulletCount = Player.data.get(parsingID)[0]
        self.bulletSpeed = Player.data.get(parsingID)[1]
        self.bulletImage = Player.data.get(parsingID)[2]
        self.bulletType = Player.data.get(parsingID)[3]
        self.bulletSizeX = Player.data.get(parsingID)[4]
        self.bulletSizeY = Player.data.get(parsingID)[5]
        self.attackDamage = Player.data.get(parsingID)[6]

    def Modify_Abilities(self):
        # speed
        self.moveSpeedMeterPerMinute = (self.moveSpeed * 1000.0 / 60.0)
        self.moveSpeedMterPerSecond = (self.moveSpeedMeterPerMinute / 60.0)
        self.moveSpeedPixelPerSecond = (self.moveSpeedMterPerSecond * PIXEL_PER_METER)

    def collideActive(self, opponent):
        self.hp -= opponent.attackDamage

    def update(self):
        #player_time
        self.BulletTime += mainframe.frame_time

        TimeToFrameQuantity = FRAMES_PER_ACTION * ACTION_PER_TIME * mainframe.frame_time

        if self.turncheck == True:
            # 회전 이동 상태일때
            # 회전 스프라이트 끝 장면에 프레임을 고정
            if self.frame < 6:
               # self.frame = (self.frame + 1) % 7
               self.frame = (self.frame + TimeToFrameQuantity) % 7
        else:
            # 만약 회전 이동 상태가 아니라면 IDLE 상태로 돌아오는
            # 스프라이트를 재생한다.(프레임을 거꾸로 돌린다)
            if self.reformframe < 0:
                self.frameID = 0
                # self.frame = (self.frame + 1) % 7
                self.frame = (self.frame + TimeToFrameQuantity) % 7
            else:
                self.reformframe = self.reformframe - TimeToFrameQuantity
                self.frame = self.reformframe

        # 이동 계산
        self.y += self.velocityY * mainframe.frame_time
        self.x += self.velocityX * mainframe.frame_time

        # 화면 내 이동
        # boy.x = clamp(25, boy.x, 1600 - 25)


        # 공격(추후 상점 추가시 고칠 예정)
        if self.pushAttcheck == True :
            if self.BulletTime > self.BulletDelay:

                angleTerm = 0
                angle = 90
                for cnt in range(0, self.bulletCount):
                    bullet = Bullet(self.x + 5, self.y + 20, angle + angleTerm, self.bulletSpeed, self.bulletImage, 0, self.bulletType
                           , self.bulletSizeX, self.bulletSizeY, self.attackDamage)
                    bullet.set_rotation(angle)
                    game_world.add_object(bullet, BULLET_PLAYER)

                    if angleTerm == 0:
                        angleTerm += 10
                    elif angleTerm > 0:
                        angleTerm *= -1
                    elif angleTerm < 0:
                        angleTerm *= -1
                        angleTerm += 10


                self.BulletTime = 0

                # # 필살기
                # game_world.add_object(Bullet(100, 150, 90, 60, 'Thunder', 0, 'Anim_Stop', 6, 6, self.attackDamage * 2), BULLET_PLAYER)
                # game_world.add_object(Bullet(250, 150, 90, 60, 'Thunder', 0, 'Anim_Stop', 6, 6, self.attackDamage * 2), BULLET_PLAYER)
                # game_world.add_object(Bullet(400, 150, 90, 60, 'Thunder', 0, 'Anim_Stop', 6, 6, self.attackDamage * 2), BULLET_PLAYER)

        return False

    def draw(self):
        Player.image.clip_draw(int(self.frame) * 70, self.frameID * 70, 70, 70, self.x, self.y)

        # DEBUG
        # print(str(self.pushLcheck) + " " + str(self.pushRcheck))
        # print(len(stage_scene.bullets))
        # print(self.frame)
        # print

    def draw_rect(self):
        draw_rectangle(*self.get_rect())


