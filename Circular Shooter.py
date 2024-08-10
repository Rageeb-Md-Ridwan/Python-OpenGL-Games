from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import math
import random

WINDOW_WIDTH = 500
WINDOW_HEIGHT = 500
shooter_x = WINDOW_WIDTH // 2
shooter_radius = 20
circle_radius = 15
circle_speed = 2
circles = []
bullets = []
score = 0
missed = 0
game_over = False
paused = False

pause_button_y = WINDOW_HEIGHT - 30
pause_button_width = 20
pause_button_height = 20
pause_button_x = (WINDOW_WIDTH - pause_button_width) // 2


def draw_points(x, y, size=1):
    draw_circle(size, x, y)


def draw_circle(radius, x0, y0):
    def circlePoints(x, y, x0, y0):
        glVertex2f(x + x0, y + y0)
        glVertex2f(y + x0, x + y0)
        glVertex2f(y + x0, -x + y0)
        glVertex2f(x + x0, -y + y0)
        glVertex2f(-x + x0, -y + y0)
        glVertex2f(-y + x0, -x + y0)
        glVertex2f(-y + x0, x + y0)
        glVertex2f(-x + x0, y + y0)

    def midpointCircle(radius, x0, y0):
        d = 1 - radius
        x = 0
        y = radius

        glBegin(GL_POINTS)
        while x < y:
            if d < 0:
                d = d + 2 * x + 3
                x += 1
            else:
                d = d + 2 * x - 2 * y + 5
                x += 1
                y = y - 1

            circlePoints(x, y, x0, y0)
        glEnd()

    midpointCircle(radius, x0, y0)


def initialize():
    glClearColor(0.0, 0.0, 0.0, 1.0)


def display():
    glClear(GL_COLOR_BUFFER_BIT)
    glColor3f(1.0, 1.0, 0.0)

    draw_circle(shooter_radius, shooter_x, shooter_radius)

    for circle in circles:
        draw_circle(circle_radius, circle[0], circle[1])

    for bullet in bullets:
        draw_circle(5, bullet[0], bullet[1])

    draw_pause_button() if not paused else draw_resume_button()

    glutSwapBuffers()


def draw_pause_button():
    glColor3f(1.0, 1.0, 0.0)  # Yellow color
    glPointSize(2.0)  # Set point size for better visibility

    glBegin(GL_POINTS)
    # Draw the left vertical line
    for y in range(
        pause_button_y - pause_button_height, pause_button_y + pause_button_height - 20
    ):
        glVertex2f(pause_button_x + pause_button_width / 2, y)

    # Draw the right vertical line
    for y in range(
        pause_button_y - pause_button_height, pause_button_y + pause_button_height - 20
    ):
        glVertex2f(pause_button_x + 2 * pause_button_width / 2, y)

    glEnd()

    glPointSize(1.0)  # Reset point size


def draw_resume_button():
    glColor3f(1.0, 1.0, 0.0)  # Yellow color
    glPointSize(2.0)  # Set point size for better visibility

    glBegin(GL_POINTS)
    # Render the vertical line
    for y in range(pause_button_y - pause_button_height, pause_button_y + 1):
        glVertex2f(pause_button_x, y)

    # Render the upper part of the triangle
    for x in range(pause_button_x, pause_button_x + 12):
        glVertex2f(x, pause_button_y - (x - pause_button_x))

    # Render the lower part of the triangle
    for x in range(pause_button_x, pause_button_x + 11):
        glVertex2f(
            x, pause_button_y - (pause_button_x + 12 - x + 10)
        )  # Mirror the upper part

    glEnd()

    glPointSize(1.0)  # Reset point size


def timer(value):
    global circles, missed, game_over, score
    if game_over or paused:
        return
    for i in range(len(circles)):
        circles[i][1] -= circle_speed

    for circle in circles:
        distance = math.sqrt(
            (circle[0] - shooter_x) ** 2 + (circle[1] - shooter_radius) ** 2
        )
        if distance <= circle_radius + shooter_radius:
            game_over = True
            print("Game Over! Circle touched the shooter.")
            print("Final Score:", score)
            return  # Exit the timer loop

        if circle[1] <= 0:
            circles.remove(circle)
            missed += 1
            if missed >= 3:
                game_over = True
                print("Game Over! Score:", score)
                return

    for bullet in bullets:
        bullet[1] += 5
        for circle in circles:
            if (
                math.sqrt((bullet[0] - circle[0]) ** 2 + (bullet[1] - circle[1]) ** 2)
                < circle_radius
            ):
                bullets.remove(bullet)
                circles.remove(circle)
                score += 1
                print("Score:", score)
                break

    if random.randint(0, 100) < 2:
        circles.append(
            [random.randint(circle_radius, WINDOW_WIDTH - circle_radius), WINDOW_HEIGHT]
        )

    glutPostRedisplay()
    glutTimerFunc(30, timer, 0)


def restart_game():
    global score, circles, bullets, missed, game_over
    print("Starting Over\n.\n.\n.\nScore:", score)
    score = 0
    circles = []
    bullets = []
    missed = 0
    game_over = False


def mouse(button, state, x, y):
    global paused
    if button == GLUT_LEFT_BUTTON and state == GLUT_DOWN:
        if (
            x >= pause_button_x
            and x <= pause_button_x + pause_button_width
            and y >= WINDOW_HEIGHT - pause_button_y
            and y <= WINDOW_HEIGHT - (pause_button_y - pause_button_height)
        ):
            paused = not paused
            if not paused:
                glutTimerFunc(0, timer, 0)


def keyboard(key, x, y):
    global shooter_x, bullets, paused
    shooter_speed = 20  # Increased speed for shooter
    if key == b"a":
        shooter_x -= shooter_speed
        # Check if shooter is out of bounds to the left
        if shooter_x - shooter_radius < 0:
            shooter_x = shooter_radius
    elif key == b"d":
        shooter_x += shooter_speed
        # Check if shooter is out of bounds to the right
        if shooter_x + shooter_radius > WINDOW_WIDTH:
            shooter_x = WINDOW_WIDTH - shooter_radius
    elif key == b" ":
        bullets.append([shooter_x, shooter_radius * 2])
    elif key == b"r":
        restart_game()


def reshape(width, height):
    glViewport(0, 0, width, height)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    glOrtho(0.0, width, 0.0, height, 0.0, 1.0)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()


def close_callback():
    print(".\n.\n.\nGoodbye")


def main():
    glutInit()
    glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB)
    glutInitWindowSize(WINDOW_WIDTH, WINDOW_HEIGHT)
    glutCreateWindow(b"Shoot The Circles!")
    glutDisplayFunc(display)
    glutTimerFunc(0, timer, 0)
    glutKeyboardFunc(keyboard)
    glutMouseFunc(mouse)
    glutReshapeFunc(reshape)
    glutCloseFunc(close_callback)
    initialize()
    print("Score:", score)  # print initital score
    glutMainLoop()


if __name__ == "__main__":
    main()
