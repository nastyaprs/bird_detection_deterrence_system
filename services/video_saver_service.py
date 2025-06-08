import cv2
import tempfile
import platform


class VideoSaver:
    def __init__(self, width: int, height: int, fps: int):
        self.width = width
        self.height = height
        self.fps = fps
        self.path = None
        self.writer = None

    def create_temp_writer(self):
        if platform.system() == 'Windows':
            fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        else:
            fourcc = cv2.VideoWriter_fourcc(*'avc1')
        temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.mp4')
        self.path = temp_file.name
        self.writer = cv2.VideoWriter(self.path, fourcc, self.fps, (self.width, self.height))
        return self.writer, self.path

    def write_frame(self, frame):
        if self.writer:
            self.writer.write(frame)

    def release(self):
        if self.writer:
            self.writer.release()
        return self.path
