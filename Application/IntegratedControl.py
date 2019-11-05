#!/usr/bin/env python3
# -*- coding: utf-8 -*-
'集成控制核心'
__author__ = '林金行'

import threading
from CopyFunction import *
from InteractiveCenter import *
from DownloadPicture import *

class IntegratedControl(object):
    def run(self):
        #cf = CopyFunction("G:\\Downloads\\[Xrip][Sora_no_Otoshimono_Final-Eternal_My_Master][BDrip][1080P][hevc_8bit_flac].mkv","F:\\")
        dp = DownPict(2)
        tic = InteractiveCenter(dp)
        try:
            tic.start()
            time.sleep(0.5)
            dp.start()
            tic.join()
            dp.join()
            #print("控制输出：" + cf.control)
        except BaseException as e:
            print(e)
        pass
    pass


inc = IntegratedControl()
inc.run()