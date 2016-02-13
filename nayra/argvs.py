import sys

class Parser(object):

    def __init__(self):
        self.type = ''
        self.url = ''
        self.method = 'GET'
        self.name = 'php_1'
        self.cookies = None
        self.proxy = ''
        self.path = 0
        self.file = ''
        self.help = False

    def parse(self):
        numArgvs = len(sys.argv) - 1
        if sys.argv[numArgvs] == '-h' or sys.argv[numArgvs] == '--help':
            self.help = True
        elif numArgvs == 1:
            self.help = True
        else:
            for i in range((numArgvs / 2)):
                opt = sys.argv[i + (i + 1)]
                value = sys.argv[i + (i + 2)]

                if opt == '-t' or opt == '--type':
                    self.type = value

                elif opt == '-u' or opt == '--url':
                    self.url = value

                elif opt == '-m' or opt == '--method':
                    self.method = value

                elif opt == '-n' or opt == '--name':
                    self.name = value

                elif opt == '-c' or opt == '--cookies':
                    self.cookies = value

                elif opt == '-x' or opt == '--proxy':
                    self.proxy = value

                elif opt == '-p' or opt == '--path':
                    self.path = value

                elif opt == '-f' or opt == '--file':
                    self.file = value

                else:
                    self.help = True
