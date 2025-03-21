import numpy as np
import pygame
import sys
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import time

# GLUT initialisieren
glutInit(sys.argv)
glutInitDisplayMode(GLUT_RGBA | GLUT_DOUBLE | GLUT_DEPTH)

# Challenge Punkte mit (x, y, z) Koordinaten
challenge_points = {
    "start": (0, 0, 0),
    "quiz_1": (1, 1, 0.7),
    "quiz_2": (1.2, 1, 1),
    "quiz_3": (1.4, 1, 1.2),
    "quiz_4": (1.6, 1, 1.5),
    "jury_A": (0.5, -1, 0.7),
    "jury_B": (-0.5, -1, 0.7),
    "water_pad": (1.5, 0, 0.5),
    "square": (0, 1, 1.1),
    "triangle": (-1, 1, 1.3),
    "cube": (-1, 0, 1.2),
    "pyramid": (-1.5, -1, 1.4),
}

drone_position = list(challenge_points["start"])
SPEED = 0.02


def draw_points():
    glPointSize(5)
    glBegin(GL_POINTS)
    glColor3f(1, 0, 0)
    for pos in challenge_points.values():
        glVertex3fv(pos)
    glEnd()


def draw_drone():
    glPushMatrix()
    glColor3f(0, 0, 1)
    glTranslatef(*drone_position)
    glutSolidSphere(0.1, 20, 20)
    glPopMatrix()


def move_to(target):
    global drone_position
    steps = 50
    for i in range(steps):
        drone_position[0] += (target[0] - drone_position[0]) * SPEED
        drone_position[1] += (target[1] - drone_position[1]) * SPEED
        drone_position[2] += (target[2] - drone_position[2]) * SPEED
        time.sleep(0.02)
        display()


def flight_path():
    for point in challenge_points.values():
        move_to(point)


def display():
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()
    gluLookAt(0, -3, 2, 0, 0, 0, 0, 0, 1)
    draw_points()
    draw_drone()
    pygame.display.flip()


def main():
    pygame.init()
    display = (800, 600)
    pygame.display.set_mode(display, DOUBLEBUF | OPENGL)
    gluPerspective(45, (display[0] / display[1]), 0.1, 50.0)
    glTranslatef(0.0, 0.0, -5)
    glEnable(GL_DEPTH_TEST)

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        flight_path()
        pygame.quit()
        break


if __name__ == "__main__":
    main()
