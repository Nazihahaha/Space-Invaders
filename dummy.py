import sys
import random
import math
from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *

# Constants
WINDOW_WIDTH = 500
WINDOW_HEIGHT = 700
ENEMY_SIZE = 30
NUM_ENEMIES = 10

# Enemy class
class Enemy:
    def __init__(self):
        self.x = random.randint(0, WINDOW_WIDTH - ENEMY_SIZE)
        self.y = random.randint(WINDOW_HEIGHT, WINDOW_HEIGHT + 200)
        self.speed = random.uniform(0.5, 2.0)

# List to hold enemy objects
enemies = []

# Initialize OpenGL
def init():
    glClearColor(0.0, 0.0, 0.0, 1.0)

    # Initialize enemy ships
    for _ in range(NUM_ENEMIES):
        enemies.append(Enemy())

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
        for i in range(36):
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
def updateEnemies():
    for enemy in enemies:
        enemy.y -= enemy.speed

        # Reset position if enemy reaches the bottom
        if enemy.y < 0:
            enemy.x = random.randint(0, WINDOW_WIDTH - ENEMY_SIZE)
            enemy.y = random.randint(WINDOW_HEIGHT, WINDOW_HEIGHT + 200)
            enemy.speed = random.uniform(0.5, 2.0)

# Function to handle window resizing
def reshape(w, h):
    glViewport(0, 0, w, h)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluOrtho2D(0, w, 0, h)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()

# Function to display content
def display():
    glClear(GL_COLOR_BUFFER_BIT)
    glLoadIdentity()

    drawEnemies()
    updateEnemies()

    glutSwapBuffers()

# Function for the main loop
def mainLoop(value):
    glutPostRedisplay()
    glutTimerFunc(1000 // 60, mainLoop, 0)

# Main function
def main():
    glutInit(sys.argv)
    glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB)
    glutInitWindowSize(WINDOW_WIDTH, WINDOW_HEIGHT)
    glutCreateWindow(b"Space Invaders")

    glutDisplayFunc(display)
    glutReshapeFunc(reshape)

    init()

    glutTimerFunc(0, mainLoop, 0)

    glutMainLoop()

if __name__ == "__main__":
    main()
