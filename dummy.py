import sys
import random
import math
from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import time

# Constants
WINDOW_WIDTH = 500
WINDOW_HEIGHT = 700
ENEMY_SIZE = 30
NUM_ENEMIES = 5  # Increase the number of enemies

# Projectile class
class Projectile:
    def __init__(self, start_x, start_y):
        self.x = start_x
        self.y = start_y
        self.speed = 0.5

    def update(self):
        # Move the projectile towards the target
        print("hello")
        self.x -= self.speed
        self.y -= self.speed

    def draw(self):
        glColor3f(1.0, 1.0, 1.0)  # White color for the projectile
        glBegin(GL_POINTS)
        glVertex2f(self.x, self.y)
        glEnd()

# Enemy class
class Enemy:
    def __init__(self):
        self.x = random.randint(0, WINDOW_WIDTH - ENEMY_SIZE)
        self.y = random.randint(WINDOW_HEIGHT, WINDOW_HEIGHT + 200)
        self.speed = random.uniform(0.5, 2.0)
        self.shoot_cooldown = 2.0  # Cooldown between shots in seconds
        self.last_shot_time = 0.0
        self.projectiles = []  # List to hold projectiles
        self.shooting = False

    def shoot(self):
        self.shooting = True
        self.last_shot_time = time.time()
        # Choose a random target position within the window
        self.projectiles.append(Projectile(self.x + ENEMY_SIZE / 2, self.y))

    def update_projectiles(self):
        for projectile in self.projectiles:
            projectile.update()
            # Remove projectiles that are out of bounds
            if projectile.y <= 0 or projectile.x <= 0 or projectile.x >= WINDOW_WIDTH:
                self.projectiles.remove(projectile)

    def draw_projectiles(self):
        for projectile in self.projectiles:
            projectile.draw()

# List to hold enemy objects
enemies = []

# Initialize OpenGL
def init():
    glClearColor(0.0, 0.0, 0.0, 1.0)

    # Initialize enemy ships
    for _ in range(NUM_ENEMIES):
        enemies.append(Enemy())

# Function to draw enemy ships and projectiles
def drawEnemies():
    glColor3f(0.0, 1.0, 0.0)
    for enemy in enemies:
        x = enemy.x
        y = enemy.y

        # Draw head
        glPointSize(4.0)
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

        # Check if the enemy is shooting
        if enemy.shooting:
            # Update the projectiles fired by the enemy
            enemy.update_projectiles()
            # Draw the projectiles
            enemy.draw_projectiles()
        else:
            # Determine if the enemy should shoot
            if random.random() < 5:  # Adjust the probability as needed
                enemy.shoot()  # Call the shoot function to fire a projectile

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
