from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import math
import random
import time
diamond_colour = (random.uniform(10.0, 5.0), random.uniform(10.0, 5.0), random.uniform(10.0, 5.0))
collision = False
W_Width, W_Height = 500,700

class dimensions:
    x = 0
    y = 0
    w = 0
    h = 0 

    def __init__(self, x, y, w, h):
        self.x, self.y, self.w, self.h = x, y, w, h


arrow = dimensions(10, 660, 35, 35) # arrow
pause_icon = dimensions(230, 660, 35, 35) #pause
cross_icon = dimensions(450, 660, 35, 35) #cross

pause = False

class AABB:
    x = 0
    y = 0
    w = 0
    h = 0 

    def __init__(self, x, y, w, h):
        self.x, self.y, self.w, self.h = x, y, w, h
    
    def collides_with(box1, box2):
        return (box1.x < box2.x + box2.w and # x_min_1 < x_max_2
                box1.x + box1.w > box2.x  and # x_max_1 > m_min_2
                box1.y < box2.y + box2.h and # y_min_1 < y_max_2
                box1.y + box1.h > box2.y)     # y_max_1 > y_min_2

# Global variables
diamond = AABB(random.randint(5,W_Width-10 ), 640, 15, 18) # diamond

def find_line_zone(x1, y1, x2, y2):
    dx = x2 - x1
    dy = y2 - y1
    zone = 0

    if abs(dx) < abs(dy):
        if dx > 0 and dy > 0:
            zone = 1
        elif dx < 0 and dy > 0:
            zone = 2
        elif dx < 0 and dy < 0:
            zone = 5
        else:
            zone = 6
    else:
        if dx > 0 and dy > 0:
            zone = 0
        elif dx < 0 and dy > 0:
            zone = 3
        elif dx < 0 and dy < 0:
            zone = 4
        else:
            zone = 7
    return zone

def convert(original_zone,x,y) :

    if (original_zone == 0) :
        return x,y
    elif (original_zone == 1) :
        return y,x
    elif (original_zone == 2) :
        return -y,x
    elif (original_zone == 3) :
        return -x,y
    elif (original_zone == 4) :
        return -x,-y
    elif (original_zone == 5) :
        return -y,-x
    elif (original_zone == 6) :
        return -y,x
    elif (original_zone == 7) :
        return x,-y


def convert_back(original_zone,x,y) :

    if (original_zone == 0) :
        return x,y
    elif (original_zone == 1) :
        return y,x
    elif (original_zone == 2) :
        return -y,-x
    elif (original_zone == 3) :
        return -x,y
    elif (original_zone == 4) :
        return -x,-y
    elif (original_zone == 5) :
        return -y,-x
    elif (original_zone == 6) :
        return y,-x
    elif (original_zone == 7) :
        return x,-y
   
def midpoint_algo(zone, x1 , y1, x2, y2 ):
    dx = abs(x2 - x1)
    dy = abs(y2 - y1)
    d = 2*dy-dx
    incE = 2*dy
    incNE = 2*(dy-dx)

    y = y1
    x = x1
    for x in range(x1, x2 + 1):
        conv_x1 , conv_y1 = convert_back(zone,x,y)
        glVertex2f(conv_x1, conv_y1)

        if d>0:
            d = d+incNE
            y = y+1
            x = x + 1
        else:
            d = d+incE
            x = x + 1


def eight_way_symmetry(x1,y1,x2,y2) :

    x1 = int(x1)
    y1 = int(y1)
    x2 = int(x2)
    y2 = int(y2)
    zone = find_line_zone(x1,y1,x2,y2)
    converted_x1, converted_y1 = convert(zone,x1,y1)
    converted_x2, converted_y2 = convert(zone,x2,y2)
    midpoint_algo(zone,converted_x1,converted_y1,converted_x2,converted_y2) 


