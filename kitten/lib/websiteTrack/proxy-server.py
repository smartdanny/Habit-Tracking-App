# ***************************************************
# THIS FILE IS TO ONLY BE RUN ON THE KITTEN PROXY WEB SERVER
# DO NOT BUNDLE WITH CLIENT-SIDE APPLICATION
# ****************************************************
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import urlparse
import logging
import datetime

# Set up initial logging settings for user POST requests
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s %(message)s')
file_handler = logging.FileHandler('/var/log/squid/server_tracing.log')
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)

DIR = '/var/log/squid/' # file location
FILE = 'access.log' # file name

def getLines():
    '''
    Simply returns all the lines from /var/log/squid/access.log
    '''
    # Open access.log with read permission
    try:
        log = open(DIR + FILE, 'r')
    except Error as err:
        logger.info('Error opening access.log:', err)
    lines = log.readlines()
    return lines

def clearLog(lines, host):
    '''
    This function erases all footprints left behind on the Kitten proxy log. This serves
    two purposes:

    1) Slows down the process of file bloating - access.log grows very quickly which can hinder the getLines() funciton
    2) Assure that the next tracking session is accurate and doesn't read any prior GET requests from access.log
    '''
    count = 0

    with open(DIR + FILE, 'w') as log:
        for line in lines:

            # Parse through line and get client_ip
            line_params = line.split()
            client_ip = line_params[2]

            # Write line back if it doesn't hold client_ip
            if client_ip != host:
                log.write(line)
            else:
                count += 1
    logger.info("Deleted %s lines from access.log...", str(count))

def getWebsiteCount(lines, host, website_list):
    '''
    Takes the user-provided website list and compares it against all entries in access.log
    where the IP address of the client host matches
    '''
    # Initialize dictionary to store website visit count
    website_count = {}

    # Parse & grab all lines that contain client address
    for line in lines:

        # Parse through line and get client_ip
        line_params = line.split()
        client_ip = line_params[2]

        # Compare client_ip to all other IP addresses in access.log
        if client_ip == host:

            # Get domain
            url = line_params[6]
            output = urlparse(url)
            domain = output[2]

            # Process the domain
            if domain.find(':') != -1:
                domain = domain[0:domain.find(':')]
            if domain.find('www') != -1:
                domain = domain[domain.find('www.') + 4:]

            # If the log's domain matches the user-provided websites list
            if domain in website_list:

                # Increase website count if a match is found
                if domain in website_count:
                    website_count[domain] = website_count[domain] + 1
                else:
                    website_count[domain] = 1

                logger.info("Count of %s increased by one...", domain)

    return website_count

class CustomHTTPRequestHandler(BaseHTTPRequestHandler):
    '''
    Overrides the BaseHTTPRequestHandler class to provide a custom handler for Kitten
    client POST requests. This handler extracts the provided user-inputted website list and
    executes the necessary processing to return an access count per website in .csv format
    '''
    # Handle POST request
    def do_POST(self):
        # Log the host and the port
        logger.info('---------------------')
        (host, port) = self.client_address
        logger.info('Client Host: %s', host)
        logger.info('Client Port: %s', str(port))

        # Get lines from all log files
        lines = getLines()
        length = str(len(lines))
        logger.info('Num of access.log lines: %s', length)

        # Get list of websites from client
        content_length = int(self.headers['Content-Length'])
        data = self.rfile.read(content_length)
        websites = str(data, 'utf-8')
        website_list = websites.split()
        logger.info('Websites List:')
        for website in website_list:
            logger.info('--> %s', website)

        # Get website count
        website_count = getWebsiteCount(lines, host, website_list)
        length = str(len(website_count))
        logger.info('Website count calculated for %s websites...', length)

        # Open logs files to overwite them
        clearLog(lines, host)
        logger.info("Cleared access.log of client's prior activity...")

        # Send 200 OK
        self.send_response(200)

        # Send headers first
        self.send_header('Content-type','text')
        self.end_headers()

        # Send content to client formatted as csv
        logger.info("The following values will be sent to %s at %s", host, str(port))
        for key, value in website_count.items():
            logger.info('%s, %s', key, str(value))
            self.wfile.write(str.encode(key + ", " + str(value) + "\n"))

        return

def run():
    now = datetime.datetime.now()
    logger.info("Time:", now.strftime("%Y-%m-%d %H:%M"))
    HOST = ''
    PORT = 8080
    logger.info('Server starting up')
    server_address = (HOST, PORT)
    httpd = HTTPServer(server_address, CustomHTTPRequestHandler)
    logger.info('Server running on port ' + str(PORT) + '...')
    httpd.serve_forever()

if __name__ == '__main__':
    run()
