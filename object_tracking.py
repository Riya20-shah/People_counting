import math

# import dlib
class obj_track_class():
    def __init__(self):
        # store the center pionts with id in dict
        self.center_point = {}
        #  # Keep the count of the IDs
        # each time a new object id detected, the count will increase by one
        self.id_count = 0
        self.status = 'Waiting'
        self.counted_object = False

    def update_track(self,obj_bounding_box):
        self.status = "Waiting"
        obj_bbox_ids = []
        for box in obj_bounding_box:
            # print(box)
            x,y,w,h = box
            cx = int((x+x+w)/2)
            cy = int((y+y+h)/2)

            # Find out if that object was detected already
            same_object_detected = False
            for id , pt in self.center_point.items():
                self.status = "Tracking"
                distance = math.hypot(cx-pt[0] , cy-pt[1])

                if distance < 35:
                    print('distance' , distance)
                    self.center_point[id] = (cx,cy)
                    print(self.center_point)
                    obj_bbox_ids.append([x,y,w,h,id])
                    same_object_detected = True
                    self.counted_object = False
                    break

            #if new object is detected we have to assign id
            if same_object_detected is False:
                self.status = "Tracking"
                self.counted_object = True
                self.center_point[self.id_count] = (cx,cy)
                obj_bbox_ids.append([x, y, w, h, self.id_count])
                print(self.center_point)
                self.id_count+=1


        # clean the centerpoints from dict to remove the ids not used anymore

        # # print("center point " ,self.center_point)
        # new_center_point = {}
        # for bbox in obj_bbox_ids:
        #     _, _, _, _, id = bbox
        #     center = self.center_point[id]
        #     new_center_point[id] = center
        # print("new dict " , new_center_point)
        # # Update dictionary with IDs not used removed
        # self.center_point = new_center_point.copy()
        return obj_bbox_ids

