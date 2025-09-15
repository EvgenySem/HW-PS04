import sys

try:
    print("Attempting to exit...")
    sys.exit(0)  # Exit with status 0 (success)

except SystemExit as e:
    print(f"Caught SystemExit with exit code: {e.code}")
    # You can perform cleanup or logging here before re-raising or allowing the program to terminate
    # If you want to prevent the program from exiting at this point, you would not re-raise.
    # If you want to ensure the program exits, you can re-raise the exception or call sys.exit() again.
    # raise # Uncomment to re-raise the SystemExit and terminate the program
except:
    print("Error")

