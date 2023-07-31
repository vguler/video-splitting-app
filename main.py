from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.filechooser import FileChooserListView
from kivy.config import Config
from moviepy.video.io.VideoFileClip import VideoFileClip

Config.set('graphics', 'width', '300')
Config.set('graphics', 'height', '500')

class VideoSplitterApp(App):
    def build(self):
        self.input_file = TextInput(multiline=False, size_hint_y=None, height=40)
        self.input_file.text = "Enter video file path here..."

        self.file_chooser = FileChooserListView(path=".")
        self.file_chooser.bind(selection=self.on_file_selection)

        self.clip_duration = TextInput(multiline=False, size_hint_y=None, height=40)
        self.clip_duration.text = "30"

        self.split_button = Button(text="Split Video Clips", size_hint_y=None, height=40)
        self.split_button.bind(on_press=self.split_video_into_clips)

        self.output_label = Label(text="", size_hint_y=None, height=40)

        layout = BoxLayout(orientation='vertical')
        layout.add_widget(self.input_file)
        layout.add_widget(self.file_chooser)
        layout.add_widget(self.clip_duration)
        layout.add_widget(self.split_button)
        layout.add_widget(self.output_label)

        return layout

    def on_file_selection(self, instance, selection, touch):
        if selection:
            self.input_file.text = selection[0]

    def split_video_into_clips(self, instance):
        input_video_path = self.input_file.text
        clip_duration = int(self.clip_duration.text)

        try:
            video = VideoFileClip(input_video_path)
            total_duration = video.duration

            for i, start_time in enumerate(range(0, int(total_duration), clip_duration)):
                clip_filename = f"clip_{i}.mp4"
                end_time = min(start_time + clip_duration, total_duration)
                clip = video.subclip(start_time, end_time)

                clip.write_videofile(clip_filename, codec="libx264", audio_codec="aac", temp_audiofile="temp-audio.m4a", remove_temp=True)

            video.reader.close()

            self.output_label.text = "Video clips have been created successfully!"
        except Exception as e:
            self.output_label.text = f"Error: {e}"

if __name__ == "__main__":
    VideoSplitterApp().run()