def draw_box(box):
    global collision, diamond, catcher, arrow, pause_icon, cross_icon, diamond_colour

    glBegin(GL_POINTS)
    x1, y1 = box.x, box.y  # Top-left corner
    x2, y2 = box.x + box.w, box.y  # Top-right corner
    x3, y3 = box.x + box.w, box.y + box.h  # Bottom-right corner
    x4, y4 = box.x, box.y + box.h  # Bottom-left corner

    if collision:
       glColor3f(0.0, 0.0, 0.0)  # The diamond disappearing
    else:
       glColor3f(diamond_colour[0], diamond_colour[1], diamond_colour[2])

    if box == diamond:  # if diamond
        eight_way_symmetry(x1, (y1 + y4) // 2, (x1 + x2) // 2, y4)
        eight_way_symmetry((x1 + x2) // 2, y4, x3, (y4 + y1) // 2)
        eight_way_symmetry(x3, (y4 + y1) // 2, (x1 + x3) // 2, y1)
        eight_way_symmetry(x4, (y4+y1)//2, (x3+x4)//2, y1)

    if collision:
        glColor3f(1.0, 0.0, 0.0)
    else:
        glColor3f(0.0, 1.0, 0.0)
   
    if box == arrow:  # if arrow
        glColor3f(0.0, 0.5, 0.5)
        eight_way_symmetry(x1, (y1 + y4) // 2, (x1 + x2) // 2, y4)
        eight_way_symmetry(x1, (y4 + y1) // 2, (x1 + x3) // 2, y1)
        eight_way_symmetry(x1, (y1 + y4) // 2, x3, (y2 + y3) // 2)

    if box == cross_icon:  # if cross
        glColor3f(1.0, 0.0, 0.0)
        eight_way_symmetry(x1, y1, x3, y3)
        eight_way_symmetry(x4, y4, x2, y2)

    if box == pause_icon:
        if pause != True: # pause
            glColor3f(1.0, 0.75, 0.0)
            eight_way_symmetry(x1, y4, x1, y1)
            eight_way_symmetry(x3 - 20, y4, x1 + 15, y1)
        else:
            glColor3f(1.0, 0.75, 0.0)  #play
            eight_way_symmetry(x1, y4, x1, y1)
            eight_way_symmetry(x1, y4, x3, (y2 + y3) // 2)
            eight_way_symmetry(x1, y1, x3, (y2 + y3) // 2)

    glEnd()


def draw_circle(x,y,r):
    global shooter_frozen
    x_p = 0
    y_p = r
    d = 1 - r
    
    
    while x_p <= y_p:

        glVertex2f(x_p + x, y_p + y)
        glVertex2f(-x_p + x, y_p + y)
        glVertex2f(x_p + x, -y_p + y)
        glVertex2f(-x_p + x, -y_p + y)
        glVertex2f(y_p+ x, x_p + y)
        glVertex2f(-y_p + x, x_p + y)
        glVertex2f(y_p + x, -x_p + y)
        glVertex2f(-y_p + x, -x_p + y)

        forSE = 2*(x_p-y_p)+5
        forE = (2*x_p) +3 

        
        if d >= 0:
            x_p += 1
            y_p -= 1
            d += forSE
        else:
            x_p += 1
            d += forE


# Mouse callback function
def mouse_click(button, state, x, y):
    global  pause , diamond ,score ,  pause , shooter_frozen , collision, enemies
    mx, my = x, W_Height - y
    
    if state == GLUT_DOWN and button == GLUT_LEFT_BUTTON:
        if cross_icon.x <= mx <= (cross_icon.x + cross_icon.w) and cross_icon.y <= my <= (cross_icon.y + cross_icon.h):
            glutLeaveMainLoop()
        elif pause_icon.x <= mx <= (pause_icon.x + pause_icon.w) and pause_icon.y <= my <= (pause_icon.y + pause_icon.h):
              pause = not pause
              if pause == False :
                shooter_frozen = False
                circles_frozen = False
              else:
                shooter_frozen = True
                circles_frozen = True

        elif arrow.x <= mx <= (arrow.x + arrow.w) and arrow.y <= my <= (arrow.y + arrow.h):  # Check if arrow button is clicked
            print("Starting Over")
            score = 0
            enemies.clear()
            fire_projectiles.clear()
            shooter_frozen = False
            circles_frozen = False
            missed_circles_count = 0
            pause = False
 


# Keyboard callback function to handle key presses
def keyboard(key, x, y):
    global shooter_radius, W_Width, fire_projectiles
    if shooter_frozen:
        return  # If shooter is frozen, do not allow shooter movement

    if key == b' ':  # Spacebar key
        new_projectile = FireProjectile(shooter.x  , shooter_radius +shooter.y) 
        fire_projectiles.append(new_projectile)

    elif key == b'a':  # Move left when 'a' key is pressed
        if shooter.x >= 25 :  # Keep the shooter within the window bounds
            shooter.x -= 10

    elif key == b'd':  # Move right when 'd' key is pressed
        if shooter.x <= 475:  # Keep the shooter within the window bounds
            shooter.x += 10
    glutPostRedisplay()  # Trigger a redraw to update

misfires_count = 0


enemy_x = 250  # X-coordinate of the center of the enemy spaceship
enemy_y = 600  # Y-coordinate of the center of the enemy spaceship


def draw_enemy_spaceship():
    # Define the dimensions of the enemy spaceship
    global enemy_x, enemy_y
    body_width = 80  # Width of the body of the enemy spaceship
    body_height = 40  # Height of the body of the enemy spaceship
    wing_width = 30  # Width of the wings of the enemy spaceship
    wing_height = 20  # Height of the wings of the enemy spaceship
    front_height = 30  # Height of the front part of the enemy spaceship
    
    glBegin(GL_POINTS)
    glColor3f(1.0, 0.0, 0.0)  # Set color to red
    
    # Draw the body of the enemy spaceship
    x1 = enemy_x - (body_width // 2)
    y1 = enemy_y
    x2 = enemy_x + (body_width // 2)
    y2 = enemy_y
    mid_x = (x1+x2)/2
    mid_y = (y1+y2)/2 - 48
    eight_way_symmetry(x1, y1, x2, y2)  # Draw a horizontal line for body
    
    x1 = enemy_x - (body_width // 2)
    y1 = enemy_y
    x2 = enemy_x - (body_width // 2)
    y2 = enemy_y - body_height
    eight_way_symmetry(x1, y1, x2, y2)  # Draw left edge of body

                                          # Draw vertical lines for left and right edges of the body
    x1 = enemy_x - (body_width // 2.5)
    y1 = enemy_y
    x2 = enemy_x - (body_width // 2.5)
    y2 = enemy_y - body_height
    l_mid_x = (x1+x2)/2
    l_mid_y = (y1+y2)/2
    eight_way_symmetry(x1, y1, x2, y2)  # Draw left vertical line

    x1 = enemy_x - (body_width // 2)
    y1 = enemy_y - body_height
    x2 = enemy_x - (body_width // 2.5)
    y2 = enemy_y - body_height
    eight_way_symmetry(x1, y1, x2, y2)

   
    x1 = enemy_x + (body_width // 2)
    y1 = enemy_y
    x2 = enemy_x + (body_width // 2)
    y2 = enemy_y - body_height
    eight_way_symmetry(x1, y1, x2, y2)  # Draw right edge of body
     
    x1 = enemy_x + (body_width // 2.5)
    y1 = enemy_y
    x2 = enemy_x + (body_width // 2.5)
    y2 = enemy_y - body_height
    r_mid_x = (x1+x2)/2
    r_mid_y = (y1+y2)/2
    eight_way_symmetry(x1, y1, x2, y2)  # Draw right vertical line

    x1 = enemy_x + (body_width // 2.5)
    y1 = enemy_y - body_height
    x2 = enemy_x + (body_width // 2)
    y2 = enemy_y - body_height
    eight_way_symmetry(x1, y1, x2, y2)

    x1 = r_mid_x
    y1 = r_mid_y
    x2 = mid_x
    y2 = mid_y
    eight_way_symmetry(x1, y1, x2, y2)

    x1 = r_mid_x 
    y1 = r_mid_y - 10
    x2 = mid_x
    y2 = mid_y - 10
    eight_way_symmetry(x1, y1, x2, y2)

    x1 = l_mid_x
    y1 = l_mid_y
    x2 = mid_x
    y2 = mid_y
    eight_way_symmetry(x1, y1, x2, y2)

    x1 = l_mid_x 
    y1 = l_mid_y - 10
    x2 = mid_x
    y2 = mid_y - 10
    eight_way_symmetry(x1, y1, x2, y2)
    
    glEnd()     
Right = False
Left = False
def updateEnemy():
    global enemy_y, enemy_x, Left, Right
    if enemy_y >= 400:
        enemy_y -= 0.1
        #print(enemy_y,"y")
        Left = True
    else:
        if Left:
            if enemy_x >= 50:
                enemy_x -= 0.1
                print("Left")
                print(enemy_x,"xL")
            else:
                Right = True
                Left = False
        if Right:
            if enemy_x<= 450:
                enemy_x += 0.1
            else:
                Left = True
                Right = False
            print(enemy_x,"xR")

     

def show_screen():
    global W_Width, W_Height, fire_projectiles, shooter_radius
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()
    
    draw_box(arrow)
    draw_box(pause_icon)
    draw_box(cross_icon)
    draw_box(diamond)

    draw_enemy_spaceship()  # Draw the enemy spaceship

    glutSwapBuffers()


# Add updating of fire projectiles to the animation() function
last_circle_spawn_time = 0  # Variable to track the last time a circle was generated
circle_spawn_interval = 1  # Interval in seconds between circle spawns
def animation():
    global last_circle_spawn_time, circle_spawn_interval, shooter_frozen, missed_circles_count,  fire_projectiles, circle_frozen

    updateEnemy()

    glutPostRedisplay()


def initialize():
    glViewport(0, 0, W_Width, W_Height)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    glOrtho(0.0,W_Width, 0.0, W_Height, 0.0, 1.0)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()

glutInit()
glutInitDisplayMode(GLUT_RGBA | GLUT_DOUBLE | GLUT_DEPTH)
glutInitWindowSize(W_Width, W_Height)
glutInitWindowSize(500, 700)
glutInitWindowPosition(0, 0)
window = glutCreateWindow(b"shoot")

glutDisplayFunc(show_screen)
glutIdleFunc(animation)
glutKeyboardFunc(keyboard)
glutMouseFunc(mouse_click)

glEnable(GL_DEPTH_TEST)
initialize()
glutMainLoop()
