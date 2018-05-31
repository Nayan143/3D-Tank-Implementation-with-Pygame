import math
import random
import sys

import numpy
import pygame
from decimal import *
from OpenGL.GL import *
from OpenGL.GLU import *
from pygame.locals import *
from frange import *

class TankEngine:
    # size in pixel 
    window_size = w_width, w_height = 700, 700
    def init(size=window_size):
        #pygame.init()
        a=0
        # set screen
        #screen = pygame.display.set_mode(size, OPENGL|DOUBLEBUF)
         # set OpenGL clear color
        #glClearColor(0.0, 0.0, 0.0, 0.0)
        # enable the OpenGL 1depth test function
        #glDepthFunc(GL_LEQUAL)
        #glEnable(GL_DEPTH_TEST)
        #glShadeModel(GL_SMOOTH)
    def end():
        pygame.quit()      
    def keyboard_detection(pressed,player):
        change = False        
        speed_l,speed_r = 0,0

        if pressed[K_UP]:
            if (player._pos[1] + (math.cos(0.0174532925*player._heading)*player._speed)) <=-5: 
                player._pos[0] = player._pos[0] + (math.sin(0.0174532925*player._heading)*player._speed)
                player._pos[1] = player._pos[1] + (math.cos(0.0174532925*player._heading)*player._speed)
                change = True
                speed_l += player._speed
                speed_r += player._speed
            
            
        elif pressed[K_DOWN]:
            if (player._pos[1] + (math.cos(0.0174532925*player._heading)*player._speed)) <=-5:
                player._pos[0] = player._pos[0] - (math.sin(0.0174532925*player._heading)*player._speed)
                player._pos[1] = player._pos[1] - (math.cos(0.0174532925*player._heading)*player._speed)
                change = True
                speed_l -= player._speed
                speed_r -= player._speed
            
        if pressed[K_LEFT]:
            if player._heading <= 0:
                player._heading = 360
            else:
                player._heading -= 0.5
            change = True
            speed_l -= 0.05
            speed_r += 0.05
        elif pressed[K_RIGHT]:
            if player._heading >= 360:
                player._heading = 0
            else:
                player._heading += 0.5
            change = True
            speed_l += 0.05
            speed_r -= 0.05
        if change:
            player.rotate_wheel_left(speed_l)
            player.rotate_wheel_right(speed_r)

        if pressed[K_z]:
            if player.canon_angle <= 0:
                player.canon_angle = 0
            else:
                player.canon_angle -= 0.2
            change = True
        elif pressed[K_a]:
            if player.canon_angle >= 80:
                player.canon_angle = 80
            else:
                player.canon_angle += 0.2
            change = True
        elif pressed[K_g]:
            if player.pov_dist >= 10:
                player.pov_dist -= 0.2
            else:
                player.pov_dist = 10
        elif pressed[K_h]:
            if player.pov_dist <= 90:
                player.pov_dist += 0.2
            else:
                player.pov_dist = 90
        elif pressed[K_1]:
            player.perspective = 0
        elif pressed[K_2]:
            player.perspective = 1
        elif pressed[K_3]:
            player.perspective = 2
        elif pressed[K_4]:
            if player.perspective != 3:
                player.last_perspective = player.perspective   
                player.perspective = 3
        elif pressed[K_5]:
            player.perspective = 4  
        elif pressed[K_6]:
            player.perspective = 5
        elif pressed[K_7]:
            player.perspective = 6
        elif pressed[K_RETURN]:
            player.shoot(300)    
        #if  change == True:
            #print (player._pos, player._heading, player.canon_angle,(math.cos(player._heading*math.pi/180)),(math.sin(player._heading*math.pi/180)))  
    def set_perspective(player,enemy):
        # Modelview transformation
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()
        if player.perspective == 3: 
            if (player.cannonball._is_shooted == True) or (player.cannonball._is_exploded ==True):
                perspective = player.perspective
            else:
                perspective = player.last_perspective
        else:
            perspective = player.perspective   
        if perspective == 0:
                view_x = -(player.pov_dist*math.sin(player._heading*math.pi/180))+player._pos[0]
                view_y = -(player.pov_dist*math.cos(player._heading*math.pi/180))+player._pos[1]
                gluLookAt(view_x, view_y, player.pov_dist-30,
                    player._pos[0],player._pos[1],0,
                    0,0,1) 
        elif perspective == 5:
                view_x = -(player.pov_dist*math.cos(player._heading*math.pi/180))+player._pos[0]
                view_y = -(player.pov_dist*math.sin(player._heading*math.pi/180))+player._pos[1]
                gluLookAt(view_x, view_y, 10,
                    player._pos[0],player._pos[1],0,
                    0,0,1) 
        elif perspective == 6:
                view_x = -(player.pov_dist*math.cos(player._heading*math.pi/180))+player._pos[0]
                view_y = -(player.pov_dist*math.sin(player._heading*math.pi/180))+player._pos[1]
                gluLookAt(-view_x, view_y, 10,
                    player._pos[0],player._pos[1],0,
                    0,0,1) 
        elif perspective == 1:           
            if player._pos[0] - enemy._pos[0] == 0:
                theta = 0
            else:
                theta = math.atan2(player._pos[1] - enemy._pos[1],player._pos[0] - enemy._pos[0])
            
            eye_pos = [-player.pov_dist * math.sin(theta*math.pi/180)+enemy._pos[0],player.pov_dist * math.cos(theta*math.pi/180)+enemy._pos[1]]
            gluLookAt(eye_pos[0], eye_pos[1], 30,
                player._pos[0],player._pos[1],0,
                0,0,1)    
        elif perspective == 2:
            gluLookAt(0, 85, 120,
                enemy._pos[0],enemy._pos[1],0,
                0,0,1)     
        elif perspective == 3:
            gluLookAt(0, 85, 120,
                player.cannonball._pos[0],player.cannonball._pos[1],player.cannonball._pos[2],
                0,0,1)     
        elif perspective == 4:
            gluLookAt(0, 0, 235,
                0,0,0,
                0,1,0)   
    def run(size = window_size):
        pygame.init()
        width, height = 700,700
        black = 0, 0, 0
        white = 255, 255, 255
        # set screen
        screen = pygame.display.set_mode(size, OPENGL|DOUBLEBUF)

        # clock setup
        clock = pygame.time.Clock()

        # material setup
        mat_diffuse = [1.0, 1.0, 1.0, 1.0]
        mat_ambient = [0.2, 0.2, 0.2, 1.0]
        mat_specular = [1.0, 1.0, 1.0, 1.0]
        mat_shininess = [1.0]
        

        light1_position = [0.0, 0.0, 0.0, 0.0]
        light1_ambient = [  0.4, 0.4,0.4, 1.0]
        light1_diffuse = [0.4, 0.4, 0.4, 1.0]
        light1_specular = [1.0, 1.0, 1.0, 1.0]

        light2_position = [0.0, 0.0, 0.0, 0.0]
        light2_ambient = [  0, 0,0, 1.0]
        light2_diffuse = [0, 0.2, 0, 1.0]
        light2_specular = [0, 1.0, 0, 1.0]
        
       
        
        glMaterialfv(GL_FRONT, GL_AMBIENT_AND_DIFFUSE, mat_diffuse)
        glMaterialfv(GL_FRONT, GL_SPECULAR, mat_specular)
        glMaterialfv(GL_FRONT, GL_SHININESS, mat_shininess)

        # light0 setup battle field
        light_position = [0.0, 0.0, 0.0, 0.0]
        light_ambient = [  100, 100,100, 1.0]
        light_diffuse = [100.0, 100.0, 100.0, 1.0]
        light_specular = [1.0, 1.0, 1.0, 1.0]       
        glLightfv(GL_LIGHT0, GL_POSITION, light_position)
        glLightfv(GL_LIGHT0, GL_AMBIENT, light_ambient)
        glLightfv(GL_LIGHT0, GL_DIFFUSE, light_diffuse)
        glLightfv(GL_LIGHT0, GL_SPECULAR, light_specular)
        glLightf(GL_LIGHT0, GL_CONSTANT_ATTENUATION, 1.0)
        glLightf(GL_LIGHT0, GL_LINEAR_ATTENUATION, 0.05)
        glLightf(GL_LIGHT0, GL_QUADRATIC_ATTENUATION, 0.02)
        glEnable(GL_LIGHT0)

        # light1 setup cannon
        glLightfv(GL_LIGHT1, GL_POSITION, light1_position)
        glLightfv(GL_LIGHT1, GL_AMBIENT, light1_ambient)
        glLightfv(GL_LIGHT1, GL_DIFFUSE, light1_diffuse)
        glLightfv(GL_LIGHT1, GL_SPECULAR, light1_specular)
        glLightf(GL_LIGHT1, GL_CONSTANT_ATTENUATION, 0.3)
        glLightf(GL_LIGHT1, GL_LINEAR_ATTENUATION, 0)
        glLightf(GL_LIGHT1, GL_QUADRATIC_ATTENUATION, 0)
        #glEnable(GL_LIGHT1)
        
         # light2 setup
        glLightfv(GL_LIGHT2, GL_POSITION, [0,0,1,1])
        glLightfv(GL_LIGHT2, GL_AMBIENT, light2_ambient)
        glLightfv(GL_LIGHT2, GL_DIFFUSE, light2_diffuse)
        glLightfv(GL_LIGHT2, GL_SPECULAR, light2_specular)
        glLightf(GL_LIGHT2, GL_CONSTANT_ATTENUATION, 0.5)
        glLightf(GL_LIGHT2, GL_LINEAR_ATTENUATION, 0)
        glLightf(GL_LIGHT2, GL_QUADRATIC_ATTENUATION, 0)
        glEnable(GL_LIGHT2)

          # light4 setup
        glLightfv(GL_LIGHT4, GL_POSITION, [0,0,1,1])
        glLightfv(GL_LIGHT4, GL_AMBIENT, light2_ambient)
        glLightfv(GL_LIGHT4, GL_DIFFUSE, light2_diffuse)
        glLightfv(GL_LIGHT4, GL_SPECULAR, light2_specular)
        glLightf(GL_LIGHT4, GL_CONSTANT_ATTENUATION, 0.5)
        glLightf(GL_LIGHT4, GL_LINEAR_ATTENUATION, 0)
        glLightf(GL_LIGHT4, GL_QUADRATIC_ATTENUATION, 0)
        glEnable(GL_LIGHT4)

        light3_position = [0.0, 0 ,0, 0]
        light3_ambient =  [0.0, 0,0, 1.0]
        light3_diffuse =  [0.0, 25, 25, 1.0]
        light3_specular = [1.0, 1.0, 1.0, 1.0]
        #glDisable(GL_LIGHT3)
        glLightfv(GL_LIGHT3, GL_POSITION, light3_position)
        glLightfv(GL_LIGHT3, GL_AMBIENT, light3_ambient)
        glLightfv(GL_LIGHT3, GL_DIFFUSE, light3_diffuse)
        glLightfv(GL_LIGHT3, GL_SPECULAR, light3_specular)
        glLightf(GL_LIGHT3, GL_CONSTANT_ATTENUATION, 10)
        glLightf(GL_LIGHT3, GL_LINEAR_ATTENUATION, 0)
        glLightf(GL_LIGHT3, GL_QUADRATIC_ATTENUATION, 0)
        
        glEnable(GL_LIGHT3)
        
        glEnable(GL_LIGHTING)

        # set OpenGL clear color
        glClearColor(0.0, 0.0, 0.0, 0.0)

        # set viewport and perspective projection 
        glViewport(0, 0, 700, height)
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        gluPerspective(65, float(width)/float(height), 1, 1000)
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()

        # enable the OpenGL depth test function
        glDepthFunc(GL_LESS)
        glEnable(GL_DEPTH_TEST)

        # antialiasing
        glHint(GL_POLYGON_SMOOTH_HINT, GL_NICEST)

        # shade model setup
        glShadeModel(GL_SMOOTH)

        flag = 1
        angle = 0
        cam_ang = 180
        cam_pos = [0,15,20]
        #spawn player
        player = Tank()
        player.set_position([0,-75,0])
        glEnable(GL_COLOR_MATERIAL)
        #spawn enemy
        enemy_color = TankColorPalette(TankColorPalette.cyan,TankColorPalette.pink,TankColorPalette.yellow)
        enemy = Enemy(enemy_color)
        while flag:
            # set FPS
            clock.tick(60)

            for event in pygame.event.get():
                # QUIT
                if event.type == pygame.QUIT:
                    flag = 0
                # exit with escape
                if event.type == pygame.KEYUP and event.key == pygame.K_ESCAPE:
                    flag = 0

            # process keyboard input
            TankEngine.keyboard_detection(pygame.key.get_pressed(),player)
            
            
            glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        
            # Update perspective
            TankEngine.set_perspective(player,enemy)


            # reposition the light
            light_position = [0, -75, 100, 1.0] # 0=dir, 1=pos
            light_spot_dir = [0, 0, -1]
            light_spot_exp = [50]
            light_spot_cutoff = [90]
            
            glLightfv(GL_LIGHT2, GL_POSITION, [-75,10,1,1])
            glLightfv(GL_LIGHT4, GL_POSITION, [75,10,1,1])
            
            glLightfv(GL_LIGHT0, GL_POSITION, light_position)
            glLightfv(GL_LIGHT0, GL_SPOT_CUTOFF, light_spot_cutoff)
            glLightfv(GL_LIGHT0, GL_SPOT_DIRECTION, light_spot_dir)
            glLightfv(GL_LIGHT0, GL_SPOT_EXPONENT, light_spot_exp)

            light3_position = [0.0, 85, 100, 1.0]
            light3_ambient =  [0.0, 0,0, 1.0]
            light3_diffuse =  [0.0, 250, 250, 1.0]
            light3_specular = [1.0, 1, 1, 1.0]
            #glDisable(GL_LIGHT3)
           
            light3_spot_dir = [0, 0, -1]
            light3_spot_exp = [50]
            light3_spot_cutoff = [90]
            glLightfv(GL_LIGHT3, GL_POSITION, light3_position)
            glLightfv(GL_LIGHT3, GL_SPOT_CUTOFF, light3_spot_cutoff)
            glLightfv(GL_LIGHT3, GL_SPOT_DIRECTION, light3_spot_dir)
            glLightfv(GL_LIGHT3, GL_SPOT_EXPONENT, light3_spot_exp)
          
            # # draw lightbulb
            # glPushMatrix()
            # glTranslate(light_position[0],light_position[1],light_position[2])
            # # draw one at a new location
            # lightbulb = gluNewQuadric()
            # glMaterialfv(GL_FRONT, GL_EMISSION, light_diffuse)
            # gluSphere(lightbulb, 0.25, 25, 25)
            # glMaterialfv(GL_FRONT, GL_EMISSION, [0,0,0,1])
            # glPopMatrix()

           
            # transform the model (coordinate)
        
            
            BattleField.draw()     
            is_enemy_hitted = player.draw(enemy._pos) 
            if is_enemy_hitted:
                enemy.change_color()
            enemy.update_pos()
            enemy.draw()
            


            glFlush()

            pygame.display.flip()
            
