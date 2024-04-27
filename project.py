from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import math
import random
import time

W_Width, W_Height = 500, 700
ENEMY_SIZE = 30
NUM_ENEMIES = 1
count = 0
background_color_change_start_time = 0
diamond_speed = 0.01
health_cnt = 3
# Add the following imports at the beginning of your code
from collections import deque

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
diamond_x_init = 250
diamond = AABB(random.randint(5,W_Width-10 ), 640, 15, 18) # diamond


class Enemy:
    def __init__(self):
        self.x = random.randint(0, W_Width - ENEMY_SIZE)
        self.y = random.randint(W_Height, W_Height)  # Set initial y-coordinate
        self.speed = 0.1
        self.shooting = False
        self.shoot_cooldown = 2000  # Cooldown between shots in milliseconds
        self.last_shot_time = 0  # Time when the enemy last shot
        self.spawn_time = time.time()  # Store the time when the enemy was spawned
    def shoot(self):
        self.shooting = True
        self.last_shot_time = time.time()

    def update(self):
        if self.shooting and time.time() - self.last_shot_time > self.shoot_cooldown / 1000:
            bullets.append(Bullet(self.x + ENEMY_SIZE / 2, self.y - ENEMY_SIZE / 2))
            self.last_shot_time = time.time()

class Bullet:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.speed = 0.5




# List to hold enemy objects
enemies = []
enemy = None
last_enemy_time = time.time()
bullets = deque()  # Queue to hold bullets
bullet_speed = 0.2
BOSS = False
shooter_pass = True




class dimensions:
    x = 0
    y = 0
    w = 0
    h = 0

    def __init__(self, x, y, w, h):
        self.x, self.y, self.w, self.h = x, y, w, h


enemy_cnt = 0
def init():
    global enemy_cnt
    glClearColor(0.0, 0.0, 0.0, 1.0)

    # Initialize enemy ships
    for _ in range(NUM_ENEMIES):
        enemies.append(Enemy())
        enemy_cnt += 1


shooter = dimensions(40, 20, 30, 20)  # catcher
arrow = dimensions(10, 660, 35, 35)  # arrow
pause_icon = dimensions(230, 660, 35, 35)  # pause
cross_icon = dimensions(450, 660, 35, 35)  # cross
collision = False
shooter_frozen = False
circle_falling = True
pause = False
circles_frozen = False
diamond_colour = (random.uniform(10.0, 5.0), random.uniform(10.0, 5.0), random.uniform(10.0, 5.0))

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
boss_coming = False
Right = False
Left = False
shooter_bullet_cnt = 0
def updateEnemy():
    global enemy_y, enemy_x, Left, Right, shooter_bullet_cnt, shooter_pass, boss_coming
    if shooter_bullet_cnt == 10:
        shooter_pass = False
        if enemy_y >= -5:
            enemy_y -= 0.2
    if shooter_pass:
        if enemy_y >= 400:
            enemy_y -= 0.1
            boss_coming = True
            Left = True
            shooter_bullet_cnt = 0
        else:
            boss_coming = False
            if Left:
                if enemy_x >= 50:
                    enemy_x -= 0.2
                    #print("Left")
                    #print(enemy_x,"xL")
                else:
                    Right = True
                    Left = False
            if Right:
                if enemy_x<= 450:
                    enemy_x += 0.2
                else:
                    Left = True
                    Right = False
                #print(enemy_x,"xR")
