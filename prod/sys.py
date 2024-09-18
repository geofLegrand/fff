import subprocess
import shutil

def kill_current_process():
    # The process name to be terminated
    process_name = "chromedriver.exe"
    try:
        # Employing the taskkill command to terminate the process
        result = subprocess.run(f"taskkill /f /im {process_name}", shell=True)

        if result.returncode == 0:
            print(f"Instance deletion successful: {process_name}")
            #shutil.rmtree("C:\\Users\\pc\\.wdm\\drivers\\chromedriver\\win64\\116.0.5845.188\\chromedriver-win32")
        else:
            print("Error occurred while deleting the instance.")
    except:
        pass