class TankColorPalette:
    black = 0, 0, 0
    white = 1, 1, 1
    blue = 0,0,1
    red = 1,0,0
    green = 0,1,0
    pink = 1,0,1
    cyan = 0,1,1
    yellow = 1,1,0
    def __init__(self,def_cannon=green,def_body=blue,def_cannon_base=red):
        self.cannon = def_cannon
        self.cannon_base = def_cannon_base
        self.body = def_body
        self.list = [self.cannon,self.cannon_base,self.body]
    def update_color(self):
        self.cannon = self.list[0]
        self.cannon_base = self.list[1]
        self.body = self.list[2]

class BattleField:
     # draw ground
    ground_size = 300
    ground_gridsize = int(ground_size/10) # min=1
    ground_grids = (ground_size/ground_gridsize)+1
    building_width = 20
    # material setup
    mat_diffuse = [1.0, 1.0, 1.0, 1.0]
    mat_ambient = [0.2, 0.2, 0.2, 1.0]
    mat_specular = [1.0, 1.0, 1.0, 1.0]
    mat_shininess = [1.0]
    building = [[-building_width, -building_width, 0.0],    # bottom face
                [building_width, -building_width, 0.0],
                [building_width, building_width, 0.0],
                [-building_width, building_width, 0.0],
                [-building_width, -building_width, 50],    # top face
                [-building_width, building_width, 50],
                [building_width, building_width, 50],
                [building_width, -building_width, 50],
                [-building_width, -building_width, 0.0],    # left face
                [-building_width, -building_width, 50],
                [-building_width, building_width, 50],
                [-building_width, building_width, 0.0],
                [building_width, -building_width, 0.0],    # right face
                [building_width, -building_width, 50],
                [building_width, building_width, 50],
                [building_width, building_width, 0.0],
                [-building_width, building_width, 0.0],    # front face
                [-building_width, building_width, 50],
                [building_width, building_width, 50],
                [building_width, building_width, 0.0],
                [-building_width, -building_width, 0.0],    # back face
                [-building_width, -building_width, 50],
                [building_width, -building_width, 50],
                [building_width, -building_width, 0.0]]
    field_img = pygame.image.load('spaceship_texture_300px.png')
    field_img_py = pygame.image.tostring(field_img, "RGB", 1) # Flip image for OpenGL. See pygame doc.
    acid_img = pygame.image.load('acid_texture_300px.png')
    acid_img_py = pygame.image.tostring(acid_img, "RGB", 1) # Flip image for OpenGL. See pygame doc.
    building_img = pygame.image.load('building_texture.png')
    building_img_py = pygame.image.tostring(building_img, "RGB", 1) # Flip image for OpenGL. See pygame doc.


    def draw():
        
        # material setup
        mat_zero = [0.0, 0.0, 0.0, 1.0]
        mat_diffuse_white = [1.0, 1.0, 1.0, 1.0]
        mat_diffuse_red = [1.0, 0.0, 0.0, 1.0]
        mat_diffuse_green = [0.0, 1.0, 0.0, 1.0]
        mat_diffuse_blue = [0.0, 0.0, 1.0, 1.0]
        mat_ambient_white = [1.0, 1.0, 1.0, 1.0]
        mat_ambient_red = [1.0, 0.0, 0.0, 1.0]
        mat_specular = [1.0, 1.0, 1.0, 1.0]
        mat_no_shininess = [0.0]
        mat_low_shininess = [10.0]
        mat_high_shininess = [100.0]
        mat_emission = [0.0, 0.0, 0.1, 0.0]
        
        # load Texture
        glTexImage2D(GL_TEXTURE_2D,
                       0,   # level
                       3,   # components (3 for RGB)
                       BattleField.field_img.get_width(),  # width
                       BattleField.field_img.get_height(),  # height
                       0,   #border
                       GL_RGB, # format
                       GL_UNSIGNED_BYTE,  # type
                       BattleField.field_img_py)
        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST) # GL_LINEAR
        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)

        ## Battle Field
        # set material properties
        glMaterialfv(GL_FRONT_AND_BACK, GL_AMBIENT, mat_zero)
        glMaterialfv(GL_FRONT_AND_BACK, GL_DIFFUSE, mat_diffuse_blue)
        glMaterialfv(GL_FRONT_AND_BACK, GL_SPECULAR, mat_zero)
        glMaterialfv(GL_FRONT_AND_BACK, GL_SHININESS, mat_no_shininess)
        glMaterialfv(GL_FRONT_AND_BACK, GL_EMISSION, mat_zero)
        
        glPolygonMode(GL_FRONT_AND_BACK, GL_FILL) # POINT, LINE, FILL
        glPushMatrix()
        glTranslate(-BattleField.ground_gridsize/2,BattleField.ground_gridsize/2,0)
        glEnable(GL_TEXTURE_2D)
        for i in range(int(-BattleField.ground_size/2)+int(BattleField.ground_gridsize/2), int(BattleField.ground_size/2), BattleField.ground_gridsize):
            for j in range (int(-BattleField.ground_size/2)+int(BattleField.ground_gridsize/2), int(BattleField.ground_size/2), BattleField.ground_gridsize):
                glPushMatrix()
                glTranslate(i,j,0)
                glBegin(GL_QUADS)
                glColor3f(0.5, 0.5, 0.5)
                glNormal3d(0, 0, 1)
                glTexCoord2f(0, 0)
                glVertex3f(0, 0, 0)
                glNormal3d(0, 0, 1)
                glTexCoord2f(1, 0)
                glVertex3f(BattleField.ground_gridsize, 0, 0)
                glNormal3d(0, 0, 1)
                glTexCoord2f(1, 1)
                glVertex3f(BattleField.ground_gridsize, -BattleField.ground_gridsize, 0)              
                glNormal3d(0, 0, 1)
                glTexCoord2f(0, 1)
                glVertex3f(0, -BattleField.ground_gridsize, 0)
                glEnd()
                glPopMatrix()
        glPopMatrix()
        glDisable(GL_TEXTURE_2D)
        
        
        
        
        ## River
        # load texture
        glTexImage2D(GL_TEXTURE_2D,
                       0,   # level
                       3,   # components (3 for RGB)
                       BattleField.acid_img.get_width(),  # width
                       BattleField.acid_img.get_height(),  # height
                       0,   #border
                       GL_RGB, # format
                       GL_UNSIGNED_BYTE,  # type
                       BattleField.acid_img_py)
        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST) # GL_LINEAR
        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)
        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)
        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)

        # set material properties
        glMaterialfv(GL_FRONT_AND_BACK, GL_AMBIENT, mat_zero)
        glMaterialfv(GL_FRONT_AND_BACK, GL_DIFFUSE, mat_diffuse_red)
        glMaterialfv(GL_FRONT_AND_BACK, GL_SPECULAR, mat_specular)
        glMaterialfv(GL_FRONT_AND_BACK, GL_SHININESS, mat_high_shininess)
        glMaterialfv(GL_FRONT_AND_BACK, GL_EMISSION, [0,0.5,0,1])
        # draw      
        glEnable(GL_TEXTURE_2D)
        glPushMatrix()
        glTranslate(-BattleField.ground_gridsize/2,0,0)
        gridsize = 2
        tilesize = 20 / gridsize
        for j in range(0,gridsize):
            for i in range(int(-BattleField.ground_size/2)+int(BattleField.ground_gridsize/2), int(BattleField.ground_size/2), BattleField.ground_gridsize):
                glPushMatrix()
                glTranslate(i,j*tilesize,0.5)
                glColor3f(0.5, 0.5, 0.5)
                glBegin(GL_QUADS)           
                glTexCoord2f(0, 0)
                glNormal3d(0, 0,1)
                glVertex3f(0, 0, 0)              
                glTexCoord2f(1, 0)
                glNormal3d(0, 0,1)
                glVertex3f(0, 20/gridsize, 0)              
                glTexCoord2f(1, 1)
                glNormal3d(0, 0,1)
                glVertex3f(BattleField.ground_gridsize, 20/gridsize, 0)          
                glTexCoord2f(0, 1)
                glNormal3d(0,0,1)
                glVertex3f(BattleField.ground_gridsize, 0, 0)           
                glEnd()
                glPopMatrix()
        glPopMatrix()
        glDisable(GL_TEXTURE_2D)
        

        ## building
        # load texture
        glTexImage2D(GL_TEXTURE_2D,
                       0,   # level
                       3,   # components (3 for RGB)
                       BattleField.building_img.get_width(),  # width
                       BattleField.building_img.get_height(),  # height
                       0,   #border
                       GL_RGB, # format
                       GL_UNSIGNED_BYTE,  # type
                       BattleField.building_img_py)
        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST) # GL_LINEAR
        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)
        
        # set material properties
        glMaterialfv(GL_FRONT_AND_BACK, GL_AMBIENT, mat_zero)
        glMaterialfv(GL_FRONT_AND_BACK, GL_DIFFUSE, mat_zero)
        glMaterialfv(GL_FRONT_AND_BACK, GL_SPECULAR, mat_zero)
        glMaterialfv(GL_FRONT_AND_BACK, GL_SHININESS, mat_zero)
        glMaterialfv(GL_FRONT_AND_BACK, GL_EMISSION, [0,1,1,1])
        glPolygonMode(GL_FRONT, GL_FILL) # POINT, LINE, FILL
        
        glPushMatrix()
        glTranslate(0,85,0)
    
        glEnable(GL_TEXTURE_2D)
        glNormal3d(0, 0, 1)
        for i in range(6):
            glColor3f(0.0, 1, 1)
            glBegin(GL_QUADS)
            
            glTexCoord2f(0, 0)
            glVertex3f(BattleField.building[i*4][0], BattleField.building[i*4][1], BattleField.building[i*4][2]+0.1)
            glTexCoord2f(1, 0)
            glVertex3f(BattleField.building[(i*4)+1][0], BattleField.building[(i*4)+1][1], BattleField.building[(i*4)+1][2]+0.1)
            glTexCoord2f(1, 1)
            glVertex3f(BattleField.building[(i*4)+2][0], BattleField.building[(i*4)+2][1], BattleField.building[(i*4)+2][2]+0.1)
            glTexCoord2f(0, 1)      
            glVertex3f(BattleField.building[(i*4)+3][0], BattleField.building[(i*4)+3][1], BattleField.building[(i*4)+3][2]+0.1)
            glEnd()
        glPopMatrix()
        glDisable(GL_TEXTURE_2D)

