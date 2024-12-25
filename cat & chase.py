from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import random
import time
import math


window_width=500
window_height=500
bait_lifetime=5
cat_speed=10
circles=[]
speed=2
cat_x=200
cat_y=0
score=0
fish_bait=[]
mouse_bait=[]
scorpio_bait=[]
cat_width=60
cat_height=130
bait_radius=10
play_mode=True

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
    if x1 == x2:
        if y1 > y2:
            y1, y2 = y2, y1

    zone = find_zone(x1, y1, x2, y2)
    x1, y1 = convert_to_zone0(x1, y1, zone)
    x2, y2 = convert_to_zone0(x2, y2, zone)

    dx = x2 - x1
    dy = y2 - y1

    if dx == 0:
        for y in range(y1, y2 + 1):
            points_converted = [convert_from_zone0(x1, y, zone)]
            for p in points_converted:
                draw_point(p[0], p[1])
        return

    D = 2 * dy - dx
    e = 2 * dy
    ne = 2 * (dy - dx)
    x = x1
    y = y1

    points = [(x, y)]

    while x < x2:
        if D > 0:
            y = y + 1
            D = D + ne
        else:
            D = D + e
        x = x + 1
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


def add_fish():
    x = random.randint(50, window_width - 50)
    y = random.randint(50, window_height - 50)
    timestamp = time.time()
    fish_bait.append({'x': x, 'y': y, 'timestamp': timestamp})


def add_mouse():
    x = random.randint(50, window_width - 50)
    y = random.randint(50, window_height - 70)
    timestamp = time.time()
    mouse_bait.append({'x': x, 'y': y, 'timestamp': timestamp})

def add_scorpio():
    x = random.randint(50, window_width - 50)
    y = random.randint(50, window_height - 50)
    timestamp = time.time()
    scorpio_bait.append({'x': x, 'y': y, 'timestamp': timestamp})
class AABB:
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height

    def collides_with(self, other):
        return (self.x < other.x + other.width and
                self.x + self.width > other.x and
                self.y < other.y + other.height and
                self.y + self.height > other.y)

def leftarrow():
    glColor3f(0.0, 0.5, 0.5)
    draw_line(10, 450, 40, 470)
    draw_line(10, 450, 40, 430)
    draw_line(10, 450, 60, 450)

def play():
    glColor3f(1.0, 0.75, 0.0)
    draw_line(240, 470, 240, 430)
    draw_line(260, 470, 260, 430)

def pause():
    glColor3f(1.0, 0.75, 0.0)
    draw_line(240, 470, 240, 430)
    draw_line(240, 470, 280, 455)
    draw_line(240, 430, 280, 455)

def cross():
    glColor3f(1.0, 0.0, 0.0)
    draw_line(445, 430, 490, 470)
    draw_line(445, 470, 490, 430)

cross_AABB = AABB(445, 430, 50, 40)
play_AABB = AABB(240, 430, 20, 40)
pause_AABB = AABB(260, 430, 20, 40)
leftArrow_AABB = AABB(10, 430, 50, 40)

def draw_cat(x, y):
    glColor3f(0.4, 0.1, 0.05)
    draw_line(x, y, x + 60, y)
    draw_line(x, y, x, y + 70)
    draw_line(x + 60, y, x + 60, y + 70)
    draw_line(x, y + 70, x + 60, y + 70)

    glColor3f(0.4, 0.1, 0.05)
    draw_line(x+5,y+70,x+55,y+70)
    draw_line(x+5,y+110, x+55, y+ 110)
    draw_line(x+5,y+70, x+5,y+110)
    draw_line(x+55,y+70, x+55, y+ 110)

    glColor3f(0.4, 0.1, 0.05)
    draw_line(x+10,y+110, x+30,y+110)
    draw_line(x + 10, y + 110, x + 20, y + 130)
    draw_line(x+30,y+110, x + 20, y + 130)

    glColor3f(0.4, 0.1, 0.05)
    draw_line(x+50, y+ 110, x+30, y+ 110)
    draw_line(x+50, y+ 110, x + 40, y + 130)
    draw_line(x+30, y+ 110, x + 40, y + 130)

    glColor3f(0.4, 0.1, 0.05)
    draw_circle_midpoint(x+30,y+90,2)

    glColor3f(0.4, 0.1, 0.05)
    draw_line(x+28,y+90,x+10,y+100)
    draw_line(x+28,y+90,x+10,y+80)
    draw_line(x+32,y+90,x+50,y+100)
    draw_line(x+32,y+90,x+50,y+80)

def draw_fish():
    global fish_bait
    current_time = time.time()
    bait = [m for m in fish_bait if current_time - m['timestamp'] < bait_lifetime]
    for m in bait:
        glColor3f(0.3, 0.5, 1.0)
        x, y = m['x'], m['y']
        draw_circle_midpoint(x,y, 5)
        draw_line(x+5,y,x+10,y+10)
        draw_line(x+5,y,x+10,y-10)

