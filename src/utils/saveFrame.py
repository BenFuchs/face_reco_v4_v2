import os 
import cv2 as cv 

def save_frame(frame, user_name, userFolder, regionFolder):
    output_dir = os.path.join(userFolder, regionFolder)
    os.makedirs(output_dir, exist_ok=True)
    
     # Construct the filename based on user name, region, and a unique identifier
    frame_count = len([f for f in os.listdir(output_dir) if f.endswith('.png')])
    png_filename = os.path.join(output_dir, f"{user_name}_{regionFolder}_{frame_count:04d}.png")
    cv.imwrite(png_filename, frame)
    # print(f"Saved {png_filename}") 
