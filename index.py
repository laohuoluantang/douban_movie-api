import tornado.web
from tornado import gen
import tornado.httpserver
import tornado.ioloop
import tornado.options
import  aiomysql
import asyncio
import time
import logging
import json
logging.basicConfig(level = logging.DEBUG)
pool = " "
class IndexHandler(tornado.web.RequestHandler):

    async def get(self):
        # pool = await get_mysql_pool()
        if self.application.first_time:
            global pool
            pool = await self.application.pool
            self.application.first_time = False
        movie_id = self.get_argument('id', "0")
        async with pool.acquire() as conn:
            async with conn.cursor() as cur:
                sql = "select *from movie_messages where movie_id=" + movie_id
                await cur.execute(sql)
                value = await cur.fetchall()
                logging.info(value)
                keys = ['id', 'title', 'imageurl', 'rate', 'report', 'looked', 'wantlook']
                ret  = {k:v for (k, v) in zip(keys , value[0])}
                ret  = json.dumps(ret, ensure_ascii=False)
        self.write(ret)

    def write_error(self, status_code, **kwargs):
        self.write("error233333")


async def get_mysql_pool():
    print("dididid")
    return await aiomysql.create_pool(minsize=5,maxsize=100,host='172.17.0.3', port=3306, user='root', password='root', db='doubantop250')

class MyApplication(tornado.web.Application):

    def __init__(self):
        self.pool = get_mysql_pool()
        self.first_time= True
        handlers = [(r"/", IndexHandler)]
        tornado.web.Application.__init__(self, handlers)




if __name__ == "__main__":
    http_server = tornado.httpserver.HTTPServer(MyApplication())
    http_server.listen(8080)
    tornado.ioloop.IOLoop.instance().start()

