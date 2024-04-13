"""
Build the world around you for you
"""
import toga
from toga.style import Pack
from toga.style.pack import COLUMN, ROW


class VisuAIizeApp(toga.App):
    def startup(self):
        
        main_box = toga.Box()
        button = toga.Button(
            "START MY DAY",
            on_press=self.take_picture,
            style=Pack(padding=5)
        )

        main_box.add(
            toga.ImageView(
                
                style=Pack(flex=1, width=150),
            )
        )

        main_box.add(button)

        self.main_window = toga.MainWindow(title=self.formal_name)
        self.main_window.content = main_box
        self.main_window.show()
    async def take_picture(self, widget, **kwargs):
        photo = self.activate_camera
        self.main_box.ImageView(
            photo
        )
    async def activate_camera(self, widget, **kwargs):
        self.camera.request_permission()
        photo = await self.camera.take_photo()
        return photo
        


def main():
    return VisuAIizeApp()

