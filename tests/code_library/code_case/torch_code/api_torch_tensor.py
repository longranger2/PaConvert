# Copyright (c) 2023 PaddlePaddle Authors. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#

import torch

print("#########################case1#########################")
# case 1: dtype、device、requires_grad、pin_memory
a = torch.tensor(
    torch.tensor([2, 3, 4]),
    dtype=torch.float32,
    device=torch.device("cuda"),
    requires_grad=True,
    pin_memory=True,
)
print("#########################case2#########################")
# case 2:
flag = True
a = torch.tensor(
    torch.tensor([2, 3, 4]),
    dtype=torch.float32,
    device=torch.device("cuda"),
    requires_grad=flag,
    pin_memory=True,
)
