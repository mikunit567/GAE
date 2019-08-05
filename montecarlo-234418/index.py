#!/usr/bin/env python2.7
import os
import webapp2
import jinja2
import httplib

template_dir = os.path.join(os.path.dirname(__file__), 'templates')
jinja_environment = jinja2.Environment(loader=jinja2.FileSystemLoader(template_dir), autoescape=True)


def doRender(handler, tname, values={}):
    temp = os.path.join(os.path.dirname(__file__), 'templates/' + tname)
    if not os.path.isfile(temp):
        doRender(handler, 'results.htm')
        return

    # Make a copy of the dictionary and add the path
    newval = dict(values)
    newval['path'] = handler.request.path

    template = jinja_environment.get_template(tname)
    handler.response.out.write(template.render(newval))
    return True


# Modified from: http://www.ibm.com/developerworks/aix/library/au-threadingpython/
# Fixed with try-except around urllib call

# https://8j3xxxjqml.execute-api.eu-central-1.amazonaws.com/prod


class Handler(webapp2.RequestHandler):
    def post(self):
        c = httplib.HTTPSConnection("9kbhzyrrok.execute-api.eu-west-2.amazonaws.com")
        dart = self.request.get('dartshots')
        decimal = self.request.get('decimal_accuracy')
        reporting = self.request.get('reporting_rate')
        resources = self.request.get('resources')
        service = self.request.get('lambda')

        json = '{ "dartshots": "' + dart + '",' '"decimal_accuracy": "' + str(decimal) + '","reporting_rate": "' + str(reporting) + '",''"resources": "' + str(resources) + '",''"lambda": "' + str(service) + '"}'

        c.request("POST", "/default", json)
        response = c.getresponse()
        data = response.read()
        doRender(self, 'results.htm', {'note': data})


class MainPage(webapp2.RequestHandler):
    def get(self):
        path = self.request.path
        doRender(self, path)


app = webapp2.WSGIApplication([('/random', Handler), ('/.*', MainPage)], debug=True)
