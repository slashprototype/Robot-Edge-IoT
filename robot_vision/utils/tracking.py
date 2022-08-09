import pyrealsense2.pyrealsense2 as rs
import cv2

global data_translation
data_translation=[0,0,0]


# Declare RealSense pipeline, encapsulating the actual device and sensors
pipe = rs.pipeline()

# Build config object and request pose data
cfg = rs.config()
cfg.enable_stream(rs.stream.pose)

# Start streaming with requested config
pipe.start(cfg)

try:
    while True:
        # time.spleep(0.1)
        # Wait for the next set of frames from the camera
        frames = pipe.wait_for_frames()

        # Fetch pose frame
        pose = frames.get_pose_frame()
        if pose:
            # Print some of the pose data to the terminal
            data = pose.get_pose_data()
            # print("Frame #{}".format(pose.frame_number))
            data_1 = str(data.translation)
            
            # position = re.findall(r'\[(\S.*)\]', line)

            data_1 = data_1.split(',')
            data_2 = data_1[0].split(':')
            data_translation[0] = float(data_2[1])
            data_2 = data_1[1].split(':')
            data_translation[1] = float(data_2[1])
            data_2 = data_1[2].split(':')
            data_translation[2] = float(data_2[1])


            # print(data_translation)
            
            # pos_x = re.findall(r'x\s,',data_translation[0])
            
            # print(data_)
            # print("Position: {}".format(data.translation))
            # print("Velocity: {}".format(data.velocity))
            # print("Acceleration: {}\n".format(data.acceleration))

except:
    print('no camera')
    pipe.stop()