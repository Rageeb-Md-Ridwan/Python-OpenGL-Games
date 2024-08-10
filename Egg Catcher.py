from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import random as r
import math

# Window dimensions
width = 800
height = 600

# Basket parameters
basket_width = 120
basket_height = 80
basket_position = [width // 2 - basket_width // 2, 0]

# Egg parameters
egg_width = 15
egg_height = 20
egg_speed = 2
egg_y_initial = height - 170
egg_x_positions = [
    100,
    250,
    400,
    550,
    700,
]  # Specific x positions for eggs to fall from
egg_position = [
    r.choice(egg_x_positions),
    egg_y_initial,
]  # Randomly choose one of the x positions
egg_color = [
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

# Miss count
miss_count = 0


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


def draw_egg(x, y, width, height, color):
    glColor3f(color[0], color[1], color[2])
    num_segments = 100
    glBegin(GL_POINTS)  # Changed to draw points
    for i in range(num_segments):
        theta = 2.0 * math.pi * i / num_segments
        glVertex2f(x + width * math.cos(theta), y + height * math.sin(theta))
    glEnd()
    glColor3f(1, 1, 1)


def draw_basket(x, y, width, height):
    glColor3f(0.5, 0.35, 0.05)  # Brown color for basket
    glBegin(GL_POINTS)  # Changed to draw points
    for i in range(width):
        glVertex2i(x + i, y)
        glVertex2i(x + i, y + height)
    for i in range(height):
        glVertex2i(x, y + i)
        glVertex2i(x + width, y + i)
    glEnd()
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


def draw_chicken(x, y, size):
    # Adjusting the size
    body_size = size * 1.2
    head_size = size * 1.0
    comb_size = size * 0.75
    wing_size = size * 0.6  # Increased wing size

    # Adjusting the position
    body_y = y - size * 0.3  # Lifted the body higher
    head_y = y + size * 0.6  # Lifted the head higher
    comb_y = head_y + head_size * 0.6  # Lifted the comb higher
    glPointSize(4)
    # Draw body
    glColor3f(1, 1, 1)  # White color for body
    draw_circle(x, body_y, body_size / 2)
    # Draw wings
    glColor3f(1, 1, 1)  # White color for wings
    glBegin(GL_POINTS)  # Changed to draw points
    # Left wing
    glVertex2f(x - body_size * 0.7, body_y - wing_size / 2)
    glVertex2f(
        x - body_size * 0.7 - wing_size * 0.5, body_y - wing_size * 0.25
    )  # Additional point
    glVertex2f(x - body_size * 0.7 - wing_size, body_y)
    glVertex2f(
        x - body_size * 0.7 - wing_size * 0.5, body_y + wing_size * 0.25
    )  # Additional point
    glVertex2f(x - body_size * 0.7, body_y + wing_size / 2)
    # Right wing
    glVertex2f(x + body_size * 0.7, body_y - wing_size / 2)
    glVertex2f(
        x + body_size * 0.7 + wing_size * 0.5, body_y - wing_size * 0.25
    )  # Additional point
    glVertex2f(x + body_size * 0.7 + wing_size, body_y)
    glVertex2f(
        x + body_size * 0.7 + wing_size * 0.5, body_y + wing_size * 0.25
    )  # Additional point
    glVertex2f(x + body_size * 0.7, body_y + wing_size / 2)
    glEnd()

    # Draw head
    draw_circle(x, head_y, head_size // 3)

    # Draw comb
    glColor3f(1, 0, 0)  # Red color for comb
    glBegin(GL_POINTS)  # Changed to draw points
    # Left comb
    glVertex2f(x - comb_size / 2, comb_y)  # Left comb point
    glVertex2f(
        x - comb_size / 2 + comb_size / 4, comb_y + comb_size / 4
    )  # Additional point
    glVertex2f(x - comb_size / 2, comb_y + comb_size * 0.8)  # Top comb point
    # Middle comb
    glVertex2f(x, comb_y)  # Middle comb point
    glVertex2f(x, comb_y + comb_size * 0.8)  # Top comb point
    # Right comb
    glVertex2f(x + comb_size / 2, comb_y)  # Right comb point
    glVertex2f(
        x + comb_size / 2 - comb_size / 4, comb_y + comb_size / 4
    )  # Additional point
    glVertex2f(x + comb_size / 2, comb_y + comb_size * 0.8)  # Top comb point
    glEnd()


def draw_polygons(positions):
    for x in positions:
        draw_chicken(x, height * 0.8, egg_width * 2)


def draw_circle(x, y, radius):
    num_segments = 100
    glBegin(GL_POINTS)  # Changed to draw points
    for i in range(num_segments):
        theta = 2.0 * math.pi * i / num_segments
        glVertex2f(x + radius * math.cos(theta), y + radius * math.sin(theta))
    glEnd()


def display_callback():
    glClear(GL_COLOR_BUFFER_BIT)

    glColor3f(1, 1, 1)  # Set color to white

    # Draw polygons at specified positions
    draw_polygons(egg_x_positions)

    # Draw basket
    draw_basket(basket_position[0], basket_position[1], basket_width, basket_height)

    # Draw egg
    draw_egg(egg_position[0], egg_position[1], egg_width, egg_height, egg_color)

    # Draw button
    draw_pause_button(
        button_position[0], button_position[1], button_width, button_height, paused
    )

    glutSwapBuffers()


# Function to update the game state
def update_callback(value):
    global egg_position, score, egg_color, miss_count

    if not paused:
        egg_position[1] -= egg_speed

        # Check if egg is caught
        if (
            basket_position[0] <= egg_position[0] <= basket_position[0] + basket_width
        ) and (
            basket_position[1] <= egg_position[1] <= basket_position[1] + basket_height
        ):
            score += 1
            egg_position = [r.choice(egg_x_positions), egg_y_initial]
            egg_color = [
                r.random(),
                r.random(),
                r.random(),
            ]  # New random color
            print("Score:", score)
            miss_count = 0  # Reset miss count when egg is caught

        # Check if egg is missed
        if egg_position[1] < 0:
            miss_count += 1
            if miss_count == 2:  # End game if missed 2 eggs in a row
                print("Game Over! Your Score:", score)
                for _ in range(3):
                    print(".")
                print("Starting Over : ")
                score = 0
                miss_count = 0  # Reset miss count
            else:
                egg_position = [r.choice(egg_x_positions), egg_y_initial]
                egg_color = [
                    r.random(),
                    r.random(),
                    r.random(),
                ]  # New random color

    glutTimerFunc(10, update_callback, 0)
    glutPostRedisplay()


# Function to handle keyboard input
def keyboard_callback(key, x, y):
    global basket_position, paused

    if not paused:
        if key == b"a" and basket_position[0] > 0:
            basket_position[0] -= 25
        elif key == b"d" and basket_position[0] < width - basket_width:
            basket_position[0] += 25


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
glutCreateWindow(b"Catch the Eggs!")
glutDisplayFunc(display_callback)
glutKeyboardFunc(keyboard_callback)
glutMouseFunc(mouse_callback)
glutCloseFunc(close_callback)
init()
glutTimerFunc(10, update_callback, 0)
glutMainLoop()
