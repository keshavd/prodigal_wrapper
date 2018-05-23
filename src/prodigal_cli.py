
class prodigal_runner(object):
    def __init__(self, config):
        self.cores = config.cores
        self.genus = config.genus
        self.files = config.files
        self.output_dir = config.output_dir
    def run(self):
        import sys, os
        sys.path.append(os.path.abspath(os.path.join('..', 'deps')))
        os.system('deps/prodigal -h')

