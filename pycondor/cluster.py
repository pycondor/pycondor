import re
import subprocess
from enum import Enum
from configparser import RawConfigParser
from typing import Dict, Literal, List, Optional, Sequence, Union


class JobStatus(Enum):
    IDLE = 1
    RUNNING = 2
    REMOVING = 3
    COMPLETED = 4
    HELD = 5
    TRANSFERRING_OUTPUT = 6
    SUSPENDED = 7
    CANCELLED = 8
    FAILED = 9


def query(id: int) -> List[Dict[str, str]]:
    """
    Condor query a cluster or job id and return its
    response parsed as a config dictionary.
    """

    result = subprocess.check_output(["condor_q", "-l", str(id)], text=True)
    if not result:
        return []

    raw_configs = [i for i in result.split("\n\n") if i]
    configs = []
    for raw in raw_configs:
        config = RawConfigParser()
        config.read_string(rf"[DEFAULT]\n{raw}")
        config = dict(config["DEFAULT"])

        # strip out strings that are wrapped in quotes
        config = {k: v.strip('"') for k, v in config.items()}
        configs.append(config)
    return configs


class JobCluster:
    def __init__(self, id: int):
        self._id = id

        # query the entire cluster up front to parse out
        # the ids and condor files for each of the associated
        # processes in order to avoid having to make a query
        # for each process in the cluster.
        configs = query(id)
        procs = []
        for config in configs:
            proc = Proc(
                self,
                int(config["procid"]),
                log_file=config["userlog"],
                out=config["out"],
                err=config["err"],
            )
            procs.append(proc)

        self.procs: list[Proc] = procs

    def get_statuses(self) -> List[JobStatus]:
        """
        Condor query the cluster id and parse the responses
        for individual processes to get their statuses,
        returned as a list.
        """
        configs = query(self.id)
        configs = {int(c.pop("procid")): c for c in configs}
        statuses = []
        for proc in self.procs:
            try:
                config = configs.pop(proc.proc_id)
            except KeyError:
                status = proc.determine_exit_status()
            else:
                status = JobStatus(int(config["jobstatus"]))
            statuses.append(status)
        return statuses

    def check_status(
        self,
        status: Union[JobStatus, Sequence[JobStatus]],
        how: Literal["all", "any"] = "any"
    ) -> bool:
        """
        Determine if any or all of the processes in
        this job cluster have achieved any of the
        indicated statuses.
        """
        if isinstance(status, JobStatus):
            status = [status]
        statuses = self.get_statuses()
        reducer = any if how == "any" else all
        return reducer([i in status for i in statuses])

    @property
    def id(self):
        return self._id

    def rm(self) -> None:
        response = subprocess.run(
            ["condor_rm", str(self.id)], stderr=subprocess.STDOUT, text=True
        )
        if response.returncode:
            stdout = response.stdout

            # if the issue was just that the job no longer exists,
            # I guess consider this a succes? TODO: should this
            # be controlled with a kwarg?
            if stdout.startswith("Couldn't find/remove all jobs"):
                return
            raise RuntimeError(
                "condor_rm for cluster {} failed with message {}".format(
                    self.id, stdout
                )
            )


