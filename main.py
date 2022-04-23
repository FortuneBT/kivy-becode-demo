#!/usr/bin/env python3
"""
This module will execute a program that make a windows with face recognition
"""
import cv2
from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.image import Image
from kivy.uix.textinput import TextInput
from kivy.clock import Clock
from kivy.graphics.texture import Texture   







class MyApp(App):
    """
    This is the class that manage the application
    """

    def build(self):
        """
        this functino will build all the widget in the
        app.
        """
        self.window = GridLayout()
        self.window.cols = 1
        self.screen = GridLayout()
        self.screen.cols = 1
        self.body = GridLayout()
        self.body.cols = 1

        self.body.size_hint = (0.4,0.3)
        self.body.pos_hint = {"center_x":0.5,"center_y":0.5}

        self.my_label = Label(text="who is this guy ?")
        self.my_button = Button(text="Press me")
        self.my_input = TextInput(multiline=False)
        self.my_image = Image(source="./ressources/car.jpg")
        self.image = Image()

        self.screen.add_widget(self.image)
        self.body.add_widget(self.my_label)
        self.body.add_widget(self.my_input)
        self.body.add_widget(self.my_button)

        self.window.add_widget(self.screen)
        self.window.add_widget(self.body)

        #self.my_button.bind(on_press=self.cam_on)

        self.capturation = cv2.VideoCapture(0)
        Clock.schedule_interval(self.load_video,1.0/30.0)
        return self.window


    def load_video(self,*args):
        succes, frame = self.capturation.read()
        

        face_multi = cv2.CascadeClassifier(
            "./ressources/haarcascade_frontalface_default.xml"
        )
        img_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = face_multi.detectMultiScale(img_gray, 1.1, 4)

        for (x_axis, y_axis, width, height) in faces:
            cv2.rectangle(
                frame, (x_axis, y_axis), (x_axis + width, y_axis + height), (255, 0, 0), 2
            )
            cv2.putText(
                frame,
                "awesome face",
                (x_axis, y_axis - 15),
                cv2.FONT_HERSHEY_COMPLEX,
                1,
                (255, 0, 0),
                2,
            )
            print("face detected")
    
        self_image_frame = frame
        buffer = cv2.flip(frame,0).tostring()
        texture = Texture.create(size=(frame.shape[1],frame.shape[0]),colorfmt='bgr')
        texture.blit_buffer(buffer,colorfmt='bgr',bufferfmt='ubyte')
        self.image.texture = texture

if __name__ == "__main__":
    app = MyApp()
    app.run()
