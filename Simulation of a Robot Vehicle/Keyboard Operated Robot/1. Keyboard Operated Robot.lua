-- 1. Keyboard Operated Robot

function sysCall_init() 
    
    -- Motors Initialization
    motorLeft=sim.getObjectHandle("Pioneer_p3dx_leftMotor") 
    motorRight=sim.getObjectHandle("Pioneer_p3dx_rightMotor") 
    speed= 5
    
    -- Sensors Initialization
    usensors={-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1}
    for i=1,16,1 do
        usensors[i]=sim.getObjectHandle("Pioneer_p3dx_ultrasonicSensor"..i)
    end
    noDetectionDist=0.5
    maxDetectionDist=0.2
    detect={0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0}
    
    -- Braitenberg Values Initialization
    braitenbergL={-0.2,-0.4,-0.6,-0.8,-1,-1.2,-1.4,-1.6, 0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0}
    braitenbergR={-1.6,-1.4,-1.2,-1,-0.8,-0.6,-0.4,-0.2, 0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0}
end

function sysCall_cleanup() 
 
end 

function sysCall_actuation() 
    message, auxiliaryData = sim.getSimulatorMessage()

    -- Measuring Distance using Sensors
    for i=1,16,1 do
        res,dist=sim.readProximitySensor(usensors[i])
        if (res>0) and (dist<noDetectionDist) then
            if (dist<maxDetectionDist) then
                dist=maxDetectionDist
            end
            printToConsole('Distance', dist)
            detect[i]=1-((dist-maxDetectionDist)/(noDetectionDist-maxDetectionDist))
        else
            detect[i]=0
        end
    end

    -- Moving in the Arena Using Keyboard Keys
    if (message==sim.message_keypress) then

        -- Moving with the Up Key
        if (auxiliaryData[1] == 2007) then
            sim.setJointTargetVelocity(motorLeft,speed)
            sim.setJointTargetVelocity(motorRight,speed)
            printToConsole('Up Key', 'Left Motor', speed, 'Right Motor', speed)
        end

        -- Moving with the Down Key       
        if (auxiliaryData[1] == 2008) then
            sim.setJointTargetVelocity(motorLeft, -speed)
            sim.setJointTargetVelocity(motorRight, -speed)
            printToConsole('Down Key', 'Left Motor', -speed, 'Right Motor', -speed)
        end

        -- Moving with the Left Key
        if (auxiliaryData[1] == 2009) then
            sim.setJointTargetVelocity(motorLeft, 0)
            sim.setJointTargetVelocity(motorRight, speed)
            printToConsole('Left Key', 'Left Motor', 0, 'Right Motor', speed)
        end

        -- Moving with the Right Key
        if (auxiliaryData[1] == 2010) then
            sim.setJointTargetVelocity(motorLeft, speed)
            sim.setJointTargetVelocity(motorRight, 0)
            printToConsole('Right Key', 'Left Motor', speed, 'Right Motor', 0)
        end

    end

end
