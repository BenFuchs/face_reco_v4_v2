### TO DO
    27/10/24
     - current issues:
        [V]  The save frame function on the individual recognition scripts isnt importing correctly. 
            FullFace works. check the differences.
            Not an issue with the saving rn , but with the camera not opening properly on the second function (eyes) could be due to fullface using destroyallwindows function 

            FIXED: 
            Error was, each recognition file had a closing of the camera statement at the end. Removed that and passed opening and closing of camera as part of the functions in 'face_capture.py'