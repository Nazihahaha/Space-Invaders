class Projectile:
    def __init__(self, start_x, start_y, target_x, target_y):
        self.x = start_x
        self.y = start_y
        self.target_x = target_x
        self.target_y = target_y
        self.speed = 5

    def update(self):
        # Move the projectile towards the target
        direction_x = self.target_x - self.x
        direction_y = self.target_y - self.y
        distance = math.sqrt(direction_x ** 2 + direction_y ** 2)
        if distance != 0:
            direction_x /= distance
            direction_y /= distance
        self.x += direction_x * self.speed
        self.y += direction_y * self.speed

    def draw(self):
        glColor3f(1.0, 1.0, 1.0)  # White color for the projectile
        glBegin(GL_POINTS)
        glVertex2f(self.x, self.y)
        glEnd()