import os
import requests
#from requests.models import Response

class Molgenis:
    """
    
    """

    def __init__(self, url, database, email, password):
        self.url = url
        self.database = database
        self.email = email
        self.password = password
        
        self.signin()
    

    def signin(self):
        """Sign into molgenis and retrieve session cookie"""
        query = 'mutation{signin(email: "%s", password: "%s"){status,message}}' % (self.email, self.password)

        response = requests.post(self.url + 'apps/central/graphql',
                                 json={'query': query}
                                 )

        responseJson = response.json()

        status = responseJson['data']['signin']['status']
        message = responseJson['data']['signin']['message']

        if status == 'SUCCESS':
            self.cookies = response.cookies
        elif status == 'FAILED':
            print(message)
            exit()
        else:
            print('Error: sign in failed, exiting.')
            exit()

    def downloadZip(self):
        """Download molgenis zip for given Database."""
        response = requests.get(
            self.url + self.database + '/api/zip',
            auth=(self.email, self.password),
            allow_redirects=True,
            cookies=self.cookies
        )

        if response.content:
            fh = open('data.zip', 'wb')
            fh.write(response.content)
            fh.close()
        else:
            print('Error: download failed, did you use the correct credentials?')
            exit()

    def uploadZip(self):
        """Upload molgenis zip to fill Database"""
        query = 'mutation{signin(email: "%s", password: "%s"){status,message}}' % (self.email, self.password)
        response = requests.post(
            self.url + 'apps/graphql-playground/graphql',
            json={'query': query}
        )

        self.cookies = response.cookies

        zip = {'file': open('upload.zip', 'rb')}
        response = requests.post(
            self.url + self.database + '/api/zip?async=true',
            auth=(self.email, self.password),
            allow_redirects=True,
            cookies=self.cookies,
            files=zip
        )
        try:
            os.remove("upload.zip")
        except PermissionError:
            # remove fails on windows
            pass
