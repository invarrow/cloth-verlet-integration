import pygame,random,math
pygame.init

def distance(p1,p2):
    x1,y1=p1[0],p1[1]
    x2,y2=p2[0],p2[1]
    d=math.sqrt((x1-x2)**2+(y1-y2)**2)
    return d
wdth,height=800,700
dis = pygame.display.set_mode((wdth,height))
pygame.display.set_caption('vertlet_integration')

black = 0,0,0
white = 25,250,100

clock = pygame.time.Clock()
verlet_on = True

points=[]
sticks=[]

threads=20
fixation_spacing=3
startx,starty=100,20
fixed = False
ycount=0
test_list =[]




for y in range(threads):
    xcount=0
    for x in range(threads):
        
        points.append([startx+xcount,starty+ycount,startx+xcount,starty+ycount,fixed])
        xcount+=int(10)
    
    ycount+=int(10)




bounce=0.9
gravity=2
friction=0.999
class verlet:
    def __init__(self,points,sticks):
        self.points = points 
        self.stick_lengths=[]
        self.sticks=self.getSticks()
    def getStick_lengths(self):
        count=0
        for i in range(len(self.points)):
            if i in [x for x in range(threads-1,len(self.points),threads)]:
                continue
            
            self.stick_lengths.append(distance(self.points[i],self.points[i+1]))
            count+=1
        print('this is a ',self.stick_lengths)
    def updatePoints(self):
        new_points=self.points
        for point in self.points:
            if not point[-1]:
                x,y=point[0],point[1]
                oldx,oldy=point[2],point[3]
                vx =(x-oldx)
                vy = (y-oldy)
                index = self.points.index(point)

                oldx=x
                oldy=y
                x+=vx
                y+=vy
                y+=int(gravity)
                
                new_points[index] = [x,y,oldx,oldy,point[-1]]

    def constrainPoints(self):
        new_points=self.points
        for point in self.points:
            
            if not point[-1]:
                x,y=point[0],point[1]
                oldx,oldy=point[2],point[3]
                vx =(x-oldx)
                vy = (y-oldy)
                index = self.points.index(point)

                if x>=wdth:
                    x=wdth-2
                    oldx=x+int(vx*bounce)
                if x<=0:
                    x=0
                    oldx=x+int(vx*bounce)
                if y>=height:
                    y=height-2
                    oldy=y+int(vy*bounce)
                if y<=0:
                    y=0
                    oldy=y+int(vy*bounce)
                new_points[index] = [x,y,oldx,oldy,point[-1]]
                

    
    def renderPoints(self):
        for point in self.points:
            pygame.draw.circle(dis,white,(int(point[0]),int(point[1])),5)

    def updateSticks(self):
        self.getSticks()       

        for stick in self.sticks:
            p0=stick[0]
            p1=stick[1]
            p0x,p0y=p0[0],p0[1]
            p1x,p1y=p1[0],p1[1]
            dx=p1x-p0x
            dy=p1y-p0y

            distance = math.sqrt((dx)**2+(dy)**2)
            
            difference=stick[2]-distance
            try:
                percent=difference/distance/2
            except ZeroDivisionError:
                pass
            
            offsetX=dx*percent
            offsetY=dy*percent

            index0=self.points.index(p0)
            index1=self.points.index(p1)

            if not points[index0][-1]:
                self.points[index0][0]-=offsetX
                self.points[index0][1]-=offsetY
            if not points[index1][-1]:
                self.points[index1][0]+=offsetX
                self.points[index1][1]+=offsetY

        
    def renderSticks(self):
        self.getSticks()
        
        for stick in self.sticks:
            p0=stick[0]
            p1=stick[1]
            p0x,p0y=p0[0],p0[1]
            p1x,p1y=p1[0],p1[1]
            pygame.draw.line(dis,white,(int(p0x),int(p0y)),(int(p1x),int(p1y)),2)
    def getSticks(self):
        self.sticks=[]
        
        
        count = 0
        for i in range(len(self.points)):
            

            if i not in range(len(self.points)-threads,len(self.points)):
                self.sticks.append([self.points[i],self.points[i+threads],5])
            if i not in [x for x in range(threads-1,len(self.points),threads)]:
                self.sticks.append([self.points[i],self.points[i+1],5])
            count+=1
        
        
        return self.sticks

point=verlet(points,sticks)
point.getStick_lengths
print(point.stick_lengths)
while verlet_on:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            verlet_on=False
            quit()
    
    
    dis.fill(black)
    mouse = pygame.mouse.get_pos()
    point.updatePoints()
    for i in range(3):
        
        point.constrainPoints()
        
        
        for i in range(0,threads,fixation_spacing):
            point.points[i][-1]=True
            
        point.updateSticks()
    point.constrainPoints()
    point.renderPoints()
    point.renderSticks()
  
    pygame.display.update()
    clock.tick(50)