
class Config(object):
    def __init__(self, files, cores=1, output_dir="."):
        from glob import glob
        import os
        self.files = glob("%s%s%s" % (files, os.sep, "*.fasta"))
        self.cores = cores
        self.output_dir = output_dir
