import sys
import os

# Print to check the path
print("Current directory:", os.getcwd())
print("Absolute path exists:", os.path.exists('/Users/benayah/Desktop/Code/Sec_camera_project/face_reco_v4/face_reco_v4_v2/src'))

# Add the src path to sys.path
sys.path.insert(0, '/Users/benayah/Desktop/Code/Sec_camera_project/face_reco_v4/face_reco_v4_v2/src')

# Try the import again
from face_capture import face_capture  # Direct import if src is already added
print("Import works")