 

from assets.PageName import PageName
from assets.ButtonName import ButtonName
from assets.PopupName import PopupName

from modules.AllPage.Page import Page
from modules.AllTask.Task import Task

from modules.utils import click, swipe, match, page_pic, button_pic, popup_pic, sleep, ocr_area

import numpy as np
import logging

class RunExchangeFight(Task):
    def __init__(self, levelnum, runtimes, name="RunExchangeFight") -> None:
        """
        after enter the location, start to raid
        
        levelnum start from 0
        """
        super().__init__(name)
        self.levelnum = levelnum
        self.runtimes = runtimes

     
    def pre_condition(self) -> bool:
        return Page.is_page(PageName.PAGE_EXCHANGE_SUB)
    
     
    def on_run(self) -> None:
        # 找到目标关卡点击，不用滚动
        clickind = self.levelnum
        points = np.linspace(209, 605, 5)
        logging.info("click level {}".format(self.levelnum+1))
        seepopup = self.run_until(
            lambda: click((1118, points[clickind])),
            lambda: match(popup_pic(PopupName.POPUP_TASK_INFO)))
        if not seepopup:
            logging.warn("没有成功点击到关卡，任务结束")
            return
        logging.info("start raid")
        # max raid or times raid
        if self.runtimes < 0:
            click((1084, 302))
        else:
            for t in range(max(0,self.runtimes-1)):
                # add times
                click((1014, 300))
        # 点击开始扫荡
        self.run_until(
            lambda: click(button_pic(ButtonName.BUTTON_CFIGHT_START)),
            lambda: match(popup_pic(PopupName.POPUP_NOTICE)) or match(popup_pic(PopupName.POPUP_TOTAL_PRICE))
        )
        # 如果弹出购买票卷的弹窗，取消任务
        if match(popup_pic(PopupName.POPUP_TOTAL_PRICE), threshold=0.9):
            logging.warn("扫荡卷或体力不足，取消任务")
        else:
            # 弹出确认框，点击确认
            logging.info("confirm and close notice popup")
            self.run_until(
                lambda: click(button_pic(ButtonName.BUTTON_CONFIRMB)),
                lambda: not match(popup_pic(PopupName.POPUP_NOTICE))
            )
        
        # 关闭弹窗，回到EXCHANGE_SUB页面
        self.run_until(
            lambda: click(Page.MAGICPOINT),
            lambda: Page.is_page(PageName.PAGE_EXCHANGE_SUB)
        )
        
        
        
    
     
    def post_condition(self) -> bool:
        return Page.is_page(PageName.PAGE_EXCHANGE_SUB)