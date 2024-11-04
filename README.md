### TO DO
    27/10/24
     - current issues:
        [V]  The save frame function on the individual recognition scripts isnt importing correctly. 
            FullFace works. check the differences.
            Not an issue with the saving rn , but with the camera not opening properly on the second function (eyes) could be due to fullface using destroyallwindows function 

            FIXED: 
            Error was, each recognition file had a closing of the camera statement at the end. Removed that and passed opening and closing of camera as part of the functions in 'face_capture.py'



    29/10/24
    - to do features:
    [] QOL feature: loading bar in terminal for face capture segments (https://stackoverflow.com/questions/3173320/text-progress-bar-in-terminal-with-block-characters)

    - move register back to terminal use
    - server should only be receiving "username" and hour that its logged 
    - if an unregistered username is noticed return unknown and send an image of user to the server 

    -change the whole view. the server just needs to be for receiving data and displaying it in an app. not activiating the scripts.

    3/11/24
    [V] register back in terminal
    [V] Change model in the backend to recieve username and hour logging
    [V] if user does not match database of faces return a new username as unknown and take an image of the user 
    [ ] add feedback for the AI on the unknown users (loss function and good/bad function) + fixing function (if they get the user wrong tell them who it is)
    [ ] ORDER THE PI
