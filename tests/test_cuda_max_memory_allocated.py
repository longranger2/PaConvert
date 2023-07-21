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

import textwrap

from apibase import APIBase


class cudaMaxMemoryAllocatedAPI(APIBase):
    def compare(
        self,
        name,
        pytorch_result,
        paddle_result,
        check_value=True,
        check_dtype=True,
        check_stop_gradient=True,
    ):
        return pytorch_result == paddle_result


obj = cudaMaxMemoryAllocatedAPI("torch.cuda.max_memory_allocated")


def test_case_1():
    pytorch_code = textwrap.dedent(
        """
        import torch
        result = None
        if torch.cuda.is_available():
            result = torch.cuda.max_memory_allocated()
        """
    )
    obj.run(pytorch_code, ["result"])


def test_case_2():
    pytorch_code = textwrap.dedent(
        """
        import torch
        result = None
        if torch.cuda.is_available():
            t = torch.tensor([1,2,3]).cuda()
            result = torch.cuda.max_memory_allocated()
        """
    )
    obj.run(pytorch_code, ["result"])


def test_case_3():
    pytorch_code = textwrap.dedent(
        """
        import torch
        result = None
        if torch.cuda.is_available():
            t = torch.tensor([1,2,3]).cuda()
            result = torch.cuda.max_memory_allocated(0)
        """
    )
    obj.run(pytorch_code, ["result"])


def test_case_4():
    pytorch_code = textwrap.dedent(
        """
        import torch
        result = None
        if torch.cuda.is_available():
            t = torch.tensor([1,2,3]).cuda()
            result = torch.cuda.max_memory_allocated(device=0)
        """
    )
    obj.run(pytorch_code, ["result"])


def test_case_5():
    pytorch_code = textwrap.dedent(
        """
        import torch
        result = None
        if torch.cuda.is_available():
            t = torch.tensor([1,2,3]).cuda()
            result = torch.cuda.max_memory_allocated(torch.device("cuda:0"))
        """
    )
    obj.run(pytorch_code, ["result"])


def test_case_6():
    pytorch_code = textwrap.dedent(
        """
        import torch
        result = None
        if torch.cuda.is_available():
            t = torch.tensor([1,2,3]).cuda()
            result = torch.cuda.max_memory_allocated(device=torch.device("cuda:0"))
        """
    )
    obj.run(pytorch_code, ["result"])
