from dis import disco
import math
import random

import pygame
from pygame import mixer
import keras
from threading import Thread
from window_capture import WindowCapture
import numpy as np
import cv2 as cv
import tensorflow as tf
from tensorflow.keras.optimizers import Adam
# import tensorflow_probability as tfp

model = keras.models.load_model('model')
print(model.summary())
bullet_state = "ready"




# Game Loop
def start_game() :
    global bullet_state

    # Intialize the pygame
    pygame.init()
    # global playerX, playerY, playerX_change, enemyX, enemyY, bulletX, bulletY, bullet_state, score_value

    # create the screen
    screen = pygame.display.set_mode((800, 600))

    # Background
    background = pygame.image.load('background.png')


    # Caption and Icon
    pygame.display.set_caption("Space Invader")
    icon = pygame.image.load('ufo.png')
    pygame.display.set_icon(icon)

    # Player
    playerImg = pygame.image.load('player.png')
    playerX = 370
    playerY = 480
    playerX_change = 0

    # Enemy
    enemyImg = [None for _ in range (6)]
    enemyX = [None for _ in range (6)]
    enemyY = [None for _ in range (6)]
    enemyX_change = [None for _ in range (6)]
    enemyY_change = [None for _ in range (6)]
    num_of_enemies = 6

    def initializePosition() :
        for i in range(num_of_enemies):
            enemyImg[i]=pygame.image.load('enemy.png')
            enemyX[i]=random.randint(0, 736)
            enemyY[i]=random.randint(50, 150)
            enemyX_change[i]=4
            enemyY_change[i]=40
        playerX = 370
        playerY = 480
        playerX_change = 0

    # Bullet

    # Ready - You can't see the bullet on the screen
    # Fire - The bullet is currently moving

    bulletImg = pygame.image.load('bullet.png')
    bulletX = 0
    bulletY = 480
    bulletX_change = 0
    bulletY_change = 10
    

    # Score

    score_value = 0
    font = pygame.font.Font('freesansbold.ttf', 32)

    textX = 10
    testY = 10

    # Game Over
    over_font = pygame.font.Font('freesansbold.ttf', 64)
    running = True
    game_over = False
    reward =[]
    episodes =10


    def show_score(x, y):
        score = font.render("Score : " + str(score_value), True, (255, 255, 255))
        screen.blit(score, (x, y))


    def game_over_text():
        over_text = over_font.render("GAME OVER", True, (255, 255, 255))
        screen.blit(over_text, (200, 250))


    def player(x, y):
        screen.blit(playerImg, (x, y))


    def enemy(x, y, i):
        screen.blit(enemyImg[i], (x, y))


    def fire_bullet(x, y):
        global bullet_state
        bullet_state = "fire"
        screen.blit(bulletImg, (x + 16, y + 10))


    def isCollision(enemyX, enemyY, bulletX, bulletY):
        distance = math.sqrt(math.pow(enemyX - bulletX, 2) + (math.pow(enemyY - bulletY, 2)))
        if distance < 27:
            return True
        else:
            return False
        

    def predictAction(screenshot):
        res = model(screenshot)
        action = res.numpy()[0][0]
        return action
        

    def calculateDiscountedReward(rewards,discountedRewards) :
        sum_reward = 0
        gamma=0.99
        rewards.reverse()  # starting from the last element
        for r in rewards:  # calculates the cumulative expected reward for each state
            sum_reward = r + gamma * sum_reward
            discountedRewards.append(sum_reward)
        discountedRewards.reverse()

    def calculateLoss(prob,action,reward) :

        # prob = tf.convert_to_tensor(prob)
        # dist = tfp.distributions.Categorical(probs=(prob), dtype=tf.float32)
        # log_prob = dist.log_prob(action)
        # loss = -log_prob * reward  # isch gradient ascent wenn ich mich ned tüsche ned descent
        loss = -np.log(prob)*reward
        return tf.convert_to_tensor(loss)

    def gradientDescent(states,rewards,actions):
        optimizer = Adam(.0003)
        discountedRewards=[]
        calculateDiscountedReward(rewards,discountedRewards)
        print(discountedRewards)
        for state, G_t, action in zip(states, discountedRewards, actions):
            with tf.GradientTape() as g:
                p = predictAction(state)
                loss = calculateLoss(p, action, G_t)
                print("Loss",loss)
            grads = g.gradient(loss, model.trainable_variables)
            optimizer.apply_gradients(zip(grads,model.trainable_variables))
        print('Here')
        # for i in range (len(rewards)) :
        #     train = optimizer.minimize(calculateLoss(rewards,i+1,actions[i])) 
        #     # init = tf.initialize_all_variables()
        #     with tf.Session() as session:
        #     #     session.run(init)
        #     #     for step in range(10):
        #         session.run(train)

    for i in range (10):
        running = True
        game_over = False
        states=[]
        reward = []
        actions =[]
        score_value=0
        initializePosition()
        print("Episode = ",i)
        while running:
            # auto shoot
            if (bullet_state == "ready" and game_over!=True) :
                bulletSound = mixer.Sound("laser.wav")
                bulletSound.play()
                # Get the current x cordinate of the spaceship
                bulletX = playerX
                fire_bullet(bulletX, bulletY)
            # RGB = Red, Green, Blue
            screen.fill((0, 0, 0))
            # Background Image
            # screen.blit(background, (0, 0))

            # quit 
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
            
            # capturing game state
            screenshot= WindowCapture('Space Invader').take_screenshot()
            states.append(screenshot)
            
            # predicting through model
            action = predictAction(screenshot)
            actions.append(action)
            # sampling (for exploration)
            if np.random.uniform() < action :
                action =0
            else :
                action= 1

            # performing action
            if action == 0: #going left
                playerX_change = -5
            else: #going right
                playerX_change = 5
            playerX += playerX_change

            if playerX <= 0:
                playerX = 0
            elif playerX >= 736:
                playerX = 736

            # Enemy Movement
            for i in range(num_of_enemies):

                if enemyY[i] > 440:
                    for j in range(num_of_enemies):
                        enemyY[j] = 2000
                    game_over_text()
                    reward.append(-10)
                    game_over = True
                    running = False
                    break

                enemyX[i] += enemyX_change[i]
                if enemyX[i] <= 0:
                    enemyX_change[i] = 4
                    enemyY[i] += enemyY_change[i]
                elif enemyX[i] >= 736:
                    enemyX_change[i] = -4
                    enemyY[i] += enemyY_change[i]

                # Collision
                collision = isCollision(enemyX[i], enemyY[i], bulletX, bulletY)
                if collision:
                    explosionSound = mixer.Sound("explosion.wav")
                    explosionSound.play()
                    bulletY = 480
                    bullet_state = "ready"
                    score_value += 1
                    enemyX[i] = random.randint(0, 736)
                    enemyY[i] = random.randint(50, 150)
                    reward.append(10)
                    # running = False

                enemy(enemyX[i], enemyY[i], i)
            
            # Bullet Movement
            if bulletY <= 0:
                bulletY = 480
                bullet_state = "ready"

            if bullet_state == "fire":
                fire_bullet(bulletX, bulletY)
                bulletY -= bulletY_change

            player(playerX, playerY)
            show_score(textX, testY)
            if game_over == False : 
                reward.append(0)
            pygame.display.update()
        
        if not running and not game_over :
            break

        if running == False :
            gradientDescent(states,reward,actions)

start_game()