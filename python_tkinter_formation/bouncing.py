import random
import tkinter as tk
from typing import Optional

FRAME_RATE = 60
MAX_SPEED = 5
MIN_SIZE = 20
MAX_SIZE = 40


def speed_collision(m1, m2, s1, s2):
    return ((m1 - m2) * s1 + 2 * m2 * s2) / (m1 + m2)


class Ball:
    def __init__(
        self,
        canvas: "BouncingCanvas",
        pos: tuple[int, int],
        size_ball: int,
        color: str = "white",
        speed: Optional[list[int]] = None,
    ) -> None:
        self.canvas = canvas
        self.size = size_ball
        self.pos = pos
        if speed:
            self.speed = speed
        else:
            self.speed = [0.0, 0.0]
        self.color = color

        # Create the ball into the canvas
        self.__id = self.canvas.create_oval(
            self.convert_size_to_coordinates(self.pos, self.size),
            fill=self.color,
        )

    def convert_size_to_coordinates(
        self, pos: tuple[int, int], size: int
    ) -> tuple[tuple[int, int], tuple[int, int]]:
        return (tuple(x + size for x in pos), tuple(x - size for x in pos))

    def collision(self, pos: tuple[int, int], size: int) -> bool:
        distance = (self.pos[0] - pos[0]) ** 2 + (self.pos[1] - pos[1]) ** 2
        return (self.size + size) ** 2 >= distance

    def update_speed_ball_collision(self, b: "Ball"):
        if self.collision(b.pos, b.size):
            v1x = speed_collision(self.size, b.size, self.speed[0], b.speed[0])
            v1y = speed_collision(self.size, b.size, self.speed[1], b.speed[1])
            v2x = speed_collision(b.size, self.size, b.speed[0], self.speed[0])
            v2y = speed_collision(b.size, self.size, b.speed[1], self.speed[1])

            self.speed = [v1x, v1y]
            b.speed = [v2x, v2y]

    def out_of_bound(self) -> tuple[bool, bool]:
        return (
            self.pos[0] + self.size > self.canvas.width
            or self.pos[0] - self.size < 0,
            self.pos[1] + self.size > self.canvas.height
            or self.pos[1] - self.size < 0,
        )

    def move(self):
        self.pos = self.pos[0] + self.speed[0], self.pos[1] + self.speed[1]
        self.canvas.move(self.__id, *self.speed)


class BouncingCanvas(tk.Canvas):
    def __init__(self, master: tk.Misc | None = None, *args, **kwargs) -> None:
        tk.Canvas.__init__(self, master, *args, **kwargs)
        self.pack(fill=tk.BOTH, expand=1)
        # Required to keep track of the geometry of the canvas
        self.bind("<Configure>", self.on_resize)

        self.balls: list[Ball] = []

        self.bind("<Button 1>", self.random_ball_event)
        self.update_frame()

    def add_ball(
        self,
        pos: tuple[int, int],
        size: int,
        color: str,
        speed: list[int],
    ) -> bool:
        if self.check_valide_ball(pos, size):
            self.balls.append(Ball(self, pos, size, color, speed))
            return True
        return False

    def out_of_bound(self, pos: tuple[int, int], size: int):
        return (
            pos[0] + size > self.width
            or pos[0] - size < 0
            or pos[1] + size > self.height
            or pos[1] - size < 0
        )

    def check_valide_ball(self, pos: tuple[int, int], size: int):
        if not self.out_of_bound(pos, size):
            return all((not b.collision(pos, size) for b in self.balls))
        return False

    def random_ball(self, pos):
        size = random.randint(MIN_SIZE, MAX_SIZE)
        color = "#" + "".join(
            [random.choice("ABCDEF0123456789") for i in range(6)]
        )
        speed = [random.randint(0, MAX_SPEED), random.randint(0, MAX_SPEED)]
        if self.check_valide_ball(pos, size):
            self.add_ball(pos, size, color, speed)

    def random_ball_event(self, event):
        self.random_ball((event.x, event.y))

    def update_frame(self):
        for i, b in enumerate(self.balls):
            b.move()
            oob = b.out_of_bound()
            if any(oob):
                if oob[0]:
                    b.speed[0] = -b.speed[0]
                if oob[1]:
                    b.speed[1] = -b.speed[1]
            for j in range(i, len(self.balls)):
                b.update_speed_ball_collision(self.balls[j])

        self.after(int(1000 / FRAME_RATE), self.update_frame)

    def on_resize(self, event: tk.Event):
        self.width, self.height = event.width, event.height
