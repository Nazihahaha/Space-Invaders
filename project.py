from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import math
import random
import time

W_Width, W_Height = 500, 700


class dimensions:
    x = 0
    y = 0
    w = 0
    h = 0

    def __init__(self, x, y, w, h):
        self.x, self.y, self.w, self.h = x, y, w, h


class FireProjectile:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.radius = 5  # Adjust size as needed
        self.speed = 1  # Adjust speed as needed


fire_projectiles = []  # List to store fire projectile objects

shooter_radius = 15

shooter = dimensions(40, 20, 30, 20)  # catcher
arrow = dimensions(10, 660, 35, 35)  # arrow
pause_icon = dimensions(230, 660, 35, 35)  # pause
cross_icon = dimensions(450, 660, 35, 35)  # cross
collision = False
score = 0
shooter_frozen = False
circle_falling = True
pause = False
circles_frozen = False


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


def convert(original_zone, x, y):
    if (original_zone == 0):
        return x, y
    elif (original_zone == 1):
        return y, x
    elif (original_zone == 2):
        return -y, x
    elif (original_zone == 3):
        return -x, y
    elif (original_zone == 4):
        return -x, -y
    elif (original_zone == 5):
        return -y, -x
    elif (original_zone == 6):
        return -y, x
    elif (original_zone == 7):
        return x, -y


def convert_back(original_zone, x, y):
    if (original_zone == 0):
        return x, y
    elif (original_zone == 1):
        return y, x
    elif (original_zone == 2):
        return -y, -x
    elif (original_zone == 3):
        return -x, y
    elif (original_zone == 4):
        return -x, -y
    elif (original_zone == 5):
        return -y, -x
    elif (original_zone == 6):
        return y, -x
    elif (original_zone == 7):
        return x, -y


def midpoint_algo(zone, x1, y1, x2, y2):
    dx = abs(x2 - x1)
    dy = abs(y2 - y1)
    d = 2 * dy - dx
    incE = 2 * dy
    incNE = 2 * (dy - dx)

    y = y1
    x = x1
    for x in range(x1, x2 + 1):
        conv_x1, conv_y1 = convert_back(zone, x, y)
        glVertex2f(conv_x1, conv_y1)

        if d > 0:
            d = d + incNE
            y = y + 1
            x = x + 1
        else:
            d = d + incE
            x = x + 1


def eight_way_symmetry(x1, y1, x2, y2):
    x1 = int(x1)
    y1 = int(y1)
    x2 = int(x2)
    y2 = int(y2)
    zone = find_line_zone(x1, y1, x2, y2)
    converted_x1, converted_y1 = convert(zone, x1, y1)
    converted_x2, converted_y2 = convert(zone, x2, y2)
    midpoint_algo(zone, converted_x1, converted_y1, converted_x2, converted_y2)


