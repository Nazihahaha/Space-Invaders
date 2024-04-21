import sys
import random
from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *

# Window dimensions
W_Width, W_Height = 500, 700

# Enemy Ship properties
ENEMY_SIZE = 10
NUM_ENEMIES = 10

class Enemy:
    def __init__(self):
        self.x = random.randint(0, W_Width - ENEMY_SIZE)
        self.y = random.randint(W_Height, W_Height + 100)
        self.speed = random.uniform(0.5, 1.5)

enemies = [Enemy() for _ in range(NUM_ENEMIES)]

# GUI Element dimensions
class dimensions:
    def __init__(self, x, y, w, h):
        self.x, self.y, self.w, self.h = x, y, w, h

# GUI elements
shooter = dimensions(40, 20, 30, 20)
arrow = dimensions(10, 660, 35, 35)
pause_icon = dimensions(230, 660, 35, 35)
cross_icon = dimensions(450, 660, 35, 35)

# Game states
collision = False
score = 0
pause = False

# Midpoint line algorithm
def draw_midpoint_line(x1, y1, x2, y2):
    dx = x2 - x1
    dy = y2 - y1
    d = dy - (dx/2)
    x = x1
    y = y1

    glBegin(GL_POINTS)
    glVertex2f(x, y)
    while x < x2:
        x += 1
        if d < 0:
            d = d + dy
        else:
            d += (dy - dx)
            y += 1
        glVertex2f(x, y)
    glEnd()

# Midpoint circle algorithm
def draw_midpoint_circle(cx, cy, r):
    x = r
    y = 0
    d = 1 - r
    glBegin(GL_POINTS)
    glVertex2f(cx + x, cy + y)
    if r > 0:
        glVertex2f(cx + x, cy - y)
        glVertex2f(cx + y, cy + x)
        glVertex2f(cx - y, cy + x)
    while x > y:
        y += 1
        if d <= 0:
            d = d + 2 * y + 1
        else:
            x -= 1
            d = d + 2 * (y - x) + 1
        if x < y:
            break
        glVertex2f(cx + x, cy + y)
        glVertex2f(cx - x, cy + y)
        glVertex2f(cx + x, cy - y)
        glVertex2f(cx - x, cy - y)
        if x != y:
            glVertex2f(cx + y, cy + x)
            glVertex2f(cx - y, cy + x)
            glVertex2f(cx + y, cy - x)
            glVertex2f(cx - y, cy - x)
    glEnd()

def display():
    glClear(GL_COLOR_BUFFER_BIT)
    glLoadIdentity()

    # Draw enemies with circles for heads
    for enemy in enemies:
        draw_midpoint_circle(enemy.x + ENEMY_SIZE/2, enemy.y, ENEMY_SIZE/2)

    # Use line drawing to render shooter
    draw_midpoint_line(shooter.x, shooter.y, shooter.x + shooter.w, shooter.y)
    draw_midpoint_line(shooter.x, shooter.y, shooter.x, shooter.y + shooter.h)
    draw_midpoint_line(shooter.x + shooter.w, shooter.y, shooter.x + shooter.w, shooter.y + shooter.h)
    draw_midpoint_line(shooter.x, shooter.y + shooter.h, shooter.x + shooter.w, shooter.y + shooter.h)

    glutSwapBuffers()

def reshape(w, h):
    glViewport(0, 0, w, h)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluOrtho2D(0, w, 0, h)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()

def timer(value):
    if not pause:
        for enemy in enemies:
            enemy.y -= enemy.speed
            if enemy.y < 0:
                enemy.y = random.randint(W_Height, W_Height + 100)
                enemy.x = random.randint(0, W_Width - ENEMY_SIZE)
    glutPostRedisplay()
    glutTimerFunc(1000//60, timer, 0)

def main():
    glutInit(sys.argv)
    glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB)
    glutInitWindowSize(W_Width, W_Height)
    glutInitWindowPosition(100, 100)
    glutCreateWindow(b"Space Invaders with Line and Circle Drawing")
    glutDisplayFunc(display)
    glutReshapeFunc(reshape)
    glutTimerFunc(1000//60, timer, 0)
    glClearColor(0.0, 0.0, 0.0, 0.0)
    gluOrtho2D(0.0, W_Width, 0.0, W_Height)
    glutMainLoop()

if __name__ == "__main__":
    main()