# Define a function to draw bullets
def drawBullets():
    glColor3f(0.5, 1.0, 1.0)
    glPointSize(2.0)
    glBegin(GL_POINTS)
    for bullet in bullets:
        glVertex2f(bullet.x, bullet.y)
    glEnd()


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
spawn_enemies = True
# Function to update enemy positions
def updateEnemies():
    global W_Width, W_Height, enemies, spawn_enemies, BOSS
    enemies_to_remove = []


    for enemy in enemies:
        
        if enemy.y <= 10:
            enemies.remove(enemy)
        if enemy.y >= 0:
            enemy.y -= enemy.speed
            #print(enemy.y,"y")

        if enemy.y < 0:
            enemy.x = random.randint(0, W_Width - ENEMY_SIZE)
            enemy.y = random.randint(W_Height, W_Height + 200)
    if len(enemies)>20:
        spawn_enemies = False
        # Remove the enemy from the list of enemies
        #print(time.time())
        BOSS = True
        enemies.clear()

def check_collision_enemy_bullet(enemy_x, enemy_y, bullet_x, bullet_y, threshold):
    """
    Function to check collision between an enemy and a bullet.
    """
    distance_squared = (enemy_x - bullet_x) ** 2 + (enemy_y - bullet_y) ** 2
    # Compare the squared distance with the square of the threshold
    return distance_squared <= threshold ** 2



def updateBullets():
    global bullets, enemies
    threshold = 20
    # Iterate over copies of bullets
    for bullet in bullets.copy():
        bullet.y += bullet.speed

        # Iterate over copies of enemies
        for enemy in enemies.copy():
             if check_collision_enemy_bullet(enemy.x + ENEMY_SIZE / 2, enemy.y, bullet.x, bullet.y, threshold):
                bullets.remove(bullet)  # Remove bullet
                enemies.remove(enemy)  # Remove enemy

    # Remove bullets that have moved out of the screen
    bullets = [bullet for bullet in bullets if bullet.y <= W_Height]
# Function to handle shooting logic
def check_collision(enemy1, enemy2):
    """
    Function to check collision between two enemies.
    """
    # Calculate the distance between the centers of the two enemies
    distance = math.sqrt((enemy1.x - enemy2.x)**2 + (enemy1.y - enemy2.y)**2)
    # Check if the distance is less than the sum of their radii
    return distance < ENEMY_SIZE

def check_collision_shooter_enemy(shooter_x, shooter_y, enemy_x, enemy_y, threshold):
    distance_squared = (shooter_x - enemy_x) ** 2 + (shooter_y - enemy_y) ** 2
    return distance_squared <= threshold ** 2

# Function to handle collision between the shooter and enemies
def handle_collision_shooter():
    global shooter, enemies, collision, count, pause, background_color_change_start_time, health_cnt
    for enemy in enemies:
        if check_collision_shooter_enemy(shooter.x + shooter.w / 2, shooter.y + shooter.h / 2, enemy.x + ENEMY_SIZE / 2, enemy.y + ENEMY_SIZE / 2, shooter.w):

            collision = True
            enemies.remove(enemy)
            background_color_change_start_time = time.time()
            health_cnt -= 1
            print(background_color_change_start_time)

            count += 1
            print(background_color_change_start_time)

            if count == 3:
                pause = True
                print('over')

            return
    collision = False

    if time.time() - background_color_change_start_time <= 0.2:

        # print('red')
        #glClearColor(1.0, 0.0, 0.0, 0.0)
        pass
    else:
        # print('black')
        glClearColor(0.0, 0.0, 0.0, 1.0)
    glutPostRedisplay()

diamond_collided = False
def check_diamond_collision():
    global diamond, shooter, diamond_collided, background_color_change_start_time
    if diamond.y <= shooter.y and shooter.x < diamond.x <shooter.x + shooter.w:
        background_color_change_start_time = time.time()
        diamond_collided = True
        print("collided")

    if time.time() - background_color_change_start_time <= 0.2:

        # print('red')
        glClearColor(0.0, 1.0, 0.0, 0.0)
    else:
        # print('black')
        glClearColor(0.0, 0.0, 0.0, 1.0)
    glutPostRedisplay()



