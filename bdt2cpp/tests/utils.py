import os

def prepare_test_env():
    if not os.path.isdir('./build'):
        os.mkdir('build')
