import sys, argparse
from urllib.parse import urlparse, parse_qsl
import longpass
from hurry.filesize import filesize

def main():

    # Use argparse to get command line options
    # @todo Clean this up
    parser = argparse.ArgumentParser(description='Description here')
    parser.add_argument('-u', '--url', dest='url', type=str, required=True,help='url')
    parser.add_argument('-s', '--size', dest='size', type=int, default=1000000, help='Size of the password')
    parser.add_argument('-d','--delay', dest='delay', type=float, default=1, help='Time between requests in seconds')
    parser.add_argument('-r','--repeats', dest='repeats', type=int, default=20, help='Number of iterations')
    parser.add_argument('--variables', dest='variables', type=str, default=None, help='Additional POST variables')

    # Set command line options to a object
    args = parser.parse_args()


    # Create longpass object
    login = longpass.Longpass()

    # Set options
    login.url = args.url
    login.size = args.size
    login.repeats = args.repeats
    login.delay = args.delay
    try:
        if args.variables:
            login.payload = dict(parse_qsl(args.variables.replace(',', '&'), False, True))
    except Exception as e:
        exit(e)

    # Print the summary of the assigment
    # @todo Add url and ask for confirmation
    #login.updateUI(0, "Sending " + str(login.repeats) + " passwords sized " + filesize.size(login.size) + " in every " + str(login.delay) + " seconds.")
    login.updateUI(0, "Sending %d passwords sized %s in every %s seconds."
                   % (
                       login.repeats,
                       filesize.size(login.size),
                       login.delay
                   ))

    login.run()

if __name__ == '__main__':
    main()