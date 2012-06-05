from _fbusker import *

def main():
    """
        fbusker.py
        AUTHOR: magnate/r82x
        USAGE: python fbusker.py facebookuserid (destinationpath)

        Facebook hides photo tags from you while searching plainly for them --
        So you have to grab the albums of your mutual friends and then search
        for tags within.

        This automates this via the API. Filenames are saved in the format 
        userid_albumid_sourcefile in a directory specified by the second
        argument, the first being the user ID of the user you are targeting.
        If the destination path is not provided, the files will be saved in the
        current directory.
    """
    if len(sys.argv) < 2:
        print "Requires a UID of a facebook user to find in photos"
        exit(1)

    target = sys.argv[1]
    if len(sys.argv) >= 3:
        # provided a directory
        destination = sys.argv[2]
        if destination[-1] != '/':
            destination += '/'
    else:
        destination = os.getcwd()

    fbusker = FBusker(target, destination)
    fbusker.run()

if __name__ == "__main__":
    main()