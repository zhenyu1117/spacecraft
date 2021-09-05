import sys, random, math, pygame
from pygame.locals import *

#显示飞船的坐标
class Point(object):
    def __init__(self, x, y):
        self.__x = x
        self.__y = y

    #X property
    def getx(self): return self.__x
    def setx(self, x): self.__x = x
    x = property(getx, setx)

    #Y property
    def gety(self): return self.__y
    def sety(self, y): self.__y = y
    y = property(gety, sety)

    def __str__(self):
        return "{X:" + "{:.0f}".format(self.__x) + \
            ",Y:" + "{:.0f}".format(self.__y) + "}"
    
#绘制文本内容的函数
def print_text(font, x, y, text, color=(255,255,255)):
    imgText = font.render(text, True, color)
    screen.blit(imgText, (x,y))

#改变角度
def wrap_angle(angle):
    return angle % 360


pygame.init()								#初始化游戏
screen = pygame.display.set_mode((800,600))	#设置窗口大小
pygame.display.set_caption("Orbit Demo")	#设置标题
font = pygame.font.Font(None, 18)			#设置字体

#load bitmaps
space = pygame.image.load("space.png").convert_alpha()		#加载背景图片
planet = pygame.image.load("planet2.png").convert_alpha()	#加载地球图片
ship = pygame.image.load("freelance.png").convert_alpha()	#加载飞船图片
width,height = ship.get_size()								#获取飞船的宽度，高度
ship = pygame.transform.smoothscale(ship, (width//2, height//2))	#缩放飞船

radius = 250	#轨道的半径
angle = 0.0		#初始角度
pos = Point(0,0)	#记录飞船的位置	
old_pos = Point(0,0)

#repeating loop
while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            sys.exit()
    keys = pygame.key.get_pressed()
    if keys[K_ESCAPE]:
        sys.exit()

    #draw background
    screen.blit(space, (0,0))		#绘制背景

    #draw planet
    width,height = planet.get_size()	#绘制地球
    screen.blit(planet, (400-width/2,300-height/2))

    #move the ship	
    angle = wrap_angle(angle - 0.1)		#让飞船在圆周轨道上移动
    pos.x = math.sin( math.radians(angle) ) * radius
    pos.y = math.cos( math.radians(angle) ) * radius

    #rotate the ship
    delta_x = ( pos.x - old_pos.x )		#让飞船旋转
    delta_y = ( pos.y - old_pos.y )
    rangle = math.atan2(delta_y, delta_x)
    rangled = wrap_angle( -math.degrees(rangle) )
    scratch_ship = pygame.transform.rotate(ship, rangled)

    #draw the ship
    width,height = scratch_ship.get_size()
    x = 400+pos.x-width//2
    y = 300+pos.y-height//2
    screen.blit(scratch_ship, (x,y))

    print_text(font, 0, 0, "Orbit: " + "{:.0f}".format(angle))
    print_text(font, 0, 20, "Rotation: " + "{:.2f}".format(rangle))
    print_text(font, 0, 40, "Position: " + str(pos))
    print_text(font, 0, 60, "Old Pos: " + str(old_pos))
    
    pygame.display.update()
    
    #remember position
    old_pos.x = pos.x		#不断让坐标进行变化
    old_pos.y = pos.y
