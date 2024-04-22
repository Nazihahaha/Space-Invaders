from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import math
import random
import time

W_Width, W_Height = 500, 700
ENEMY_SIZE = 30
NUM_ENEMIES = 1

# Add the following imports at the beginning of your code
from collections import deque
# Modify the Enemy class to include shooting mechanism

class Enemy:
    def __init__(self):
        self.x = random.randint(0, W_Width - ENEMY_SIZE)
        self.y = random.randint(W_Height, W_Height)  # Set initial y-coordinate
        self.speed = 0.05
        self.shooting = False
        self.shoot_cooldown = 2000  # Cooldown between shots in milliseconds
        self.last_shot_time = 0  # Time when the enemy last shot


class dimensions:
    x = 0
    y = 0
    w = 0
    h = 0

    def __init__(self, x, y, w, h):
        self.x, self.y, self.w, self.h = x, y, w, h


# List to hold enemy objects
enemies = []
enemy = None
last_enemy_time = time.time()
def init():
    glClearColor(0.0, 0.0, 0.0, 1.0)

    # Initialize enemy ships
    for _ in range(NUM_ENEMIES):
        enemies.append(Enemy())


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

# Function to draw enemy ships
# Function to draw enemy ships
def drawEnemies():
    glColor3f(0.0, 1.0, 0.0)
    for enemy in enemies:
        x = enemy.x
        y = enemy.y

        # Draw head
        glPointSize(2.0)
        glBegin(GL_POINTS)
        glVertex2f(x + ENEMY_SIZE / 2, y)
        glVertex2f(x, y - ENEMY_SIZE)
        glVertex2f(x + ENEMY_SIZE, y - ENEMY_SIZE)
        glEnd()

        # Draw eyes
        glColor3f(1.0, 1.0, 1.0)
        glBegin(GL_POINTS)
        for i in range(20):
            angle = math.radians(i * 10)
            glVertex2f(x + ENEMY_SIZE / 4 + math.cos(angle) * ENEMY_SIZE / 16, 
                       y - ENEMY_SIZE / 2 + math.sin(angle) * ENEMY_SIZE / 16)
            glVertex2f(x + ENEMY_SIZE * 3 / 4 + math.cos(angle) * ENEMY_SIZE / 16, 
                       y - ENEMY_SIZE / 2 + math.sin(angle) * ENEMY_SIZE / 16)
        glEnd()

        # Draw evil smile
        glColor3f(1.0, 0.0, 0.0)
        glBegin(GL_POINTS)
        for i in range(36):
            angle = math.radians(i * 10)
            glVertex2f(x + ENEMY_SIZE / 3 + math.cos(angle) * ENEMY_SIZE / 12, 
                       y - ENEMY_SIZE * 2 / 3 + math.sin(angle) * ENEMY_SIZE / 12)
            glVertex2f(x + ENEMY_SIZE * 2 / 3 + math.cos(angle) * ENEMY_SIZE / 12, 
                       y - ENEMY_SIZE * 2 / 3 + math.sin(angle) * ENEMY_SIZE / 12)
        glEnd()

# Function to update enemy positions
# Define the enemy object globally
# Function to handle window resizing
def reshape(w, h):
    glViewport(0, 0, w, h)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluOrtho2D(0, w, 0, h)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()

# Function to display content
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


def show_screen():
    global W_Width, W_Height
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()

    draw_box(shooter)
    draw_box(arrow)
    draw_box(pause_icon)
    draw_box(cross_icon)

    glColor3f(255, 191, 0)
    glPointSize(2)
    
    drawEnemies()

    glutSwapBuffers()


def keyboard(key, x, y):
    global shooter_radius, W_Width
    if shooter_frozen:
        return  # If shooter is frozen, do not allow shooter movement

    elif key == b'a':  # Move left when 'a' key is pressed
        if shooter.x >= 20 :  # Keep the shooter within the window bounds
            shooter.x -= 10

    elif key == b'd':  # Move right when 'd' key is pressed
        if shooter.x <= 455:  # Keep the shooter within the window bounds
            shooter.x += 10
    glutPostRedisplay()  # Trigger a redraw to update


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

def updateEnemies():
    global W_Width, W_Height, enemies
  
    for enemy in enemies:
        enemy.y -= enemy.speed

        if enemy.y < 0:
            enemy.x = random.randint(0, W_Width - ENEMY_SIZE)
            enemy.y = random.randint(W_Height, W_Height + 200)
        
# Define a variable to keep track of the elapsed time
start_time = time.time()

# Set a threshold time after which you want to increase the enemy count
threshold_time = 20  # Adjust this value as needed
def check_collision(enemy1, enemy2):
    """
    Function to check collision between two enemies.
    """
    # Calculate the distance between the centers of the two enemies
    distance = math.sqrt((enemy1.x - enemy2.x)**2 + (enemy1.y - enemy2.y)**2)
    # Check if the distance is less than the sum of their radii
    return distance < ENEMY_SIZE
def animation():
    global enemy, last_enemy_time, start_time, NUM_ENEMIES, shooter
    
    # Calculate the elapsed time
    elapsed_time = time.time() - start_time
    
    # Check if the elapsed time exceeds the threshold
    if elapsed_time > threshold_time:
        print(elapsed_time, threshold_time)
        # Increase the enemy count
        NUM_ENEMIES += 1
        print("Enemy count increased to:", NUM_ENEMIES)
        
        # Reset the start time to the current time
        start_time = time.time()
    
    updateEnemies()  # Call the updateEnemies function here
    
    # Update the enemy positions
    current_time = time.time()
    if current_time - last_enemy_time > 10:  # Adjust interval as needed
        for _ in range(NUM_ENEMIES):  # Spawn multiple enemies
            new_enemy = Enemy()
            # Check for collision with existing enemies
            while any(check_collision(new_enemy, existing_enemy) for existing_enemy in enemies):
                new_enemy = Enemy()  # Generate a new enemy until no collision occurs
            enemies.append(new_enemy)  # Append new enemies to the enemies list
        last_enemy_time = current_time

    for enemy in enemies:  # Update the positions of all enemies
        enemy.y -= enemy.speed

        if enemy.y < 0:
            enemy.x = random.randint(0, W_Width - ENEMY_SIZE)
            enemy.y = random.randint(W_Height, W_Height + 200)
       
    glutPostRedisplay()
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

glutIdleFunc(animation)
glutDisplayFunc(show_screen)

glutReshapeFunc(reshape)
glutKeyboardFunc(keyboard)
glutMouseFunc(mouse_click)

glEnable(GL_DEPTH_TEST)
initialize()
init()
glutMainLoop()
