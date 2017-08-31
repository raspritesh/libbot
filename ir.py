import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BOARD)
GPIO.setup(29,GPIO.IN)    #left ir sensor
GPIO.setup(31,GPIO.IN)    #right ir sensor
GPIO.setup(32,GPIO.OUT)   #en1 for motor A
GPIO.setup(33,GPIO.OUT)   #motor A1
GPIO.setup(35,GPIO.OUT)   #motor A2
GPIO.setup(36,GPIO.OUT)   #motor B1
GPIO.setup(37,GPIO.OUT)   # motor B2
GPIO.setup(38,GPIO.OUT)   #en2 for motor B
while True:
    leftirsensor=GPIO.input(29)
    rightirsensor=GPIO.input(31)
    if leftirsensor and rightirsensor: # move forward-both enable pins should be high
        GPIO.output(32,GPIO.HIGH)     #en1 for enabling left motor high
        GPIO.output(38,GPIO.HIGH)      #en2 for enabling right motor high
        GPIO.output(33,GPIO.HIGH)       #for moving left motor in forward direction
        GPIO.output(35,GPIO.LOW)        # for moving left motor in forward direction
        GPIO.output(36,GPIO.HIGH)       """for moving right motor in 
        GPIO.output(37,GPIO.LOW)              forward direction"""
    elif leftirsensor==0 and rightirsensor:  #if leftirsensor comes on black line;move bot left;run only right motor
        GPIO.output(32,GPIO.LOW)             #for disabling left motor
        GPIO.output(38,GPIO.HIGH)            # for enabling right motor
        GPIO.output(36,GPIO.HIGH)            """ for moving right motor 
        GPIO.output(37,GPIO.LOW)                    in forward direction"""
    elif rightirsensor==0 and leftirsensor:  # if rightirsensor comes on black line;move bot right;run only left motor
        GPIO.output(32,GPIO.HIGH)         #enabling left motor 
        GPIO.output(38,GPIO.LOW)     #disabling right motor
        GPIO.output(33,GPIO.HIGH)    """ moving left motor
        GPIO.output(35,GPIO.LOW)              in forward direction"""
    else:                          # if both ir sensor comes on black line then stops
        GPIO.output(32,GPIO.LOW)      """ disabling both motors"""  
        GPIO.output(38,GPIO.LOW)
        
    
      
    