def draw_box(box):
    global collision, arrow, pause_icon, cross_icon, shooter, W_Height, shooter_radius

    glBegin(GL_POINTS)
    x1, y1 = box.x, box.y  # Top-left corner
    x2, y2 = box.x + box.w, box.y  # Top-right corner
    x3, y3 = box.x + box.w, box.y + box.h  # Bottom-right corner
    x4, y4 = box.x, box.y + box.h  # Bottom-left corner

    if box == shooter:
        glColor3f(1.0, 0.5, 0.0)  # amber color for the shooter
        # Draw the shooter's shape
        eight_way_symmetry(x4, y4, x1, y1)
        eight_way_symmetry(x3, y4, x2, y2)
        eight_way_symmetry((x4+x2)//2, y4+ 20, x3, y4)
        eight_way_symmetry((x4+x2)//2, y4+ 20, x4, y4)
        eight_way_symmetry((x4+x2)//2, y2+ 10, x1, y1)
        eight_way_symmetry((x4+x2)//2, y2+ 10, x3, y1)
        glColor3f(1.0, 1.0, 1.0)
        eight_way_symmetry((x4+x2)//2, y2+ 8, (x4+x2)//2, y1)
        eight_way_symmetry(((x4 + x2) // 2)+3, y2 + 6, ((x4 + x2) // 2)+ 3, y1)
        eight_way_symmetry(((x4 + x2) // 2) - 3, y2 + 6, ((x4 + x2) // 2) - 3, y1)



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
        if pause != True:  # pause
            glColor3f(1.0, 0.75, 0.0)
            eight_way_symmetry(x1, y4, x1, y1)
            eight_way_symmetry(x3 - 20, y4, x1 + 15, y1)
        else:
            glColor3f(1.0, 0.75, 0.0)  # play
            eight_way_symmetry(x1, y4, x1, y1)
            eight_way_symmetry(x1, y4, x3, (y2 + y3) // 2)
            eight_way_symmetry(x1, y1, x3, (y2 + y3) // 2)

    glEnd()

#def shooter():

def show_screen():
    global W_Width, W_Height, fire_projectiles, shooter_radius
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()

    draw_box(shooter)
    draw_box(arrow)
    draw_box(pause_icon)
    draw_box(cross_icon)

    glColor3f(255, 191, 0)
    glPointSize(2)

    glutSwapBuffers()


# def animation():
#     global last_circle_spawn_time, circle_spawn_interval, shooter_frozen, missed_circles_count,  fire_projectiles, circle_frozen

#     current_time = time.time()

#     # Check if it's time to spawn a new circle
#     if shooter_frozen:
#         return  # If shooter is frozen due to game over, do not update falling circles

#     if current_time - last_circle_spawn_time > circle_spawn_interval:
#         # Generate and add a new falling circle
#         falling_circles.append(FallingCircle())
#         last_circle_spawn_time = current_time

#     # Check for missed falling circles
#     for circle in falling_circles:
#         if circle.y - circle.radius < 30:
#             missed_circles_count += 1
#             falling_circles.remove(circle)


#     update_fire_projectiles()  # Update positions of fire projectiles
#     update_falling_circles()   # Update positions of falling circles
#     glutPostRedisplay()
def mouse_click(button, state, x, y):
    global pause, diamond, score, pause, shooter_frozen, collision, circles_frozen
    mx, my = x, W_Height - y

    if state == GLUT_DOWN and button == GLUT_LEFT_BUTTON:
        if cross_icon.x <= mx <= (cross_icon.x + cross_icon.w) and cross_icon.y <= my <= (cross_icon.y + cross_icon.h):
            print("Goodbye! Score:", score)
            glutLeaveMainLoop()
        elif pause_icon.x <= mx <= (pause_icon.x + pause_icon.w) and pause_icon.y <= my <= (
                pause_icon.y + pause_icon.h):
            pause = not pause
            if pause == False:
                shooter_frozen = False
                circles_frozen = False
            else:
                shooter_frozen = True
                circles_frozen = True

        elif arrow.x <= mx <= (arrow.x + arrow.w) and arrow.y <= my <= (
                arrow.y + arrow.h):  # Check if arrow button is clicked
            print("Starting Over")
            score = 0
            shooter_frozen = False
            circles_frozen = False
            missed_circles_count = 0
            pause = False


def initialize():
    glViewport(0, 0, W_Width, W_Height)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    glOrtho(0.0, W_Width, 0.0, W_Height, 0.0, 1.0)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()


glutInit()
glutInitDisplayMode(GLUT_RGBA | GLUT_DOUBLE | GLUT_DEPTH)
glutInitWindowSize(W_Width, W_Height)
glutInitWindowSize(500, 700)
glutInitWindowPosition(0, 0)
window = glutCreateWindow(b"shoot")

# glutIdleFunc(animation)
glutDisplayFunc(show_screen)
glutMouseFunc(mouse_click)

glEnable(GL_DEPTH_TEST)
initialize()
glutMainLoop()
