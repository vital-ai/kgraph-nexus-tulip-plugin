import json
import sys
import requests


class KGraphNexusClient:
    def __init__(self, endpoint, port):
        self.endpoint = endpoint
        self.port = port

    def status(self):

        url = f"http://{self.endpoint}:{self.port}/health"

        status = "unknown"

        try:

            response = requests.get(url)
            response.raise_for_status()  # Raise an error for bad status codes
            data = response.json()

            status = data.get('status')

        except Exception as e:
            print(f"KGraphNexusClient Error: {e}", file=sys.stderr)
            status = "error"

        return status

    def search(self, search_string):

        result_list = []

        url = f"http://{self.endpoint}:{self.port}/query"

        headers = {
            'Content-Type': 'application/json'
        }
        payload = {
            'search_string': search_string
        }

        try:
            response = requests.post(url, headers=headers, data=json.dumps(payload))

            if response.status_code == 200:
                print(f"Response: {response.json()}", file=sys.stdout)

                response_data = response.json()

                result_list = response_data['result_list']
            else:
                print(f"Failed to call /query endpoint: {response.status_code}", file=sys.stderr)
                print(f"Response: {response.text}", file=sys.stderr)

        except Exception as e:
            print(f"KGraphNexusClient Error: {e}", file=sys.stderr)

        return result_list

    def domain_search(self, search_string):
        pass

    def graph_explore(self, uri_list, distance=1):

        result_list = []

        url = f"http://{self.endpoint}:{self.port}/graph-query"

        headers = {
            'Content-Type': 'application/json'
        }
        payload = {
            'node_list': uri_list
        }

        try:
            response = requests.post(url, headers=headers, data=json.dumps(payload))

            if response.status_code == 200:
                print(f"Response: {response.json()}", file=sys.stdout)

                response_data = response.json()

                result_list = response_data['result_list']
            else:
                print(f"Failed to call /graph-query endpoint: {response.status_code}", file=sys.stderr)
                print(f"Response: {response.text}", file=sys.stderr)

        except Exception as e:
            print(f"KGraphNexusClient Error: {e}", file=sys.stderr)

        return result_list

    def graph_import(self, graph_id):
        pass

    def graph_sync(self):
        pass



