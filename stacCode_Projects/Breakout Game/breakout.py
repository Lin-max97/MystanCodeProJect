"""
stanCode Breakout Project
Adapted from Eric Roberts's Breakout by
Sonja Johnson-Yu, Kylie Jue, Nick Bowman,
and Jerry Liao.

YOUR DESCRIPTION HERE
"""

from campy.graphics.gwindow import GWindow
from campy.gui.events.timer import pause
from breakoutgraphics import BreakoutGraphics
from campy.graphics.gobjects import GLabel, GOval

FRAME_RATE = 10         # 100 frames per second
NUM_LIVES = 3			# Number of attempts
window = GWindow


def main():

    graphics = BreakoutGraphics()
    lives = NUM_LIVES
    game_start_label = GLabel('START')  # add "START"
    game_start_label.font = '-40'
    game_start_label.color = 'green'
    x_center = (graphics.window.width - game_start_label.width) / 2  # "GAME OVER" in middle
    y_center = (graphics.window.height - game_start_label.height) / 2
    graphics.window.add(game_start_label, x_center, y_center)

    # Add the animation loop here!
    hearts = []
    for i in range(NUM_LIVES):
        heart = GLabel('❤️')
        heart.font = '-10'
        heart.color = 'pink'
        hearts.append(heart)
        graphics.window.add(heart, 10 + i * 15, 30)

    while lives > 0:
        if graphics.ball_in_motion:
            graphics.move_ball()
            graphics.window.remove(game_start_label)
            if graphics.ball.y >= graphics.window.height:  # 球掉出下邊界
                lives -= 1
                graphics.reset_ball_position()
                if lives < len(hearts):
                    graphics.window.remove(hearts[lives])
        pause(FRAME_RATE)

    game_over_label = GLabel('GAME OVER')  # add "GAME OVER"
    game_over_label.font = '-40'
    game_over_label.color = 'red'
    x_center = (graphics.window.width - game_over_label.width) / 2  # "GAME OVER" in middle
    y_center = (graphics.window.height - game_over_label.height) / 2
    graphics.window.add(game_over_label, x_center, y_center)


if __name__ == '__main__':
    main()
