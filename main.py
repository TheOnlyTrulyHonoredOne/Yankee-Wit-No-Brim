import random
import pygame
import os

pygame.font.init()
pygame.mixer.init()
pygame.init()

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
green = (0, 255, 0)
blue = (0, 0, 128)
orange = (219, 104, 15)
yellow = (255, 255, 0)
RED = (255, 0, 0)


# Specs of the window
WIDTH, HEIGHT = 900, 600
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("YANKEE WITH NO BRIM")
FPS = 60


# CLASSES
class Player:
    def __init__(self, health, attack, defense, speed):
        self.health = health
        self.MAX_HEALTH = health
        self.heathArray = [1] * self.health
        self.attack = attack
        self.defense = defense
        self.LOVE = 0
        self.speed = 10
        self.HEART_WIDTH = 20
        self.HEART_HEIGHT = 20
        self.PLAYER_HEART_IMAGE = pygame.image.load(os.path.join("Assets", "undertaleHeart.png"))
        self.PLAYER_HEART = pygame.transform.rotate(
            pygame.transform.scale(self.PLAYER_HEART_IMAGE, (self.HEART_WIDTH, self.HEART_HEIGHT)), 360)
        self.HEART_VEL = 4
        self.HEART_HITBOX = pygame.Rect(450, 300, self.HEART_WIDTH, self.HEART_HEIGHT)
        self.HEART_VISIBLE = True

    def dealDamage(self, enemy, damageDone):
        enemy.health = enemy.health - damageDone
        print("Damage: " + str(damageDone))
        print("Enemy Health: " + str(enemy.health))

    def setHeartInvisible(self):
        self.HEART_VISIBLE = False

    def drawCharacterInfo(self):
        font = pygame.font.Font('freesansbold.ttf', 25)
        theText = font.render("CHARA", True, WHITE, BLACK)
        WIN.blit(theText, (60, 490))
        theText = font.render("LV " + str(19), True, WHITE, BLACK)
        WIN.blit(theText, (180, 490))
        font = pygame.font.Font('freesansbold.ttf', 15)
        theText = font.render("HP", True, WHITE, BLACK)
        WIN.blit(theText, (290, 495))

        color = green
        for i in range(self.health):
            if self.heathArray[i] == 1:
                color = yellow
            else:
                color = RED

            pygame.draw.rect(WIN, color, (320 + i * 5, 490, 1, 20), 3)

        font = pygame.font.Font('freesansbold.ttf', 25)
        theText = font.render(str(self.health) + "/" + str(self.MAX_HEALTH), True, WHITE, BLACK)
        WIN.blit(theText, (430, 490))


class Yankee:
    def __init__(self):
        self.health = 350
        self.width = 160
        self.height = 120
        self.sprite = pygame.image.load(os.path.join("Assets", "noBrim.png"))
        self.yankee = pygame.transform.rotate(pygame.transform.scale(self.sprite, (self.width, self.height)), 360)
        self.yankee_HITBOX = pygame.Rect(370, 40, self.width, self.height)
        self.goingDown = True


class AttackBar:
    def __init__(self):
        self.xPos = 50
        self.goingRight = True


class Projectile:
    def __init__(self, speed, direction, position):
        self.direction = direction
        self.speed = speed
        self.position = position

    def changePosition(self, speed, direction):
        self.position = direction * speed


