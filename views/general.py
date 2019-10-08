from .base import View
from .logger import LoggerView
from .viewer import ViewerView
# from . import statistics


class GeneralView(View):
    def __init__(self):
        super().__init__()
        self.logger = LoggerView()
        self.viewer = ViewerView()
        # self.statistics = StatisticsView()

        self.menu_name = 'MAIN MENU'
        self.menu_options = {
            'logger':
            {'name': 'add new log', 'key': 'Enter', 'command': self.logger.main},
            'viewer':
            {'name': 'see last logs', 'key': 'l', 'command': self.viewer.main},
            # 'statistics':
            # {'name': 'see statistics', 'key': 's', 'command': statistics.main}
        }


if __name__ == '__main__':
    m = GeneralView()
    m.main()
