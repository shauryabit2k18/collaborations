# DESTELLO
## https://shauryabit2k18.github.io/.

### **Problem Description :**

- Concentrating while studying is one of the most difficult tasks that a human can do. With all the distractions surrounding us, it becomes even harder to focus all of our attention to reading papers, books, pdfs, etc, or even watching online course video lectures. Sometimes while reading we tend to space out and wander out in our imaginative world. So when we see the big picture even after sitting at the desk for almost 2-3 hours a day the total time we soak up the information we read or see is not more than 30min. 

- Also sometimes there is an important work that needs to be done immidiately due to a deadline the next day but while completing if we tend to fall asleep thereby can suffer losses. Also there is no metric currently available that tells us how productive were we the entire day and how much time were we stressed or really concentrated while studying.

- Parents are not able to keep a check on the productiveness and activity of their children and the same cases happens with employer and employee. Also in today's world where we have screens all around us, continuous use of these gadgets can cause fatigue and Computer Vision Syndrome(CVS) which in turn causes severe eye damage. 

### **Solution we offer:**

- Our hack would first check the activity of our user, if the user is reading a pdf or reading stuff on websites like Medium or blogs that has been tagged under education, our program would track the eye of the user using the webcam which will provide him with important data about his productivity i.e what fraction of time was the user really concentrating.

- We will provide an android app which will keep a track record of the user’s activities, the time he spends on the computer studying and concentrated while doing so, which will be visible to authorized users (the user himself/ Parent/ Employer).

- Our program will also detect hazardous behavior based on the user's eye dynamics and detect any anomalies in the blink frequency using standard values set by the medical community.


### **OUR PLAN OF EXECUTION :**

- **Deep Learning:**
  We will be using deep learning to track eye movement, blink frequency to get data for the concentration-time and eye fatigue. First we will detect the face of the user (i.e. to detect if the user is studying or not) then localize it to eye detection and then further to detect and track the iris and pupil for blink and gaze detection.

- **Desktop Application:** 
  In the laptop we will be displaying the data of his productiveness by tracking the processes happening in the laptop i.e whether the website he has opened has an educational tag or the user is reading a pdf and integrating this to our ML model for eye detection as explained above.

### **Tech-stack used**

RabbitMQ, MongoDB, NodeJs, Tkinter(for gui), ExpressJs, youtube's and a few other apis.

### **Future Scope**

- We would continue to work on this project even after the hacathon is over incooperating new ideas and features to this is just prototype and should not be considered as a production level code.
- In the future we would also incooperate better UI and UX with individual user login and signup with gaze detection (which was not possible this time due to an absence of an HD camera).
- With not just an windows based application in the future users will be able to access their profiles via websites and anroid apps as well.

### **Challenges we faced**

- The biggest challenge we faced was scanning the eye of the user with low resolution camera but with low specs and under appropriate conditions it can provide better accuracy. Then the next challenge was monitoring the processes which was difficult because there are a number of background apps running which windows won't allow to close. Then integrating all parts ML, process scanner, chrome extension was the toughest one. Thanks to RabbitMQ, it would have been impossible without it which provided realtime messaging service to which we used to communicate between all of the above mentioned parts. 

### ** Steps to Run**

1. Start RabbitMq server
2. Start mongodb server
3. start Avinish/database/index.js with node
4. Then just run Avinish/gui/ui.py with python

### **Screenshots**
![Landing](https://github.com/hackabit19/Hack_Elite/blob/master/Capture.PNG)

![Drowziness Detection](https://github.com/hackabit19/Hack_Elite/blob/master/Capture1.PNG)

![No face detected](https://github.com/hackabit19/Hack_Elite/blob/master/Capture2.PNG)
![Facial detection](https://github.com/hackabit19/Hack_Elite/blob/master/Capture3.PNG)
![Blinking](https://github.com/hackabit19/Hack_Elite/blob/master/Capture4.PNG)
