from util import get_attach, save_file, logging
import re

class Spider:
    def __init__(self, endId, startId):
        self.endId = endId
        if startId:
            self.initId = int(startId)
        else:
            print('reading init id from log')
            self.initId = self.get_init_id(-50)
        self.rootUrl = 'https://bbs.tju.edu.cn/api/attach/'

    def get_init_id(self, offset):
        try:
            with open('log', 'rb+') as logger:
                while True:
                    logger.seek(offset, 2)
                    lines = logger.readlines()
                    if len(lines) >= 2:
                        last_line = lines[-1]
                        print(last_line)
                        break
                    else:
                        offset *= 2
                init_id = re.match(r'(.*--->>>---\s)(\d+)(.*)', last_line.decode('utf-8')).group(2)
                return int(init_id)

        except EnvironmentError:
            return 50000

    def start(self):
        try:
            logger = open('log', 'a')
            for attachId in range(self.initId+1, self.endId):
                attachment = get_attach(self.rootUrl + str(attachId))
                if attachment:
                    save_file(attachment)
                logging(logger, attachId)
        finally:
            if logger:
                logger.close()

start_id = input('enter start id: (OPTIONAL)')
end_id = input('enter end id: ')
bbsSpider = Spider(int(end_id), start_id)
bbsSpider.start()
