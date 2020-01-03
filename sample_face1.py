#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Bezelie Sample Code : Face Recognition Test
import picamera                        # カメラ用モジュール
import picamera.array                  # カメラ用モジュール
import cv2                             # Open CVモジュール    
import bezelie                         # べゼリー専用サーボ制御モジュール

cascade_path =  "haarcascade_frontalface_alt.xml" # 顔認識xml
cascade = cv2.CascadeClassifier(cascade_path)

# サーボの準備
bez = bezelie.Control()               # べゼリー操作インスタンスの生成
bez.moveCenter()                      # サーボをセンタリング

# メインループ
def main():
  with picamera.PiCamera() as camera:                         # Open Pi-Camera as camera
    with picamera.array.PiRGBArray(camera) as stream:         # Open Video Stream from Pi-Camera as stream
      camera.resolution = (640, 480)                          # Display Resolution
      camera.hflip = True                                     # Vertical Flip 
      camera.vflip = True                                     # Horizontal Flip
      while True:
        camera.capture(stream, 'bgr', use_video_port=True)    # Capture the Video Stream
        gray = cv2.cvtColor(stream.array, cv2.COLOR_BGR2GRAY) # Convert BGR to Grayscale
        facerect = cascade.detectMultiScale(gray,             # Find face from gray
          scaleFactor=1.9,                                    # 1.1 - 1.9 :the bigger the quicker & less acurate 
          minNeighbors=3,                                     # 3 - 6 : the smaller the more easy to detect
          minSize=(80,120),                                  # Minimam face size 
          maxSize=(640,480))                                  # Maximam face size
        if len(facerect) > 0:
          for rect in facerect:
            cv2.rectangle(stream.array,                       # Draw a red rectangle at face place 
              tuple(rect[0:2]),                               # Upper Left
              tuple(rect[0:2]+rect[2:4]),                     # Lower Right
              (0,0,255), thickness=2)                         # Color and thickness
          print ("顔を発見")
        cv2.imshow('frame', stream.array)                     # Display the stream
        bez.movePitch (1, 0)
        if cv2.waitKey(1) & 0xFF == ord('q'):                 # Quit operation
          break
        stream.seek(0)                                        # Reset the stream
        stream.truncate()
      cv2.destroyAllWindows()

if __name__ == "__main__":
  main()
