# motion_detection_video_capture
* Camera is installed on a raspberry pi (raspbian OS).
* When camera detects motion, it uploads pictures of detected motion drop box. 

## High level Summary
* Makes use of python's CV2 algorithms to compare frames.
* Use image subtraction and averaging of pixels to detect motion.
