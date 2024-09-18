import sys
import time




class Spining:

    def __init__(self):
        separate = ["|","/","--","//"]

        try:

            while True:
                for _sep in separate:
                    sys.stdout.write(f'\rLoading.....{_sep}')  # Overwrite previous character
                    sys.stdout.flush() # Force print to terminal without delay
                    time.sleep(0.2)
        except KeyboardInterrupt:
            sys.stdout.write('\rDone!  \n') # Clean exit message



v= Spining()