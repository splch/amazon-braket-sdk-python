from braket.validation import dry_run 
#import enable, is_enabled, disable, print_stats
from braket.aws import AwsDevice
from braket.circuits import Circuit
from braket.devices import Devices
from braket.device_schema.device_action_properties import DeviceActionType

dry_run.enable()


d = AwsDevice(Devices.Amazon.SV1)
c = Circuit().h(0)
t = d.run(c, shots=1)
print(t)
r = t.result()
print(r)


dry_run.print_stats()

# dry_run.disable()
# t = d.run(c, shots=1)
# print(t)
# r = t.result()
# print(r)