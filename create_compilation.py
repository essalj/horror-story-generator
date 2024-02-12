
import os

path_0 = "C:\my\__youtube\videos\2024-02-12_1145_compillation"
xp_path = os.path.normpath(path_0)
mp4_files = [os.path.join(xp_path, file) for file in os.listdir(xp_path) if file.endswith(".png")]
