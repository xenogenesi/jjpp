from jinja2 import Template, Environment, FileSystemLoader
from time import gmtime, strftime
import json
import sys
import codecs
import yaml


class App:
    env = None
    json = None
    tpl = None
    out = None

    # def datetimeformat(self, value, format='%H:%M / %d-%m-%Y'):
    #     return strftime(format, value)

    def fatal(*objs):
        sys.stderr.write(*objs)
        sys.exit(1)

    def setOutput(self, filename):
        self.out = filename

    def run(self, inConfig, jinjaTemplates):
        # self.env = Environment(loader=FileSystemLoader('.'))
        # self.env = Environment(loader=FileSystemLoader('.'),extensions=['jinja2.ext.i18n'])

        if inConfig.endswith('.yml'):
            yml = yaml.load(open(inConfig,'r'))
            self.json = json.loads(json.dumps(yml))
        elif inConfig.endswith('.json'):
            self.json = json.load(open(inConfig,'r'))
        else:
            self.fatal("config format not handled, must be .yml or .json")


        # self.env.filters['datetime'] = self.datetimeformat

        # self.json['now'] = gmtime()

        self.env = Environment(loader=FileSystemLoader('.'),extensions=['jinja2.ext.do'])
        self.env.globals['output'] = self.setOutput

        for tpl in jinjaTemplates:
            self.tpl = self.env.get_template(tpl)
            render = self.tpl.render(self.json) #.encode('utf-8')
            if self.out == None:
                print render
            else:
                with codecs.open(self.out,'w',encoding='utf8') as out:
                    out.write(render)
                    out.close()
                    self.out = None



if __name__ == "__main__":
    if len(sys.argv) < 2:
        print "usage: cmd [config.json] [jinja2 templates...]"
        sys.exit(1)

    app = App()
    inConfig =  sys.argv[1]
    jinjaTemplates = sys.argv[2:]
    app.run(inConfig, jinjaTemplates)
