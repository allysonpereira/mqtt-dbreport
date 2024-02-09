import cv2
import numpy as np
from datetime import datetime
 
class Walk:
    def __init__(self):
        self.max_data_len = 100000
        self.clip_low = -20000
        self.clip_high = 2000
        self.middle_val = 150
        self.scale_neg = 4.0
        self.walk_img = None
        self.avg_pixel_intensities = []
        self.avg_intensity = 0
 
    def process(self, img):
        img_b = img[:, :, 0]
        img_b = img_b.astype(np.float32)
        diff = img_b - self.middle_val
        diff[diff < 0] *= self.scale_neg
        if self.walk_img is not None:
            self.walk_img += diff
        else:
            self.walk_img = diff
        self.walk_img = np.clip(self.walk_img, self.clip_low, self.clip_high)
        avg_px_intensity = np.sum(self.walk_img)/self.walk_img.size
        avg_px_intensity = (avg_px_intensity - self.clip_low) / (self.clip_high - self.clip_low) * 100
        self.avg_pixel_intensities.append(avg_px_intensity)
        if len(self.avg_pixel_intensities) > self.max_data_len:
            self.avg_pixel_intensities.pop(0)
        self.avg_intensity = avg_px_intensity  
        return self.walk_img, avg_px_intensity
   
    def post_process(self, img):
        img = ((img - np.min(img)) / (np.max(img) - np.min(img)) * 255).astype(np.uint8)
        img = cv2.normalize(img, None, 0, 255, cv2.NORM_MINMAX, cv2.CV_8U)
        return img
 
if __name__ == "__main__":
    show = True
    scab = False
    threshold_high = 25
    threshold_low = 16
    cap = cv2.VideoCapture(r"C:/Users/c000851700/Desktop/MQTT_Deployment/short_vids/scab1_cut.mp4")
    walk = Walk()
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        processed_img, avg_intensity = walk.process(frame)
        post_processed_img = walk.post_process(processed_img)
        
        # Print the value of avg_intensity
        print("Average Intensity:", avg_intensity)
        
        # Print the value of scab before the condition
        print("Scab Status (Before Condition):", scab)
 
        # TODO - Do something with the avg_intensity
        if scab and avg_intensity > threshold_high:
            scab = False
            time_scab_disappear = datetime.now()
            print("Scab Disappear, frame: ", cap.get(cv2.CAP_PROP_POS_FRAMES))

            # print what would be going to database
            print("Scab Appear at: ", time_scab_appear)
            print("Scab Disappear at: ", time_scab_disappear)
            print("Scab Duration: ", time_scab_disappear - time_scab_appear)

        elif not scab and avg_intensity < threshold_low:
            scab = True
            time_scab_appear = datetime.now()
            print("Scab Appear, frame: ", cap.get(cv2.CAP_PROP_POS_FRAMES))
            
        # Print the value of scab after the condition
        print("Scab Status (After Condition):", scab)
 
        # print(avg_intensity)
 
        # Optionally display the images
        if show:
            cv2.putText(frame, f'Avg Intensity: {avg_intensity:.2f}', (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2, cv2.LINE_AA)
            cv2.imshow('Original', frame)
            cv2.imshow('Processed', post_processed_img)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
 
    cap.release()
    cv2.destroyAllWindows()