def shoot():
    global bullets
    bullet_x = shooter.x + shooter.w / 2
    bullet_y = shooter.y + shooter.h
    new_bullet = Bullet(bullet_x, bullet_y)
    bullets.append(new_bullet)


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
    global collision, arrow, pause_icon, cross_icon, shooter, W_Height, diamond

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

    if box == shooter:
        glColor3f(1.0, 0.5, 0.0)  # amber color for the shooter
        # Draw the shooter's shape
        eight_way_symmetry(x4, y4, x1, y1)
        eight_way_symmetry(x3, y4, x2, y2)
        eight_way_symmetry((x4 + x2) // 2, y4 + 20, x3, y4)
        eight_way_symmetry((x4 + x2) // 2, y4 + 20, x4, y4)
        eight_way_symmetry((x4 + x2) // 2, y2 + 10, x1, y1)
        eight_way_symmetry((x4 + x2) // 2, y2 + 10, x3, y1)
        glColor3f(1.0, 1.0, 1.0)
        eight_way_symmetry((x4 + x2) // 2, y2 + 8, (x4 + x2) // 2, y1)
        eight_way_symmetry(((x4 + x2) // 2) + 3, y2 + 6, ((x4 + x2) // 2) + 3, y1)
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




def keyboard(key, x, y):
    global shooter_radius, W_Width, shooter_bullet_cnt, boss_coming, shooter_pass
    if shooter_frozen:
        return  # If shooter is frozen, do not allow shooter movement

    elif key == b'a':  # Move left when 'a' key is pressed
        if shooter.x >= 20:  # Keep the shooter within the window bounds
            shooter.x -= 10

    elif key == b'd':  # Move right when 'd' key is pressed
        if shooter.x <= 455:  # Keep the shooter within the window bounds
            shooter.x += 10

    elif key == b' ':  # Shoot bullet when spacebar is pressed
        if not boss_coming and shooter_pass:
            shooter_bullet_cnt += 1
            shoot()
       

    glutPostRedisplay()  # Trigger a redraw to update


# Define a function to handle shooting logic
def shoot():
    global bullets, diamond_collided
    if not diamond_collided:
        bullet_x = shooter.x + shooter.w / 2
        bullet_y = shooter.y + shooter.h
        new_bullet = Bullet(bullet_x, bullet_y)
        bullets.append(new_bullet)
    else:
        print("THIS")
        bullet_x1 = shooter.x 
        bullet_y = shooter.y + shooter.h
        bullet_x2 = shooter.x + shooter.w
        new_bullet1 = Bullet(bullet_x1, bullet_y)
        new_bullet2 = Bullet(bullet_x2, bullet_y)
        bullets.append(new_bullet1)
        bullets.append(new_bullet2)

def updateDiamond():
    global diamond_speed
    if diamond.y > -20:
        diamond.y -= 0.1

def mouse_click(button, state, x, y):
    global pause, pause, shooter_frozen, collision, enemies, enemy_cnt
    mx, my = x, W_Height - y

    if state == GLUT_DOWN and button == GLUT_LEFT_BUTTON:
        if cross_icon.x <= mx <= (cross_icon.x + cross_icon.w) and cross_icon.y <= my <= (cross_icon.y + cross_icon.h):
            glutLeaveMainLoop()
        elif pause_icon.x <= mx <= (pause_icon.x + pause_icon.w) and pause_icon.y <= my <= (pause_icon.y + pause_icon.h):
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
            diamond.x = diamond_x_init
            diamond.y = 640
            pause = False
            enemy_cnt = 0
            enemies.clear()
def draw_circle(x,y,r):
    global shooter_frozen
    x_p = 0
    y_p = r
    d = 1 - r
    
    
    while x_p <= y_p:

        glVertex2f(x_p + x, y_p + y)
        glVertex2f(-x_p + x, y_p + y)
        #glVertex2f(x_p + x, -y_p + y)
        #glVertex2f(-x_p + x, -y_p + y)
        glVertex2f(y_p+ x, x_p + y)
        glVertex2f(-y_p + x, x_p + y)
        #glVertex2f(y_p + x, -x_p + y)
        #glVertex2f(-y_p + x, -x_p + y)

        forSE = 2*(x_p-y_p)+5
        forE = (2*x_p) +3 

        
        if d >= 0:
            x_p += 1
            y_p -= 1
            d += forSE
        else:
            x_p += 1
            d += forE

def draw_health(dx, dy, color):
    glBegin(GL_POINTS)
    x, y = 270, 660
    glColor3f(255, 191, 0)
    eight_way_symmetry(x+dx, y-dy, x+dx+15, y+dy)
    eight_way_symmetry(x+dx-15, y+dy, x+dx, y-dy)
    draw_circle(x+dx+7.5, y+dy, 7.5)
    draw_circle(x+dx-7.5, y+dy, 7.5)

    glEnd()

# Define a variable to keep track of the elapsed time
start_time = time.time()

# Set a threshold time after which you want to increase the enemy count
threshold_time = 20
def show_screen():
    global W_Width, W_Height, BOSS, shooter_bullet_cnt, enemies, enemy_cnt, health_cnt
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()

    draw_box(shooter)
    draw_box(arrow)
    draw_box(pause_icon)
    draw_box(cross_icon)

    glColor3f(255, 191, 0)
    glPointSize(2)

    drawEnemies()
    drawBullets()

    for i in range(health_cnt):
        draw_health(60 + (i*40), 8, (1.0, 0, 0))

    if BOSS:
        draw_enemy_spaceship()
        #print(shooter_bullet_cnt)

    if enemy_cnt > 2:
        draw_box(diamond)

    glutSwapBuffers()
def animation():
    global enemy, last_enemy_time, start_time, NUM_ENEMIES, shooter, collision,spawn_enemies, BOSS, enemies, enemy_cnt

    if not pause:

        handle_collision_shooter()
        check_diamond_collision()

        # Calculate the elapsed time
        elapsed_time = time.time() - start_time

        # Check if the elapsed time exceeds the threshold
        if elapsed_time > threshold_time:

            # Increase the enemy count
            NUM_ENEMIES += 1
            print("Enemy count increased to:", NUM_ENEMIES)

            # Reset the start time to the current time
            start_time = time.time()

        updateEnemies()  # Call the updateEnemies function here

        # Update the enemy positions
        current_time = time.time()
        if spawn_enemies and current_time - last_enemy_time > 2:  # Adjust interval as needed
            for _ in range(NUM_ENEMIES):  # Spawn multiple enemies
                new_enemy = Enemy()
                # Check for collision with existing enemies
                while any(check_collision(new_enemy, existing_enemy) for existing_enemy in enemies):
                    new_enemy = Enemy()  # Generate a new enemy until no collision occurs
                enemies.append(new_enemy)  # Append new enemies to the enemies list
                enemy_cnt += 1
            last_enemy_time = current_time
        updateBullets()  # Update bullet positions
        #updateDiamond()
        if enemy_cnt >2:
            updateDiamond()
        if BOSS:
            updateEnemy()
        

    glutPostRedisplay()



def initialize():
    glViewport(0, 0, W_Width, W_Height)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    glOrtho(0.0, W_Width, 0.0, W_Height, 0.0, 1.0)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()


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


glutInit()
glutInitDisplayMode(GLUT_RGBA | GLUT_DOUBLE | GLUT_DEPTH)
glutInitWindowSize(W_Width, W_Height)
glutInitWindowSize(500, 700)
glutInitWindowPosition(0, 0)
window = glutCreateWindow(b"shoot")


glutDisplayFunc(show_screen)
glutIdleFunc(animation)

glutReshapeFunc(reshape)
glutKeyboardFunc(keyboard)
glutMouseFunc(mouse_click)

glEnable(GL_DEPTH_TEST)
initialize()
init()
glutMainLoop()
