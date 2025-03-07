"""
File: babygraphics.py
Name: 
--------------------------------
SC101 Baby Names Project
Adapted from Nick Parlante's Baby Names assignment by
Jerry Liao.
"""

import tkinter
import babynames
import babygraphicsgui as gui

FILENAMES = [
    'data/full/baby-1900.txt', 'data/full/baby-1910.txt',
    'data/full/baby-1920.txt', 'data/full/baby-1930.txt',
    'data/full/baby-1940.txt', 'data/full/baby-1950.txt',
    'data/full/baby-1960.txt', 'data/full/baby-1970.txt',
    'data/full/baby-1980.txt', 'data/full/baby-1990.txt',
    'data/full/baby-2000.txt', 'data/full/baby-2010.txt',
    'data/full/baby-2020.txt'
]
CANVAS_WIDTH = 1080
CANVAS_HEIGHT = 600
YEARS = [1900, 1910, 1920, 1930, 1940, 1950,
         1960, 1970, 1980, 1990, 2000, 2010, 2020]
GRAPH_MARGIN_SIZE = 20
COLORS = ['red', 'purple', 'green', 'blue']
TEXT_DX = 2
LINE_WIDTH = 2
MAX_RANK = 1000


def get_x_coordinate(width, year_index):
    """
    Given the width of the canvas and the index of the current year
    in the YEARS list, returns the x coordinate of the vertical
    line associated with that year.

    Input:
        width (int): The width of the canvas
        year_index (int): The index where the current year is in the YEARS list
    Returns:
        x_coordinate (int): The x coordinate of the vertical line associated
                            with the current year.
    """
    num_years = len(YEARS)  # 計算年份的數量
    can_use_width = width - 2 * GRAPH_MARGIN_SIZE  # 計算可用的寬度，從整個畫布寬度中減去左右的邊距
    space = can_use_width / (num_years - 0.1)  # 每隔的大小
    x_coordinate = GRAPH_MARGIN_SIZE + year_index * space  # 計算 x 座標
    return x_coordinate


def draw_fixed_lines(canvas):
    """
    Draws the fixed background lines on the canvas.

    Input:
        canvas (Tkinter Canvas): The canvas on which we are drawing.
    """
    canvas.delete('all')            # delete all existing lines from the canvas

    # ----- Write your code below this line ----- #

    canvas.create_line(GRAPH_MARGIN_SIZE, GRAPH_MARGIN_SIZE, CANVAS_WIDTH - GRAPH_MARGIN_SIZE, GRAPH_MARGIN_SIZE)

    # Draw the bottom margin line
    canvas.create_line(GRAPH_MARGIN_SIZE, CANVAS_HEIGHT - GRAPH_MARGIN_SIZE, CANVAS_WIDTH - GRAPH_MARGIN_SIZE, CANVAS_HEIGHT - GRAPH_MARGIN_SIZE)

    # Draw vertical lines for each year
    i = 0  # 初始化索引
    for year in YEARS:
        x = get_x_coordinate(CANVAS_WIDTH, i)
        canvas.create_line(x, 0, x, CANVAS_HEIGHT)
        canvas.create_text(x + TEXT_DX, CANVAS_HEIGHT - GRAPH_MARGIN_SIZE, text=str(year), anchor=tkinter.NW)
        i += 1  # 手動增加索引


def draw_names(canvas, name_data, lookup_names):
    """
    Given a dict of baby name data and a list of name, plots
    the historical trend of those names onto the canvas.

    Input:
        canvas (Tkinter Canvas): The canvas on which we are drawing.
        name_data (dict): Dictionary holding baby name data
        lookup_names (List[str]): A list of names whose data you want to plot

    Returns:
        This function does not return any value.
    """
    draw_fixed_lines(canvas)        # draw the fixed background grid

    # ----- Write your code below this line ----- #
    i = 0  # 初始化索引
    for name in lookup_names:
        color = COLORS[i % len(COLORS)]  # Cycle through colors
        if name in name_data:
            j = 0  # 初始化年份索引
            while j < len(YEARS) - 1:
                year = str(YEARS[j])
                next_year = str(YEARS[j + 1])

                # Get ranks for the current year and the next year
                rank = int(name_data[name].get(year, MAX_RANK + 1))
                next_rank = int(name_data[name].get(next_year, MAX_RANK + 1))

                # Convert ranks to y座標
                y1 = GRAPH_MARGIN_SIZE + (rank - 1) * (CANVAS_HEIGHT - 2 * GRAPH_MARGIN_SIZE) / MAX_RANK
                y2 = GRAPH_MARGIN_SIZE + (next_rank - 1) * (CANVAS_HEIGHT - 2 * GRAPH_MARGIN_SIZE) / MAX_RANK

                # Get x座標
                x1 = get_x_coordinate(CANVAS_WIDTH, j)
                x2 = get_x_coordinate(CANVAS_WIDTH, j + 1)

                # Draw the line
                canvas.create_line(x1, y1, x2, y2, width=LINE_WIDTH, fill=color)

                # Draw text for the current year
                text = f'{name} {rank if rank <= MAX_RANK else "*"}'
                canvas.create_text(x1 + TEXT_DX, y1, text=text, anchor=tkinter.SW, fill=color)

                j += 1  # 手動增加年份索引

            final_year = str(YEARS[-1])  # 2020 年
            final_rank = int(name_data[name].get(final_year, MAX_RANK + 1))
            x_final = get_x_coordinate(CANVAS_WIDTH, len(YEARS) - 1)
            y_final = GRAPH_MARGIN_SIZE + (final_rank - 1) * (CANVAS_HEIGHT - 2 * GRAPH_MARGIN_SIZE) / MAX_RANK
            final_text = f'{name} {final_rank if final_rank <= MAX_RANK else "*"}'
            canvas.create_text(x_final + TEXT_DX, y_final, text=final_text, anchor=tkinter.SW, fill=color)
        i += 1  # 手動增加顏色索引


# main() code is provided, feel free to read through it but DO NOT MODIFY
def main():
    # Load data
    name_data = babynames.read_files(FILENAMES)

    # Create the window and the canvas
    top = tkinter.Tk()
    top.wm_title('Baby Names')
    canvas = gui.make_gui(top, CANVAS_WIDTH, CANVAS_HEIGHT, name_data, draw_names, babynames.search_names)

    # Call draw_fixed_lines() once at startup so we have the lines
    # even before the user types anything.
    draw_fixed_lines(canvas)

    # This line starts the graphical loop that is responsible for
    # processing user interactions and plotting data
    top.mainloop()


if __name__ == '__main__':
    main()
