import sys
import subprocess
import os
import datetime
import platform
import time
import sys

# ASCII Art
shleemypants_ascii = """
 _____ _     _                                             _       
/  ___| |   | |                                           | |      
\ `--.| |__ | | ___  ___ _ __ ___  _   _ _ __   __ _ _ __ | |_ ___ 
 `--. \ '_ \| |/ _ \/ _ \ '_ ` _ \| | | | '_ \ / _` | '_ \| __/ __|
/\__/ / | | | |  __/  __/ | | | | | |_| | |_) | (_| | | | | |_\__ \

\____/|_| |_|_|\___|\___|_| |_| |_|\__, | .__/ \__,_|_| |_|\__|___/
                                    __/ | |                        
                                   |___/|_|                        

                 SUPER AWESOME SHLEEMING TOOL
     This tool is used to catch hackers doing bad things
"""

other_ascii = """
                             @                              
                            @                               
                       @ @(((&#(((((&                       
                      @((#(((&(((/@%(((((@                  
                     @(@((((((@(((((%(((((                  
                    ((((((((@(((@@@(((&&((((                
                  @(#@@@@@(/*/@@&&@@(#(((((@(@              
                  %/&&&&&&&&@ &&&@ #     . @*@              
                 @#@(((&#(((((((((@@ &@  @&@@               
                 *%@#(##((((((@(((@@(@(((@((((@             
 @@@#             %@#%@##%((#@#(@#&(##%#@@  %               
 %#(.@@                @@%#%%###(##@###@   #         @ @@/&@
  @(@((                 ...../###@.,  ,              %@ (@(@
     %(@             @...,.....@.....@              #(@((%  
       ((         (..... ......... @...@           /(%      
         ((@    /.&...  @.........   *...@       ((         
           (#%(%@.(@.  @..........     ...%@  @(&           
              @   @    %.........*      @  ###@             
                       /.........&                          
                       ..........@                          
                      %..........@                          
                      ,..........@                          
                     @........@@.&                          
                    @......*&..@,                           
                       ..../@@#                         

"""

print(shleemypants_ascii)
print(other_ascii)

# ASCII Skull
ascii_skull = " ☠ "

# Function to display a progress bar
def display_progress_bar(total, progress, bar_length=20):
    skull_count = int((progress / total) * bar_length)
    bar = ascii_skull * skull_count + '-' * (bar_length - skull_count)
    percent = (progress / total) * 100
    sys.stdout.write(f"\rProgress: [{bar}] {percent:.2f}%")
    sys.stdout.flush()

# Simulated task with progress bar
def simulated_task(total_steps=20, verbose=False):
    for step in range(total_steps + 1):
        if verbose:
            display_progress_bar(total_steps, step)
        time.sleep(0.5)  # Simulating a task
    print("\nTask Completed!")

# Run the simulated task with verbose output
simulated_task(verbose=True)

# Function to check if pywin32 is installed
def is_pywin32_installed():
    try:
        import win32evtlog
        return True
    except ImportError:
        return False

# Function to install pywin32 from a .whl file
def install_pywin32(whl_file):
    subprocess.run([sys.executable, "-m", "pip", "install", whl_file], check=True)
    # Restart the script after installation
    os.execl(sys.executable, sys.executable, *sys.argv)

# Function to get the appropriate .whl file based on the Python version
def get_pywin32_whl_file():
    version_info = platform.python_version_tuple()
    version_major = version_info[0]
    version_minor = version_info[1]
    architecture = 'win_amd64' if platform.architecture()[0] == '64bit' else 'win32'

    if (version_major, version_minor) == ('3', '9'):
        return f'pywin32-306-cp39-cp39-{architecture}.whl'
    elif (version_major, version_minor) == ('3', '11'):
        return f'pywin32-306-cp311-cp311-{architecture}.whl'
    else:
        raise RuntimeError("Unsupported Python version for this script.")

# Check if pywin32 is installed, if not and -i flag is present, install it
if '-i' in sys.argv and not is_pywin32_installed():
    whl_file = get_pywin32_whl_file()
    install_pywin32(os.path.join(os.getcwd(), whl_file))

# Rest of your imports should be placed here, after the potential installation of pywin32
import win32evtlog  # Requires pywin32

# Helper functions
def create_folder(folder_name):
    os.makedirs(folder_name, exist_ok=True)
    return folder_name

def write_to_file(path, text, mode='a'):
    with open(path, mode, encoding='utf-8') as file:
        file.write(text + '\n')

def get_events(log_type, event_ids=None, start_date=None):
    events = []
    hand = win32evtlog.OpenEventLog(None, log_type)
    flags = win32evtlog.EVENTLOG_BACKWARDS_READ|win32evtlog.EVENTLOG_SEQUENTIAL_READ

    while True:
        records = win32evtlog.ReadEventLog(hand, flags, 0)
        if not records:
            break
        for record in records:
            if (event_ids is None or record.EventID in event_ids) and (start_date is None or record.TimeGenerated >= start_date):
                events.append(f"Time: {record.TimeGenerated} \nEvent: {record.StringInserts}")
    win32evtlog.CloseEventLog(hand)
    return events

def dump_evtx_logs(log_names, output_folder):
    for log_name in log_names:
        subprocess.run(["wevtutil", "epl", log_name, os.path.join(output_folder, f"{log_name}.evtx")], check=True)

# Process command line arguments
folder_name = "audit" # Default folder name
start_date = None

for arg in sys.argv[1:]:
    if arg.startswith('--folder='):
        folder_name = arg.split('=')[1]
    elif len(arg) == 8 and arg.isdigit():
        start_date = datetime.datetime(int(arg[:4]), int(arg[4:6]), int(arg[6:8]))

# Create folder in the current execution directory
output_folder = create_folder(os.path.join(os.getcwd(), folder_name))

# Define the output file path
output_file = os.path.join(output_folder, "log.txt")

# Get software installation events
software_install_events = get_events("Application", [11707, 11724], start_date)

# Get WLAN and Wired AutoConfig events
wlan_events = get_events("Microsoft-Windows-WLAN-AutoConfig/Operational", None, start_date)
wired_events = get_events("Microsoft-Windows-Wired-AutoConfig/Operational", None, start_date)

# Write to the output file
write_to_file(output_file, "Software Installation Events:", mode='w') # 'w' to overwrite existing content
for event in software_install_events:
    write_to_file(output_file, event)

write_to_file(output_file, "\n\nWLAN-AutoConfig Events:")
for event in wlan_events:
    write_to_file(output_file, event)

write_to_file(output_file, "\n\nWired-AutoConfig Events:")
for event in wired_events:
    write_to_file(output_file, event)

# Dump

dump_evtx_logs(["Application", "Security", "System"], output_folder)

