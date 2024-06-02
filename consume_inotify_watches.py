import os
import inotify_simple
import tempfile
import errno
import time

def consume_inotify_watches():
    inotify = inotify_simple.INotify()
    watch_flags = inotify_simple.flags.MODIFY

    # Create a list to store watch descriptors
    watch_descriptors = []

    # Define the directory to create files in
    base_dir = '/tmp/inotify_test'

    # Create the base directory if it doesn't exist
    os.makedirs(base_dir, exist_ok=True)

    try:
        while True:
            # Create a temporary file in the base directory
            temp_file = tempfile.NamedTemporaryFile(dir=base_dir, delete=False)
            temp_file.close()

            # Add a new inotify watch on the temporary file
            wd = inotify.add_watch(temp_file.name, watch_flags)
            watch_descriptors.append((wd, temp_file.name))

            print(f'Added watch {wd} on file {temp_file.name}')

    except OSError as e:
        if e.errno == errno.ENOSPC:
            print(f'OSError: {e} (ENOSPC: No space left on device)')
            print('Reached the limit of inotify watches or another system limit.')
        else:
            print(f'OSError: {e}')
        print('Continuing to run...')

    # Enter an infinite loop to keep the program running
    while True:
        try:
            time.sleep(60)  # Sleep for a while to reduce CPU usage
        except KeyboardInterrupt:
            break  # Exit the loop if interrupted by the user

    print('Cleaning up...')
    # Clean up by removing all watches and deleting files
    for wd, temp_file in watch_descriptors:
        inotify.rm_watch(wd)
        os.remove(temp_file)

if __name__ == '__main__':
    consume_inotify_watches()
