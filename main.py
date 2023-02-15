from modules.face_detection import FaceDetector
from modules.face_recognition import FaceRecognition
import cv2
if __name__ == '__main__':
    face_detector = FaceDetector()
    face_recognition = FaceRecognition()

    test1 = cv2.imread('test/test2.jpg')
    # test2 = cv2.imread('test/test2.jpg')
    face1 = face_detector.detect(test1)['faces'][0]
    # face2 = face_detector.detect(test2)['faces'][0]
    # print(face_recognition.compare(face1, face2))

    
    # define a video capture object
    vid = cv2.VideoCapture(0)
    
    while(True):
        
        # Capture the video frame
        # by frame
        ret, frame = vid.read()

        predict  = face_detector.detect(frame)
        boxes = predict['boxes']
        faces = predict['faces']


        for idx,(x, y, w, h) in enumerate(boxes):
            cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
            cv2.putText(frame,str(face_recognition.compare(faces[idx],face1)),(x,y),cv2.FONT_HERSHEY_SIMPLEX,1,(0,255,255),1,cv2.LINE_AA)




        # Display the resulting frame
        cv2.imshow('frame', frame)
        
        # the 'q' button is set as the
        # quitting button you may use any
        # desired button of your choice
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    
    # After the loop release the cap object
    vid.release()
    # Destroy all the windows
    cv2.destroyAllWindows()

