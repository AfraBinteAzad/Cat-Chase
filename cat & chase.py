from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import random

window_width=500
window_height=500
projectiles=[]
projectile_speed=5
cat_speed=10
circles=[]
speed=2
cat_x=200
cat_y=0
score=0
game_paused=False
game_over=False

def find_zone(x1, y1, x2, y2):
    dx = x2 - x1
    dy = y2 - y1
    if abs(dx)>abs(dy):
        if dx>0 and dy>0:
            return 0
        if dx<0 and dy>0:
            return 3
        if dx<0 and dy<0:
            return 4
        if dx>0 and dy<0:
            return 7
    if abs(dy)>abs(dx):
        if dx>0 and dy>0:
            return 1
        if dx<0 and dy>0:
            return 2
        if dx<0 and dy<0:
            return 5
        if dx>0 and dy<0:
            return 6

def convert_to_zone0(x, y, zone):
    if zone == 1:
        x, y = y, x
    elif zone == 2:
        x, y = y, x
        x = -x
    elif zone == 3:
        x = -x
        y = y
    elif zone == 4:
        x = -x
        y = -y
    elif zone == 5:
        x, y = -y, -x
    elif zone == 6:
        x, y = y, x
        x = -x
    elif zone == 7:
        y = -y
    return x, y

def convert_from_zone0(x, y, zone):
    if zone == 1:
        x, y = y, x
    elif zone == 2:
        x, y = y, x
        x = -x
    elif zone == 3:
        x = -x
    elif zone == 4:
        x,y = -x,-y
    elif zone == 5:
        x, y = -y, -x
    elif zone == 6:
        x, y = y, -x
    elif zone == 7:
        x, y = x,-y
    return x, y

def draw_line(x1, y1, x2, y2):
    if x1 > x2:
        x1, x2 = x2, x1
        y1, y2 = y2, y1
    zone = find_zone(x1, y1, x2, y2)
    x1, y1 = convert_to_zone0(x1, y1, zone)
    x2, y2 = convert_to_zone0(x2, y2, zone)

    dx = x2 - x1
    dy = y2 - y1
    if dx == 0:
        for y in range(y1, y2 + 1):
            points_converted=[convert_from_zone0(x1, y, zone)]
            for p in points_converted:
                draw_point(p[0], p[1])
        return

    D = 2*dy-dx
    e = 2*dy
    ne = 2*(dy-dx)
    x = x1
    y = y1

    points = [(x, y)]

    while x < x2:
        if D > 0:
            y =y+1
            D =D+ne
        else:
            D =D+e
        x =x+1
        points.append((x, y))

    points_converted = [convert_from_zone0(x, y, zone) for x, y in points]
    for p in points_converted:
        draw_point(p[0], p[1])

def draw_point(x, y):
    glBegin(GL_POINTS)
    glVertex2i(int(x), int(y))
    glEnd()

def draw_circle_midpoint(x_center, y_center, r):
    x = 0
    y = r
    d = 1 - r
    while x <= y:
        draw_symmetric_points(x_center, y_center, x, y)
        x =x+1
        if d < 0:
            d =d+2*x+1
        else:
            y =y-1
            d =d+2*(x-y)+1

def draw_symmetric_points(x_center, y_center, x, y):
    draw_point(x_center + x, y_center + y)
    draw_point(x_center - x, y_center + y)
    draw_point(x_center + x, y_center - y)
    draw_point(x_center - x, y_center - y)
    draw_point(x_center + y, y_center + x)
    draw_point(x_center - y, y_center + x)
    draw_point(x_center + y, y_center - x)
    draw_point(x_center - y, y_center - x)


def draw_cat(x, y):
    #draw body
    glColor3f(0.7, 0.4, 0.2)  # Brownish color
    draw_line(x, y, x + 60, y)  # Bottom line
    draw_line(x, y, x, y + 70)  # Left line
    draw_line(x + 60, y, x + 60, y + 70)  # Right line
    draw_line(x, y + 70, x + 60, y + 70)  # Top line

    glColor3f(0.7, 0.4, 0.2)  # Brownish color
    draw_line(x+5,y+70,x+55,y+70)  # Bottom line
    draw_line(x+5,y+110, x+55, y+ 110)  # Left line
    draw_line(x+5,y+70, x+5,y+110)  # Right line
    draw_line(x+55,y+70, x+55, y+ 110)  # Top line

    glColor3f(0.5, 0.2, 0.1)  # Darker brown
    draw_line(x+10,y+110, x+30,y+110)
    draw_line(x + 10, y + 110, x + 20, y + 130)
    draw_line(x+30,y+110, x + 20, y + 130)

    glColor3f(0.5, 0.2, 0.1)  # Darker brown
    draw_line(x+50, y+ 110, x+30, y+ 110)
    draw_line(x+50, y+ 110, x + 40, y + 130)
    draw_line(x+30, y+ 110, x + 40, y + 130)

    glColor3f(0.5, 0.2, 0.1)  # Darker brown
    draw_circle_midpoint(x+30,y+90,2)

    glColor3f(0.5, 0.2, 0.1)  # Darker brown
    draw_line(x+28,y+90,x+10,y+100)
    draw_line(x+28,y+90,x+10,y+80)
    draw_line(x+32,y+90,x+50,y+100)
    draw_line(x+32,y+90,x+50,y+80)

def draw_text(x, y, text):
    glRasterPos2f(x, y)
    for char in text:
        glutBitmapCharacter(GLUT_BITMAP_HELVETICA_18, ord(char))

def display():
    glClear(GL_COLOR_BUFFER_BIT)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluOrtho2D(0, window_width, 0, window_height)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()

    draw_cat(cat_x, cat_y)
    glColor3f(1.0, 1.0, 1.0)
    draw_text(10, 480, f"Score: {score}")
    glutSwapBuffers()
def keyboard(key, x, y):
    global cat_x,cat_y,cat_speed
    if key == b'l':
        cat_x = max(0,cat_x-cat_speed)
    elif key == b'r':
        cat_x = min(window_width-60,cat_x+cat_speed)
    elif key == b'd':
        cat_y = max(0,cat_y-cat_speed)
    elif key == b'u':
        cat_y = min(window_height-70,cat_y+cat_speed)
    glutPostRedisplay()
glutInit()
glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB)
glutInitWindowSize(window_width, window_height)
glutCreateWindow(b"Shooting Game")
glutDisplayFunc(display)
glutKeyboardFunc(keyboard)
glutMainLoop()