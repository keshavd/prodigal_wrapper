class InterProRunner(object):
    def __init__(self, faa_dir, output_dir):
        from glob import glob
        import os
        self.faas = glob("%s%s*.faa" % (faa_dir, os.sep))
        self.output_dir = output_dir
    def clean_input(self, input):
        import os
        cmd = "sed -i 's/*//g' %s\n" % input
        os.system(cmd)
        return 0
    def generate_cmd(self, input):
        import os
        import re
        out_file = "%s%s%s" % (self.output_dir, os.sep, re.sub(".faa", ".ip", os.path.basename(input)))
        cmd = "/mnt/storage/grid/home/keshav/tools/interpro_0517/interproscan-5.29-68.0/interproscan.sh -i  %s -b %s -goterms -pa -f json" % (input, out_file)
        return cmd
    def grid_run(self, input):
        from qsub import qsub
        self.clean_input(input)
        cmd = self.generate_cmd(input)
        qsub.single_job(name="interpro", user="keshav", errfile='/mnt/storage/grid/home/keshav/logs',
                        logfile="/mnt/storage/grid/home/keshav/logs", priority="smp-high", slots=1,
                        script=cmd).submit()
        return 0
    def grid_batch_run(self):
        from multiprocessing import Pool
        pool = Pool(1)
        try:
            pool.map(self.grid_run, self.faas)
        finally:
            pool.close()
            pool.join()
        return 0