class MovementBox:
    def __init__(self):
        self.width = 800
        self.height = 200
        self.xPosition = 50
        self.yPosition = 270
        self.left = self.xPosition
        self.right = self.left + self.width
        self.top = self.yPosition
        self.bottom = self.yPosition + self.height
        self.mode = "text"
        self.attackBar = AttackBar()
        self.inActMode = False
        self.mercyLevel = 0
        self.canMercy = False
        self.willAct = False
        self.seeActList = False


    def changeToFightingMode(self):
        self.width = 250
        self.height = 250
        self.xPosition = 320
        self.yPosition = 220
        self.setBarriers()
        self.mode = "fighting"

    def changeToActionMode(self):
        self.width = 800
        self.height = 200
        self.xPosition = 50
        self.yPosition = 270
        self.setBarriers()
        self.mode = "action"

    def setBarriers(self):
        self.left = self.xPosition
        self.right = self.left + self.width
        self.top = self.yPosition
        self.bottom = self.yPosition + self.height

    def changeToAttackMode(self):
        self.mode = "attack"

    def changeToTextMode(self):
        self.width = 800
        self.height = 200
        self.xPosition = 50
        self.yPosition = 270
        self.setBarriers()
        self.mode = "text"

    def drawTheBox(self):
        pygame.draw.rect(WIN, WHITE, (self.xPosition, self.yPosition, self.width, self.height), 3)

        if self.mode == "text":

            ## the bullet
            BULLET_WIDTH, BULLET_HEIGHT = 30, 20
            BULLET_IMAGE = pygame.image.load(os.path.join("Assets", "nameBullet.png"))
            BULLET = pygame.transform.rotate(pygame.transform.scale(BULLET_IMAGE, (BULLET_WIDTH, BULLET_HEIGHT)), 360)
            BULLET_HITBOX = pygame.Rect(80, 300, BULLET_WIDTH, BULLET_HEIGHT)
            WIN.blit(BULLET, (BULLET_HITBOX.x, BULLET_HITBOX.y))

            font = pygame.font.Font('freesansbold.ttf', 35)
            if self.inActMode:
                if self.seeActList == True:
                    if self.mercyLevel == 0:
                        theText = font.render("Compliment Yankee", True, WHITE, BLACK)
                    elif self.mercyLevel == 1:
                        theText = font.render("Compliment Yankee", True, WHITE, BLACK)
                    elif self.mercyLevel == 2:
                        theText = font.render("Compliment Yankee", True, WHITE, BLACK)
                    elif self.mercyLevel == 3:
                        theText = font.render("Ask Yankee to go around", True, WHITE, BLACK)
                else:
                    theText = font.render("Yankee", True, WHITE, BLACK)

            else:
                theText = font.render("Yankee with no brim!", True, WHITE, BLACK)
            ## THE TEXT


            WIN.blit(theText, (120, 295))

        if self.mode == "attack":
            ATTACK_SCREEN_WIDTH, ATTACK_SCREEN_HEIGHT = 800, 200
            ATTACK_SCREEN_IMAGE = pygame.image.load(os.path.join("Assets", "attackAim.png"))
            ATTACK_SCREEN = pygame.transform.rotate(pygame.transform.scale(ATTACK_SCREEN_IMAGE, (ATTACK_SCREEN_WIDTH, ATTACK_SCREEN_HEIGHT)), 360)
            ATTACK_SCREEN_HITBOX = pygame.Rect(50, 270, ATTACK_SCREEN_WIDTH, ATTACK_SCREEN_HEIGHT)
            WIN.blit(ATTACK_SCREEN, (ATTACK_SCREEN_HITBOX.x, ATTACK_SCREEN_HITBOX.y))


class ActionBox:
    isActive = False
    name = "test"

    def __init__(self, xLocation, yLocation, image, text, activeIndex, personalIndex):
        self.setIsActive(activeIndex == personalIndex)
        self.name = text
        font = pygame.font.Font('freesansbold.ttf', 32)

        theText = font.render(text, True, orange, BLACK)
        if self.isActive:
            theText = font.render(text, True, yellow, BLACK)

        WIN.blit(theText, (xLocation, yLocation))
        self.drawBOX(xLocation, yLocation, text)

    def drawBOX(self, xLocation, yLocation, text):
        text = str(text)
        numOfCharacters = len(text)

        if self.isActive:
            if self.name == "ACT":
                surounding_box = pygame.draw.rect(WIN, yellow, (xLocation - 90, yLocation - 10, 170, 50),
                                                  3)  # WIN, Color, (X, Y, WIDTH, HEIGHT), 3 (for no fill)
            else:
                surounding_box = pygame.draw.rect(WIN, yellow, (xLocation - 45, yLocation - 10, 170, 50),
                                                  3)  # WIN, Color, (X, Y, WIDTH, HEIGHT), 3 (for no fill)
        else:

            if self.name == "ACT":
                surounding_box = pygame.draw.rect(WIN, orange, (xLocation - 90, yLocation - 10, 170, 50),
                                                  3)  # WIN, Color, (X, Y, WIDTH, HEIGHT), 3 (for no fill)
            else:
                surounding_box = pygame.draw.rect(WIN, orange, (xLocation - 45, yLocation - 10, 170, 50), 3)

    def setIsActive(self, boolean):
        self.isActive = boolean


