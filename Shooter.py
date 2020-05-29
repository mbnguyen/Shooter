#####################################################################
# SHOOTER by Minh Nguyen                                            #
#                                                                   #
# Project's name: Shooter                                           #
# Programmer: Minh Nguyen                                           #
# Last Modified: May 27, 2020                                       #
# Description: A shooting game written using Python and PyGame      #
# Please read the requirement.txt                                   #
# Please put all the files in /Data folder                          #
#                                                                   #
#####################################################################

import pygame as pg
import os
import random
import time
pg.init()

class Data:
    def __init__(self):
        self.path = os.getcwd() + "/Data/"
        self.backGround = pg.image.load(self.path + "bg.jpg")
        self.bgSize = self.backGround.get_rect().size

        self.music = pg.mixer.music.load(self.path + "music.wav")
        self.bulletSound = pg.mixer.Sound(self.path + "shoot.wav")
        self.hitSound = pg.mixer.Sound(self.path + "hit.wav")

        self.caption = "Shooter"
        self.frame = 27
        self.fps = 3
        self.font = pg.font.SysFont('comicsans', 32, True)
        self.fontBig = pg.font.SysFont('comicsans', 50, True)

        self.heart = pg.image.load(self.path + "heart.png")
        self.heartSize = self.heart.get_rect().size

        self.explosion = [pg.image.load(self.path + 'F0.png'), pg.image.load(self.path + 'F1.png'),
                          pg.image.load(self.path + 'F2.png'), pg.image.load(self.path + 'F3.png'),
                          pg.image.load(self.path + 'F4.png'), pg.image.load(self.path + 'F5.png'),
                          pg.image.load(self.path + 'F6.png'), pg.image.load(self.path + 'F7.png'),
                          pg.image.load(self.path + 'F8.png'), pg.image.load(self.path + 'F9.png'),
                          pg.image.load(self.path + 'F10.png'), pg.image.load(self.path + 'F11.png')]
        self.explosionSize = self.explosion[0].get_rect().size
        self.explosionFrame = len(self.explosion) * self.fps

        self.playerStanding = pg.image.load(self.path + "standing.png")
        self.playerWalkRight = [pg.image.load(self.path + 'R1.png'), pg.image.load(self.path + 'R2.png'),
                                pg.image.load(self.path + 'R3.png'), pg.image.load(self.path + 'R4.png'),
                                pg.image.load(self.path + 'R5.png'), pg.image.load(self.path + 'R6.png'),
                                pg.image.load(self.path + 'R7.png'), pg.image.load(self.path + 'R8.png'),
                                pg.image.load(self.path + 'R9.png')]
        self.playerWalkLeft = [pg.image.load(self.path + 'L1.png'), pg.image.load(self.path + 'L2.png'),
                               pg.image.load(self.path + 'L3.png'), pg.image.load(self.path + 'L4.png'),
                               pg.image.load(self.path + 'L5.png'), pg.image.load(self.path + 'L6.png'),
                               pg.image.load(self.path + 'L7.png'), pg.image.load(self.path + 'L8.png'),
                               pg.image.load(self.path + 'L9.png')]
        self.playerSize = self.playerStanding.get_rect().size
        self.playerFrame = len(self.playerWalkLeft) * self.fps
        self.playerX = self.bgSize[0] - (9 * (self.bgSize[0] // 10))
        self.playerY = self.bgSize[1] - (self.bgSize[1] // 10) - self.playerSize[1]
        self.playerVel = 7
        self.playerMaxBullet = 5
        self.playerJumpMax = 30
        self.playerShootMax = 10
        self.playerMaxHeart = 3

        self.bullet = {"vel" : 8,
                        "left" : pg.image.load(self.path + "bullet left.png"),
                        "right" : pg.image.load(self.path + "bullet right.png"),
                        "enemy left": pg.image.load(self.path + "bullet enemy left.png"),
                        "enemy right": pg.image.load(self.path + "bullet enemy right.png")}
        self.bullet["size"] = self.bullet.get("left").get_rect().size

        self.enemyWalkRight = [pg.image.load(self.path + 'R1E.png'), pg.image.load(self.path + 'R2E.png'),
                               pg.image.load(self.path + 'R3E.png'), pg.image.load(self.path + 'R4E.png'),
                               pg.image.load(self.path + 'R5E.png'), pg.image.load(self.path + 'R6E.png'),
                               pg.image.load(self.path + 'R7E.png'), pg.image.load(self.path + 'R8E.png'),
                               pg.image.load(self.path + 'R9E.png'), pg.image.load(self.path + 'R10E.png'),
                               pg.image.load(self.path + 'R11E.png')]
        self.enemyWalkLeft = [pg.image.load(self.path + 'L1E.png'), pg.image.load(self.path + 'L2E.png'),
                              pg.image.load(self.path + 'L3E.png'), pg.image.load(self.path + 'L4E.png'),
                              pg.image.load(self.path + 'L5E.png'), pg.image.load(self.path + 'L6E.png'),
                              pg.image.load(self.path + 'L7E.png'), pg.image.load(self.path + 'L8E.png'),
                              pg.image.load(self.path + 'L9E.png'), pg.image.load(self.path + 'L10E.png'),
                              pg.image.load(self.path + 'L11E.png')]
        self.enemyFrame = len(self.enemyWalkLeft) * self.fps
        self.enemySize = self.enemyWalkLeft[0].get_rect().size
        self.enemyY = self.bgSize[1] - (self.bgSize[1] // 10) - self.enemySize[1] + 8
        self.enemyVel = 1
        self.enemyMaxBullet = 2
        self.enemyMax = 2
        self.enemyDelay = 300
        self.enemyHealth = 5
        self.enemyDelayCreating = 200

        self.showTime = 20
        self.textAddHeart = self.fontBig.render("+1 Heart!", True, (255, 0, 0))
        self.textAddHeartPos = (self.heartSize[0], self.textAddHeart.get_rect().size[1] * 4)

        self.textAddBullet = self.fontBig.render("+1 Bullet", True, (255, 0, 0))
        self.textAddBulletPos = (self.bgSize[0] - self.textAddBullet.get_rect().size[0] - self.bullet.get("size")[0], self.textAddBullet.get_rect().size[1] * 4)

class Win:
    def __init__(self, data):
        infoObject = pg.display.Info()
        print(infoObject)
        w = int(infoObject.current_w)
        h = int(infoObject.current_h)
        data.bgSize = (min(w, data.bgSize[0]), min(h, data.bgSize[1]))
        self.display = pg.display.set_mode(data.bgSize)
        pg.display.set_caption(data.caption)
        self.textDied = data.fontBig.render('You died!!!', True, (255, 0, 0))
        self.textDiedPos = ((data.bgSize[0] // 2) - (self.textDied.get_rect().size[0] // 2), self.textDied.get_rect().size[1] * 3)

        self.textPlayAgain = data.fontBig.render("Hit 'Enter' to play again", True, (255, 0, 0))
        self.textPlayAgainPos = ((data.bgSize[0] // 2) - (self.textPlayAgain.get_rect().size[0] // 2), self.textPlayAgain.get_rect().size[1] * 5)

        self.clock = pg.time.Clock()
        self.clock.tick(data.frame)

        self.texts = []

    def delay(self, time):
        pg.display.update()
        for i in range(time):
            pg.time.delay(10)
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    i = time + 1
                    pg.quit()

    def drawHealthBar(self, data, position, health):
        size = round(data.enemySize[0] / data.enemyHealth)
        x = position[0]
        y = position[1] - 10
        pg.draw.rect(self.display, (0, 255, 0), (x, y, size * health, 10))
        if health < data.enemyHealth:
            pg.draw.rect(self.display, (255, 0, 0), (x + size * health, y, size * (data.enemyHealth - health), 10))

    def drawHeart(self, data, heart):
        x = 0
        y = data.heartSize[1]
        for i in range(heart):
            x += data.heartSize[0] * 2
            self.display.blit(data.heart, (x, y))

    def drawBullet(self, data, player):
        x = data.bgSize[0]
        y = data.bullet.get("size")[1]
        for i in range(data.playerMaxBullet - player.getNumberBullets()):
            x -= data.bullet.get("size")[0] * 2
            self.display.blit(data.bullet.get("right"), (x, y))

    def playAgain(self):
        self.display.blit(self.textPlayAgain, self.textPlayAgainPos)
        pg.display.update()

    def getHarder(self, data):
        data.enemyVel += 0.05
        data.enemyMaxBullet += 0.05
        data.enemyMax += 0.05
        data.enemyDelay -= 5
        data.enemyDelayCreating -= 5

    def boostPlayer(self, data, player):
        list = []
        if player.getScore() % 2 == 0:
            player.addHeart()
            list.append({"text" : data.textAddHeart, "position" : data.textAddHeartPos})
        if player.getScore() % 5 == 0:
            data.playerMaxBullet += 1
            list.append({"text" : data.textAddBullet, "position" : data.textAddBulletPos})
        return list


    def playing(self, data, player, enemies, startTime):
        self.clock.tick(data.frame)
        if player is None:
            return False

        self.display.blit(data.backGround, (0, 0))

        self.textScore = data.font.render("Score: " + str(player.getScore()), True, (0, 0, 0))
        self.display.blit(self.textScore, (data.bgSize[0] - self.textScore.get_rect().size[0] - 20, data.bgSize[1] - self.textScore.get_rect().size[1] * 2))

        self.textTime = data.font.render("Time: " + str(round(time.time() - startTime)), True, (0, 0, 0))
        self.textTimePos = ((data.bgSize[0] // 2) - (self.textTime.get_rect().size[0] // 2), self.textTime.get_rect().size[1])
        self.display.blit(self.textTime, self.textTimePos)

        self.display.blit(player.draw(data).get("image"), player.draw(data).get("position"))
        self.drawHeart(data, player.getHeart())
        self.drawBullet(data, player)

        for bullet in player.getBullets(data):
            if bullet.isVisible:
                self.display.blit(bullet.draw(data).get("image"), bullet.draw(data).get("position"))
                for enemy in enemies:
                    if bullet.hit(enemy) and not enemy.isDrawingExplosion():
                        if bullet in player.getBullets(data):
                            player.getBullets(data).remove(bullet)
                        enemy.gotHit()
                        if enemy.isDead():
                            player.addScore()
                            textShow = self.boostPlayer(data, player)
                            for text in textShow:
                                self.texts.append(Text(text.get("text"), text.get("position")))
                            enemies.remove(enemy)
                            self.getHarder(data)

        for enemy in enemies:
            position = enemy.getPosition()
            self.display.blit(enemy.draw(data).get("image"), enemy.draw(data).get("position"))
            if enemy.isDrawingExplosion():
                continue
            self.drawHealthBar(data, position, enemy.getHealth())
            for bullet in enemy.getBullets(data):
                if bullet.isVisible():
                    self.display.blit(bullet.draw(data).get("image"), bullet.draw(data).get("position"))
                    if bullet.hit(player):
                        if bullet in enemy.getBullets(data):
                            enemy.getBullets(data).remove(bullet)
                        player.gotHit()
                        if player.isDead():
                            self.display.blit(self.textDied, self.textDiedPos)
                            self.delay(100)
                            return False

        for text in self.texts:
            if text.getCount() <= data.showTime:
                text.draw()
                self.display.blit(text.getText(), text.getPosition())
            else:
                if text in self.texts:
                    self.texts.remove(text)

        pg.display.update()
        return True

class Text:
    def __init__(self, text, position):
        self.countFrame = 0
        self.text = text
        self.x = position[0]
        self.y = position[1]

    def getCount(self):
        return self.countFrame

    def getText(self):
        return self.text

    def getPosition(self):
        return (self.x, self.y)

    def draw(self):
        self.y -= 3
        self.countFrame += 1

class Projectile:
    def __init__(self, data, x, y, facingLeft, enemy):
        self.x = x
        self.y = y
        self.size = data.bullet.get("size")
        self.facing = -1 if facingLeft else 1
        self.vel = data.bullet["vel"] * self.facing
        self.visible = True
        self.enemy = enemy
        self.img = data.bullet.get("left")

    def isVisible(self):
        return self.visible

    def draw(self, data):
        if self.facing == -1:
            if self.enemy:
                image = data.bullet.get("enemy left")
            else:
                image = data.bullet["left"]
        else:
            if self.enemy:
                image = data.bullet.get("enemy right")
            else:
                image = data.bullet["right"]
        position = (self.x, self.y)
        self.x += self.vel
        self.img = image
        return {"image" : image, "position" : position}

    def hit(self, object):
        objectMask = object.getMask()
        bulletMask = pg.mask.from_surface(self.img)
        position = object.getPosition()
        offset = (round(self.x - position[0]), round(self. y - position[1]))
        collisionPoint = objectMask.overlap(bulletMask, offset)
        return collisionPoint

class Player:
    def __init__(self, data):
        self.x = data.playerX
        self.y = data.playerY
        self.size = data.playerSize
        self.vel = data.playerVel
        self.isJump = False
        self.facingLeft = False
        self.jumpMax = data.playerJumpMax
        self.shootMax = data.playerShootMax
        self.walkCount = 0
        self.jumpCount = 10
        self.jumpLoop = 0
        self.standing = True
        self.bullets = []
        self.shootLoop = 0
        self.heart = data.playerMaxHeart
        self.score = 0
        self.img = data.playerStanding

    def getMask(self):
        return pg.mask.from_surface(self.img)

    def getNumberBullets(self):
        return len(self.bullets)

    def getScore(self):
        return self.score

    def addScore(self):
        self.score += 1

    def addHeart(self):
        self.heart += 1

    def getHeart(self):
        return self.heart

    def getPosition(self):
        return (self.x, self.y)

    def gotHit(self):
        if self.heart > 0:
            self.heart -= 1

    def isDead(self):
        if self.heart <= 0:
            return True
        return False

    def draw(self, data):
        position = (self.x, self.y)
        if self.walkCount + 1 >= data.playerFrame:
            self.walkCount = 0

        if self.jumpLoop > 0:
            self.jumpLoop += 1
        if self.jumpLoop > self.jumpMax:
            self.jumpLoop = 0

        if self.shootLoop > 0:
            self.shootLoop += 1
        if self.shootLoop > self.shootMax:
            self.shootLoop = 0

        if self.standing:
            if self.facingLeft:
                image = data.playerWalkLeft[0]
            else:
                image = data.playerWalkRight[0]
        else:
            if self.facingLeft:
                image = data.playerWalkLeft[self.walkCount // data.fps]
            else:
                image = data.playerWalkRight[self.walkCount // data.fps]

        if self.isJump:
            if self.jumpCount >= -10:
                neg = 1
                if self.jumpCount <= 0:
                    neg = -1
                self.y -= (round(self.jumpCount ** 2)) * 0.5 * neg
                self.jumpCount -= 1
            else:
                self.isJump = False
                self.jumpCount = 10
        self.img = image

        return {"image" : image, "position" : position}

    def getBullets(self, data):
        for bullet in self.bullets:
            if bullet.x < 0 or bullet.x > data.bgSize[0] - data.bullet.get("size")[0]:
                self.bullets.pop(0)
        return self.bullets


    def stand(self):
        self.walkCount = 0
        self.standing = True

    def walk(self, data, walkLeft):
        if walkLeft:
            if (self.x <= self.vel):
                self.standing = True
                self.walkCount = 0
            else:
                self.x -= self.vel
                self.facingLeft = True
                self.standing = False
                self.walkCount += 1
        else:
            if (self.x >= data.bgSize[0] - data.playerSize[0] - self.vel):
                self.standing = True
                self.walkCount = 0
            else:
                self.x += self.vel
                self.facingLeft = False
                self.standing = False
                self.walkCount += 1

    def jump(self, data):
        if not self.isJump and self.jumpLoop == 0:
            self.isJump = True
            self.walkCount = 0
            self.jumpLoop = 1

    def shoot(self, data):
        if self.shootLoop == 0 and len(self.bullets) < data.playerMaxBullet:
            self.bullets.append(Projectile(data, round(self.x + self.size[0] // 2), round(self.y + self.size[1] // 2), self.facingLeft, False))
            self.shootLoop = 1
            data.bulletSound.play()

class Enemy:
    def __init__(self, data, x, facingLeft):
        self.x = x
        self.y = data.enemyY
        self.size = data.enemySize
        self.vel = data.enemyVel
        self.isJump = False
        self.facingLeft = facingLeft
        self.loop = data.enemyDelay
        self.walkCount = 0
        self.jumpCount = 10
        self.jumpLoop = 0
        self.standing = True
        self.bullets = []
        self.shootLoop = 0
        self.health = data.enemyHealth

        self.explosionX = self.x + ((data.enemySize[0] - data.explosionSize[0]) // 2)
        self.explosionY = self.y + ((data.enemySize[1] - data.explosionSize[1]) // 2)
        self.explosionCount = 0
        self.drawingExplosion = True

        self.img = data.enemyWalkRight[0]

    def getMask(self):
        return pg.mask.from_surface(self.img)

    def isDrawingExplosion(self):
        return self.drawingExplosion

    def getPosition(self):
        return (self.x, self.y)

    def getHealth(self):
        return self.health

    def isDead(self):
        if self.health <= 0:
            return True
        return False

    def draw(self, data):
        if self.explosionCount < data.explosionFrame:
            position = (self.explosionX, self.explosionY)
            image = data.explosion[self.explosionCount // data.fps]
            self.explosionCount += 1
            return {"image" : image, "position" : position}

        self.drawingExplosion = False
        position = (self.x, self.y)
        if self.walkCount + 1 >= data.enemyFrame:
            self.walkCount = 0

        if self.jumpLoop > 0:
            self.jumpLoop += 1
        if self.jumpLoop > self.loop:
            self.jumpLoop = 0

        if self.shootLoop > 0:
            self.shootLoop += 1
        if self.shootLoop > self.loop:
            self.shootLoop = 0

        if self.standing:
            if self.facingLeft:
                image = data.enemyWalkLeft[0]
            else:
                image = data.enemyWalkRight[0]
        else:
            if self.facingLeft:
                image = data.enemyWalkLeft[self.walkCount // data.fps]
            else:
                image = data.enemyWalkRight[self.walkCount // data.fps]

        if self.isJump:
            if self.jumpCount >= -10:
                neg = 1
                if self.jumpCount <= 0:
                    neg = -1
                self.y -= (round(self.jumpCount ** 2)) * 0.5 * neg
                self.jumpCount -= 1
            else:
                self.isJump = False
                self.jumpCount = 10

        self.walk(data, self.facingLeft)
        self.img = image

        return {"image" : image, "position" : position}

    def getBullets(self, data):
        for bullet in self.bullets:
            if bullet.x < 0 or bullet.x > data.bgSize[0] - data.bullet.get("size")[0]:
                self.bullets.pop(0)
        return self.bullets

    def changeDirection(self):
        if self.facingLeft:
            self.facingLeft = False
        else:
            self.facingLeft = True
        self.walkCount = 0

    def stand(self):
        self.walkCount = 0
        self.standing = True

    def walk(self, data, walkLeft):
        if walkLeft:
            if self.x <= self.vel:
                self.standing = True
                self.walkCount = 0
                self.changeDirection()
            else:
                self.x -= self.vel
                self.facingLeft = True
                self.standing = False
                self.walkCount += 1
        else:
            if self.x >= data.bgSize[0] - data.enemySize[0] - self.vel:
                self.standing = True
                self.walkCount = 0
                self.changeDirection()
            else:
                self.x += self.vel
                self.facingLeft = False
                self.standing = False
                self.walkCount += 1

    def jump(self, data):
        if not self.isJump and self.jumpLoop == 0:
            self.isJump = True
            self.walkCount = 0
            self.jumpLoop = 1

    def shoot(self, data):
        if self.shootLoop == 0 and len(self.bullets) < data.enemyMaxBullet:
            self.bullets.append(Projectile(data, round(self.x + self.size[0] // 2), round(self.y + self.size[1] // 2), self.facingLeft, True))
            self.shootLoop = 1
            data.bulletSound.play()

    def defense(self, data, bullets):
        for bullet in bullets:
            if abs(bullet.x - self.x) < 100:
                self.jump(data)

    def attack(self, data, player):
        if self.facingLeft and player.x < self.x:
            self.shoot(data)
        if not self.facingLeft and player.x > self.x:
            self.shoot(data)

    def gotHit(self):
        if self.health > 0 and not self.drawingExplosion:
            self.health -= 1


def main():
    data = Data()
    win = Win(data)
    player = Player(data)
    enemies = []
    count = 0
    start = time.time()
    pg.mixer.music.play(-1)

    run = True
    while run:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                run = False

        if not win.playing(data, player, enemies, start):
            player = None
            enemies.clear()
            keys = pg.key.get_pressed()
            if not keys[pg.K_RETURN]:
                win.playAgain()
                continue
            else:
                player = Player(data)
                data = Data()
                start = time.time()
                pg.mixer.music.play(-1)

        count += 1

        if len(enemies) < data.enemyMax and count >= data.enemyDelayCreating:
            enemies.append(Enemy(data, random.randrange(0, data.bgSize[0] - data.enemySize[0]), random.choice((True, False))))
            count = 0

        for enemy in enemies:
            if enemy.isDrawingExplosion():
                continue
            enemy.defense(data, player.getBullets(data))
            enemy.attack(data, player)


        keys = pg.key.get_pressed()

        if keys[pg.K_LEFT]:
            player.walk(data, True)
        elif keys[pg.K_RIGHT]:
            player.walk(data, False)
        else:
            player.stand()

        if keys[pg.K_UP]:
            player.jump(data)

        if keys[pg.K_SPACE]:
            player.shoot(data)


main()
pg.quit()