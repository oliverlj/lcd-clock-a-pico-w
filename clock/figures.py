import framebuf


def draw(fb: framebuf, figure: int, color: int):
    if figure == 0:
        _draw0(fb, color)
    elif figure == 1:
        _draw1(fb, color)
    elif figure == 2:
        _draw2(fb, color)
    elif figure == 3:
        _draw3(fb, color)
    elif figure == 4:
        _draw4(fb, color)
    elif figure == 5:
        _draw5(fb, color)
    elif figure == 6:
        _draw6(fb, color)
    elif figure == 7:
        _draw7(fb, color)
    elif figure == 8:
        _draw8(fb, color)
    elif figure == 9:
        _draw9(fb, color)


def _draw0(fb: framebuf, color: int):
    _draw_top_rect(fb, color)
    _draw_left_top_rect(fb, color)
    _draw_left_bottom_rect(fb, color)
    _draw_right_top_rect(fb, color)
    _draw_right_bottom_rect(fb, color)
    _draw_bottom_rect(fb, color)


def _draw1(fb: framebuf, color: int):
    _draw_right_top_rect(fb, color)
    _draw_right_bottom_rect(fb, color)


def _draw2(fb: framebuf, color: int):
    _draw_top_rect(fb, color)
    _draw_right_top_rect(fb, color)
    _draw_middle_rect(fb, color)
    _draw_left_bottom_rect(fb, color)
    _draw_bottom_rect(fb, color)


def _draw3(fb: framebuf, color: int):
    _draw_top_rect(fb, color)
    _draw_right_top_rect(fb, color)
    _draw_middle_rect(fb, color)
    _draw_right_bottom_rect(fb, color)
    _draw_bottom_rect(fb, color)


def _draw4(fb: framebuf, color: int):
    _draw_left_top_rect(fb, color)
    _draw_right_top_rect(fb, color)
    _draw_middle_rect(fb, color)
    _draw_right_bottom_rect(fb, color)


def _draw5(fb: framebuf, color: int):
    _draw_top_rect(fb, color)
    _draw_left_top_rect(fb, color)
    _draw_middle_rect(fb, color)
    _draw_right_bottom_rect(fb, color)
    _draw_bottom_rect(fb, color)


def _draw6(fb: framebuf, color: int):
    _draw_top_rect(fb, color)
    _draw_left_top_rect(fb, color)
    _draw_middle_rect(fb, color)
    _draw_left_bottom_rect(fb, color)
    _draw_right_bottom_rect(fb, color)
    _draw_bottom_rect(fb, color)


def _draw7(fb: framebuf, color: int):
    _draw_top_rect(fb, color)
    _draw_right_top_rect(fb, color)
    _draw_right_bottom_rect(fb, color)


def _draw8(fb: framebuf, color: int):
    _draw_top_rect(fb, color)
    _draw_left_top_rect(fb, color)
    _draw_left_bottom_rect(fb, color)
    _draw_middle_rect(fb, color)
    _draw_right_top_rect(fb, color)
    _draw_right_bottom_rect(fb, color)
    _draw_bottom_rect(fb, color)


def _draw9(fb: framebuf, color: int):
    _draw_top_rect(fb, color)
    _draw_left_top_rect(fb, color)
    _draw_right_top_rect(fb, color)
    _draw_middle_rect(fb, color)
    _draw_right_bottom_rect(fb, color)
    _draw_bottom_rect(fb, color)


def _draw_top_rect(fb: framebuf, color: int):
    fb.fill_rect(40, 35, 55, 10, color)


def _draw_left_top_rect(fb: framebuf, color: int):
    fb.fill_rect(20, 50, 10, 60, color)


def _draw_left_bottom_rect(fb: framebuf, color: int):
    fb.fill_rect(20, 130, 10, 60, color)


def _draw_middle_rect(fb: framebuf, color: int):
    fb.fill_rect(40, 115, 55, 10, color)


def _draw_right_top_rect(fb: framebuf, color: int):
    fb.fill_rect(105, 50, 10, 60, color)


def _draw_right_bottom_rect(fb: framebuf, color: int):
    fb.fill_rect(105, 130, 10, 60, color)


def _draw_bottom_rect(fb: framebuf, color: int):
    fb.fill_rect(40, 195, 55, 10, color)


