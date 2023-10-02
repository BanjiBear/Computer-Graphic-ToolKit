import os
from typing import Dict

from package.util import constant


class EnvSetting:

	ENV : Dict[str, str] = {}

	# def __init__(self, path_to_env_file):
	# 	self.path_to_env_file = path_to_env_file
	# 	self.ENV : Dict[str, str] = {}

	@classmethod
	def read_env_file(cls, path_to_env_file):
		with open(path_to_env_file, "rt") as file:
			for line in file:
				line = line.strip()
				if line.find(constant.ENV_FILE_COMMENT) >= 0 or line.find(constant.ENV_FILE_SEP) < 0:
					continue
				cls.ENV[line[0 : line.find(constant.ENV_FILE_SEP)]] = line[line.find(constant.ENV_FILE_SEP) + 1 : len(line)]

