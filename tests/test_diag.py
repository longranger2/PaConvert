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

obj = APIBase("torch.diag")


def test_case_1():
    pytorch_code = textwrap.dedent(
        """
        import torch
        x = torch.tensor([[-0.4264, 0.0255,-0.1064],
                        [ 0.8795,-0.2429, 0.1374],
                        [ 0.1029,-0.6482,-1.6300]])
        result = torch.diag(x, 0)
        """
    )
    obj.run(pytorch_code, ["result"])


def test_case_2():
    pytorch_code = textwrap.dedent(
        """
        import torch
        x = torch.tensor([ 0.5950,-0.0872, 2.3298])
        result = torch.diag(x)
        """
    )
    obj.run(pytorch_code, ["result"])


def test_case_3():
    pytorch_code = textwrap.dedent(
        """
        import torch
        x = torch.tensor([[-0.4264, 0.0255,-0.1064],
                        [ 0.8795,-0.2429, 0.1374],
                        [ 0.1029,-0.6482,-1.6300]])
        result = torch.diag(x, 2)
        """
    )
    obj.run(pytorch_code, ["result"])


def test_case_4():
    pytorch_code = textwrap.dedent(
        """
        import torch
        x = torch.tensor([[-0.4264, 0.0255,-0.1064],
                        [ 0.8795,-0.2429, 0.1374],
                        [ 0.1029,-0.6482,-1.6300]])
        result = torch.diag(input=x, diagonal=-3)
        """
    )
    obj.run(pytorch_code, ["result"])


def test_case_5():
    pytorch_code = textwrap.dedent(
        """
        import torch
        x = torch.tensor([[-0.4264, 0.0255,-0.1064],
                        [ 0.8795,-0.2429, 0.1374],
                        [ 0.1029,-0.6482,-1.6300]])
        out = torch.tensor([-0.4264, 0.0255,-0.1064])
        result = torch.diag(input=x, diagonal=0, out=out)
        """
    )
    obj.run(pytorch_code, ["result", "out"])