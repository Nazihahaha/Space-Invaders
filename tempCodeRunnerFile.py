# Check for collision with the shooter
    # for circle in falling_circles:
    #     #print(shooter.y + 40,circle.y,"Y")
    #     if shooter.y + 40>=circle.y and circle.x-circle.radius<= shooter.x-shooter_radius<=circle.x+circle.radius+circle.radius :
    #         print("Game Over! Final Score:", score)
    #         print("Falling circle collided with shooter")
    #         falling_circles.clear()  # Remove all falling circles
    #         fire_projectiles.clear()
    #         shooter_frozen = True  # Disable shooter movement
    #         circles_frozen = True  # Freeze falling circles

    # # Check game over condition: missed 3 falling circles
    # if missed_circles_count >= 3:
    #     print("Game Over! Final Score:", score)
    #     print("Three missed circles")
    #     falling_circles.clear()  # Remove all falling circles
    #     fire_projectiles.clear()
    #     shooter_frozen = True  # Disable shooter movement
    #     circles_frozen = True  # Freeze falling circles
    #     return