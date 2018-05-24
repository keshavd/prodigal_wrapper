class ProdigalRunner(object):

    def __init__(self, config):
        self.cores = config.cores
        self.files = config.files
        self.output_dir = config.output_dir

    def generate_cmd(self, input):
        import re
        import os
        out_aa = "%s%s%s" % (self.output_dir, os.sep, re.sub(".fasta", ".faa", os.path.basename(input)))
        out_coord = "%s%s%s" % (self.output_dir, os.sep, re.sub(".fasta", ".out", os.path.basename(input)))
        goi = re.sub(".fasta", ".prodigal", input)
        goi_exists = os.path.isfile(goi)
        prodigal_abs = os.path.abspath("../deps/prodigal")
        if goi_exists:
            cmd = '%s -i %s -o %s -a %s -t %s' % (prodigal_abs, input, out_coord, out_aa, goi)
        else:
            cmd = '%s -i %s -o %s -a %s -p meta' % (prodigal_abs, input, out_coord, out_aa)
        return cmd

    def local_run(self, input):
        import subprocess
        import os
        import shlex
        cmd = self.generate_cmd(input)
        args = shlex.split(cmd)
        print("PROCESSING %s" % (os.path.basename(input)))
        p = subprocess.Popen(args, stderr=subprocess.PIPE, stdout=subprocess.PIPE)
        output, errors = p.communicate()
        if errors == 0:
            return 0
        else:
            return 1

    def local_batch_run(self):
        from multiprocessing import Pool
        pool = Pool(self.cores)
        try:
            pool.map(self.local_run, self.files)
        finally:
            pool.close()
            pool.join()
        return 0

    def grid_run(self, input):
        from src.qsub import qsub
        cmd = self.generate_cmd(input)
        qsub.single_job(name="prodigal", user="keshav", errfile='/mnt/storage/grid/home/keshav/logs',
                        logfile="/mnt/storage/grid/home/keshav/logs", priority="smp-high", slots=1,
                        script=cmd).submit()
        return 0

    def grid_batch_run(self):
        from multiprocessing import Pool
        pool = Pool(self.cores)
        try:
            pool.map(self.grid_run, self.files)
        finally:
            pool.close()
            pool.join()
        return 0

