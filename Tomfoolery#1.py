import pygame
import random
import math

#initializing game
pygame.init()
screen = pygame.display.set_mode((600, 600))
pygame.display.set_caption('Bouncing')
gameActive = True
gravity = 0.5
Xvelocity = 0
Yvelocity = 0
#colors
BLUE = (65,150,245)
WHITE = (255,255,255)
CLEAR = (0,0,0,0)
BLACK = (0,0,0)

borderWidth = 5
class circleSprite(pygame.sprite.Sprite):
    #constructer for circles
    def __init__(self, color, radius, position, hollow):
        super().__init__()
        self.image = pygame.Surface((2 * radius, 2 * radius), pygame.SRCALPHA)
        if hollow:
            pygame.draw.circle(self.image,color,(radius, radius), radius, borderWidth)
        else:
            pygame.draw.circle(self.image,color,(radius, radius), radius)
        self.rect = self.image.get_rect(center = position)
        self.radius = radius

#returns an array of all points around the circle
def getEdgePoints(center, radius, step=0.03):
    x_center, y_center = center
    points = []
    theta = 0
    while theta <= 2 * math.pi:
        x = radius * math.cos(theta)
        y = radius * math.sin(theta)
        points.append((round(x_center + x, 1), round(y_center + y, 1)))
        theta += step
    
    return points

def angleBetweenLines(center, collisionPt, previousPt):
    # Calculate the slopes of the lines formed by the pairs of points
    
    slope1 = (center[1] - collisionPt[1]) / (center[0] - collisionPt[0])
    slope2 = (previousPt[1] - collisionPt[1]) / (previousPt[0] - collisionPt[0])
    
    # Calculate the angle between the lines using arctan formula
    angleRadians = math.atan(abs((slope2 - slope1) / (1 + slope1 * slope2)))
    angleDegrees = math.degrees(angleRadians)
    
    return angleDegrees

center = (300, 300)
perimeterRadius = 200
ballRadius = 15
inboundsRadius = perimeterRadius - (ballRadius * 2) - borderWidth
lowestRand = center[0] - (inboundsRadius * math.sqrt(2))/2
highestRand = center[0] + (inboundsRadius * math.sqrt(2))/2
randomPosition = (random.uniform(lowestRand,highestRand), random.uniform(lowestRand,highestRand))

perimeterSprite = circleSprite(BLUE,perimeterRadius,center,True)
ballSprite = circleSprite(BLUE,ballRadius,randomPosition,False)
allSprites = pygame.sprite.Group(perimeterSprite, ballSprite)
edgePoints = getEdgePoints(center, perimeterRadius)
edgeCircles = pygame.sprite.Group()
for point in edgePoints:
    circleSprite(BLACK,1,point,False)
    edgeCircles.add(circleSprite(BLACK,1,point,False))

clock = pygame.time.Clock()

while gameActive:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        
    screen.fill(WHITE)
    previousPt = (ballSprite.rect.center)
    ballSprite.rect.y += Yvelocity
    ballSprite.rect.x += Xvelocity
    
    #collision detection
    if pygame.sprite.spritecollideany(ballSprite, edgeCircles):
        collidedSprite = pygame.sprite.spritecollideany(ballSprite, edgeCircles)
        collisionPt = collidedSprite.rect.center
        #print(collisionPt)

        pygame.draw.line(screen,BLACK,center,collisionPt)
        pygame.draw.line(screen,BLACK,collisionPt,previousPt)
        print(angleBetweenLines(center,collisionPt,previousPt))
        Xvelocity += random.uniform(-3,3)
        Yvelocity *= -1.1

    
    allSprites.draw(screen)
    #pygame.draw.circle(screen,BLACK,previousPt,4)
    Yvelocity += gravity
    pygame.display.flip()

    clock.tick(60)