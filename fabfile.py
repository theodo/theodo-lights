from fabric.api import *
from fabric.contrib.project import rsync_project
import os
from time import strftime

env.use_ssh_config = True
env.user = 'root'

env.roledefs = { 'test': ['192.168.101.146'], }

@roles('test')
def deploy():
  rsync_project(remote_dir='/opt/theodo-lights/', local_dir='./')
