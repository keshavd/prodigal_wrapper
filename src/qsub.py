class qsubTemplate(str):

    @staticmethod
    def qsub_installed():
        import shutil
        loc = shutil.which('qsub')
        if loc is not None:
            return True
        else:
            return False

    def submit(self):
        import tempfile
        import subprocess
        import shlex
        fp = tempfile.NamedTemporaryFile()
        fp.write(str(self).encode('ascii'))
        fp.seek(0)
        file_name = fp.name
        if self.qsub_installed():
            cmd = "qsub %s" % file_name
            args = shlex.split(cmd)
            p = subprocess.Popen(args, stderr=subprocess.PIPE, stdout=subprocess.PIPE)
            output, errors = p.communicate()
            fp.close()
            print(output)
            return 0
        else:
            fp.close()
            raise FileNotFoundError("'qsub' is not installed")


class qsub(object):

    @staticmethod
    def single_job(**kwargs):
        SINGLE_TEMPLATE = """
#####################################
#$ -S /bin/bash
#$ -cwd
#$ -N {name}
#$ -u {user}
#$ -e {errfile}
#$ -o {logfile}
#$ -j y
#$ -pe {priority} {slots}
#$ -R y
#####################################
echo "------------------------------------------------------------------------"
echo "Job started on" `date`
echo "------------------------------------------------------------------------"
{script}
echo "------------------------------------------------------------------------"
echo "Job ended on" `date`
echo "------------------------------------------------------------------------"
"""
        try:
            temp = SINGLE_TEMPLATE.format(**kwargs)
            return qsubTemplate(temp)
        except KeyError as e:
            print("Missing arguments including: %s" % e)
            return 1

    def array_job(**kwargs):
        ARRAY_TEMPLATE = """
#####################################
#$ -S /bin/bash
#$ -cwd
#$ -u {user}
#$ -t 1 - {jobs}
#$ -N {name}
#$ -e {errfile}
#$ -o {logfile}
#$ -j y
#$ -pe {priority} {slots}
#$ -R y
#####################################
echo "------------------------------------------------------------------------"
echo "Job started on" `date`
echo "------------------------------------------------------------------------"
{script}
echo "------------------------------------------------------------------------"
echo "Job ended on" `date`
echo "------------------------------------------------------------------------"
"""
        try:
            temp = ARRAY_TEMPLATE.format(**kwargs)
            return qsubTemplate(temp)
        except KeyError as e:
            print("Missing arguments including: %s" % e)
            return 1


