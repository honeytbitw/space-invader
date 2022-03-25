# def displayScreenshot() :
#     while True:
#         screenshot= WindowCapture('Space Invader').take_screenshot()
#         cv.imshow('Computer Vision',screenshot)
        
#         if cv.waitKey(1) == ord('q') :
#             cv.destroyAllWindows()
#             break
#         screenshot.shape= (1,562, 784, 3)
#         res = model(screenshot)
#         action = res.numpy()[0][0]
#         print(action)
#         if(action>0.5) : 
#             print("Right")
#         else :
#             print("Left")
        

# Thread(target = start_game).start()
# Thread(target = displayScreenshot).start()
# from asyncio import run
# import math
# import random
# from turtle import screensize

# import pygame
# from pygame import mixer

# class Game :
#     def __init__(self) :
#         # Intialize the pygame
#         pygame.init()
#         self.screen = pygame.display.set_mode((800, 600))

#         # Background
#         self.background = pygame.image.load('background.png')


#         # Caption and Icon
#         pygame.display.set_caption("Space Invader")
#         icon = pygame.image.load('ufo.png')
#         pygame.display.set_icon(icon)

#         # Player
#         self.playerImg = pygame.image.load('player.png')
#         self.playerX = 370
#         self.playerY = 480
#         self.playerX_change = 0

#         # Enemy
#         self.enemyImg = []
#         self.enemyX = []
#         self.enemyY = []
#         self.enemyX_change = []
#         self.enemyY_change = []
#         self.num_of_enemies = 6

#         for i in range(self.num_of_enemies):
#             self.enemyImg.append(pygame.image.load('enemy.png'))
#             self.enemyX.append(random.randint(0, 736))
#             self.enemyY.append(random.randint(50, 150))
#             self.enemyX_change.append(4)
#             self.enemyY_change.append(40)

#         # Bullet

#         # Ready - You can't see the bullet on the screen
#         # Fire - The bullet is currently moving

#         self.bullet_state = "ready"
#         self.bulletImg = pygame.image.load('bullet.png')
#         self.bulletX = 0
#         self.bulletY = 480
#         self.bulletX_change = 0
#         self.bulletY_change = 10
#         # bullet_state = "ready"

#         # Score

#         self.score_value = 0
#         self.font = pygame.font.Font('freesansbold.ttf', 32)

#         self.textX = 10
#         self.testY = 10

#         # Game Over
#         self.over_font = pygame.font.Font('freesansbold.ttf', 64)

#     def show_score(self,x, y):
#         score = self.font.render("Score : " + str(self.score_value), True, (255, 255, 255))
#         self.screen.blit(score, (x, y))


#     def game_over_text(self):
#         self.over_text = self.over_font.render("GAME OVER", True, (255, 255, 255))
#         self.screen.blit(self.over_text, (200, 250))


#     def player(self,x, y,playerImg):
#         self.screen.blit(playerImg, (x, y))


#     def enemy(self,x, y, enemyImg):
#         self.screen.blit(enemyImg, (x, y))


#     def fire_bullet(self,x, y,bulletImg):
#         self.bullet_state = "fire"
#         self.screen.blit(bulletImg, (x + 16, y + 10))


#     def isCollision(self,enemyX, enemyY, bulletX, bulletY):
#         distance = math.sqrt(math.pow(enemyX - bulletX, 2) + (math.pow(enemyY - bulletY, 2)))
#         if distance < 27:
#             return True
#         else:
#             return False

#     def startGame(self) :

#         # Game Loop
#         running = True
#         game_over = False
#         while running:
#             # auto shoot
#             if (self.bullet_state == "ready" and game_over!=True) :
#                 bulletSound = mixer.Sound("laser.wav")
#                 bulletSound.play()
#                 # Get the current x cordinate of the spaceship
#                 self.bulletX = self.playerX
#                 self.fire_bullet(self.bulletX, self.bulletY,self.bulletImg)


#             # RGB = Red, Green, Blue
#             self.screen.fill((0, 0, 0))
#             # Background Image
#             self.screen.blit(self.background, (0, 0))
#             for event in pygame.event.get():
#                 if event.type == pygame.QUIT:
#                     running = False

#                 # if keystroke is pressed check whether its right or left
#                 if event.type == pygame.KEYDOWN:
#                     if event.key == pygame.K_LEFT:
#                         self.playerX_change = -5
#                     if event.key == pygame.K_RIGHT:
#                         self.playerX_change = 5
#                     # if event.key == pygame.K_SPACE:
#                     #     if self.bullet_state == "ready":
#                     #         bulletSound = mixer.Sound("laser.wav")
#                     #         bulletSound.play()
#                     #         # Get the current x cordinate of the spaceship
#                     #         self.bulletX = self.playerX
#                     #         self.fire_bullet(self.bulletX, self.bulletY,self.bulletImg)

#                 if event.type == pygame.KEYUP:
#                     if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
#                         self.playerX_change = 0

#             self.playerX += self.playerX_change
#             if self.playerX <= 0:
#                 self.playerX = 0
#             elif self.playerX >= 736:
#                 self.playerX = 736

#             # Enemy Movement
#             for i in range(self.num_of_enemies):

#                 # Game Over
                
#                 if self.enemyY[i] > 440:
#                     for j in range(self.num_of_enemies):
#                         self.enemyY[j] = 2000
#                     game_over=True
#                     self.game_over_text()
#                     break

#                 self.enemyX[i] += self.enemyX_change[i]
#                 if self.enemyX[i] <= 0:
#                     self.enemyX_change[i] = 4
#                     self.enemyY[i] += self.enemyY_change[i]
#                 elif self.enemyX[i] >= 736:
#                     self.enemyX_change[i] = -4
#                     self.enemyY[i] += self.enemyY_change[i]

#                 # Collision
#                 collision = self.isCollision(self.enemyX[i], self.enemyY[i], self.bulletX, self.bulletY)
#                 if collision:
#                     explosionSound = mixer.Sound("explosion.wav")
#                     explosionSound.play()
#                     self.bulletY = 480
#                     self.bullet_state = "ready"
#                     self.score_value += 1
#                     self.enemyX[i] = random.randint(0, 736)
#                     self.enemyY[i] = random.randint(50, 150)

#                 self.enemy(self.enemyX[i], self.enemyY[i], self.enemyImg[i])

#             # Bullet Movement
#             if self.bulletY <= 0:
#                 self.bulletY = 480
#                 self.bullet_state = "ready"

#             if ( self.bullet_state == "fire") :
#                 self.fire_bullet(self.bulletX, self.bulletY,self.bulletImg)
#                 self.bulletY -= self.bulletY_change

#             self.player(self.playerX, self.playerY,self.playerImg)
#             self.show_score(self.textX, self.testY)
#             pygame.display.update()
# # Game().startGame()