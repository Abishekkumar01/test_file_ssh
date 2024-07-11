import cv2
import cvlib as cv
from cvlib.object_detection import draw_bbox
import urllib.request
import numpy as np
import concurrent.futures

# Replace with your camera's IP address
url = 'http://192.168.32.121/cam-hi.jpg'

def fetch_and_display(url, window_name):
    cv2.namedWindow(window_name, cv2.WINDOW_AUTOSIZE)
    while True:
        try:
            img_resp = urllib.request.urlopen(url)
            img_data = img_resp.read()
            imgnp = np.array(bytearray(img_data), dtype=np.uint8)
            img = cv2.imdecode(imgnp, -1)

            if img is not None:
                if window_name == "live transmission":
                    cv2.imshow(window_name, img)
                elif window_name == "detection":
                    bbox, label, conf = cv.detect_common_objects(img)
                    img = draw_bbox(img, bbox, label, conf)
                    cv2.imshow(window_name, img)
            else:
                print("Failed to decode image")
                print(img_data[:100])  # Print the first 100 bytes of the response to check the content
        except Exception as e:
            print(f"Error fetching or processing image: {e}")

        key = cv2.waitKey(5)
        if key == ord('q'):
            break

    cv2.destroyAllWindows()

if __name__ == '__main__':
    print("Started")

    # Run fetch_and_display concurrently for live transmission and detection windows
    with concurrent.futures.ProcessPoolExecutor() as executor:
        executor.submit(fetch_and_display, url, "live transmission")
        executor.submit(fetch_and_display, url, "detection")
