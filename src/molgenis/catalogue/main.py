import requests
import sys
import os


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

        response = requests.post(
            self.url + 'apps/central/graphql',
            json={'query': query}
        )

        responseJson = response.json()

        status = responseJson['data']['signin']['status']
        message = responseJson['data']['signin']['message']

        if status == 'SUCCESS':
            self.cookies = response.cookies
        elif status == 'FAILED':
            print(message)
            exit(1)
        else:
            print('Error: sign in failed, exiting.')
            exit(1)

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
            exit(1)

    def uploadZip(self):
        """Upload molgenis zip to fill Database"""
        query = 'mutation{signin(email: "%s", password: "%s"){status,message}}' % (self.email, self.password)
        response = requests.post(
            self.url + 'apps/graphql-playground/graphql',
            json={'query': query}
        )

        self.cookies = response.cookies

        # upload = zipfile.ZipFile('upload.zip', 'w')
        data = {'file': open('upload.zip', 'rb')}
        response = requests.post(
            self.url + self.database + '/api/zip?async=true',
            auth=(self.email, self.password),
            allow_redirects=True,
            cookies=self.cookies,
            files=data
        )
        data['file'].close()
        responseJson = response.json()

        try:
            response_id = responseJson['id']
            url = responseJson['url']
            print(f'Upload successful, id: {response_id}, url: {url}')
        except:
            errors = responseJson['errors'][0]
            print(f'Upload failed: {errors}')
        finally:
            try:
                if os.path.exists('upload.zip'):
                    os.remove('upload.zip')
            except PermissionError:
                sys.exit('Error deleting upload.zip')