def draw_mouse():
    global mouse_bait
    current_time = time.time()
    bait = [m for m in mouse_bait if current_time - m['timestamp'] < bait_lifetime]

    for m in bait:
        glColor3f(0.25, 0.25, 0.25)
        x, y = m['x'], m['y']
        draw_circle_midpoint(x,y, 2.5)
        draw_line(x+2.5,y,x+25,y+10)
        draw_line(x+2.5,y,x+25,y)
        draw_line(x+25,y,x+25,y+10)

def draw_scorpio():
    global scorpio_bait
    current_time = time.time()
    bait = [m for m in scorpio_bait if current_time - m['timestamp'] < bait_lifetime]

    for m in bait:
        glColor3f(1.0, 0.0, 0.0)
        x, y = m['x'], m['y']
        draw_circle_midpoint(x,y, 3)
        draw_circle_midpoint(x + 5, y, 4)
        draw_circle_midpoint(x + 10, y, 5)
        draw_circle_midpoint(x + 15, y, 6)


def draw_text(x, y, text):
    glRasterPos2f(x, y)
    for char in text:
        glutBitmapCharacter(GLUT_BITMAP_HELVETICA_18, ord(char))

def display():
    global play_mode
    glClear(GL_COLOR_BUFFER_BIT)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluOrtho2D(0, window_width, 0, window_height)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    
    draw_background() 
    leftarrow()
    if play_mode == True:
        play()
    else:
        pause()
    cross()
    draw_cat(cat_x, cat_y)
    draw_fish()
    draw_mouse()
    draw_scorpio()
    glColor3f(1.0, 1.0, 1.0)
    draw_text(10, 480, f"Score: {score}")
    glutSwapBuffers()

def check_collision(cat_x, cat_y, bait_x, bait_y):
    global cat_width, cat_height, bait_radius
    cat_center_x = cat_x + cat_width / 2
    cat_center_y = cat_y + cat_height / 2

    cat_radius = math.sqrt((cat_width / 2) ** 2 + (cat_height / 2) ** 2)
    distance = math.sqrt((cat_center_x - bait_x) ** 2 + (cat_center_y - bait_y) ** 2)
    return distance <= cat_radius + bait_radius

def update_score():
    global score
    for fish in fish_bait[:]:
        if check_collision(cat_x, cat_y, fish['x'], fish['y']):
            score=score+10
            fish_bait.remove(fish)

    for mouse in mouse_bait[:]:
        if check_collision(cat_x, cat_y, mouse['x'], mouse['y']):
            score=score+10
            mouse_bait.remove(mouse)


    for scorpio in scorpio_bait[:]:
        if check_collision(cat_x, cat_y, scorpio['x'], scorpio['y']):
            score=score-10
            scorpio_bait.remove(scorpio)
def update(value):
    if random.random() < 0.33:
        add_fish()
    if random.random() < 0.33:
        add_mouse()
    if random.random() < 0.33:
        add_scorpio()
    update_score()
    glutPostRedisplay()
    glutTimerFunc(1000, update, 0)

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


def restart_game():
    global score, fish_bait, mouse_bait, scorpio_bait, cat_x, cat_y, play_mode
    score = 0
    fish_bait = []
    mouse_bait = []
    scorpio_bait = []
    cat_x = 200
    cat_y = 0
    play_mode = True

def mouse_click(button, state, x, y):
    global play_mode

    mx, my = x, window_height - y

    if (button == GLUT_LEFT_BUTTON and state == GLUT_DOWN) or (button == GLUT_RIGHT_BUTTON and state == GLUT_DOWN):

        if cross_AABB.collides_with(AABB(mx, my, 1, 1)):
            glutLeaveMainLoop()

        if play_AABB.collides_with(AABB(mx, my, 1, 1)) or pause_AABB.collides_with(AABB(mx, my, 1, 1)):
            play_mode = not play_mode

        if leftArrow_AABB.collides_with(AABB(mx, my, 1, 1)):
            restart_game()

    glutPostRedisplay()

def animation():
    global play_mode
    if play_mode == True:
        glutPostRedisplay()


def draw_rectangle(x1, y1, x2, y2, color):
    glColor3f(*color)
    
    for y in range(int(y1), int(y2)):
        draw_line(x1, y, x2, y)

def draw_background():
    
    
    draw_rectangle(0, 0, window_width, window_height // 3, (0.0, 0.8, 0.0))   
    draw_rectangle(0, window_height // 2, window_width, window_height, (0.53, 0.81, 0.98))  
    draw_rectangle(0, window_height // 3, window_width, window_height // 2, (0.0, 0.4, 0.8))  
    
     

   



glutInit()
glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB)
glutInitWindowSize(window_width, window_height)
glutCreateWindow(b"Shooting Game")
glutDisplayFunc(display)
glutIdleFunc(animation)
glutKeyboardFunc(keyboard)
glutMouseFunc(mouse_click)
glutTimerFunc(1000, update, 0)
glutMainLoop()