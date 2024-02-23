# Copyright Amazon.com Inc. or its affiliates. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License"). You
# may not use this file except in compliance with the License. A copy of
# the License is located at
#
#     http://aws.amazon.com/apache2.0/
#
# or in the "license" file accompanying this file. This file is
# distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF
# ANY KIND, either express or implied. See the License for the specific
# language governing permissions and limitations under the License.

from collections import Counter
from typing import Optional

import numpy as np


class MeasurementsList(list):
    """
    The gate model quantum task result measurements list. The measurements
    list is callable and can take in a list of qubits to measure.

    Args:
        measurements:  measurements (np.ndarray): 2d array - row is shot and column is qubit.
            Default is None. Only available when shots > 0. The qubits in `measurements`
            are the ones in `GateModelQuantumTaskResult.measured_qubits`.
    """

    def __init__(self, measurements: np.ndarray):
        super().__init__(measurements)

    def __call__(self, **kwds: np.ndarray) -> np.ndarray:
        if kwds:
            return MeasurementsList._selected_measurements(
                self, range(len(self)), kwds.get("qubits")
            )

    def __str__(self):
        return str(np.asarray(self))

    def _selected_measurements(
        measurements: np.ndarray, measured_qubits: list[int], targets: Optional[list[int]]
    ) -> np.ndarray:
        selected_measurements = np.array(measurements)
        if targets is not None and not np.array_equal(targets, measured_qubits):
            # Only some qubits targeted
            columns = [measured_qubits.index(t) for t in targets]
            selected_measurements = selected_measurements[:, columns]
        return selected_measurements