class Proc:
    def __init__(
        self,
        cluster: JobCluster,
        proc_id: int,
        log_file: Optional[str] = None,
        out: Optional[str] = None,
        err: Optional[str] = None,
    ) -> None:
        self.cluster = cluster
        self.proc_id = proc_id

        # if we specified all of the relevant files
        # for this process up front, then there's no
        # need to query the process id to determine them.
        self._ip = None
        if all([i is not None for i in [log_file, out, err]]):
            self._log_file = log_file
            self._out = out
            self._err = err
        else:
            # otherwise query the process and infer the names
            # of its stdout/stderr/log files. Since we're
            # querying anyway, check if this process has
            # been assigned an IP address
            config = query(self.id)
            if config:
                self._log_file = config["userlog"]
                self._err = config["err"]
                self._out = config["out"]

                if config["jobstatus"] == "2":
                    self._ip = self._parse_ip(config)

    @property
    def cluster_id(self) -> int:
        return self.cluster.id

    @property
    def id(self) -> str:
        proc_id = str(self.proc_id).zfill(3)
        return f"{self.cluster_id}.{proc_id}"

    def query(self) -> dict:
        """
        Condor query the metadata associated with this process
        """
        result = query(self.id)
        if not result:
            return {}
        return result[0]

    def read_log(self) -> str:
        """
        Read and return the condor log file associated
        with this process.
        """

        with open(self.log_file, "r") as f:
            return f.read()

    def parse_exit_code(self, log: str) -> Optional[int]:
        """
        Parse a process' condor log to see if it has
        exited, and if so whether it did so on its own accord.
        If yes, returns its exit code. In any other case,
        returns `None`.
        """

        for line in log.splitlines():
            if line.strip("\t ").startswith(
                "Job terminated of its own accord"
            ):
                match = re.search("(?<=with exit-code )[0-9]+", line)
                if match is None:
                    return None
                else:
                    return int(match.group(0))
        else:
            return None

    def parse_abort(self, log: str) -> bool:
        """
        Parse a process' condor log to determine
        whether it exited because it was aborted.
        """
        for line in log.splitlines():
            if line.endswith("Job was aborted."):
                return True
        return False

    def determine_exit_status(self) -> JobStatus:
        """
        Read this job's condor log and determine the
        conditions of its exit, whether it:
        - was aborted
        - failed on its own
        - successfully completed
        - what else?
        """

        # there's no config for this job, so assume
        # that it has finished and check its log
        # for any exit info
        log = self.read_log()
        exit_code = self.parse_exit_code(log)

        if exit_code is not None and exit_code > 0:
            # job exited of its own accord but with
            # a non-zero exit code, indicating a failure
            return JobStatus.FAILED
        elif exit_code == 0:
            # job exited of its own accord with exit
            # code zero, meaning the job completed
            # successfully
            return JobStatus.COMPLETED
        elif self.parse_abort(log):
            # the job didn't exit of its own accord,
            # but the log indicated it was aborted
            return JobStatus.CANCELLED
        else:
            # Anything else that might have caused
            # the job not to exist. TODO: this should
            # probably have its own status, e.g. UNKNOWN
            return JobStatus.COMPLETED

    def get_status(self) -> JobStatus:
        """
        Condor query the process' current status, and if
        the query is empty parse the process' condor log
        to determine why it's no longer running.
        """

        config = self.query()
        if not config:
            return self.determine_exit_status()
        return JobStatus(int(config["jobstatus"]))

    def _parse_ip(self, config):
        """
        Parse the metadata returned by `condor_q` to determine
        the internal cluster IP of the node to which the job was
        assigned. If the status of the process indicates that it's
        not currently running, return `None`.
        """
        if config["jobstatus"] != "2":
            return None

        pci = config["publicclaimid"]
        match = re.search("(?<=^<)[0-9.]+", pci)
        if match is None:
            raise ValueError(
                f"Couldn't parse IP address from public claim id {pci}"
            )
        return match.group(0)

    @property
    def ip(self) -> str:
        """
        Returns the cluster-internal IP address of the
        node on which the process is running, assuming
        that the process is currently running. This value
        is cached once it's successfully queried for future use.
        """

        if self._ip is not None:
            return self._ip

        config = self.query()
        if not config:
            return None

        ip = self._parse_ip(config)
        if ip is not None:
            self._ip = ip
        return ip

    @property
    def log_file(self) -> str:
        """
        Return the process' condor log file
        """

        if self._log_file is not None:
            return self._log_file

        config = self.query()
        if not config:
            return None
        self._log_file = config["userlog"]
        return self._log_file

    @property
    def err(self) -> str:
        """
        Return the process' stderr file
        """

        if self._err is not None:
            return self._err

        config = self.query()
        if not config:
            return None
        self._out = config["err"]
        return self._out

    @property
    def out(self) -> str:
        """
        Return the process' stderr file
        """
        if self._out is not None:
            return self._out

        config = self.query()
        if not config:
            return None
        self._out = config["out"]
        return self._out
