Takes folder of bunch of images of moving object and combines them into one sequence image

![alt text](https://github.com/pete995/Sequence-Combiner/blob/master/banner.jpg)

Usage:
  -install python and pip
  -install opencv by running command line argument "pip install opencv-python"
  -run main.py with command "python .\main.py yourfoldernamehere useBlur useDilate treshold=50 o=out.jpg"
    
Extra command line arguments:
  -treshold= = custom treshold (defaults to 50) <br/>
  -useBlur = uses blur to help motion detection <br/>
  -useDilate = uses dilate to help motion detection <br/>
  -width = custom width to output <br/>
  -height = custom height to output <br/>
  -o= = custom output name (defaults to out.jpg) <br/>