class Enemy:
    sphere = gluNewQuadric()
    cylinder = gluNewQuadric()
    disk = gluNewQuadric()
    color_set = TankColorPalette()

    def __init__(self,color=color_set):

        self.y_magnitude = 1.5
        self.x_magnitude = math.pow(3,2)
        self.heading_flag = False
        self.sine_engine = 0
        self.pov_dist = 80
        self.color_set = color
        self.canon_base =  [0,0,5]
        self.canon_base_radius = 2.5
        self.canon_radius = 1
        self.canon_angle = 15
        self.canon_length = 10
        self.last_pos = [1,0]
        self.last_slope = 0
        self.last_heading = 0
        self.left_wheel_rotation = 0
        self.right_wheel_rotation = 0
        
        self._pos = [0,0,0]
        self._last_pos = [0,0,0]
        
        self._heading = 0
        self._speed = 0.5
        self._body = [[-5, -5, 0.0],    # bottom face
                [-5, 5, 0.0],
                [5, 5, 0.0],
                [5, -5, 0.0],
                [-5, -5, 5],    # top face
                [-5, 5, 5],
                [5, 5, 5],
                [5, -5, 5],
                [-5, -5, 0.0],    # left face
                [-5, -5, 5],
                [-5, 5, 5],
                [-5, 5, 0.0],
                [5, -5, 0.0],    # right face
                [5, -5, 5],
                [5, 5, 5],
                [5, 5, 0.0],
                [-5, 5, 0.0],    # front face
                [-5, 5, 5],
                [5, 5, 5],
                [5, 5, 0.0],
                [-5, -5, 0.0],    # back face
                [-5, -5, 5],
                [5, -5, 5],
                [5, -5, 0.0]]
    def rotate_wheel_left(self,distance):
        angle = (distance / (math.pi*5))*360
        self.left_wheel_rotation += angle 
        if self.left_wheel_rotation >= 360:
            self.left_wheel_rotation = self.left_wheel_rotation - (360*int(self.left_wheel_rotation/360))
        elif self.left_wheel_rotation < 0:
            self.left_wheel_rotation = self.left_wheel_rotation + 360 

    def rotate_wheel_right(self,distance):
        angle = (distance / (math.pi*5))*360
        self.right_wheel_rotation += angle 
        if self.right_wheel_rotation >= 360:
            self.right_wheel_rotation = self.right_wheel_rotation - (360*int(self.right_wheel_rotation/360))
        elif self.right_wheel_rotation < 0:
            self.right_wheel_rotation = self.right_wheel_rotation + 360 

    
    def update_pos(self):
        #update sine engine
        self.sine_engine += self._speed
        if self.sine_engine >= 360:
            self.sine_engine = 0
        
        #update current position from sine engine
        current_pos = [0,self.y_magnitude*math.sin(0.0174532925*self.sine_engine)]
        
        # from elclip formular (x^2/a^2) + (y^2/b^2) = 1 , update relative position base on y postion
        a2 = self.x_magnitude
        b2 = self.y_magnitude
        y2 = math.pow(current_pos[1],2)       
        if current_pos[1] - self.last_pos[1] > 0:
            current_pos[0] =  math.sqrt(a2*(self.y_magnitude-(y2/b2)))
        else:
            current_pos[0] = -math.sqrt(a2*(self.y_magnitude-(y2/b2)))             
        
        #find current heading from slope of 2 point 
        if (current_pos[0] - self.last_pos[0]) != 0:
            slope = (self.last_pos[1] - current_pos[1])/(self.last_pos[0] - current_pos[0])
        else:
            slope = self.last_slope
        self.last_slope = slope
        
        # heading correction, since heading value is in range [-90..90], remaping to [0..360]
        heading =  (math.atan(slope)*(180/math.pi)) + 90
        if abs(heading - self.last_heading) > 300:
            self.heading_flag = False
        elif abs(heading - self.last_heading) > 150:
            self.heading_flag = True      
        if self.heading_flag == True:
            heading = heading+180
        
        # update reference paramater
        self.last_heading = heading 
        self.last_pos = current_pos

        # update heading and position
        self.set_heading(-heading)
        self._pos[0] = 30*current_pos[0]
        self._pos[1] = 85+30*current_pos[1]        
        # rolling speed 
        spd_x = abs(self._pos[0]-self._last_pos[0])
        spd_y = abs(self._pos[1]-self._last_pos[1])
        spd = math.sqrt(math.pow(spd_x,2)+math.pow(spd_y,2))
        angle = math.atan2(self._pos[1]-self._last_pos[1],self._pos[0]-self._last_pos[0]) * 180/math.pi
        #print(self._heading,angle,spd_x,spd_y)
       
        self._last_pos[0] = self._pos[0]
        self._last_pos[1] = self._pos[1]
        
        if spd_x >= spd_y:
            self.rotate_wheel_left(spd_y)
            self.rotate_wheel_right(spd_x)
        else:
            self.rotate_wheel_left(spd_x)
            self.rotate_wheel_right(spd_y)
        

    def set_position(self,pos):
        self._pos = pos
    def set_heading(self,heading):
        self._heading = heading
    def set_color(self,color,mode=False):
        if mode == False:
            glColor3f(color[0], color[1], color[2])
        else:
            glColor4f(color[0], color[1], color[2], 0.0)
    def change_color(self):
        print(len(self.color_set.list))
        for i in range(0,len(self.color_set.list)):
            r = random.uniform(0.0, 1.0)
            g = random.uniform(0.0, 1.0)
            b = random.uniform(0.0, 1.0)
            self.color_set.list[i] = [r,g,b]
        self.color_set.update_color()
    def draw(self):
        # material setting
        mat_zero = [0.0, 0.0, 0.0, 1.0]
        mat_diffuse_white = [1.0, 1.0, 1.0, 1.0]
        mat_diffuse_red = [1.0, 0.0, 0.0, 1.0]
        mat_diffuse_green = [0.0, 1.0, 0.0, 1.0]
        mat_diffuse_blue = [0.0, 0.0, 1.0, 1.0]
        mat_ambient_white = [1.0, 1.0, 1.0, 1.0]
        mat_ambient_red = [1.0, 0.0, 0.0, 1.0]
        mat_specular = [1.0, 1.0, 1.0, 1.0]
        mat_no_shininess = [0.0]
        mat_low_shininess = [10.0]
        mat_high_shininess = [100.0]
        mat_emission = [0.0, 0.0, 0.1, 0.0]
        mat_emission_green = [0.0, 0.5, 0.0, 0.0]
        mat_emission_red = [0.5, 0.0, 0.0, 0.0]

       
        glPushMatrix()
        glTranslatef(self._pos[0], self._pos[1], self._pos[2])
        
        ## rotating signboard
        # set material
        glMaterialfv(GL_FRONT_AND_BACK, GL_AMBIENT, mat_zero)
        glMaterialfv(GL_FRONT_AND_BACK, GL_DIFFUSE, mat_diffuse_white)
        glMaterialfv(GL_FRONT_AND_BACK, GL_SPECULAR, mat_zero)
        glMaterialfv(GL_FRONT_AND_BACK, GL_SHININESS, mat_low_shininess)
        glMaterialfv(GL_FRONT_AND_BACK, GL_EMISSION, mat_zero)
        glPushMatrix()
        glTranslatef(0,0, 8)
        self.set_color(self.color_set.white)
        glPolygonMode(GL_FRONT, GL_FILL)
        self.draw_unit_quad_horizontal(5,1,0,1)
        self.draw_unit_quad_horizontal(5,1,5,1)
        self.draw_unit_quad_vertical(1,5,2.5,'right')
        self.draw_unit_quad_vertical(1,5,-2.5,'left')
        self.draw_unit_quad_vertical(5,5,-0.5,'rear')        
        self.draw_unit_quad_vertical(5,5,0.5,'front')
        glPopMatrix()
        
        glRotate(-self._heading, 0, 0, 1)
        
        ## signboard base 
        # set material
        glMaterialfv(GL_FRONT_AND_BACK, GL_AMBIENT, mat_zero)
        glMaterialfv(GL_FRONT_AND_BACK, GL_DIFFUSE, mat_diffuse_white)
        glMaterialfv(GL_FRONT_AND_BACK, GL_SPECULAR, mat_zero)
        glMaterialfv(GL_FRONT_AND_BACK, GL_SHININESS, mat_low_shininess)
        glMaterialfv(GL_FRONT_AND_BACK, GL_EMISSION, mat_zero)
        # draw 
        glPolygonMode(GL_FRONT_AND_BACK, GL_FILL) # POINT, LINE, FILL
        self.set_color(self.color_set.cannon_base,True)
        glPushMatrix()
        glTranslatef(self.canon_base[0], self.canon_base[1], self.canon_base[2]) # translate to canon base location
        gluSphere(Enemy.sphere, self.canon_base_radius, 25, 25)
        glPopMatrix()
        
        ## Both wheel
        #set material
        glMaterialfv(GL_FRONT_AND_BACK, GL_AMBIENT, mat_zero)
        glMaterialfv(GL_FRONT_AND_BACK, GL_DIFFUSE, mat_diffuse_white)
        glMaterialfv(GL_FRONT_AND_BACK, GL_SPECULAR, mat_zero)
        glMaterialfv(GL_FRONT_AND_BACK, GL_SHININESS, mat_low_shininess)
        glMaterialfv(GL_FRONT_AND_BACK, GL_EMISSION, mat_zero)
        glPushMatrix()
        glTranslatef(-7, 0, 5) 
        glRotate(90,0, 1, 0)   
        glRotate(-self.left_wheel_rotation,0, 0, 1)      
        self.set_color(self.color_set.black)
        gluCylinder(Enemy.cylinder, 5, 5, 2, 10, 10)
        self.set_color(self.color_set.cannon)
        glNormal3d(-1,0, 0)
        gluDisk(Enemy.disk,0,5,10,10)
        glPopMatrix()

        glPushMatrix()
        glTranslatef(5, 0, 5) # translate the canon
        glRotate(90,0, 1, 0)  # rotate (tilt) the canon         
        glRotate(-self.right_wheel_rotation,0, 0, 1)  # rotate (tilt) the canon       
        self.set_color(self.color_set.black)
        gluCylinder(Enemy.cylinder, 5, 5, 2, 10, 10)
        self.set_color(self.color_set.cannon)
        glTranslatef(0, 0, 2) # translate the canon
        glNormal3d(1,0, 0)
        gluDisk(Enemy.disk,0,5,10,10)
        glPopMatrix()
        
        ## Body
        # set material
        glMaterialfv(GL_FRONT_AND_BACK, GL_AMBIENT, mat_zero)
        glMaterialfv(GL_FRONT_AND_BACK, GL_DIFFUSE, mat_diffuse_white)
        glMaterialfv(GL_FRONT_AND_BACK, GL_SPECULAR, mat_zero)
        glMaterialfv(GL_FRONT_AND_BACK, GL_SHININESS, mat_low_shininess)
        glMaterialfv(GL_FRONT_AND_BACK, GL_EMISSION, mat_zero)
        glTranslatef(0, 0, 2.5) # translate the canon
        self.set_color(self.color_set.body)
        glPolygonMode(GL_FRONT, GL_FILL)
        self.draw_unit_quad_horizontal(10,15,5,1)
        self.draw_unit_quad_horizontal(10,15,5,1)
        self.draw_unit_quad_vertical(15,5,5,'right')
        self.draw_unit_quad_vertical(15,5,-5,'left')
        self.draw_unit_quad_vertical(10,5,-5,'rear')        
        self.draw_unit_quad_vertical(10,5,5,'front')
        glPopMatrix()
    
    def draw_unit_quad_horizontal(self,quad_size_w,quad_size_l,height,gridsize):
        #gridsize = 1
        for i in frange((-quad_size_w/2), (quad_size_w/2)-(gridsize/2), gridsize):
            for j in frange((-quad_size_l/2), (quad_size_l/2)-(gridsize/2), gridsize):
                glPushMatrix()
                glTranslate(i,j,0)
                glBegin(GL_QUADS)
                glNormal3d(0, 0, 1)
                glVertex3f(0, 0, height)
                glNormal3d(0, 0, 1)
                glVertex3f(gridsize, 0, height)
                glNormal3d(0, 0, 1)
                glVertex3f(gridsize, gridsize, height)
                glNormal3d(0, 0, 1)
                glVertex3f(0, gridsize, height)
                glEnd()
                glPopMatrix()
    
    def draw_unit_quad_vertical(self,quad_size_w,quad_size_l,shift,side):
        gridsize = 1
        if side == 'left':
            for i in frange((-quad_size_w/2), (quad_size_w/2)-(gridsize/2), gridsize):
                for j in frange(0, quad_size_l-(gridsize/2), gridsize):
                    glPushMatrix()
                    glTranslate(0,i,j)
                    glBegin(GL_QUADS)
                    glNormal3d(-1,0, 0)
                    glVertex3f(shift, 0, 0)
                    glNormal3d(-1,0, 0)
                    glVertex3f(shift, gridsize, 0)
                    glNormal3d(-1,0, 0)
                    glVertex3f(shift,gridsize, gridsize)
                    glNormal3d(-1,0, 0)
                    glVertex3f(shift, 0, gridsize)
                    glEnd()
                    glPopMatrix()
        if side == 'right':
            for i in frange((-quad_size_w/2), (quad_size_w/2)-(gridsize/2), gridsize):
                for j in frange(0, quad_size_l-(gridsize/2), gridsize):
                    glPushMatrix()
                    glTranslate(0,i,j)
                    glBegin(GL_QUADS)
                    glNormal3d(1,0, 0)
                    glVertex3f(shift, 0, 0)
                    glNormal3d(1,0, 0)
                    glVertex3f(shift, gridsize, 0)
                    glNormal3d(1,0, 0)
                    glVertex3f(shift,gridsize, gridsize)
                    glNormal3d(1,0, 0)
                    glVertex3f(shift, 0, gridsize)
                    glEnd()
                    glPopMatrix()
        elif side == 'front':
            for i in frange((-quad_size_w/2), (quad_size_w/2)-(gridsize/2), gridsize):
                for j in frange(0, quad_size_l-(gridsize/2), gridsize):
                    glPushMatrix()
                    glTranslate(i,0,j)
                    glBegin(GL_QUADS)
                    glNormal3d(0, 1, 0)
                    glVertex3f( 0,shift, 0)
                    glNormal3d(0, 1, 0)
                    glVertex3f( gridsize,shift, 0)
                    glNormal3d(0, 1, 0)
                    glVertex3f(gridsize,shift, gridsize)
                    glNormal3d(0, 1, 0)
                    glVertex3f( 0,shift, gridsize)
                    glEnd()
                    glPopMatrix()
        elif side == 'rear':
            for i in frange((-quad_size_w/2), (quad_size_w/2)-(gridsize/2), gridsize):
                for j in frange(0, quad_size_l-(gridsize/2), gridsize):
                    glPushMatrix()
                    glTranslate(i,0,j)
                    glBegin(GL_QUADS)
                    glNormal3d(0, -1, 0)
                    glVertex3f( 0,shift, 0)
                    glNormal3d(0, -1, 0)
                    glVertex3f( gridsize,shift, 0)
                    glNormal3d(0, -1, 0)
                    glVertex3f(gridsize,shift, gridsize)
                    glNormal3d(0, -1, 0)
                    glVertex3f( 0,shift, gridsize)
                    glEnd()
                    glPopMatrix()

