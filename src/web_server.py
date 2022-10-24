import tornado.ioloop
import tornado.web
import json
import requests

lists = {u"深圳": "是经济特区，紧邻广州，接壤香港，人口约1200万",
         u"青岛": "旅游城市，濒临黄海，特产啤酒，人口约920万"
         }

def get_loc(city):
    r = requests.get("http://gc.ditu.aliyun.com/geocoding?a=%s" % city.encode('UTF-8'))
    loc = r.json()
    return "经度是%s，纬度是%s" % (loc["lon"], loc["lat"])

class BaseHandler(tornado.web.RequestHandler):
    def get_current_user(self):
        return self.get_secure_cookie("user")

class MainHandler(BaseHandler):
    def get(self):
        if self.request.arguments.has_key("id"):
            greeting = self.get_argument('id', 'Hello')
        if greeting in lists:
            self.write(greeting + ": " + str(get_loc(greeting)) + "," + str(lists[greeting]))
        else:
            self.write("none")

settings = dict(cookie_secret="P1/V61oETzdkLmGeJJFuYh7Eo5KXQAGaYgEQnp2XdTo=", debug=True)
application = tornado.web.Application([(r"/", MainHandler), ], **settings)

if __name__ == "__main__":
    application.listen(8888)
    tornado.ioloop.IOLoop.current().start()