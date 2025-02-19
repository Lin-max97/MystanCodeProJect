"""
stanCode Breakout Project
Adapted from Eric Roberts's Breakout by
Sonja Johnson-Yu, Kylie Jue, Nick Bowman, 
and Jerry Liao.

YOUR DESCRIPTION HERE
"""
from campy.graphics.gwindow import GWindow
from campy.graphics.gobjects import GOval, GRect, GLabel
from campy.gui.events.mouse import onmouseclicked, onmousemoved
import random

BRICK_SPACING = 5      # Space between bricks (in pixels). This space is used for horizontal and vertical spacing
BRICK_WIDTH = 40       # Width of a brick (in pixels)
BRICK_HEIGHT = 15      # Height of a brick (in pixels)
BRICK_ROWS = 10        # Number of rows of bricks
BRICK_COLS = 10        # Number of columns of bricks
BRICK_OFFSET = 50      # Vertical offset of the topmost brick from the window top (in pixels)
BALL_RADIUS = 10       # Radius of the ball (in pixels)
PADDLE_WIDTH = 75      # Width of the paddle (in pixels)
PADDLE_HEIGHT = 15     # Height of the paddle (in pixels)
PADDLE_OFFSET = 50     # Vertical offset of the paddle from the window bottom (in pixels)
INITIAL_Y_SPEED = 7    # Initial vertical speed for the ball
MAX_X_SPEED = 5        # Maximum initial horizontal speed for the ball


class BreakoutGraphics:

    def __init__(self, ball_radius=BALL_RADIUS, paddle_width=PADDLE_WIDTH, paddle_height=PADDLE_HEIGHT,
                 paddle_offset=PADDLE_OFFSET, brick_rows=BRICK_ROWS, brick_cols=BRICK_COLS, brick_width=BRICK_WIDTH,
                 brick_height=BRICK_HEIGHT, brick_offset=BRICK_OFFSET, brick_spacing=BRICK_SPACING, title='Breakout'):

        # Create a graphical window, with some extra space
        window_width = brick_cols * (brick_width + brick_spacing) - brick_spacing
        window_height = brick_offset + 3 * (brick_rows * (brick_height + brick_spacing) - brick_spacing)
        self.window = GWindow(width=window_width, height=window_height, title=title)

        # Create a paddle
        self.paddle = GRect(width=paddle_width, height=paddle_height)
        self.paddle.filled = True
        self.window.add(self.paddle, (window_width - paddle_width) / 2, window_height - paddle_offset - paddle_height)
        onmousemoved(self.paddle_move)

        # Center a filled ball in window
        self.ball = GOval(ball_radius * 2, ball_radius * 2)
        self.ball.filled = True
        # Center the ball in the window
        ball_x = (self.window.width - self.ball.width) / 2
        ball_y = (self.window.height - self.ball.height) / 2
        self.window.add(self.ball, ball_x, ball_y)

        # Default speed for the ball
        self.__dx = 0
        self.__dy = 0
        self.ball_in_motion = False
        onmouseclicked(self.start_ball)

        # Draw bricks
        for row in range(brick_rows):
            for col in range(brick_cols):
                # The position of each brick
                x = col * (brick_width + brick_spacing)
                y = brick_offset + row * (brick_height + brick_spacing)
                # Create a brick
                brick = GRect(brick_width, brick_height)
                brick.filled = True
                # different color for each row
                brick.fill_color = self.get_brick_color(row)
                brick.color = brick.fill_color
                # Add the brick to the window
                self.window.add(brick, x, y)

    def get_brick_color(self, row):
        colors = ['silver', 'lightgrey', 'grey', 'darkgrey', 'black']
        return colors[row // 2 % len(colors)]

    def paddle_move(self, event):
        # 走橫的 new x position
        new_x = event.x - self.paddle.width / 2
        if new_x < 0:
            new_x = 0  # Prevent paddle from going out of the left
        elif new_x > self.window.width - self.paddle.width:
            new_x = self.window.width - self.paddle.width  # Prevent paddle from going out of the right
        # Set the paddle's position
        self.paddle.x = new_x
        self.paddle.y = self.window.height - PADDLE_OFFSET - self.paddle.height

    def start_ball(self, event):
        if not self.ball_in_motion:  # Ball start in 靜止
            self.ball_in_motion = True
            self.__dy = INITIAL_Y_SPEED
            self.__dx = random.randint(1, MAX_X_SPEED)
            if random.random() > 0.5:
                self.__dx = -self.__dx

    def move_ball(self):
        self.ball.move(self.__dx, self.__dy)
        # 碰到左、右邊界時反彈
        if self.ball.x <= 0 or self.ball.x + self.ball.width >= self.window.width:
            self.__dx = -self.__dx
        # 碰到上邊界時反彈
        if self.ball.y <= 0:
            self.__dy = -self.__dy
        # 是否會clash
        self.check_clash()

    def get_dx(self):
        return self.__dx

    def get_dy(self):
        return self.__dy

    def reset_ball_position(self):  # 回到中間
        self.ball.x = (self.window.width - self.ball.width) / 2
        self.ball.y = (self.window.height - self.ball.height) / 2
        self.ball_in_motion = False

    def check_clash(self):  # Balls four xy
        ball_top_left = (self.ball.x, self.ball.y)
        ball_top_right = (self.ball.x + self.ball.width, self.ball.y)
        ball_bottom_left = (self.ball.x, self.ball.y + self.ball.height)
        ball_bottom_right = (self.ball.x + self.ball.width, self.ball.y + self.ball.height)
        for corner in [ball_top_left, ball_top_right, ball_bottom_left, ball_bottom_right]:  # check corner
            bk = self.window.get_object_at(corner[0], corner[1])  # 該座標的物件 bk == brick
            if bk is not None:  # 如果碰 paddle，反彈
                if bk == self.paddle:
                    if self.__dy > 0:  # 求在向下時反彈
                        self.__dy = -self.__dy
                    return
                elif bk is not self.paddle:  # 如果碰到的是磚塊，反彈並移除磚塊
                    self.window.remove(bk)
                    self.__dy = -self.__dy
                    return