class Tank:
    default_canon_base = [0,0,5]
    sphere = gluNewQuadric()
    cylinder = gluNewQuadric()
    disk = gluNewQuadric()
    color_set = TankColorPalette()
    perspective = 0
    last_perspective = 0
    def __init__(self,color=color_set):
        self.pov_dist = 80
        self.color_set = color
        self.canon_base = Tank.default_canon_base
        self.canon_base_radius = 3
        self.canon_radius = 0.9
        self.canon_angle = 15
        self.cannonball = CannonBall()
        self.canon_length = 10
        self._pos = [0,0,0]
        self._upper = False
        self._track_left = []
        self._track_right = []
        self._track_count = 1
        self.cannonball._dispersed_frame = 0
        ang = int(360/self._track_count)
       # self._track.append(TrackWheel(ang * 2,0))
        #self._track.append(TrackWheel(ang * 5,0))
        
        for i in range(0,self._track_count):
            self._track_left.append(TrackWheel(ang * 2,0))
            self._track_right.append(TrackWheel(ang * 2,0))
            
            for j in range(0,len(self._track_left)):
                self._track_left[i].rotate_wheel(1)
                self._track_right[i].rotate_wheel(1)

        for i in range(0,50):
            for j in range(0,len(self._track_left)):
                self._track_left[j].rotate_wheel(0.2)    
                self._track_right[j].rotate_wheel(0.2)  
        # self._track.append(TrackWheel(ang * 2,1))
        # self._track.append(TrackWheel(ang * 2,2))
        # self._track.append(TrackWhbeel(ang * 2,3))
        # self._track.append(TrackWheel(ang * 2,4))
        # self._track.append(TrackWheel(ang * 2,5))
        # self._track.append(TrackWheel(ang * 2,6))
        # self._track.append(TrackWheel(ang * 2,7))
        # self._track.append(TrackWheel(ang * 2,8))
        
        # self._track.append(TrackWheel(ang * 7,4))
        # self._track.append(TrackWheel(ang * 8,3))
        # self._track.append(TrackWheel(ang * 9,2))
        # self._track.append(TrackWheel(ang * 10,1))
        # self._track.append(TrackWheel(ang * 11,0))
        
        self._track_count = len(self._track_left)
            #self._track.append(TrackWheel(270))
        #self._track[i].rotate_wheel(0)
        self._heading = 0
        self._speed = 0.2
        self.is_cannon_shooted = False
        self._body_w = 3
        self._body_h = 4.5
        self._body_l = 5
        self._body = [[-self._body_w, -self._body_l, 0.0],    # bottom face
                [-self._body_w, self._body_l, 0.0],
                [self._body_w, self._body_l, 0.0],
                [self._body_w, -self._body_l, 0.0],
                [-self._body_w, -self._body_l, self._body_h],    # top face
                [-self._body_w, self._body_l, self._body_h],
                [self._body_w, self._body_l, self._body_h],
                [self._body_w, -self._body_l, self._body_h],
                [-self._body_w, -self._body_l, 0.0],    # left face
                [-self._body_w, -self._body_l, self._body_h],
                [-self._body_w, self._body_l, self._body_h],
                [-self._body_w, self._body_l, 0.0],
                [self._body_w, -self._body_l, 0.0],    # right face
                [self._body_w, -self._body_l, self._body_h],
                [self._body_w, self._body_l, self._body_h],
                [self._body_w, self._body_l, 0.0],
                [-self._body_w, self._body_l, 0.0],    # front face
                [-self._body_w, self._body_l, self._body_h],
                [self._body_w, self._body_l, self._body_h],
                [self._body_w, self._body_l, 0.0],
                [-self._body_w, -self._body_l, 0.0],    # back face
                [-self._body_w, -self._body_l, self._body_h],
                [self._body_w, -self._body_l, self._body_h],
                [self._body_w, -self._body_l, 0.0]]  
        
    def set_position(self,pos):
        self._pos = pos
    def set_heading(self,heading):
        self._heading = heading
    def set_color(self,color,mode=False):
        if mode == False:
            glColor3f(color[0], color[1], color[2])
        else:
            glColor4f(color[0], color[1], color[2], 0.0)
    def draw(self,enemy_pos):
        mat_zero = [0.0, 0.0, 0.0, 1.0]
        mat_diffuse_white = [1.0, 1.0, 1.0, 1.0]
        mat_diffuse_red = [1.0, 0.0, 0.0, 1.0]
        mat_diffuse_green = [0.0, 1.0, 0.0, 1.0]
        mat_diffuse_blue = [0.0, 0.0, 1.0, 1.0]
        mat_ambient_white = [1.0, 1.0, 1.0, 1.0]
        mat_ambient_red = [1.0, 0.0, 0.0, 1.0]
        mat_specular = [1.0, 1.0, 1.0, 1.0]
        mat_no_shininess = [0.0]
        mat_low_shininess = [10.0]
        mat_high_shininess = [100.0]
        mat_emission = [0.0, 0.0, 0.1, 0.0]
        mat_emission_green = [0.0, 0.5, 0.0, 0.0]
        mat_emission_red = [0.5, 0.0, 0.0, 0.0]
        
        is_enemy_hitted = False
        if self.cannonball._is_shooted == True:
            glEnable(GL_LIGHT1)
            # set material properties
            glMaterialfv(GL_FRONT_AND_BACK, GL_AMBIENT, [1.0, 0.0, 0.0, 1.0])
            glMaterialfv(GL_FRONT_AND_BACK, GL_DIFFUSE, mat_diffuse_red)
            glMaterialfv(GL_FRONT_AND_BACK, GL_SPECULAR, [0,0,0,0])
            glMaterialfv(GL_FRONT_AND_BACK, GL_SHININESS, mat_no_shininess)
            glMaterialfv(GL_FRONT_AND_BACK, GL_EMISSION, [0.5,0,0,0])
            glLightfv(GL_LIGHT1, GL_AMBIENT, [0,0,0,1])
            glLightfv(GL_LIGHT1, GL_DIFFUSE, [0.5,0,0,1])
            glLightfv(GL_LIGHT1, GL_SPECULAR, [1,1,1,1])
            is_enemy_hitted = self.cannonball.compute(enemy_pos)
            #self._pos_cannonball = self.cannonball.compute(self._pos_cannonball)
            glPolygonMode(GL_FRONT_AND_BACK, GL_FILL) # POINT, LINE, FILL
            self.set_color(self.color_set.cannon_base,True)
       # glColor4f(1.0, 0.0, 0.0, 0.0)
            glPushMatrix()
            glTranslatef(self.cannonball._pos[0], self.cannonball._pos[1], self.cannonball._pos[2]) # translate to canon base location
            
            glLightfv(GL_LIGHT1, GL_POSITION, [self.cannonball._pos[0],self.cannonball._pos[1],self.cannonball._pos[2],1.0])
            
            gluSphere(Tank.sphere, self.cannonball._radius, 25, 25)
            glPopMatrix()
        if self.cannonball._is_exploded == True:
            if self.cannonball._exploding_frame < 10:
                self.cannonball._dispersed_frame = 0
                glMaterialfv(GL_FRONT_AND_BACK, GL_AMBIENT, [1.0, 0.0, 0.0, 1.0])
                glMaterialfv(GL_FRONT_AND_BACK, GL_DIFFUSE, mat_diffuse_red)
                glMaterialfv(GL_FRONT_AND_BACK, GL_SPECULAR, [0,0,0,0])
                glMaterialfv(GL_FRONT_AND_BACK, GL_SHININESS, mat_no_shininess)
                glMaterialfv(GL_FRONT_AND_BACK, GL_EMISSION, [0.5,0,0,0])
                glPolygonMode(GL_FRONT, GL_LINE) # POINT, LINE, FILL
                glLightfv(GL_LIGHT1, GL_DIFFUSE, [10,0,0,1])
                glLightfv(GL_LIGHT1, GL_SPECULAR, [1,1,1,1])
                light_height = self.cannonball._exploding_frame
                if self.cannonball._pos[2]>0 :
                    light_height = self.cannonball._pos[2] + self.cannonball._exploding_frame
                elif self.cannonball._exploding_frame == 0:
                    self.cannonball._pos[2] = 0
                #light_front = 0
                # if self.cannonball._pos[2] <=50 and self.cannonball._pos[1] > 65 and abs(self.cannonball._pos[0]) < 20:
                #     self.cannonball._pos[1] = 65
                #     light_front = 1
                #     print('ggg')
                glLightfv(GL_LIGHT1, GL_POSITION, [self.cannonball._pos[0],self.cannonball._pos[1],light_height,1.0])
            
                self.set_color(self.color_set.cannon_base,True)
        # glColor4f(1.0, 0.0, 0.0, 0.0)
                glPushMatrix()
                glTranslatef(self.cannonball._pos[0], self.cannonball._pos[1], self.cannonball._pos[2]) # translate to canon base location
                gluSphere(Tank.sphere, self.cannonball._radius + self.cannonball._exploding_frame, 25, 25)
                glPopMatrix()
                self.cannonball._exploding_frame += 0.2
            else:
                if self.cannonball._dispersed_frame < 0.5:
                    glMaterialfv(GL_FRONT_AND_BACK, GL_AMBIENT, [1.0, 0.0, 0.0, 1.0])
                    glMaterialfv(GL_FRONT_AND_BACK, GL_DIFFUSE, mat_diffuse_red)
                    glMaterialfv(GL_FRONT_AND_BACK, GL_SPECULAR, [0,0,0,0])
                    glMaterialfv(GL_FRONT_AND_BACK, GL_SHININESS, mat_no_shininess)
                    glMaterialfv(GL_FRONT_AND_BACK, GL_EMISSION, [0.5 - self.cannonball._dispersed_frame,0,0,0])
                    light_height = 10
                    if self.cannonball._pos[2]>0 :
                        light_height = self.cannonball._pos[2] + 10
                    elif self.cannonball._exploding_frame == 0:
                        light_height = 10
                        self.cannonball._pos[2] = 0
                    glPolygonMode(GL_FRONT, GL_LINE) # POINT, LINE, FILL
                    glLightfv(GL_LIGHT1, GL_DIFFUSE, [10 - (self.cannonball._dispersed_frame*20) ,0,0,1])
                    glLightfv(GL_LIGHT1, GL_SPECULAR, [1,1,1,1])
                    glLightfv(GL_LIGHT1, GL_POSITION, [self.cannonball._pos[0],self.cannonball._pos[1],light_height,1.0])
            
                    self.set_color(self.color_set.cannon_base,True)
            # glColor4f(1.0, 0.0, 0.0, 0.0)
                    glPushMatrix()
                    glTranslatef(self.cannonball._pos[0], self.cannonball._pos[1], self.cannonball._pos[2]) # translate to canon base location
                    gluSphere(Tank.sphere, self.cannonball._radius + self.cannonball._exploding_frame, 25, 25)
                    glPopMatrix()
                    self.cannonball._dispersed_frame += 0.1    
                else:
                    self.cannonball._is_exploded = False
                    self.cannonball._exploding_frame = 0
                    glLightfv(GL_LIGHT1, GL_AMBIENT, [0,0,0,1])
                    glLightfv(GL_LIGHT1, GL_DIFFUSE, [0,0,0,1])
                    glLightfv(GL_LIGHT1, GL_SPECULAR, [0,0,0,1])
                    glDisable(GL_LIGHT1)
        
        glMaterialfv(GL_FRONT_AND_BACK, GL_AMBIENT, mat_zero)
        glMaterialfv(GL_FRONT_AND_BACK, GL_DIFFUSE, mat_diffuse_white)
        glMaterialfv(GL_FRONT_AND_BACK, GL_SPECULAR, mat_zero)
        glMaterialfv(GL_FRONT_AND_BACK, GL_SHININESS, mat_low_shininess)
        glMaterialfv(GL_FRONT_AND_BACK, GL_EMISSION, mat_zero)
        
        # move to the player position
        glPushMatrix()
        glTranslatef(self._pos[0], self._pos[1], self._pos[2])
        glRotate(-self._heading, 0, 0, 1)
        
        # draw canon
        glPushMatrix()
        glPolygonMode(GL_FRONT_AND_BACK, GL_FILL) # POINT, LINE, FILL
        glTranslatef(self.canon_base[0], self.canon_base[1], self.canon_base[2]) # translate the canon
        glRotate(-90+self.canon_angle, 1, 0, 0)  # rotate (tilt) the canon       
        #self.set_color(self.color_set.black)
        glColor3f(0.4, 0.4, 0.4)
        
        #glColor3f(0.0, 1.0, 0.0)
        gluCylinder(Tank.cylinder, self.canon_radius, self.canon_radius, self.canon_length, 25, 25)
        glPopMatrix()

        # draw canon base
        glPolygonMode(GL_FRONT_AND_BACK, GL_FILL) # POINT, LINE, FILL
        #self.set_color(self.color_set.cannon_base,True)
        glColor4f(0.4, 0.4, 0.4, 0.0)
        glPushMatrix()
        glTranslatef(self.canon_base[0], self.canon_base[1], self.canon_base[2]-1.5) # translate to canon base location
        gluSphere(Tank.sphere, self.canon_base_radius, 25, 25)
        glPopMatrix()

        ###### draw self left track
        ### side body
        # set material and color
        glMaterialfv(GL_FRONT_AND_BACK, GL_AMBIENT, mat_zero)
        glMaterialfv(GL_FRONT_AND_BACK, GL_DIFFUSE, mat_diffuse_white)
        glMaterialfv(GL_FRONT_AND_BACK, GL_SPECULAR, mat_zero)
        glMaterialfv(GL_FRONT_AND_BACK, GL_SHININESS, mat_low_shininess)
        glMaterialfv(GL_FRONT_AND_BACK, GL_EMISSION, mat_zero)
        glColor3f(0.4, 0.4, 0.4) 
        # draw 
        glPushMatrix()
        glTranslatef(-(self._body_w+self._track_left[0]._track_body_dim[0]), 0, self._track_left[0]._track_dim[2])  
        self.draw_unit_quad_horizontal(2,6,0.5,1)
        self.draw_unit_quad_horizontal(2,6,4,1)
        self.draw_unit_quad_vertical(6,4,1,'right')
        self.draw_unit_quad_vertical(6,4,-1,'left')
        self.draw_unit_quad_vertical(2,4,3,'front')
        self.draw_unit_quad_vertical(2,4,-3,'rear')
       
        ### wheel1
        # set material and color
        glMaterialfv(GL_FRONT_AND_BACK, GL_AMBIENT, mat_zero)
        glMaterialfv(GL_FRONT_AND_BACK, GL_DIFFUSE, mat_diffuse_white)
        glMaterialfv(GL_FRONT_AND_BACK, GL_SPECULAR, mat_zero)
        glMaterialfv(GL_FRONT_AND_BACK, GL_SHININESS, mat_low_shininess)
        glMaterialfv(GL_FRONT_AND_BACK, GL_EMISSION, mat_emission_green)
        glColor3f(0.4, 0.4, 0.4) 
        # draw
        glPushMatrix()
        glTranslatef(-1+0.1, self._track_right[0]._track_body_dim[1], self._track_right[0]._track_body_dim[2]/2) 
        glRotate(90,0, 1, 0)        
        glRotate(-self._track_right[0]._track_rotation,0, 0, 1)         
        self.set_color(self.color_set.cannon)
        gluCylinder(Tank.cylinder, self._track_right[0]._track_wheel_radius, self._track_right[0]._track_wheel_radius, 1, 10, 10)
        glPopMatrix()
        
        ### wheel2
        # set material and color
        glMaterialfv(GL_FRONT_AND_BACK, GL_AMBIENT, mat_zero)
        glMaterialfv(GL_FRONT_AND_BACK, GL_DIFFUSE, mat_diffuse_white)
        glMaterialfv(GL_FRONT_AND_BACK, GL_SPECULAR, mat_zero)
        glMaterialfv(GL_FRONT_AND_BACK, GL_SHININESS, mat_low_shininess)
        glMaterialfv(GL_FRONT_AND_BACK, GL_EMISSION, mat_emission_green)
        glColor3f(0.4, 0.4, 0.4)
        # draw
        glPushMatrix()
        glTranslatef(-1+0.1, -self._track_right[0]._track_body_dim[1], self._track_right[0]._track_body_dim[2]/2) 
        glRotate(90,0, 1, 0) 
        glRotate(-self._track_right[0]._track_rotation,0, 0, 1)  #       
        self.set_color(self.color_set.cannon)
        gluCylinder(Tank.cylinder, self._track_right[0]._track_wheel_radius, self._track_right[0]._track_wheel_radius, 1, 10, 10)
        glPopMatrix()
        
        ### draw track !!!!!! not fully implemented, and cost very high resource, so I just show 1 of this
        # set material and color
        glMaterialfv(GL_FRONT_AND_BACK, GL_AMBIENT, mat_zero)
        glMaterialfv(GL_FRONT_AND_BACK, GL_DIFFUSE, mat_diffuse_white)
        glMaterialfv(GL_FRONT_AND_BACK, GL_SPECULAR, mat_zero)
        glMaterialfv(GL_FRONT_AND_BACK, GL_SHININESS, mat_high_shininess)
        glMaterialfv(GL_FRONT_AND_BACK, GL_EMISSION, mat_emission_red)
        glColor3f(0.0, 0.0, 0.0)
        for j in range(0,self._track_count):
            glPushMatrix()
            glTranslatef(0, self._track_left[j]._track_pos[1], self._track_left[j]._track_pos[2]-self._track_left[j]._track_dim[2])
            glRotate(-self._track_left[j]._track_body_rotation-90,1, 0, 0)  # rotate (tilt) the canon         
            for i in range(6):
                
                glBegin(GL_QUADS)
                glNormal3d(0, 0, -1)
                glVertex3f(self._track_left[j]._track[i*4][0], self._track_left[j]._track[i*4][1], self._track_left[j]._track[i*4][2])
                glNormal3d(0, 0, -1)
                glVertex3f(self._track_left[j]._track[(i*4)+1][0], self._track_left[j]._track[(i*4)+1][1], self._track_left[j]._track[(i*4)+1][2])
                glNormal3d(0, 0, -1)
                glVertex3f(self._track_left[j]._track[(i*4)+2][0], self._track_left[j]._track[(i*4)+2][1], self._track_left[j]._track[(i*4)+2][2])
                glNormal3d(0, 0, -1)
                glVertex3f(self._track_left[j]._track[(i*4)+3][0], self._track_left[j]._track[(i*4)+3][1], self._track_left[j]._track[(i*4)+3][2])
                glEnd()
            glPopMatrix()
        glPopMatrix()
        ###### end of left 

        ###### draw self right track
        
        ### side body
        # set material and color
        glMaterialfv(GL_FRONT_AND_BACK, GL_AMBIENT, mat_zero)
        glMaterialfv(GL_FRONT_AND_BACK, GL_DIFFUSE, mat_diffuse_white)
        glMaterialfv(GL_FRONT_AND_BACK, GL_SPECULAR, mat_zero)
        glMaterialfv(GL_FRONT_AND_BACK, GL_SHININESS, mat_low_shininess)
        glMaterialfv(GL_FRONT_AND_BACK, GL_EMISSION, mat_zero)
        glColor3f(0.4, 0.4, 0.4) 
        # draw 
        glPushMatrix()
        glTranslatef((self._body_w+self._track_right[0]._track_body_dim[0]), 0, self._track_right[0]._track_dim[2])
        glPolygonMode(GL_FRONT_AND_BACK, GL_FILL) # POINT, LINE, FILL
        glColor3f(0.4, 0.4, 0.4) 
        self.draw_unit_quad_horizontal(2,6,0.5,1)
        self.draw_unit_quad_horizontal(2,6,4,1)
        self.draw_unit_quad_vertical(6,4,1,'right')
        self.draw_unit_quad_vertical(6,4,-1,'left')
        self.draw_unit_quad_vertical(2,4,3,'front')
        self.draw_unit_quad_vertical(2,4,-3,'rear')
       
        ### wheel1
        # set material and color
        glMaterialfv(GL_FRONT_AND_BACK, GL_AMBIENT, mat_zero)
        glMaterialfv(GL_FRONT_AND_BACK, GL_DIFFUSE, mat_diffuse_white)
        glMaterialfv(GL_FRONT_AND_BACK, GL_SPECULAR, mat_zero)
        glMaterialfv(GL_FRONT_AND_BACK, GL_SHININESS, mat_low_shininess)
        glMaterialfv(GL_FRONT_AND_BACK, GL_EMISSION, mat_emission_green)
        glColor3f(0.4, 0.4, 0.4) 
        # draw
        glPushMatrix()
        glTranslatef(-0.1, self._track_right[0]._track_body_dim[1], self._track_right[0]._track_body_dim[2]/2) # translate the canon
        glRotate(90,0, 1, 0)  # rotate (tilt) the canon         
        glRotate(-self._track_right[0]._track_rotation,0, 0, 1)  # rotate (tilt) the canon       
        self.set_color(self.color_set.cannon)
        gluCylinder(Tank.cylinder, self._track_right[0]._track_wheel_radius, self._track_right[0]._track_wheel_radius, 1, 10, 10)
        glPopMatrix()

        ### wheel2
        # set material and color
        glMaterialfv(GL_FRONT_AND_BACK, GL_AMBIENT, mat_zero)
        glMaterialfv(GL_FRONT_AND_BACK, GL_DIFFUSE, mat_diffuse_white)
        glMaterialfv(GL_FRONT_AND_BACK, GL_SPECULAR, mat_zero)
        glMaterialfv(GL_FRONT_AND_BACK, GL_SHININESS, mat_low_shininess)
        glMaterialfv(GL_FRONT_AND_BACK, GL_EMISSION, mat_emission_green)
        glColor3f(0.4, 0.4, 0.4)
        # draw
        glPushMatrix()
        glTranslatef(-0.1, -self._track_right[0]._track_body_dim[1], self._track_right[0]._track_body_dim[2]/2) # translate the canon
        glRotate(90,0, 1, 0)  # rotate (tilt) the canon         
        glRotate(-self._track_right[0]._track_rotation,0, 0, 1)  # rotate (tilt) the canon       
        self.set_color(self.color_set.cannon)
        gluCylinder(Tank.cylinder, self._track_right[0]._track_wheel_radius, self._track_right[0]._track_wheel_radius, 1, 10, 10)
        glPopMatrix()
        
        ### draw track !!!!!! not fully implemented, and cost very high resource, so I just show 1 of this
        # set material and color
        glMaterialfv(GL_FRONT_AND_BACK, GL_AMBIENT, mat_zero)
        glMaterialfv(GL_FRONT_AND_BACK, GL_DIFFUSE, mat_diffuse_white)
        glMaterialfv(GL_FRONT_AND_BACK, GL_SPECULAR, mat_zero)
        glMaterialfv(GL_FRONT_AND_BACK, GL_SHININESS, mat_high_shininess)
        glMaterialfv(GL_FRONT_AND_BACK, GL_EMISSION, mat_emission_red)
        glColor3f(0.0, 0.0, 0.0)
        for j in range(0,self._track_count):
            glPushMatrix()
            glTranslatef(0, self._track_right[j]._track_pos[1], self._track_right[j]._track_pos[2]-self._track_right[j]._track_dim[2])
            glRotate(-self._track_right[j]._track_body_rotation-90,1, 0, 0)          
            for i in range(6):
                self.set_color(self.color_set.black)
                glBegin(GL_QUADS)
                glNormal3d(0, 0, 1)
                glVertex3f(self._track_right[j]._track[i*4][0], self._track_right[j]._track[i*4][1], self._track_right[j]._track[i*4][2])
                glNormal3d(0, 0, 1)
                glVertex3f(self._track_right[j]._track[(i*4)+1][0], self._track_right[j]._track[(i*4)+1][1], self._track_right[j]._track[(i*4)+1][2])
                glNormal3d(0, 0, 1)
                glVertex3f(self._track_right[j]._track[(i*4)+2][0], self._track_right[j]._track[(i*4)+2][1], self._track_right[j]._track[(i*4)+2][2])
                glNormal3d(0, 0, 1)
                glVertex3f(self._track_right[j]._track[(i*4)+3][0], self._track_right[j]._track[(i*4)+3][1], self._track_right[j]._track[(i*4)+3][2])
                glEnd()
            glPopMatrix()
        glPopMatrix()
        ###### end of right 

        ###### Body
        # set material and color
        glMaterialfv(GL_FRONT_AND_BACK, GL_AMBIENT, mat_zero)
        glMaterialfv(GL_FRONT_AND_BACK, GL_DIFFUSE, mat_diffuse_white)
        glMaterialfv(GL_FRONT_AND_BACK, GL_SPECULAR, mat_zero)
        glMaterialfv(GL_FRONT_AND_BACK, GL_SHININESS, mat_low_shininess)
        glMaterialfv(GL_FRONT_AND_BACK, GL_EMISSION, mat_zero)
        glColor3f(0.4, 0.4, 0.4) 
        # draw
        glTranslatef(0,0,0.5)
        glPolygonMode(GL_FRONT, GL_FILL)
        self.draw_unit_quad_horizontal(6,10,4,1)
        self.draw_unit_quad_horizontal(6,10,0,1)
        self.draw_unit_quad_vertical(10,4,3,'right')
        self.draw_unit_quad_vertical(10,4,-3,'left')
        self.draw_unit_quad_vertical(6,4,-5,'rear')        
        self.draw_unit_quad_vertical(6,4,5,'front')
        glPopMatrix()
        ###### End of bodyelf body
        return is_enemy_hitted

    def draw_unit_quad_horizontal(self,quad_size_w,quad_size_l,height,gridsize):
        #gridsize = 1
        for i in frange((-quad_size_w/2), (quad_size_w/2)-(gridsize/2), gridsize):
            for j in frange((-quad_size_l/2), (quad_size_l/2)-(gridsize/2), gridsize):
                glPushMatrix()
                glTranslate(i,j,0)
                glBegin(GL_QUADS)
                glNormal3d(0, 0, 1)
                glVertex3f(0, 0, height)
                glNormal3d(0, 0, 1)
                glVertex3f(gridsize, 0, height)
                glNormal3d(0, 0, 1)
                glVertex3f(gridsize, gridsize, height)
                glNormal3d(0, 0, 1)
                glVertex3f(0, gridsize, height)
                glEnd()
                glPopMatrix()
    
    def draw_unit_quad_vertical(self,quad_size_w,quad_size_l,shift,side):
        gridsize = 1
        if side == 'left':
            for i in frange((-quad_size_w/2), (quad_size_w/2)-(gridsize/2), gridsize):
                for j in frange(0, quad_size_l-(gridsize/2), gridsize):
                    glPushMatrix()
                    glTranslate(0,i,j)
                    glBegin(GL_QUADS)
                    glNormal3d(-1,0, 0)
                    glVertex3f(shift, 0, 0)
                    glNormal3d(-1,0, 0)
                    glVertex3f(shift, gridsize, 0)
                    glNormal3d(-1,0, 0)
                    glVertex3f(shift,gridsize, gridsize)
                    glNormal3d(-1,0, 0)
                    glVertex3f(shift, 0, gridsize)
                    glEnd()
                    glPopMatrix()
        if side == 'right':
            for i in frange((-quad_size_w/2), (quad_size_w/2)-(gridsize/2), gridsize):
                for j in frange(0, quad_size_l-(gridsize/2), gridsize):
                    glPushMatrix()
                    glTranslate(0,i,j)
                    glBegin(GL_QUADS)
                    glNormal3d(1,0, 0)
                    glVertex3f(shift, 0, 0)
                    glNormal3d(1,0, 0)
                    glVertex3f(shift, gridsize, 0)
                    glNormal3d(1,0, 0)
                    glVertex3f(shift,gridsize, gridsize)
                    glNormal3d(1,0, 0)
                    glVertex3f(shift, 0, gridsize)
                    glEnd()
                    glPopMatrix()
        elif side == 'front':
            for i in frange((-quad_size_w/2), (quad_size_w/2)-(gridsize/2), gridsize):
                for j in frange(0, quad_size_l-(gridsize/2), gridsize):
                    glPushMatrix()
                    glTranslate(i,0,j)
                    glBegin(GL_QUADS)
                    glNormal3d(0, 1, 0)
                    glVertex3f( 0,shift, 0)
                    glNormal3d(0, 1, 0)
                    glVertex3f( gridsize,shift, 0)
                    glNormal3d(0, 1, 0)
                    glVertex3f(gridsize,shift, gridsize)
                    glNormal3d(0, 1, 0)
                    glVertex3f( 0,shift, gridsize)
                    glEnd()
                    glPopMatrix()
        elif side == 'rear':
            for i in frange((-quad_size_w/2), (quad_size_w/2)-(gridsize/2), gridsize):
                for j in frange(0, quad_size_l-(gridsize/2), gridsize):
                    glPushMatrix()
                    glTranslate(i,0,j)
                    glBegin(GL_QUADS)
                    glNormal3d(0, -1, 0)
                    glVertex3f( 0,shift, 0)
                    glNormal3d(0, -1, 0)
                    glVertex3f( gridsize,shift, 0)
                    glNormal3d(0, -1, 0)
                    glVertex3f(gridsize,shift, gridsize)
                    glNormal3d(0, -1, 0)
                    glVertex3f( 0,shift, gridsize)
                    glEnd()
                    glPopMatrix()
    def shoot(self,velocity):
        if (self.cannonball._is_shooted == False) and (self.cannonball._is_exploded == False):
            self.cannonball._is_shooted = True
            self.cannonball._heading = self._heading
            self.cannonball._angle = self.canon_angle
            self.cannonball._time = 0
            self.cannonball.set_initial_velocity(velocity)
            initial_pos =  [self._pos[0]+self.canon_length*math.cos(0.0174532925*self.canon_angle)*math.sin(0.0174532925*self._heading),
                            self._pos[1]+self.canon_length*math.cos(0.0174532925*self.canon_angle)*math.cos(0.0174532925*self._heading),
                            self._pos[2]+self._body_h+(self.canon_length)*math.sin(0.0174532925*self.canon_angle)]
            self.cannonball._initial_pos = initial_pos

            
            print('shooted')
            
            print(self.cannonball._pos,self.cannonball._initial_pos,self.cannonball._angle)
    def rotate_wheel_left(self,distance):
        for i in range(0,self._track_count):
            self._track_left[i].rotate_wheel(distance)
    def rotate_wheel_right(self,distance):
        for i in range(0,self._track_count):
            self._track_right[i].rotate_wheel(distance)
               
