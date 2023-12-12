from braket.devices.local_simulator import LocalSimulator
from braket.tracking.tracker import Tracker
from braket.schema_common.schema_base import BraketSchemaBase
from braket.validation.device_validator import DeviceValidator

class DryRun:
    def __init__(self) -> None:
        self._enabled = False
        self._results = {}
        self._tracker = Tracker()

    def enable(self) -> None:
        self._enabled = True
        self._tracker.start()

    # def __enter__(self):
    #     mod = __loader__.fullname
    #     mod.AwsDevice.run = LocalSimulator.run
    #     return self

    # def __exit__(self, *args):
    #     pass

    def is_enabled(self) -> bool:
        return self._enabled

    def create_task(self, **task_args) -> str:
        device_arn = task_args["deviceArn"]
        shots = task_args["shots"]
        program = BraketSchemaBase.parse_raw_schema(task_args["action"])
        print(program)
        device = LocalSimulator()
        local_task = device.run(program, shots=shots)
        self._results[local_task.id] = local_task
        return {"quantumTaskArn": local_task.id}
    
    def retrieve_results(self, task_id: str) -> "Result":
        return self._results[task_id]
    
    def disable(self) -> None:
        self._tracker = Tracker()
        self._results = {}
        self._enabled = False

    def print_stats(self) -> None:
        print(f"Task statistics {self._tracker.quantum_tasks_statistics()}")
        print(f"QPU task cost {self._tracker.qpu_tasks_cost()}")
        print(f"Simulator task cost {self._tracker.simulator_tasks_cost()}")


_dry_runner = DryRun()
enable = _dry_runner.enable
is_enabled = _dry_runner.is_enabled
create_task_dry_run = _dry_runner.create_task
retrieve_results = _dry_runner.retrieve_results
print_stats = _dry_runner.print_stats
disable = _dry_runner.disable

# c = Circuit()
# d = AwsDevice()
# t = d.run(c)
# r = t.result() 