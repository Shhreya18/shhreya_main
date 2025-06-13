import os
import subprocess

scripts_folder = 'LVLC_0.3'
script_port = 'COM3'
main_script = 'io_test1.py'

def extract_number(filename):
    seperator = '_'
    if seperator in filename:
        parts = filename.split(seperator)
        try:
            return int(parts[0])
        except ValueError:
            return 0
    return 0

files = [f for f in os.listdir(scripts_folder) if f.endswith('.txt')]
files.sort(key=extract_number)

all_outputs = []

for idx, filename in enumerate(files):
    script_path = os.path.join(scripts_folder, filename)
    print(f'\n=== Running {filename} ===')
    result = subprocess.run(
        ['python3', main_script, script_port, script_path],
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True
    )
    print(result.stdout)
    all_outputs.append(f'\n=== Running {filename} ===\n{result.stdout}')
    ask_user = input('Pass or Fail? (p/f): ')
    if ask_user.lower() != 'y':
        print('Exiting the script. Creating a report file')
        
        for remaining in files[idx+1:]:
            remaining_path = os.path.join(scripts_folder, remaining)
            remaining_result = subprocess.run(
                ['python3', main_script, script_port, remaining_path],
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True
            )
            all_outputs.append(f'\n=== Running {remaining} ===\n{remaining_result.stdout}')
        
        with open('output.txt', 'w') as f:
            f.writelines(all_outputs)
        print('Batch output written to output.txt')
        break
    else:
        print('Continuing to the next script')