import pygame
from random import randint
import math
from sklearn.cluster import KMeans
def distance (p1, p2):
    return math.sqrt((p1[0]-p2[0])*(p1[0]-p2[0]) + (p1[1]-p2[1])*(p1[1]-p2[1]))

pygame.init()
screen = pygame.display.set_mode((1200,700))
pygame.display.set_caption("Kmeans visualization")
running = True

clock = pygame.time.Clock()
BLACK= (0,0,0)
BACKGROUND_PANEL =(249,255,230)
RED = (255,0,0)
GREEN= (0,255,0)
BLUE =(0,0,255)
YELLOW =(147,153,35)
PURPLE = (255,0,255)
SKY = (0,255,255)
ORANGE = (255,125,25)
GRAPE = (100,25,125)
GRASS =( 55,155,65)



font = pygame.font.SysFont('sans',40)
fonts = pygame.font.SysFont('sans',20)
text_plus = font.render('+',True,(255,255,255))
text_sub = font.render('-',True,(255,255,255))
text_run = font.render('Run',True,(255,255,255))
text_random = font.render('Random', True,(255,255,255))
text_algo = font.render('Algorithm',True,(255,255,255))
text_Reset=font.render('Reset',True,(255,255,255))


K = 0 # number of cluster
errors = 0
points=[]
clusters =[]
labels=[]
COLORS=[RED,GREEN,BLUE,YELLOW,PURPLE,SKY,ORANGE,GRAPE,GRASS]

def run() :
    err = 0
    labels.clear()
    # assign color point to closet cluster
    for p in points:
        list_distance=[]
        for c in clusters:
            dis= distance(p,c)
            list_distance.append(dis)

        minDistance =  min(list_distance)
        label = list_distance.index(minDistance)
        labels.append(label)
    #update cluster
    for i in range(K):
        sum_x =0
        sum_y=0
        cnt=0
        for j in range(len(points)):
            if labels[j] ==i :
                cnt+=1
                sum_x += points[j][0]
                sum_y +=points[j][1]
        if cnt!=0:
            clusters[i][0]= sum_x/cnt
            clusters[i][1]= sum_y/cnt
        # print(clusters[i][0],clusters[i][1])
    for i in range(K):
        for j in range( len(points)):
            if labels[j] == i:
               dist = distance(points[j],clusters[i])
               err= err + dist
    return err




while running:
    clock.tick(60)
    screen.fill((214,214,214))
    mouse_x, mouse_y = pygame.mouse.get_pos()
    #draw UI
    #panel
    pygame.draw.rect(screen,BLACK,(50,50,700,500))# 50 50 diem bat dau , 700 chieu dai , 500 chieu rong
    pygame.draw.rect(screen,BACKGROUND_PANEL,(55,55,690,490))
    # K button +
    pygame.draw.rect(screen,BLACK,(850,50,50,50))
    screen.blit(text_plus ,(860,50))
    # K button -
    pygame.draw.rect(screen,BLACK,(950,50,50,50))
    screen.blit(text_sub,(960,50))
    # Run button
    pygame.draw.rect(screen,BLACK,(850, 150,150,50))
    screen.blit(text_run,(860,150))
    # Random Button
    pygame.draw.rect(screen,BLACK,(850,250,150,50))
    screen.blit(text_random,(860,250))
    # Algorithm button
    pygame.draw.rect(screen,BLACK,(850,400, 150,50))
    screen.blit(text_algo,(860,400))
    # reset button
    pygame.draw.rect(screen, BLACK,(850,500,150,50))
    screen.blit(text_Reset,(860,500))
    # draw K value
    text_K = font.render("K = "+ str(K),True,(0,0,0))
    screen.blit(text_K,(1050,50))
    # draw Error
    text_error = font.render("Error = " + str(errors),True,(0,0,0))
    screen.blit(text_error,(850,325))

    #draw mouse pos
    if 50 < mouse_x < 750 and 50 < mouse_y< 550 :
        text_mouse = fonts.render('('+str(mouse_x - 50)+','+str(mouse_y-50)+')',True, BLACK)
        screen.blit(text_mouse,(mouse_x + 10,mouse_y))
    #end draw UI
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running=False
        if event.type == pygame.MOUSEBUTTONDOWN :
            #draw point
            if 50 < mouse_x< 750 and 50 < mouse_y< 550 :
                labels=[]
                point = [mouse_x-50, mouse_y-50]
                points.append(point)
                errors=0
            # change K button +
            if 850 < mouse_x < 900 and 50 < mouse_y<100 :
                if K> 8 :
                    K=8
                else :
                    K= K+1
            # change K button -
            if 950 < mouse_x < 1000 and 50 < mouse_y<100:
                K= K-1
                if K < 0 :
                    K=0
            # Run button
            if 850 < mouse_x  < 850 + 150 and 150 < mouse_y<200:
                if K == 0 or len(clusters) ==0  or K != len(clusters):
                    continue
                else :
                    errors=  int(run())
            #random button
            if 850 < mouse_x < 850 + 150 and 250 < mouse_y < 300:
                clusters = []
                labels=[]
                errors=0
                for i in range(K):
                    random_points = [randint(0, 700), randint(0, 500)]
                    clusters.append(random_points)
            #algo button
            if 850 < mouse_x< 850 +150 and 400 < mouse_y<450:
               # print("alogo")
               try  :
                    kmeans = KMeans(n_clusters=K).fit(points)
                    clusters=kmeans.cluster_centers_
                    labels=kmeans.labels_
               except:
                    print("error")
            # reset button
            if 850 < mouse_x < 850 + 150 and 500 < mouse_y<550:
                K = 0  # number of cluster
                errors = 0
                points = []
                clusters = []
                labels = []

    # ve diem
    for i in range (len(points)):
        pygame.draw.circle(screen,BLACK,(points[i][0] + 50,points[i][1] + 50),6)
        if len(labels) == 0 :
            pygame.draw.circle(screen,(255,255,255),(points[i][0] + 50,points[i][1] + 50),5)
        else :
            pygame.draw.circle(screen,COLORS[labels[i]],(points[i][0] + 50,points[i][1] + 50),5)

    #random cluster
    for i in range(len(clusters)):
        pygame.draw.circle(screen,COLORS[i],(clusters[i][0] + 50,clusters[i][1] + 50 ),6)

    # draw label to point


    pygame.display.flip()
pygame.quit()