import matplotlib
from matplotlib import image
import numpy as np 
import pyrealsense2.pyrealsense2 as rs
import time

class Camera():
    def __init__(self,resx,resy,frecuency) -> None:
        self.pipeline = rs.pipeline()
        # Configure streams
        config = rs.config()
        config.enable_stream(rs.stream.color, resx, resy, rs.format.bgr8, frecuency)
        # Start streaming
        self.pipeline.start(config)
   
    def stop(self):
        self.pipeline.stop()

    def take_snap(self):
        try:
            frames = self.pipeline.wait_for_frames()
            color_frame = frames.get_color_frame()
            
            if not color_frame:
                print('no color frame')

            image = np.asanyarray(color_frame.get_data())
            return (image)

        except:
            print('take snap error')

if __name__ == '__main__':
    camara = Camera(640,480,30)
    time.sleep(2)
    image = camara.take_snap()
    camara.stop()