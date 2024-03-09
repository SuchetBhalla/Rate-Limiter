# Modules
import requests
from multiprocessing import current_process
import time
import concurrent.futures

# This function makes a request to the (local) backend app, which uses a rate-limiting algorithm
def make_requests(user_id, ip_address, num_requests):

    # This is the API endpoint
    api_url = 'http://localhost:5000/api/resource'

    # The user must pass his user_ID and IP_Address to the server, for rate-limiting
    headers = {'user-id': user_id, 'ip-address': ip_address}

    # Prints the response of each request (by each process)
    for i in range(num_requests):
        response = requests.get(api_url, headers=headers)
        print(f"Request #{i+1} :: {response.json()['message']} :: Process #{current_process().pid}")

        # Delays consecutive-requests by 1 second
        time.sleep(1)

if __name__ == '__main__':

    # Number of requests each process will make
    requests_per_process = 4

    # 4 user-IDs (& IP-addresses) for testing
    num_processes = 4

    (u1, ip1) = ('Karan', '111')
    (u2, ip2) = (u1, '222') # Same user_ID but different IP address, requests are considered unique
    (u3, ip3) = ('Arjun', '333')
    (u4, ip4) = (u3, ip3) # Duplicate user_ID & IP_address, requests are considered common

    # Forks 4 processes to simulate 4 users who parallely access the backend
    with concurrent.futures.ProcessPoolExecutor(max_workers= num_processes) as executor:
        executor.map(make_requests, [u1, u2, u3, u4], [ip1, ip2, ip3, ip4], [requests_per_process]*num_processes)