##p1 = Player(20, 1)
##HOWEY = Player(50, 2)


# Test Function
def what_the_heck():
    print("My")
    pygame.time.wait(5000)
    print("Name")
    pygame.time.wait(5000)
    print("IS")
    pygame.time.wait(5000)
    print("Jeff")


# Movement Function
def handle_heart_movement(keys_pressed, battleBox, p1):
    if keys_pressed[pygame.K_a] and p1.HEART_HITBOX.x >= battleBox.left + 5:
        p1.HEART_HITBOX.x -= p1.HEART_VEL
    if keys_pressed[pygame.K_d] and p1.HEART_HITBOX.x <= battleBox.right - 25:  # Right
        p1.HEART_HITBOX.x += p1.HEART_VEL
    if keys_pressed[pygame.K_w] and p1.HEART_HITBOX.y >= battleBox.top + 5:  # Up
        p1.HEART_HITBOX.y -= p1.HEART_VEL
    if keys_pressed[pygame.K_s] and p1.HEART_HITBOX.y <= battleBox.bottom - 25:  # Down
        p1.HEART_HITBOX.y += p1.HEART_VEL
    if keys_pressed[pygame.K_r]:
        what_the_heck()


goingDown = True


def drawActionBoxes(activeIndex):
    ActionBox(110, 540, 10, "FIGHT", activeIndex, 0)
    ActionBox(355, 540, 10, "ACT", activeIndex, 1)
    ActionBox(510, 540, 10, "ITEM", activeIndex, 2)
    ActionBox(710, 540, 10, "MERCY", activeIndex, 3)


def draw_window(p1, YANKEE_WITH_NO_BRIM, activeIndex, battleBox):
    WIN.fill(BLACK)
    battleBox.drawTheBox()  # X, Y, WIDTH, HEIGHT
    if battleBox.mode == "fighting":
        WIN.blit(p1.PLAYER_HEART, (p1.HEART_HITBOX.x, p1.HEART_HITBOX.y))
    else:
        p1.setHeartInvisible()

    if battleBox.mode == "attack":
        if battleBox.attackBar.xPos >= battleBox.right:
            battleBox.attackBar.goingRight = False
        if battleBox.attackBar.goingRight:
            pygame.draw.rect(WIN, WHITE, (battleBox.attackBar.xPos, 272, 10, 195), 0)
            battleBox.attackBar.xPos = battleBox.attackBar.xPos + 8
        else:
            ##print("made it to fighting")
            battleBox.attackBar.xPos = 50
            battleBox.mode = "fighting"
            p1.HEART_HITBOX.x = 450
            p1.HEART_HITBOX.y = 300
            battleBox.changeToFightingMode()

    if YANKEE_WITH_NO_BRIM.goingDown:
        YANKEE_WITH_NO_BRIM.yankee_HITBOX.y = YANKEE_WITH_NO_BRIM.yankee_HITBOX.y + 1
    else:
        YANKEE_WITH_NO_BRIM.yankee_HITBOX.y = YANKEE_WITH_NO_BRIM.yankee_HITBOX.y - 1

    WIN.blit(YANKEE_WITH_NO_BRIM.yankee, (YANKEE_WITH_NO_BRIM.yankee_HITBOX.x, YANKEE_WITH_NO_BRIM.yankee_HITBOX.y))

    drawActionBoxes(activeIndex)
    p1.drawCharacterInfo()

    pygame.display.update()


top = 40
bottom = 100


