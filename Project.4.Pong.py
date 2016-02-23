# Implementation of classic arcade game Pong

import simplegui
import random

# initialize globals - pos and vel encode vertical info for paddles
WIDTH = 1200
HEIGHT = 800      
BALL_RADIUS = 10
PAD_WIDTH = 8
PAD_HEIGHT = 80
HALF_PAD_WIDTH = PAD_WIDTH / 2
HALF_PAD_HEIGHT = PAD_HEIGHT / 2
LEFT = False
RIGHT = True

PADDLE_VELOCITY=6
BALL_BOOST=.3
score1=0
score2=0
# initialize ball_pos and ball_vel for new bal in middle of table
ball_pos=[WIDTH/2,HEIGHT/2]
ball_vel=[random.randrange(3,7),(random.randrange(1,4))*-1]
paddle1_pos=[HALF_PAD_WIDTH,HEIGHT / 2]
paddle2_pos=[WIDTH - HALF_PAD_WIDTH,HEIGHT/2]
paddle1_vel=0
paddle2_vel=0
# if direction is RIGHT, the ball's velocity is upper right, else upper left
def spawn_ball(direction):
    global ball_pos, ball_vel # these are vectors stored as lists
    ball_pos=[WIDTH/2,HEIGHT/2]
    
    if direction=="LEFT":
        ball_vel[0]= (random.randrange(3,7))*-1
    elif direction=="RIGHT":
        ball_vel[0]=random.randrange(3,7)
        
    ball_vel[1]=(random.randrange(1,4))*-1
# define event handlers
def new_game():
    global paddle1_pos, paddle2_pos, paddle1_vel, paddle2_vel  # these are numbers
    global score1, score2  # these are ints
    global ball_pos,ball_vel
    score1=0
    score2=0
    paddle1_pos=[HALF_PAD_WIDTH,HEIGHT / 2]
    paddle2_pos=[WIDTH - HALF_PAD_WIDTH,HEIGHT/2]
    paddle1_vel=0
    paddle2_vel=0
    
    ball_pos=[WIDTH/2,HEIGHT/2]
    ball_vel=[random.randrange(3,7),(random.randrange(1,4))*-1]
    init_direction=random.randrange(1,3)
    
    if init_direction==1:
        ball_vel[0]=ball_vel[0]*-1  
        
        
