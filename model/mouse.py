class Mouse:
    # mouse position
    MOUSE_X, MOUSE_Y = None, None
    # left button
    LEFT_IS_DOWNED = None
    # move speed
    MOVE_SPEED = None

    def __init__(self, x=0, y=0, left_is_downed=False, move_speed=100):
        self.MOUSE_X = x
        self.MOUSE_Y = y
        self.LEFT_IS_DOWNED = left_is_downed
        self.MOVE_SPEED = move_speed
