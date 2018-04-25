# -*- coding: utf-8 -*-
import pygame
#导入pygame库
from sys import exit
#向sys模块借一个exit函数用来退出程序
import random
#导入random库
pygame.init()
#初始化pygame,为使用硬件做准备
screen = pygame.display.set_mode((1024, 683), 0, 32)
#创建了一个窗口,窗口大小和背景图片大小一样
pygame.display.set_caption("Hello, World!")
#设置窗口标题
#创建一个子弹类
class Bullet:
    def __init__(self):
        #初始化成员变量，x，y，image
        self.x = 0
        self.y = -1
        self.image = pygame.image.load('bullet.png').convert_alpha()
        self.active = False

    def move(self):
        #处理子弹的运动
        if self.y < 0:
            mouseX, mouseY = pygame.mouse.get_pos()
            self.x = mouseX - self.image.get_width() / 2
            self.y = mouseY - self.image.get_height() / 2
        else:
            self.y -= 5


class Enemy:
    def __init__(self):
        self.x = 200
        self.y = -50
        self.image = pygame.image.load('enemy.png').convert_alpha()
        self.speed = 0.5
        self.restart()

    def move(self):
        if self.y<800:
            self.y +=self.speed
        else:
            self.restart()

    def restart(self):
        self.x = random.randint(50,1000)
        self.y = random.randint(-200,50)
        self.speed = random.random()+0.1

def checkHit(enemy,bullet):
    if(bullet.x > enemy.x and bullet.x < enemy.x + enemy.image.get_width() and bullet.y > enemy.y and bullet.y < enemy.y + enemy.image.get_height()):
        enemy.restart()
        return True
#检查敌机是否中弹
def deathHit(plane,bullet_en):
    if(bullet_en.x > plane.x and bullet_en.x < plane.x + plane.image.get_width() and bullet_en.y > plane.y and bullet_en.y < plane.y + plane.image.get_height()):
        return True
#检查我机是否中弹
#创建我机的类
class Plane:
    def __init__(self):
        self.restart()
        self.image = pygame.image.load ('plane.png').convert_alpha()
        #加载飞机图像
    def move(self):
        x, y = pygame.mouse.get_pos()
        x -= self.image.get_width()/2
        y -= self.image.get_height()/2
        self.x = x
        self.y = y
    def restart(self):
        self.x = 512
        self.y = 341
#检查是否撞击
def checkCrash(enemy,plane):
    if (plane.x + 0.7*plane.image.get_width() > enemy.x) and (plane.x + 0.3*plane.image.get_width() < enemy.x + enemy.image.get_width()) and (plane.y + 0.7*plane.image.get_height() > enemy.y) and (plane.y + 0.3*plane.image.get_height() < enemy.y + enemy.image.get_height()):
        return True
    return False

background = pygame.image.load('bg.jpg').convert()
#加载并转换图像

bullet = Bullet()
#创建我机子弹实例
bullet_en = Bullet()
#创建敌机子弹实例
enemy = Enemy()
#创建敌机实例
plane = Plane()
#创建我机实例
enemys = []
for i in range(3):
    enemys.append(Enemy())
#创建敌机群
font = pygame.font.Font(None,32)
#创建文本框对象
gameover = False
#我机被敌机撞击标志
score = 0
#玩家得分

while True:
#游戏主循环
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            #接收到退出事件后退出程序
            pygame.quit()
            exit()
    screen.blit(background, (0,0))
    #将背景图画上去
    text = font.render("score:%d"%score,1,(0,0,0))
    screen.blit(text,(0,0))
    #将得分文本框画上去
    if not gameover:
        bullet.move()
        screen.blit(bullet.image,(bullet.x,bullet.y))
        #子弹组
        for e in enemys:
            crash = checkCrash(e,plane)
            if crash:
                gameover = True
                plane.restart()
            e.move()
            bullet_en.image = pygame.image.load('bullet_en.png').convert_alpha()
            bullet_en.x = e.x + bullet_en.image.get_width()
            bullet_en.y = e.y*5 + bullet_en.image.get_height()
            screen.blit(bullet_en.image,(bullet_en.x,bullet_en.y))
            screen.blit(e.image,(e.x,e.y))
            hit = checkHit(e,bullet)
            if hit:
                score += 1
            #击中敌机得分
            death = deathHit(plane,bullet_en)
            if death:
                gameover = True
                plane.restart()
        plane.move()
        screen.blit(plane.image, (plane.x,plane.y))
    else:
        if score <= 10:
            text_final = font.render("Come on! your final score is :%d"%score,1,(0,0,0))
        elif score >= 50:
            text_final = font.render("Grate! your final score is :%d"%score,1,(0,0,0))
        else:
            text_final = font.render("Good! your final score is :%d"%score,1,(0,0,0))
        screen.blit(text_final,(350,300))
    if gameover and event.type == pygame.MOUSEBUTTONUP:
        plane.restart()
        score = 0
        gameover = False
    pygame.display.update()
        #刷新一下画面
