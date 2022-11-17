import signal
import time
import cv2
from multiprocessing import Manager, Process, Pipe, Event
from djitellopy import Tello

from threading import Thread
import numpy as np

tello = None


def movement(exit_event, show_video_conn,  fly, show_video_conn2):


    global tello
    tello = Tello()
    tello.connect()
    tello.streamon()
    frame_read = tello.get_frame_read()

    if fly:
        tello.takeoff()

    def control():
        while True:
            tello.send_command_without_return('cw 30')
            time.sleep(1)
    def box():

        w = show_video_conn2.recv()
        print(w)
        time.sleep(1)

    th=Thread(target=control)
    th.start()
    th2=Thread(target=box)
    th2.start()

    while not exit_event.is_set():

        frame = frame_read.frame
        show_video_conn.send(frame)


    signal_handler(None)



def show_video(exit_event, pipe_conn, movement_conn):

    with open('object_detection_classes_coco.txt', 'r') as f:
        class_names = f.read().split('\n')
# get a different color array for each of the classes
    COLORS = np.random.uniform(0, 255, size=(len(class_names), 3))

# load the DNN model
    model = cv2.dnn.readNet(model='frozen_inference_graph.pb',
                        config='ssd_mobilenet_v2_coco_2018_03_29.pbtxt.txt',
                        framework='TensorFlow')


    while True:
        image = pipe_conn.recv()
        image_height, image_width, _ = image.shape
        blob = cv2.dnn.blobFromImage(image=image, size=(300, 300), mean=(104, 117, 123),
                                     swapRB=True)
        # start time to calculate FPS
        start = time.time()
        model.setInput(blob)
        output = model.forward()
        # end time after detection
        end = time.time()
        # calculate the FPS for current frame detection
        fps = 1 / (end-start)

        for detection in output[0, 0, :, :]:
            # extract the confidence of the detection
            confidence = detection[2]
            # draw bounding boxes only if the detection confidence is above...
            # ... a certain threshold, else skip
            class_id = detection[1]
            if confidence > .4 and class_id==1:
                # get the class id

                # map the class id to the class
                class_name = class_names[int(class_id)-1]
                color = COLORS[int(class_id)]
                # get the bounding box coordinates
                box_x = detection[3] * image_width
                box_y = detection[4] * image_height
                # get the bounding box width and height
                box_width = detection[5] * image_width
                box_height = detection[6] * image_height
                #отправляем размер рамки в процесс 1
                movement_conn.send(box_width)
                # draw a rectangle around each detected object
                cv2.rectangle(image, (int(box_x), int(box_y)), (int(box_width), int(box_height)), color, thickness=2)
                # put the class name text on the detected object
                cv2.putText(image, class_name, (int(box_x), int(box_y - 5)), cv2.FONT_HERSHEY_SIMPLEX, 1, color, 2)
                # put the FPS text on top of the frame
                cv2.putText(image, f"{fps:.2f} FPS", (20, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

        # display the frame to the screen

        cv2.imshow("Drone Tracking", image)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            exit_event.set()


if __name__ == '__main__':


    fly = True

    #канал для передачи кадров из процесса 1 в процесс 2
    parent_conn, child_conn = Pipe()
    #канал для передачи размера найденной метки из процесса 2 в процесс 1
    parent_conn2, child_conn2 = Pipe()

    exit_event = Event()


    with Manager() as manager:
        p1 = Process(target=movement,
                     args=(exit_event, child_conn, fly, parent_conn2, ))

        p2 = Process(target=show_video, args=(exit_event, parent_conn, child_conn2, ))


        p2.start()
        p1.start()
        p1.join()
        p2.terminate()
        p2.join()