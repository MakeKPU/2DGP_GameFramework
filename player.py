from pico2d import *
from static import *

import stage_scene
import mainframe
from bullet import Bullet
from effect import Effect
from ui import *
import game_world
from monster import *

# Action Speed
TIME_PER_ACTION = 0.4
ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
FRAMES_PER_ACTION = 7

# Move Speed
# 추후 변경 가능하도록 해야함

class Player:
    image = None
    data = None
    sound = None
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
        self.pushBombcheck = False
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
        self.bullet_term = 10
        self.bullet_type = 'spread'
        self.BombTime = 0
        self.BombDelay = 5
        self.TickTime = 0
        self.TickDelay = 0.2
        # speed
        self.moveSpeed = 30
        # image
        if Player.image == None:
            Player.image = load_image(os.path.join(os.getcwd(), 'resources', 'player', 'player.png'))
        # data
        if Player.data == None:
            self.initializeData()
        # player abilities
        self.hp = 150
        self.score = 0
        self.money = 0
        self.attackDamage = 10
        self.bomb = None
        self.bombCount = 3
        self.bombDamage = 5
        self.parsingID = '1'

        # modify
        self.hpBar = None
        self.scoreBar = None
        self.moneyBar = None
        self.bombBar = None
        self.stage_number = None
        self.initPlayerUI()
        self.parsingAttData(self.parsingID)
        self.Modify_Abilities()

        # sound
        if Player.sound == None:
            self.iniializeSound()
        self.bomb_sound = load_wav(os.path.join(os.getcwd(), 'resources', 'sound', 'player', 'bomb.wav'))
        self.bomb_sound.set_volume(110)


    def initPlayerUI(self):
        uiHpCheck = 0
        uiScoreCheck = 0
        uiMoneyCheck = 0
        uiBombCheck = 0
        uiLayer = game_world.get_layer(UIINGAME)

        uiStage = 0

        for ui in uiLayer:
            if ui.uiID == 'hpbar':
                self.hpBar = ui
                uiHpCheck = 1
            elif ui.uiID == 'score':
                self.scoreBar = ui
                uiScoreCheck = 1
            elif ui.uiID == 'money':
                self.moneyBar = ui
                uiMoneyCheck = 1
            elif ui.uiID == 'bomb':
                self.bombBar = ui
                uiBombCheck = 1
            elif ui.uiID == 'numbers':
                self.stage_number = ui
                uiStage = 1


        if uiHpCheck == 0:
            self.hpBar = HPBar(470, 30, self.hp)
            game_world.add_object(self.hpBar, UIINGAME)

        if uiBombCheck == 0:
            self.bombBar = BombBar(470, 80, self.bombCount)
            game_world.add_object(self.bombBar, UIINGAME)

        if uiScoreCheck == 0:
            self.scoreBar = Score(120, 680, self.score)
            game_world.add_object(self.scoreBar, UIINGAME)

        if uiMoneyCheck == 0:
            self.moneyBar = Money(480, 680, 1, 120, 2, 17, self.money)
            game_world.add_object(self.moneyBar, UIINGAME)

        if uiStage == 0:
            self.stage_number = Numbers(120, 650, 2, 2, 17, stage_scene.stage)
            game_world.add_object(self.stage_number, UIINGAME)


    def initializeData(self):
        Player.data = {
            # bullet
            # 불렛 갯수 사이각 각도, 속도, 이미지 타입, 불릿 타입, 사이즈, 데미지, 딜레이,
            #  self.BulletDelay = 0.15
            '1': [3, 130, 'SmallCircle', 'RotateOnce', 2, 2, 1, 0.09, 8, 'spread'],
            '2': [3, 120, 'SmallMiss', 'RotateOnce', 2.7, 2.7, 2, 0.11, 20, 'forward'],
            '3': [3, 150, 'Rug', 'Rotate', 2, 2, 3, 0.1, 10, 'spread'],
            '4': [3, 120, 'GreenWeak', 'RotateOnce', 2, 2, 4, 0.09, 8, 'spread'],
            '5': [3, 120, 'PurpleWeak', 'RotateOnce', 2.5, 2.5, 4, 0.08, 20, 'forward'],
            '6': [5, 110, 'GreenNormal', 'RotateOnce', 2, 2, 5, 0.10, 10, 'spread'],
            '7': [5, 110, 'PurpleNormal', 'RotateOnce', 1.75, 1.75, 5, 0.07, 20, 'forward'],
            '8': [3, 130, 'GreenStrong', 'RotateOnce', 2, 2, 6, 0.06, 6, 'spread'],
            '9': [3, 130, 'PurpleStrong', 'RotateOnce', 1.75, 1.75, 6, 0.045, 25, 'forward'],
            '10': [1, 210, 'PurpleMax', 'RotateOnce', 3, 3, 18, 0.04, 10, 'spread'],
            '11': [3, 90, 'ExplodeMiss', 'Anim', 4, 4, 8, 0.1, 25, 'forward'],
            '12': [5, 170, 'BlueCircle', '', 1.25, 1.25, 6, 0.09, 10, 'spread'],
            '13': [1, 270, 'Eagle', 'RotateOnce', 3, 3, 35, 0.035, 10, 'spread']
        }
    def iniializeSound(self):
        lazer = load_wav(os.path.join(os.getcwd(), 'resources', 'sound', 'player', 'lazer.wav'))
        lazer.set_volume(10)
        lazer2 = load_wav(os.path.join(os.getcwd(), 'resources', 'sound', 'player', 'lazer2.wav'))
        lazer2.set_volume(15)
        lazer3 = load_wav(os.path.join(os.getcwd(), 'resources', 'sound', 'player', 'lazer3.wav'))
        lazer3.set_volume(25)
        lazer4 = load_wav(os.path.join(os.getcwd(), 'resources', 'sound', 'player', 'lazer4.wav'))
        lazer4.set_volume(25)
        shoot = load_wav(os.path.join(os.getcwd(), 'resources', 'sound', 'player', 'shoot.wav'))
        shoot.set_volume(5)
        shoot2 = load_wav(os.path.join(os.getcwd(), 'resources', 'sound', 'player', 'shoot2.wav'))
        shoot2.set_volume(20)
        hit = load_wav(os.path.join(os.getcwd(), 'resources', 'sound', 'player', 'hit.WAV'))
        hit.set_volume(20)
        Player.sound = {
            # bullet
            '1': shoot2,
            '2': shoot,
            '3': shoot,
            '4': lazer,
            '5': lazer2,
            '6': lazer3,
            '7': lazer4,
            '8': lazer,
            '9': lazer2,
            '10': lazer3,
            '11': lazer4,
            '12': lazer3,
            '13': lazer2,

            # hit
            'hit' : hit
        }

    def get_rect(self):
        return self.x - 5, self.y - 10, self.x + 5, self.y + 10

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
        elif key_state == SDLK_a:
            # 필살기
            if self.pushBombcheck == False:
                game_world.add_object(Bullet(100, 150, 90, 60, 'Thunder', 0, 'Anim_Stop', 6, 6, self.attackDamage * 2), BULLET_PLAYER)
                game_world.add_object(Bullet(250, 150, 90, 60, 'Thunder', 0, 'Anim_Stop', 6, 6, self.attackDamage * 2), BULLET_PLAYER)
                game_world.add_object(Bullet(400, 150, 90, 60, 'Thunder', 0, 'Anim_Stop', 6, 6, self.attackDamage * 2), BULLET_PLAYER)
                self.bomb_sound.play()
                self.bombCount -= 1
                self.bombBar.setBombImage(self.bombCount)
                self.pushBombcheck = True

    # Att UpKey
    def Attack_State_UpKey(self, key_state):
        if key_state == SDLK_s:
            self.pushAttcheck = False

    def parsingAttData(self, parsingID):
        # 불렛 갯수 /사이각 각도/, 속도, 이미지 타입, 불릿 타입, 사이즈
        if int(parsingID) >= 13 and self.parsingID == parsingID:
            self.attackDamage += 20
            return True

        self.parsingID = parsingID
        self.bulletCount = Player.data.get(parsingID)[0]
        self.bulletSpeed = Player.data.get(parsingID)[1]
        self.bulletImage = Player.data.get(parsingID)[2]
        self.bulletType = Player.data.get(parsingID)[3]
        self.bulletSizeX = Player.data.get(parsingID)[4]
        self.bulletSizeY = Player.data.get(parsingID)[5]
        self.attackDamage = Player.data.get(parsingID)[6]
        self.BulletDelay = Player.data.get(parsingID)[7]
        self.bullet_term = Player.data.get(parsingID)[8]
        self.bullet_type = Player.data.get(parsingID)[9]
        return True

    def parsingHPBar(self, healAmount):
        if (self.hp + healAmount) >= 500:
            self.hp = 500
            self.hpBar.setHPImage(self.hp)
            return False

        self.hp += healAmount
        self.hpBar.setHPImage(self.hp)

        return True

    def parsingBombBar(self, bombAmount):
        if self.bombCount + bombAmount > 10:
            return False

        self.bombCount += bombAmount
        self.bombBar.setBombImage(self.bombCount)

        return True

    def parsingScoreBar(self, scoreAmount):
         if self.score + scoreAmount > 9999999:
             self.score = 9999999
         else:
            self.score += scoreAmount
         self.scoreBar.setScore(self.score)

    def parsingMoneyBar(self, moneyAmount):
        if (self.money + moneyAmount) < 0:
            return False

        if self.money + moneyAmount > 9999999:
            self.money = 9999999
        else:
            self.money += moneyAmount
        self.moneyBar.setMoney(self.money)

        return True

    def Modify_Abilities(self):
        # speed
        self.moveSpeedMeterPerMinute = (self.moveSpeed * 1000.0 / 60.0)
        self.moveSpeedMterPerSecond = (self.moveSpeedMeterPerMinute / 60.0)
        self.moveSpeedPixelPerSecond = (self.moveSpeedMterPerSecond * PIXEL_PER_METER)

    def collideActive(self, opponent):
        if self.hp - opponent.attackDamage <= 0:
            self.hp = 0
        else:
            self.hp -= opponent.attackDamage
            self.hpBar.setHPImage(self.hp)
            if opponent.attackDamage > 0:
                game_world.add_object(
                    Effect(self.x + 30, self.y + 20, '', 'HitEffect03', 2.75, 2.75),
                    EFFECT)
                Player.sound.get('hit').play()

    def update(self):
        # player_time
        self.BulletTime += mainframe.frame_time

        # dead
        if (self.hp <= 0):
            game_world.add_object(Effect(self.x, self.y, 'random_effect', '', 70 * 3, 70 * 3),
                                  EFFECT)
            stage_scene.score = self.score
            stage_scene.money = self.money
            return True

        # animation
        self.animation_update()

        # attack
        self.attack_normal()
        self.attack_bomb()

        # 이동 계산
        self.y += self.velocityY * mainframe.frame_time
        self.x += self.velocityX * mainframe.frame_time

        # 벽을 못나가도록
        self.block_player()

        return False

    def animation_update(self):
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

    def attack_normal(self):
        # 공격
        if self.pushAttcheck == True:
            if self.BulletTime > self.BulletDelay:
                Player.sound.get(self.parsingID).play()

                if self.bullet_type == 'spread':
                    angleTerm = 0
                    angle = 90
                    for cnt in range(0, self.bulletCount):
                        bullet = Bullet(self.x + 5, self.y + 20, angle + angleTerm, self.bulletSpeed, self.bulletImage, 0,
                                        self.bulletType
                                        , self.bulletSizeX, self.bulletSizeY, self.attackDamage)
                        bullet.set_rotation(angle)
                        game_world.add_object(bullet, BULLET_PLAYER)

                        if angleTerm == 0:
                            angleTerm += self.bullet_term
                        elif angleTerm > 0:
                            angleTerm *= -1
                        elif angleTerm < 0:
                            angleTerm *= -1
                            angleTerm += self.bullet_term
                elif self.bullet_type == 'forward':
                    posterm = self.bullet_term
                    pos = -((self.bulletCount // 2) * self.bullet_term)
                    for cnt in range(0, self.bulletCount):
                        bullet = Bullet(self.x + pos, self.y + 20, 90, self.bulletSpeed, self.bulletImage,
                                        0,
                                        self.bulletType
                                        , self.bulletSizeX, self.bulletSizeY, self.attackDamage)
                        game_world.add_object(bullet, BULLET_PLAYER)
                        pos += posterm

                self.BulletTime = 0

    def attack_bomb(self):
        # 폭탄
        if self.pushBombcheck == True:
            self.BombTime += mainframe.frame_time
            self.TickTime += mainframe.frame_time
            # 지속 시간동안
            # 모든 몬스터 보스 총알을 무효화시키며
            # 지속적인 피해를 입힘
            game_world.clear_layer(BULLET)
            game_world.clear_layer(BOSS_BULLET)

            if self.TickTime > self.TickDelay:
                monsterLayer = game_world.get_layer(MONSTER)
                for monster in monsterLayer:
                    if monster.posY <= 700:
                        monster.hp -= self.bombDamage * (1 + Monster_Pattern.difficulty)
                bossLayer = game_world.get_layer(BOSS)
                for boss in bossLayer:
                    if boss.posY <= 700:
                        boss.hp -= self.bombDamage * (1 + Monster_Pattern.difficulty)
                self.TickTime = 0

            if self.BombTime > self.BombDelay:
                self.BombTime = 0
                self.TickTime = 0
                self.pushBombcheck = False

    def draw(self):
        Player.image.clip_draw(int(self.frame) * 70, self.frameID * 70, 70, 70, self.x, self.y)

        # DEBUG
        # print(str(self.pushLcheck) + " " + str(self.pushRcheck))
        # print(len(stage_scene.bullets))
        # print(self.frame)
        # print

    def draw_rect(self):
        draw_rectangle(*self.get_rect())

    def block_player(self):
       left, bottom, right, top = self.get_rect()

       if left < 0:
           self.x -= self.velocityX * mainframe.frame_time

       if right > 500:
           self.x -= self.velocityX * mainframe.frame_time

       if top > 700:
           self.y -= self.velocityY * mainframe.frame_time

       if bottom < 0:
           self.y -= self.velocityY * mainframe.frame_time
