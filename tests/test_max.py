
import sys
import os
sys.path.append(os.path.dirname(__file__) + '/../')

import textwrap
from tests.apibase import APIBase


obj = APIBase('torch.max')

def test_case_1():
    pytorch_code = textwrap.dedent(
        '''
        import torch
        x = torch.tensor([[1, 2, 3], [3, 4, 6]])
        result = torch.max(x)
        '''
    )
    obj.run(pytorch_code, ['result'])

def _test_case_2():
    pytorch_code = textwrap.dedent(
        '''
        import torch
        x = torch.tensor([[1, 2, 3], [3, 4, 6]])
        result = torch.max(x, dim=1)
        '''
    )
    obj.run(pytorch_code, ['result'])

def _test_case_3():
    pytorch_code = textwrap.dedent(
        '''
        import torch
        x = torch.tensor([[1, 2, 3], [3, 4, 6]])
        result = torch.max(x, 1, True)
        '''
    )
    obj.run(pytorch_code, ['result'])

def _test_case_4():
    pytorch_code = textwrap.dedent(
        '''
        import torch
        x = torch.tensor([[1, 2, 3], [3, 4, 6]])
        result = torch.max(x, dim=0, keepdim=True)
        '''
    )
    obj.run(pytorch_code, ['result'])

def test_case_5():
    pytorch_code = textwrap.dedent(
        '''
        import torch
        result = torch.max(torch.tensor([[1, 2, 3], [3, 4, 6]]))
        '''
    )
    obj.run(pytorch_code, ['result'])

def _test_case_6():
    pytorch_code = textwrap.dedent(
        '''
        import torch
        x = torch.tensor([[1, 2, 1], [3, 4, 6]])
        out = [torch.tensor(0), torch.tensor(1)]
        torch.max(x, dim=1, keepdim=False, out=out)
        '''
    )
    obj.run(pytorch_code, ['out'])

def _test_case_7():
    pytorch_code = textwrap.dedent(
        '''
        import torch
        dim, keepdim = 1, False
        result = torch.max(torch.tensor([[1, 2, 3], [3, 4, 6]]), dim, keepdim)
        '''
    )
    obj.run(pytorch_code, ['result'])