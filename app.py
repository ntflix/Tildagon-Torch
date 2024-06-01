import asyncio
import app
from events.input import Buttons, BUTTON_TYPES
from system.patterndisplay.events import *
from system.eventbus import eventbus
from .torch import LEDManager


class TorchApp(app.App):
    led_manager: LEDManager
    color: tuple[int, int, int] = (255, 255, 255)
    on: bool = True

    def __init__(self):
        self.button_states = Buttons(self)
        eventbus.emit(PatternDisable())
        self.led_manager = LEDManager()

    def update(self, delta):
        if self.button_states.get(BUTTON_TYPES["RIGHT"]) or self.button_states.get(
            BUTTON_TYPES["LEFT"]
        ):
            self.toggle()
        elif self.button_states.get(BUTTON_TYPES["CANCEL"]):
            # The button_states do not update while you are in the background.
            # Calling clear() ensures the next time you open the app, it stays open.
            # Without it the app would close again immediately.
            self.button_states.clear()

    def draw(self, ctx):
        # ctx.save()
        ctx.font_size = 48
        ctx.text_align = ctx.CENTER
        ctx.text_baseline = ctx.MIDDLE

        ctx.rgb(
            self.color[0],
            self.color[1],
            self.color[2],
        ).rectangle(-120, -120, 240, 240).fill()

        ctx.rgb(0.5, 0.5, 0.5).move_to(0, 0).text("B")

        # ctx.restore()

    def toggle(self):
        self.color = (255, 255, 255) if self.color == (0, 0, 0) else (0, 0, 0)
        self.on = not self.on

        if self.color == (255, 255, 255):
            self.led_manager.on()
        else:
            self.led_manager.off()


__app_export__ = TorchApp
