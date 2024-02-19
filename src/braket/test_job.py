from braket.aws import AwsDevice, AwsQuantumJob
from braket.circuits import Circuit, FreeParameter, Observable
from braket.devices import Devices
from braket.jobs import get_job_device_arn, save_job_result
from braket.jobs.metrics import log_metric
from braket.validation import dry_run


def run_hybrid_job(num_tasks: int):
    # use the device specified in the hybrid job
    device = AwsDevice(get_job_device_arn())

    # create a parametric circuit
    circ = Circuit()
    circ.rx(0, FreeParameter("theta"))
    circ.cnot(0, 1)
    circ.expectation(observable=Observable.X(), target=0)

    # initial parameter
    theta = 0.0

    for i in range(num_tasks):
        # run task, specifying input parameter
        task = device.run(circ, shots=100, inputs={"theta": theta})
        exp_val = task.result().values[0]

        # modify the parameter (e.g. gradient descent)
        theta += exp_val

        log_metric(metric_name="exp_val", value=exp_val, iteration_number=i)

    save_job_result({"final_theta": theta, "final_exp_val": exp_val})


if __name__ == "__main__":

    dry_run.enable()
    
    job = AwsQuantumJob.create(
        device="arn:aws:braket:::device/quantum-simulator/amazon/sv1",  # choose priority device
        #source_module="/Volumes/workplace/sdkdev/amazon-braket-sdk-python/src/braket/test_job.py",  # specify file or directory with code to run
        source_module="/Volumes/workplace/sdkdev/amazon-braket-sdk-python/src/braket",  # specify file or directory with code to run
        entry_point="braket.test_job:run_hybrid_job",  # specify function to run
        hyperparameters={"num_tasks": 5},
        wait_until_complete=True,
    )
    print(type(job))
    print(job.result())