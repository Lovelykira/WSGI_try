from wsgiref.simple_server import make_server
from cgi import parse_qs, escape




def form(env):
    print(env.get('CONTENT_LENGTH','0'))
    content_length = int(env.get('CONTENT_LENGTH','0'))

    d = env['wsgi.input'].read(content_length)  #post data
    d_d = parse_qs(d)


    return d_d.get(b'a')[0].decode('UTF-8')
    #return "form"

route = {'form':form}


def app(env, resp_start):
    resp_start('200 OK', [('content-type','text/html')])
    #buf = [('%s:%s<br>'%(k,v)).encode('UTF-8') for k, v in env.items()]


    qs = env.get('QUERY_STRING', '')
    qs = parse_qs(qs)


    path = env.get('PATH_INFO')[1:]
    parts = path.split('/')
    print(parts)
    fn = route.get(parts[0])
    res = ""
    if fn is not None:
        res = fn(env)


    with open('index.html','r') as f:
        #html = (f.read() % (qs.keys(),)).encode('UTF-8')
        #html = f.read().format(qs.get('a'), res).encode('UTF-8')
        html = f.read().format("", res).encode('UTF-8')


    #return res
    return [html]    #app  must return arr of strings

serv = make_server('',8080,app)
serv.serve_forever()