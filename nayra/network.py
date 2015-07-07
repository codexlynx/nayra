import urllib2

class request(object):

    def __init__(self):
        '''Optional class variable'''
        self.proxy = '' #http://user:passwd@host:port
        self.cookies = ''
        self.userAgent = ''

    def send(self, path, method = 'GET'):
    
        if self.proxy != '':
            phandler = urllib2.ProxyHandler({'http': self.proxy})
            opr = urllib2.build_opener(phandler)
        else:
            opr = urllib2.build_opener()
            
        opr.addheaders = [('Cookie', self.cookies),
                          ('User-Agent', self.userAgent)]
        
        if method == 'GET':
            con = opr.open(path)

        elif method == 'POST':
            if path.count('?') >= 1:
                path = path.split('?')
            else:
                path = [path, '']
                
            con = opr.open(path[0], path[1])
            
        data = con.read()
        return data

    
