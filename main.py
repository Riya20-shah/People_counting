import numpy as np
from object_tracking import *
import imutils
import argparse
import cv2 as cv


# construct the argument parse and parse the arguments

ap = argparse.ArgumentParser()
ap.add_argument("-p" , "--prototxt" , required=True , help="path to caffel 'deploy' prototxt file")
ap.add_argument("-m" , "--model" , required=True , help="path to caffe pre-trained model")
ap.add_argument("-i" , "--input" , type=str , help="path to input video file")
args = vars(ap.parse_args())

# prototext_path = "MobileNetSSD_deploy.prototxt"
# model_path = "MobileNetSSD_deploy.caffemodel"

prototext_path = args["prototxt"]
model_path = args["model"]

min_condifience = 0.5
totalup = 0
totaldown = 0
status = "Waiting"
classes = ['background',
           'aeroplane', 'bicycle', 'bird', 'boat',
           'bottle', 'bus', 'car', 'cat', 'chair',
           'cow', 'diningtable', 'dog', 'horse',
           'motorbike', 'person', 'pottedplant',
           'sheep', 'sofa', 'train', 'tvmonitor']

# creatieng object tracking file object to use that class method

tracker = obj_track_class()

# ////////////////////////////////////
# Object detections
# /////////////////////////////////////

people_count = 0
bounding_boxes = []
net = cv.dnn.readNetFromCaffe(prototext_path , model_path)


if not args.get("input" , False):
    print("[info] starting video stream....")
    cap = cv.VideoCapture(0)
else:
    print("[info] opening video  file...")
    cap = cv.VideoCapture(args["input"])
while True:
    rec , image = cap.read()

    image = imutils.resize(image,600,600)
    if not rec:
        break


    height , width , _ = image.shape
    roi = image[int(height/2): , :]
    blob = cv.dnn.blobFromImage(cv.resize(image , (500 , 500)) , 0.007 , (500,500))
    net.setInput(blob)
    detected_object = net.forward()
    # here that detected in 4D array so we want to check one by one so that we check the shape of that and then iterate the one by one so the shape is [0][0][100][7] so we iterate it 100 times one by one
    # print(detected_object)
    cv.line(image , (0,height//2) , (width , height//2) ,(20,0,0) , 2 )
    for i in range(detected_object.shape[2]):
        curr_bbox = []
        status = "waiting"
        confidence = detected_object[0][0][i][2]       # in detected object we have to see 3rd because it is confidence out of 7 element from thr list so we can check it

        if confidence > min_condifience:
            class_index = int(detected_object[0][0][i][1])
            if classes[class_index] == "person":
                # upper_left_x = int(detected_object[0][0][i][3]*width)
                # upper_left_y = int(detected_object[0][0][i][4]*height)
                # lower_right_x = int(detected_object[0][0][i][5]*width)
                # lower_right_y = int(detected_object[0][0][i][6]*height)

                box = detected_object[0, 0, i, 3:7] * np.array([width, height, width, height])

                startX, startY, endX, endY = box.astype("int")

                prediction_txt = f"{classes[class_index]} : {confidence * 100:.2f}%"

                cv.rectangle(image, (startX, startY), (endX, endY), (255, 255, 255), 1)
                cv.putText(image, str(prediction_txt), (startX, startY - 25), cv.FONT_HERSHEY_SIMPLEX, 0.6, (255, 0, 255),
                           2)
                curr_bbox.append([startX, startY, endX, endY])
                # prev_bbox = curr_bbox.copy()
                # print("current box")
                # print(curr_bbox)
                # print(prev_bbox)
                # #
                 # # ////////////////////////////////////
                # # # # Object tracking
                # print("previous box")
                # # /////////////////////////////////////
                boxes_id = tracker.update_track(curr_bbox)
                status = tracker.status
                # print("boxes_id ",boxes_id)
                for box in boxes_id:
                    x, y, w, h, id = box
                    cx = ((x+w)/2)
                    cy = ((y+h)/2)

                    if int(cy) > (height / 2) and tracker.counted_object == True:
                        totalup += 1


                    if int(cy) < (height / 2) and tracker.counted_object == True:
                        totaldown += 1


                    cv.putText(image, f"Id : {str(id)}", (int(cx)-10, int(cy)-10), cv.FONT_HERSHEY_SIMPLEX, 0.6, (100, 255, 100), 2)
                    cv.circle(image , (int(cx),int(cy)), 4, (0, 120, 0), -1)






        info = [
            ("Up", totalup),
            ("Down", totaldown),
            ("Status", status)]
        for (i, (k, v)) in enumerate(info):
            text = "{}: {}".format(k, v)
            cv.putText(image, text, (10, height - ((i * 30) + 20)),
                       cv.FONT_HERSHEY_SIMPLEX, 0.6, (70, 70, 230), 2)




    # cv.putText(image , f"people count : {people_count}" ,(17 , 250), cv.FONT_HERSHEY_SIMPLEX, 0.6,(255, 0, 0), 2)
    cv.imshow("frm", image)
    key = cv.waitKey(1)
    if key == ord("q"):
        break
cv.waitKey(0)
cv.destroyAllWindows()