class TrackWheel:
    default_canon_base = [0,0,5]
    sphere = gluNewQuadric()
    cylinder = gluNewQuadric()
    disk = gluNewQuadric()
    color_set = TankColorPalette()
    perspective = 0
    def __init__(self,angle,distance_ind):
        self._track_dim = [0.9,0.45,0.2]
        self._track_pos = [0,0,0]       
        self._last_track_pos = [0,0,0]       
        self._track_wheel_radius = 1.8
        self._track_body_rotation = 0
        self._track = [[-self._track_dim[0], -self._track_dim[1], 0.0],    # bottom face
                [-self._track_dim[0], self._track_dim[1], 0.0],
                [self._track_dim[0], self._track_dim[1], 0.0],
                [self._track_dim[0], -self._track_dim[1], 0.0],
                [-self._track_dim[0], -self._track_dim[1], self._track_dim[2]],    # top face
                [-self._track_dim[0], self._track_dim[1], self._track_dim[2]],
                [self._track_dim[0], self._track_dim[1], self._track_dim[2]],
                [self._track_dim[0], -self._track_dim[1], self._track_dim[2]],
                [-self._track_dim[0], -self._track_dim[1], 0.0],    # left face
                [-self._track_dim[0], -self._track_dim[1], self._track_dim[2]],
                [-self._track_dim[0], self._track_dim[1], self._track_dim[2]],
                [-self._track_dim[0], self._track_dim[1], 0.0],
                [self._track_dim[0], -self._track_dim[1], 0.0],    # right face
                [self._track_dim[0], -self._track_dim[1], self._track_dim[2]],
                [self._track_dim[0], self._track_dim[1], self._track_dim[2]],
                [self._track_dim[0], self._track_dim[1], 0.0],
                [-self._track_dim[0], self._track_dim[1], 0.0],    # front face
                [-self._track_dim[0], self._track_dim[1], self._track_dim[2]],
                [self._track_dim[0], self._track_dim[1], self._track_dim[2]],
                [self._track_dim[0], self._track_dim[1], 0.0],
                [-self._track_dim[0], -self._track_dim[1], 0.0],    # back face
                [-self._track_dim[0], -self._track_dim[1], self._track_dim[2]],
                [self._track_dim[0], -self._track_dim[1], self._track_dim[2]],
                [self._track_dim[0], -self._track_dim[1], 0.0]]       
        self._track_body_dim = [1,2.6,3.6]
        self._track_body = [[-self._track_body_dim[0], -self._track_body_dim[1], 0.0],    # bottom face
                [-self._track_body_dim[0], self._track_body_dim[1], 0.0],
                [self._track_body_dim[0], self._track_body_dim[1], 0.0],
                [self._track_body_dim[0], -self._track_body_dim[1], 0.0],
                [-self._track_body_dim[0], -self._track_body_dim[1], self._track_body_dim[2]],    # top face
                [-self._track_body_dim[0], self._track_body_dim[1], self._track_body_dim[2]],
                [self._track_body_dim[0], self._track_body_dim[1], self._track_body_dim[2]],
                [self._track_body_dim[0], -self._track_body_dim[1], self._track_body_dim[2]],
                [-self._track_body_dim[0], -self._track_body_dim[1], 0.0],    # left face
                [-self._track_body_dim[0], -self._track_body_dim[1], self._track_body_dim[2]],
                [-self._track_body_dim[0], self._track_body_dim[1], self._track_body_dim[2]],
                [-self._track_body_dim[0], self._track_body_dim[1], 0.0],
                [self._track_body_dim[0], -self._track_body_dim[1], 0.0],    # right face
                [self._track_body_dim[0], -self._track_body_dim[1], self._track_body_dim[2]],
                [self._track_body_dim[0], self._track_body_dim[1], self._track_body_dim[2]],
                [self._track_body_dim[0], self._track_body_dim[1], 0.0],
                [-self._track_body_dim[0], self._track_body_dim[1], 0.0],    # front face
                [-self._track_body_dim[0], self._track_body_dim[1], self._track_body_dim[2]],
                [self._track_body_dim[0], self._track_body_dim[1], self._track_body_dim[2]],
                [self._track_body_dim[0], self._track_body_dim[1], 0.0],
                [-self._track_body_dim[0], -self._track_body_dim[1], 0.0],    # back face
                [-self._track_body_dim[0], -self._track_body_dim[1], self._track_body_dim[2]],
                [self._track_body_dim[0], -self._track_body_dim[1], self._track_body_dim[2]],
                [self._track_body_dim[0], -self._track_body_dim[1], 0.0]]  
        di = (self._track_body_dim[2]+self._track_dim[2]*2)
        deg_limit = (math.atan2(di/2,di)*(180/math.pi))
        #angle_dis = (distance / (math.pi*di))*360
        distance = distance_ind * (2*self._track_dim[1]+0.1)
        
        self._track_rotation = 0
        
        # if self._track_rotation >= 360:
        #     self._track_rotation = self._track_rotation - 360 
        # elif self._track_rotation < 0:
        #     self._track_rotation = self._track_rotation + 360       
        self._state = 'down' 
        if (angle > deg_limit) and (angle < 180 - deg_limit):
            self._state = 'up'
            
            self._track_pos[2] = di
            #self._track_pos[1] = distance
            self._track_body_rotation = 90
            self._last_track_pos[2] = self._track_wheel_radius+self._track_dim[2]
        elif (angle > 180 + deg_limit) and (angle < 360 - deg_limit):
            self._state = 'down'
            self._track_pos[2] = 0
            # self._track_pos[1] = distance
            self._track_body_rotation = 270
            self._last_track_pos[2] = -(self._track_wheel_radius+self._track_dim[2])
        elif (angle <= deg_limit) or (angle >= 360 - deg_limit):
            self._state = 'rear'

        elif (angle >= 180 - deg_limit) and (angle <= 180 + deg_limit):
            self._state = 'front'

        self._last_state = self._state
        #print ('Init_state',self._state,self._last_state,distance,self._track_rotation,self._track_pos[1],self._track_pos[2])
        self.rotate_wheel(distance)
        #print ('Current_state',self._state,self._last_state,distance,self._track_rotation)
        
       
    def rotate_wheel(self,distance):
        di = (self._track_body_dim[2]+self._track_dim[2]*2)
        angle = (distance / (math.pi*di))*360
        self._track_rotation += angle 
        if(distance > 4.6):
            distance = distance - 4.6
        elif (distance < -4.6):
            distance = distance + 4.6
        if self._track_rotation >= 360:
            self._track_rotation = self._track_rotation - (360*int(self._track_rotation/360))
        elif self._track_rotation < 0:
            self._track_rotation = self._track_rotation + 360 
        deg_limit = (math.atan2(di/2,di)*(180/math.pi))
        
        if self._state == 'up':
            estimated = round((self._track_pos[1] + distance),3)
            if (self._track_pos[1] + distance) <= -self._track_body_dim[1]:
                diff = (self._track_pos[1] + distance) + self._track_body_dim[1]
                angle = (diff / (math.pi*di))*360
                self._last_state = self._state
                self._state = 'rear'           
                self._track_body_rotation += angle 
                dist_x = (self._track_wheel_radius+self._track_dim[2])*math.cos(0.0174532925*self._track_body_rotation)
                dist_y = (self._track_wheel_radius+self._track_dim[2])*math.sin(0.0174532925*self._track_body_rotation)
                self._track_pos[1] = -self._track_body_dim[1] - dist_x
                self._track_pos[2] = self._track_wheel_radius+self._track_dim[2] + dist_y             
                #print('execeed',diff,angle,dist_x,dist_y,self._track_body_rotation)
            elif (self._track_pos[1] + distance) >= self._track_body_dim[1]:
                diff = estimated - self._track_body_dim[1]
                angle = (diff / (math.pi*di))*360
                self._last_state = self._state
                self._state = 'front'           
                self._track_body_rotation += angle 
                dist_x = (self._track_wheel_radius+self._track_dim[2])*math.cos(0.0174532925*self._track_body_rotation)
                dist_y = (self._track_wheel_radius+self._track_dim[2])*math.sin(0.0174532925*self._track_body_rotation)
                self._track_pos[1] = self._track_body_dim[1] - dist_x
                self._track_pos[2] = self._track_wheel_radius+self._track_dim[2] + dist_y 
                
                #print('execeed',diff,angle,dist_x,dist_y,self._track_body_rotation)
            else:
                self._track_pos[1] = round(self._track_pos[1] + distance,3)
                self._track_pos[2] = di
                
                self._track_body_rotation = 90
                self._last_track_pos[1] = 0
                self._last_track_pos[2] = round(self._track_wheel_radius+self._track_dim[2])
            
            
        elif self._state == 'down':
            #print ('estmated',round((self._track_pos[1] - distance),3))
            if (self._track_pos[1] - distance) <= -self._track_body_dim[1]:
                diff = (self._track_pos[1] - distance) + self._track_body_dim[1]
                angle = (diff / (math.pi*di))*360
                self._last_state = self._state
                self._state = 'rear'           
                self._track_body_rotation += angle 
                dist_x = (self._track_wheel_radius+self._track_dim[2])*math.cos(0.0174532925*self._track_body_rotation)
                dist_y = (self._track_wheel_radius+self._track_dim[2])*math.sin(0.0174532925*self._track_body_rotation)
                self._track_pos[1] = -self._track_body_dim[1] + dist_x
                self._track_pos[2] = self._track_wheel_radius+self._track_dim[2] + dist_y             
                #print('execeed',diff,angle,dist_x,dist_y)
            elif (self._track_pos[1] - distance) >= self._track_body_dim[1]:
                diff = (self._track_pos[1] - distance) - self._track_body_dim[1]
                angle = (diff / (math.pi*di))*360
                self._last_state = self._state
                self._state = 'front'           
                self._track_body_rotation += angle 
                dist_x = (self._track_wheel_radius+self._track_dim[2])*math.cos(0.0174532925*self._track_body_rotation)
                dist_y = (self._track_wheel_radius+self._track_dim[2])*math.sin(0.0174532925*self._track_body_rotation)
                self._track_pos[1] = self._track_body_dim[1] + dist_x
                self._track_pos[2] = self._track_wheel_radius+self._track_dim[2] + dist_y 
                
                #print('execeed',diff,angle)
            else:
                self._track_pos[1] = round(self._track_pos[1] - distance,3)
                self._track_pos[2] = 0
                
                self._track_body_rotation = 270
                self._last_track_pos[1] = 0
                self._last_track_pos[2] = -round(self._track_wheel_radius+self._track_dim[2])
            #print("current x,y: ",self._track_pos[1],self._track_pos[2])
        elif self._state == 'rear':
            
           # print ('estmated angle',self._track_body_rotation + angle)
            estimated = self._track_body_rotation + angle
            if estimated >= 90 and estimated < 180:
                diff = estimated - 90
                dist = (diff * (math.pi*di))/360
                self._last_state = self._state
                self._state = 'up' 
                #dist_x = round((self._track_wheel_radius+self._track_dim[2])*math.cos(0.0174532925*diff),5)
                self._track_body_rotation = 90
                self._track_pos[1] = -self._track_body_dim[1] + dist
                self._track_pos[2] = di
               # print('execeed',diff,dist,self._track_body_rotation)
            elif estimated <= 270 and estimated > 180:
                diff = 270 - estimated 
                dist = (diff * (math.pi*di))/360
                self._last_state = self._state
                self._state = 'down' 
                #dist_x = round((self._track_wheel_radius+self._track_dim[2])*math.cos(0.0174532925*diff),5)
                self._track_body_rotation = 270
                self._track_pos[1] = -self._track_body_dim[1] + dist
                self._track_pos[2] = 0
                #print('execeed',diff,dist,self._track_body_rotation)
            else:
                self._track_body_rotation += angle 
                if self._track_body_rotation >= 360:
                    self._track_body_rotation = self._track_body_rotation - 360 
                elif self._track_body_rotation < 0:
                    self._track_body_rotation = self._track_body_rotation + 360 
                
                dist_x = (self._track_wheel_radius+self._track_dim[2])*math.cos(0.0174532925*self._track_body_rotation)
                dist_y = (self._track_wheel_radius+self._track_dim[2])*math.sin(0.0174532925*self._track_body_rotation)
                
                self._track_pos[1] -=  dist_x - self._last_track_pos[1]
                self._track_pos[2] +=  dist_y - self._last_track_pos[2]
                self._last_track_pos[1] = dist_x
                self._last_track_pos[2] = dist_y
            
            # self._track_pos[1] = -self._track_body_dim[1] - ((self._track_wheel_radius+self._track_dim[2])*math.cos(0.0174532925*self._track_body_rotation))
            # self._track_pos[2] = (self._track_wheel_radius+self._track_dim[2]) + (self._track_wheel_radius+self._track_dim[2])*math.sin(0.0174532925*self._track_body_rotation)
        elif self._state == 'front':
            #print ('estmated angle',self._track_body_rotation + angle)
            estimated = self._track_body_rotation + angle
            if estimated <= 90:
                diff = 90 - estimated
                dist = (diff * (math.pi*di))/360
                self._last_state = self._state
                self._state = 'up' 
                #dist_x = round((self._track_wheel_radius+self._track_dim[2])*math.cos(0.0174532925*diff),5)
                self._track_body_rotation = 90
                self._track_pos[1] = self._track_body_dim[1] - dist
                self._track_pos[2] = di
               # print('execeed',diff,dist,self._track_body_rotation)
            elif estimated >= 270:
                diff = estimated - 270
                dist = (diff * (math.pi*di))/360
                self._last_state = self._state
                self._state = 'down' 
                #dist_x = round((self._track_wheel_radius+self._track_dim[2])*math.cos(0.0174532925*diff),5)
                self._track_body_rotation = 270
                self._track_pos[1] = self._track_body_dim[1] - dist
                self._track_pos[2] = 0
                #print('execeed',diff,dist,self._track_body_rotation)
            else:
                self._track_body_rotation += angle 
                dist_x = (self._track_wheel_radius+self._track_dim[2])*math.cos(0.0174532925*self._track_body_rotation)
                dist_y = (self._track_wheel_radius+self._track_dim[2])*math.sin(0.0174532925*self._track_body_rotation)
                
                self._track_pos[1] -=  dist_x - self._last_track_pos[1]
                self._track_pos[2] +=  dist_y - self._last_track_pos[2]
                self._last_track_pos[1] = dist_x
                self._last_track_pos[2] = dist_y
            #dist_x = (self._track_wheel_radius+self._track_dim[2])*math.cos(0.0174532925*self._track_body_rotation)
            #dist_y = (self._track_wheel_radius+self._track_dim[2])*math.sin(0.0174532925*self._track_body_rotation)
            
            #self._track_pos[1] -= dist_x - self._last_track_pos[1]
            #self._track_pos[2] +=  dist_y - self._last_track_pos[2]
            #self._last_track_pos[1] = dist_x
            #self._last_track_pos[2] = dist_y
            # self._track_pos[1] = self._track_body_dim[1] - ((self._track_wheel_radius+self._track_dim[2])*math.cos(0.0174532925*self._track_body_rotation))
            # self._track_pos[2] = (self._track_wheel_radius+self._track_dim[2]) + (self._track_wheel_radius+self._track_dim[2])*math.sin(0.0174532925*self._track_body_rotation)
        if abs(self._track_pos[1]) < abs(self._track_body_dim[1]) and abs(self._track_pos[2]) > self._track_body_dim[2]/2:
            self._last_state = self._state
            self._state = 'up'
            #print(self._state,self._last_state)
            self._track_body_rotation = 90
        elif abs(self._track_pos[1]) < abs(self._track_body_dim[1]) and abs(self._track_pos[2]) <= self._track_body_dim[2]/2:
            self._last_state = self._state
            self._state = 'down'
            self._track_body_rotation = 270
        elif self._track_pos[1] > 0:
            self._last_state = self._state
            self._state = 'front'
        elif self._track_pos[1] < 0:
            self._last_state = self._state
            self._state = 'rear'

        c_x = ((self._track_wheel_radius+self._track_dim[2])*math.cos(0.0174532925*self._track_body_rotation))
        c_y = ((self._track_wheel_radius+self._track_dim[2])*math.sin(0.0174532925*self._track_body_rotation))
        #print("current x,y,state,l_state: ",self._track_pos[1],self._track_pos[2],self._state,self._last_state)
        #print(self._state,self._last_state,deg_limit,self._track_body_rotation,self._track_rotation,self._track_pos[1],self._track_body_dim[1])
        #print(self._track_pos[1],self._track_pos[2],self._track_body_dim[1],self._track_body_dim[2],self._state,self._last_state,self._track_body_rotation,c_x)
        # else:
        #     #ang_x = (90 / deg_limit) * self._track_rotation
        #     ang_x = 0
        #     if self._track_rotation >= 0 and self._track_rotation <= 90:
        #         ang_x = (90 / deg_limit) * self._track_rotation  
        #         self._track_body_rotation = -(90-ang_x)
        #         cross_x = self._track_wheel_radius*math.cos(0.0174532925*ang_x)
        #         cross_y = self._track_wheel_radius*math.sin(0.0174532925*ang_x)
        #         cross_y = cross_y+self._track_wheel_radius
        #         self._track_pos[1] = -self._track_body_dim[1]-cross_x
        #         self._track_pos[2] = cross_y          
        #     elif self._track_rotation > 90 and self._track_rotation <= 180:
        #         ang_x = (90 / deg_limit) * (180 - self._track_rotation)
        #         cross_x = -self._track_wheel_radius*math.cos(0.0174532925*ang_x)
        #         cross_y = self._track_wheel_radius*math.sin(0.0174532925*ang_x)
        #         cross_y = cross_y+self._track_wheel_radius
        #         self._track_pos[1] = self._track_body_dim[1]-cross_x
        #         self._track_pos[2] = cross_y  
        #         self._track_body_rotation = 90 - ang_x  
                  
        #     elif self._track_rotation > 180 and self._track_rotation <= 270:
        #         ang_x = (90 / deg_limit) * (90- (270 - self._track_rotation))
        #         cross_x = -self._track_wheel_radius*math.cos(0.0174532925*ang_x)
        #         cross_y = -self._track_wheel_radius*math.sin(0.0174532925*ang_x)
        #         cross_y = cross_y+self._track_wheel_radius
        #         self._track_pos[1] = self._track_body_dim[1]-cross_x
        #         self._track_pos[2] = cross_y   
        #         self._track_body_rotation = -(90-ang_x )
                
        #     elif self._track_rotation > 270 and self._track_rotation < 360:
        #         ang_x = (90 / deg_limit) * (360 - self._track_rotation)
        #         cross_x = self._track_wheel_radius*math.cos(0.0174532925*ang_x)
        #         cross_y = -self._track_wheel_radius*math.sin(0.0174532925*ang_x)
        #         cross_y = cross_y+self._track_wheel_radius
        #         self._track_pos[1] = -self._track_body_dim[1]-cross_x
        #         self._track_pos[2] = cross_y        
        #         self._track_body_rotation = 90 - ang_x  
                
        #         #ang_x = (270 / (360-deg_limit)) * self._track_rotation 
            
            
        #     # far_x = di + self._track_wheel_radius
        #     # cross_x = self._track_wheel_radius - (far_x - abs(far_x*math.cos(0.0174532925*self._track_rotation)))
                
            
                  
        #     # cross_y = self._track_wheel_radius*math.sin(ang_x) 
        #     #print('curve',ang_x,cross_x,cross_y)

        #     #self._track_pos[2] = self._track_wheel_radius * self.
        # print(self._track_pos[1],di,self._track_rotation,deg_limit)

