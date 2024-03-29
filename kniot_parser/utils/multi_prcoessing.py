import abc
import time
import queue
from multiprocessing import Queue, Process, current_process
from .logger import Logger


def task(static_job, *arg, **kwarg):
    return static_job().processes_job(*arg, **kwarg)


class MultiProcessor:
    """multi processing"""

    def __init__(self, number_of_processes=6):
        self.number_of_processes = number_of_processes
        self.processes = []
        self.files_to_process = None

    def start_processes(self, static_job, *arg, **kwargs):
        """start the number of processers"""

        for index in range(self.number_of_processes):
            processor = Process(
                name=f"Process {index}",
                target=task,
                args=tuple([static_job] + list(arg)),
                kwargs=kwargs,
            )
            self.processes.append(processor)

        for processor in self.processes:
            processor.start()

            Logger.info(f"Starting process {index}.")

    def wait_to_finish(self, tasks_accomplished, size):
        """wait until all finish"""
        Logger.info("Starting waiting to all processes")
        while not tasks_accomplished.full():
            time.sleep(2)

        Logger.info("Finished waiting to all processes")

    @abc.abstractmethod
    def task_to_execute(self):
        """the task to execute"""
        raise NotImplementedError()

    @abc.abstractmethod
    def get_arguments_list(self):
        """create list of arguments"""
        raise NotImplementedError()

    def post(self, results):
        """post process the results"""
        return results

    def get_tasks_queue(
        self,
    ):
        """get a queue with all the tasks need to execute"""

        task_can_executed_indepentlly = self.get_arguments_list()
        tasks_to_accomplish = Queue()
        for raw in task_can_executed_indepentlly:
            tasks_to_accomplish.put(raw)
        return tasks_to_accomplish, len(task_can_executed_indepentlly)

    def execute(self):
        """execute task"""
        tasks_to_accomplish, size = self.get_tasks_queue()
        tasks_accomplished = Queue(maxsize=size)

        self.start_processes(
            self.task_to_execute(),
            tasks_to_accomplish=tasks_to_accomplish,
            tasks_accomplished=tasks_accomplished,
        )

        # no more jobs
        tasks_to_accomplish.close()
        tasks_to_accomplish.join_thread()

        #self.wait_to_finish(tasks_accomplished, size)

        results = []
        while not tasks_accomplished.empty() or len(results) < size:
            file_to_delete = tasks_accomplished.get(True)
            results.append(file_to_delete)

        assert len(results) == size, f"{len(results)} vs {size}"

        return self.post(results)


class ProcessJob:
    """processes jobs"""

    @abc.abstractmethod
    def job(self, **kwargs):
        """the job the process need to run"""
        raise NotImplementedError()

    def processes_job(self, tasks_to_accomplish=None, tasks_accomplished=None):
        """job to run on process"""
        while True:
            try:
                Logger.info(f"{current_process().name}: Waiting on queue.")
                task_kwargs = tasks_to_accomplish.get(True, timeout=5)
                Logger.info(f"{current_process().name}: Start processing {task_kwargs}")

            except queue.Empty:
                # other-wise the process exits at the start.
                if tasks_to_accomplish.empty():
                    Logger.info(f"{current_process().name}: Queue is empty. existing.")
                    break
            else:

                try:
                    file_processed = self.job(**task_kwargs)
                    Logger.info(
                        f"{current_process().name}: Placing results for {task_kwargs}."
                    )
                    tasks_accomplished.put(file_processed, True, timeout=5)
                    Logger.info(
                        f"{current_process().name}: End processing {task_kwargs}."
                    )
                except Exception as error:
                    Logger.info(
                        f"{current_process().name}:  failed with {error}, exiting."
                    )
                    return False

        return True