# Main Game Function
def main():
    goingDown = True
    goingRight = True
    activeIndex = 0  ## x,y,w,h
    attackBarX = 50

    clock = pygame.time.Clock()
    run = True
    rigtkeyDown = False
    leftKeyDown = False
    spaceDown = False
    battleBox = MovementBox()
    spaceWasLifted = True
    readyForFighting = False

    frameCount = 0
    endFrame = -1


    p1 = Player(20, 10, 10, 5)
    YANKEE_WITH_NO_BRIM = Yankee()


    yankeeWithNoBrim = Player(100, 10, 10, 10)

    ##while yankeeWithNoBrim.health >= 0:

    actionsTuple = ("FIGHT", "ACT", "ITEM", "MERCY")

    while run:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()

        if YANKEE_WITH_NO_BRIM.health <= 0:
            pygame.quit()

        if YANKEE_WITH_NO_BRIM.yankee_HITBOX.y >= 70:
            YANKEE_WITH_NO_BRIM.goingDown = False

        if YANKEE_WITH_NO_BRIM.yankee_HITBOX.y <= 40:
            YANKEE_WITH_NO_BRIM.goingDown = True

        draw_window(p1, YANKEE_WITH_NO_BRIM, activeIndex, battleBox)
        keys_pressed = pygame.key.get_pressed()

        if not keys_pressed[pygame.K_SPACE]:
            spaceWasLifted = True
            spaceDown = False

        if spaceDown == False:

            if keys_pressed[pygame.K_SPACE]:
                if activeIndex == 0:
                    battleBox.changeToAttackMode()
                    spaceWasLifted = False

                if activeIndex == 1:
                    battleBox.inActMode = True
                    battleBox.willAct = False
                    battleBox.seeActList = False
                    spaceDown = True

                if battleBox.inActMode and spaceWasLifted and not battleBox.willAct:
                    battleBox.willAct = True

                if battleBox.inActMode and spaceWasLifted and battleBox.willAct and not spaceDown and not readyForFighting:
                    battleBox.seeActList = True
                    spaceDown = True
                    readyForFighting = True
                    print("FIRE 1")


                if battleBox.inActMode and battleBox.willAct and battleBox.seeActList and not spaceDown and readyForFighting:
                    print("FIRE")
                    battleBox.changeToFightingMode()
                    readyForFighting = False
                    endFrame = frameCount + 300
                    battleBox.inActMode = False



                if battleBox.mode == "attack" and spaceWasLifted:
                    battleBox.attackBar.goingRight = False
                    spaceDown = True
                    if battleBox.attackBar.xPos >= 440 and battleBox.attackBar.xPos <= 470:
                        b = 4

                    else:
                        b = ((446 - battleBox.attackBar.xPos)/800) * 2

                    p1.dealDamage(YANKEE_WITH_NO_BRIM, round((p1.attack + 0 + random.randrange(-2, 6)) * b))
                    battleBox.attackBar.xPos = 50
                    endFrame = frameCount + 300

        else:
            if keys_pressed[pygame.K_SPACE] == False:
                spaceDown = False

        if battleBox.mode == "text" and not battleBox.inActMode:

            if rigtkeyDown == False:
                if keys_pressed[pygame.K_RIGHT] and activeIndex < 3:
                    activeIndex = activeIndex + 1
                    rigtkeyDown = True

            else:
                if keys_pressed[pygame.K_RIGHT] == False:
                    rigtkeyDown = False

            if leftKeyDown == False:
                if keys_pressed[pygame.K_LEFT] and activeIndex > 0:
                    activeIndex = activeIndex - 1
                    leftKeyDown = True

            else:
                if keys_pressed[pygame.K_LEFT] == False:
                    leftKeyDown = False

        else:
            activeIndex = -1
        handle_heart_movement(keys_pressed, battleBox, p1)

        if battleBox.mode == "fighting" and frameCount >= endFrame and endFrame != -1:
            ##print("ended fighting")
            battleBox.changeToTextMode()
            endFrame = -1
            battleBox.attackBar.goingRight = True

        frameCount += 1



main()