class CannonBall:
    sphere = gluNewQuadric()
  
    def __init__(self):
        self._shooting_velocity = 100
        self._gravity = 9.8
        self._pos = [0,0,0]     
        self._initial_pos = [0,0,0]   
        self._radius = 1
        self._heading = 0
        self._angle = 0
        self._time = 0.00000000000000000000000001
        self._velocity_h = 0
        self._velocity_v = 0
        self._is_shooted = False
        self._is_exploded = False
        self._exploding_frame = 0
    def set_initial_velocity(self,velocity):
        self._shooting_velocity = velocity
        self._velocity_h = velocity*math.cos(0.0174532925*self._angle)
        self._velocity_v = velocity*math.sin(0.0174532925*self._angle)
        #print(self._pos,self._velocity_h,self._velocity_v)


    def compute(self,enemy_pos):
        
        
        self._pos = [   self._initial_pos[0]+(self._velocity_h*self._time*math.sin(0.0174532925*self._heading)),
                        self._initial_pos[1]+(self._velocity_h*self._time*math.cos(0.0174532925*self._heading)), 
                        self._initial_pos[2]+(self._velocity_v*self._time - 0.5*self._gravity*math.pow(self._time,2))]
        self._velocity_v = self._velocity_v - self._gravity*self._time

        self._time += 0.01
        
        error_dist = 7.5
        # hit the enemy
        is_enemy_hitted = (abs(self._pos[0] - enemy_pos[0]) < error_dist) and (abs(self._pos[1] - enemy_pos[1]) < error_dist) and (abs(self._pos[2] - enemy_pos[2]) < error_dist*2)
        
        # hit the building
        if (self._pos[2] <= 0) or ((self._pos[1] <= 105) and (self._pos[1] > 65) and (self._pos[0] > -20) and (self._pos[0] <= 20) and (self._pos[2] <= 50)) or is_enemy_hitted:
            self._is_shooted = False
            self._is_exploded = True
            print('hit')
        
        print(self._pos,self._initial_pos,self._angle,is_enemy_hitted)
        return is_enemy_hitted

class Axis:
    def draw():
        #draw axes lines
        glBegin(GL_LINES)
        glColor3f(1.0, 0.0, 0.0)
        glVertex3f(-3.0, 0.0, 0.0)
        glVertex3f(3.0, 0.0, 0.0)
        glColor3f(0.0, 1.0, 0.0)
        glVertex3f(0, -3.0, 0.0)
        glVertex3f(0, 3.0, 0.0)
        glColor3f(0.0, 0.0, 1.0)
        glVertex3f(0, 0.0, -3.0)
        glVertex3f(0, 0.0, 3.0)
        glEnd()