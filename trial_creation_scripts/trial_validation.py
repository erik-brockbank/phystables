import sys
from phystables.creator import start_RG_creator

### Simple stub to run the RGCreator for viewing and simulating phystables trials ###
if __name__ == "__main__":

    try:
        start_RG_creator()
    except SystemExit:
        pass