def draw(canvas):
    global score1, score2, paddle1_pos, paddle2_pos, ball_pos, ball_vel
    global ball_pos,BALL_RADIUS
        
    # draw mid line and gutters
    canvas.draw_line([WIDTH / 2, 0],[WIDTH / 2, HEIGHT], 1, "White")
    canvas.draw_line([PAD_WIDTH, 0],[PAD_WIDTH, HEIGHT], 1, "White")
    canvas.draw_line([WIDTH - PAD_WIDTH, 0],[WIDTH - PAD_WIDTH, HEIGHT], 1, "White")
    # update ball   
    ball_pos[0]+=ball_vel[0]
    ball_pos[1]+=ball_vel[1]
    # draw ball
    canvas.draw_circle(ball_pos, BALL_RADIUS, 2, "orange",  "blue")   
    
    
    
    # update paddle's vertical position, keep paddle on the screen
    if paddle1_pos[1]>=HALF_PAD_HEIGHT and paddle1_pos[1]<=(HEIGHT-HALF_PAD_HEIGHT):
        paddle1_pos[1]+=paddle1_vel
    elif paddle1_pos[1]>HEIGHT/2:
        paddle1_pos[1]=(HEIGHT-HALF_PAD_HEIGHT)
    elif paddle1_pos[1]<HEIGHT/2:
        paddle1_pos[1]=(HALF_PAD_HEIGHT)
    if paddle2_pos[1]>=HALF_PAD_HEIGHT and paddle2_pos[1]<=(HEIGHT-HALF_PAD_HEIGHT):
        paddle2_pos[1]+=paddle2_vel
    elif paddle2_pos[1]>HEIGHT/2:
        paddle2_pos[1]=(HEIGHT-HALF_PAD_HEIGHT)
    elif paddle2_pos[1]<HEIGHT/2:
        paddle2_pos[1]=(HALF_PAD_HEIGHT)
    #Walls top and bottom:
    #ball hits top, reverse
    if ball_pos[1]-BALL_RADIUS<=0:
        ball_vel[1]=(ball_vel[1]*-1)
    #ball hits bottom, reverse
    if ball_pos[1]+BALL_RADIUS>=HEIGHT:
        ball_vel[1]=(ball_vel[1]*-1)
    # draw paddles
    canvas.draw_polygon([(paddle1_pos[0]+HALF_PAD_WIDTH,paddle1_pos[1]+HALF_PAD_HEIGHT),(paddle1_pos[0]-HALF_PAD_WIDTH,paddle1_pos[1]+HALF_PAD_HEIGHT),(paddle1_pos[0]-HALF_PAD_WIDTH,paddle1_pos[1]-HALF_PAD_HEIGHT),(paddle1_pos[0]+HALF_PAD_WIDTH,paddle1_pos[1]-HALF_PAD_HEIGHT)],1, "yellow", "green")
    canvas.draw_polygon([(paddle2_pos[0]+HALF_PAD_WIDTH,paddle2_pos[1]+HALF_PAD_HEIGHT),(paddle2_pos[0]-HALF_PAD_WIDTH,paddle2_pos[1]+HALF_PAD_HEIGHT),(paddle2_pos[0]-HALF_PAD_WIDTH,paddle2_pos[1]-HALF_PAD_HEIGHT),(paddle2_pos[0]+HALF_PAD_WIDTH,paddle2_pos[1]-HALF_PAD_HEIGHT)],1, "#9932CC", "#00FA9A")
    # determine whether paddle and ball collide    
    #left side collision with paddle
    if (ball_pos[0]-BALL_RADIUS)<=PAD_WIDTH and ball_pos[1]<=(paddle1_pos[1]+HALF_PAD_HEIGHT) and ball_pos[1]>=(paddle1_pos[1]-HALF_PAD_HEIGHT):
        ball_vel[0]=(ball_vel[0]*-1)+(BALL_BOOST)
    #left side padde MISS    
    elif (ball_pos[0]-BALL_RADIUS)<PAD_WIDTH and (ball_pos[1]>=(paddle1_pos[1]+HALF_PAD_HEIGHT) or ball_pos[1]<=(paddle1_pos[1]-HALF_PAD_HEIGHT)):
        score2+=1
        spawn_ball("RIGHT")
    #right side collision with paddle
    if (ball_pos[0]+BALL_RADIUS)>=(WIDTH-PAD_WIDTH) and ball_pos[1]<=(paddle2_pos[1]+HALF_PAD_HEIGHT) and ball_pos[1]>=(paddle2_pos[1]-HALF_PAD_HEIGHT):
        ball_vel[0]=(ball_vel[0]*-1)-(BALL_BOOST)
        ball_vel[1]=(random.randrange(1,10))*BALL_BOOST
    #right side padde MISS    
    elif (ball_pos[0]+BALL_RADIUS)>(WIDTH-PAD_WIDTH) and (ball_pos[1]>=(paddle1_pos[1]+HALF_PAD_HEIGHT) or ball_pos[1]<=(paddle1_pos[1]-HALF_PAD_HEIGHT)):
        score1+=1
        spawn_ball("LEFT")
    # draw scores
    canvas.draw_text(str(score1), (WIDTH/3,HALF_PAD_HEIGHT*2), 50, "blue")
    canvas.draw_text(str(score2), (WIDTH*2/3,HALF_PAD_HEIGHT*2), 50, "orange")
    
def keydown(key):
    global paddle1_vel, paddle2_vel,PADDLE_VELOCITY
    #Paddle 1 Velocity ON:
    if key==simplegui.KEY_MAP["s"]:
        paddle1_vel=PADDLE_VELOCITY
    elif key==simplegui.KEY_MAP["w"]:
        paddle1_vel=-PADDLE_VELOCITY
    #Paddle 2 Velocity ON:
    if key==simplegui.KEY_MAP["down"]:
        paddle2_vel=PADDLE_VELOCITY
    elif key==simplegui.KEY_MAP["up"]:
        paddle2_vel=-PADDLE_VELOCITY
    
    
def keyup(key):
    global paddle1_vel, paddle2_vel

    #Paddle 1 Velocity OFF:
    if key==simplegui.KEY_MAP["s"]:
        paddle1_vel=0
    elif key==simplegui.KEY_MAP["w"]:
        paddle1_vel=0
    #Paddle 2 Velocity OFF:
    if key==simplegui.KEY_MAP["down"]:
        paddle2_vel=0
    elif key==simplegui.KEY_MAP["up"]:
        paddle2_vel=0
        

# create frame
frame = simplegui.create_frame("Pong", WIDTH, HEIGHT)
frame.set_draw_handler(draw)
frame.set_keydown_handler(keydown)
frame.set_keyup_handler(keyup)
frame.add_button("RESET", new_game, 100)


# start frame
new_game()
frame.start()
