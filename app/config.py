import logging
from logging.handlers import TimedRotatingFileHandler
import os

class FeedLogger:
	def __init__(self, name='career_planner_feed', log_dir='logs', level=logging.WARNING):
		self.logger = logging.getLogger(name)
		self.logger.setLevel(level)

		if not os.path.exists(log_dir):
			os.makedirs(log_dir)

		log_file_path = os.path.join(log_dir, 'app.log')
		handler = TimedRotatingFileHandler(log_file_path, when='midnight', interval=1, backupCount=30)
		handler.suffix = '%Y-%m-%d'

		formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
		handler.setFormatter(formatter)

		if not self.logger.handlers:
			self.logger.addHandler(handler)

	def get_logger(self):
		return self.logger
