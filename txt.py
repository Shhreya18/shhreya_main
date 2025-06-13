import os
import subprocess

scripts_folder = 'LVLC_0.3'
script_port = 'COM3'
main_script = 'io_test1.py'

for filename in os.listdir(scripts_folder):
    if filename.endswith('.txt'):
        script_path = os.path.join(scripts_folder, filename) #gets the path to the txt file
        print(f'\n=== Running{filename} ===')
        subprocess.run(['python', main_script, script_port, script_path], check = True)