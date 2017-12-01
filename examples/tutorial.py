from pycondor import Job, Dagman

# Define the error, output, log, and submit directories
error = 'condor/error'
output = 'condor/output'
log = 'condor/log'
submit = 'condor/submit'

# Instantiate a Dagman
dagman = Dagman(name='tutorial_dagman',
                submit=submit)

# Instantiate two Jobs
job_date = Job(name='date_job',
               executable='/bin/date',
               submit=submit,
               error=error,
               output=output,
               log=log,
               dag=dagman)

job_sleep = Job(name='sleep_job',
                executable='/bin/sleep',
                submit=submit,
                error=error,
                output=output,
                log=log,
                dag=dagman)
job_sleep.add_arg('1')
job_sleep.add_arg('2')
job_sleep.add_arg('3')

# Add inter-job relationships
# Ensure that job_sleep finishes before job_date starts
job_sleep.add_child(job_date)

# Write all necessary submit files and submit job to Condor
dagman.build_submit()
