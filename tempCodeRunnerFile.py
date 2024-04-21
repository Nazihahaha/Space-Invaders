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
