from braket.device_schema.device_action_properties import DeviceActionType


class DeviceValidator:

    def __init__(self, device_arn) -> None:
        # TODO: Remove circular dependencies
        from braket.aws import AwsDevice
        self._device = AwsDevice(device_arn)

    def validate(self, circuit) -> None:
        for instruction in circuit.instructions:
            if instruction.operator not in self._device.properties.action[DeviceActionType.OPENQASM].supportedOperations:
                raise ValueError(f"{instruction.operator} is not supported on the device {self._device.name}")