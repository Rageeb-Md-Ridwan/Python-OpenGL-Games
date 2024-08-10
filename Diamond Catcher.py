from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import random as r

# Window dimensions
width = 800
height = 600

# Catcher parameters
catcher_width = 100
catcher_height = 20
catcher_position = [width // 2 - catcher_width // 2, 0]

# Diamond parameters
diamond_size = 30
diamond_speed = 2
diamond_position = [r.randint(0, width - diamond_size), height]
diamond_color = [
    r.random(),
    r.random(),
    r.random(),
]  # Random initial color

# Score
score = 0

# Game state
paused = False

# Button parameters
button_width = 40
button_height = 40
button_position = [width // 2 - button_width // 2, height - 50]


def draw_points(x, y):
    glBegin(GL_POINTS)
    glVertex2i(x, y)
    glEnd()


# Function to draw line using midpoint algorithm
def draw_midpoint_line(x1, y1, x2, y2):
    dx = abs(x2 - x1)
    dy = abs(y2 - y1)
    x, y = x1, y1
    sx = -1 if x1 > x2 else 1
    sy = -1 if y1 > y2 else 1

    if dx > dy:
        d = dx / 2.0
        while x != x2:
            draw_points(x, y)
            d -= dy
            if d < 0:
                y += sy
                d += dx
            x += sx
    else:
        d = dy / 2.0
        while y != y2:
            draw_points(x, y)
            d -= dx
            if d < 0:
                x += sx
                d += dy
            y += sy
    draw_points(x, y)


def draw_rectangle(x, y, width, height):
    for i in range(height):
        draw_midpoint_line(x, y + i, x + width, y + i)


def draw_diamond(x, y, size, color):
    glColor3f(color[0], color[1], color[2])
    draw_midpoint_line(x + size // 2, y, x + size, y + size // 2)
    draw_midpoint_line(x + size, y + size // 2, x + size // 2, y + size)
    draw_midpoint_line(x + size // 2, y + size, x, y + size // 2)
    draw_midpoint_line(x, y + size // 2, x + size // 2, y)
    glColor3f(1, 1, 1)


def draw_pause_button(x, y, width, height, paused):
    glColor3f(1, 1, 0)  # Yellow button color
    if paused:
        draw_midpoint_line(x + 5, y + 5, x + 5, y + height - 5)  # Left vertical line
        draw_midpoint_line(
            x + width - 5, y + 5, x + width - 5, y + height - 5
        )  # Right vertical line
    else:
        draw_midpoint_line(x + 5, y + 5, x + 5, y + height - 5)  # Left vertical line
        draw_midpoint_line(
            x + 5, y + 5, x + width - 5, y + height // 2
        )  # Top horizontal line
        draw_midpoint_line(
            x + 5, y + height - 5, x + width - 5, y + height // 2
        )  # Bottom horizontal line
    glColor3f(1, 1, 1)


# Function to display everything
def display_callback():
    glClear(GL_COLOR_BUFFER_BIT)

    glColor3f(1, 1, 1)  # Set color to white

    # Draw catcher
    draw_rectangle(
        catcher_position[0], catcher_position[1], catcher_width, catcher_height
    )

    # Draw diamond
    draw_diamond(diamond_position[0], diamond_position[1], diamond_size, diamond_color)

    # Draw button
    draw_pause_button(
        button_position[0], button_position[1], button_width, button_height, paused
    )

    glutSwapBuffers()


# Function to update the game state
def update_callback(value):
    global diamond_position, score, diamond_color

    if not paused:
        diamond_position[1] -= diamond_speed

        # Check if diamond is caught
        if (
            catcher_position[0]
            <= diamond_position[0]
            <= catcher_position[0] + catcher_width
        ) and (
            catcher_position[1]
            <= diamond_position[1]
            <= catcher_position[1] + catcher_height
        ):
            score += 1
            diamond_position = [r.randint(0, width - diamond_size), height]
            diamond_color = [
                r.random(),
                r.random(),
                r.random(),
            ]  # New random color
            print("Score:", score)

        # Check if diamond is missed
        if diamond_position[1] < 0:
            print("Game Over! Your Score:", score)
            for _ in range(3):
                print(".")
            print("Starting Over : ")
            score = 0
            diamond_position = [r.randint(0, width - diamond_size), height]
            diamond_color = [
                r.random(),
                r.random(),
                r.random(),
            ]  # New random color

    glutTimerFunc(10, update_callback, 0)
    glutPostRedisplay()


# Function to handle keyboard input
def keyboard_callback(key, x, y):
    global catcher_position, paused

    if not paused:
        if key == b"a" and catcher_position[0] > 0:
            catcher_position[0] -= 25
        elif key == b"d" and catcher_position[0] < width - catcher_width:
            catcher_position[0] += 25


# Function to handle mouse input
def mouse_callback(button, state, x, y):
    global paused

    if button == GLUT_LEFT_BUTTON and state == GLUT_DOWN:
        if (
            button_position[0] <= x <= button_position[0] + button_width
            and button_position[1] <= height - y <= button_position[1] + button_height
        ):
            paused = not paused


# Function to handle window close event
def close_callback():
    print(".\n.\n.\nGoodbye")


def init():
    glClearColor(0, 0, 0, 0)  # Set clear color to black
    gluOrtho2D(0, width, 0, height)  # Set orthographic viewing area


glutInit()
glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB)
glutInitWindowSize(width, height)
glutCreateWindow(b"Catch the Diamonds!")
glutDisplayFunc(display_callback)
glutKeyboardFunc(keyboard_callback)
glutMouseFunc(mouse_callback)
glutCloseFunc(close_callback)
init()
glutTimerFunc(10, update_callback, 0)
glutMainLoop()
