# PaConvert ![](https://img.shields.io/badge/version-v0.2.0-brightgreen) ![](https://img.shields.io/badge/docs-latest-brightgreen) ![](https://img.shields.io/badge/PRs-welcome-brightgreen) ![](https://img.shields.io/badge/pre--commit-Yes-brightgreen)

**Pa**ddlePaddle Code **Convert** Toolkits

# 重要
- 当前共支持约1200个Pytorch API的一键转换，我们通过285个Pytorch 模型代码测试，代码行数平均转换率约为 **85+%**
- 当前PaConvert转换工具还在内测中，欢迎下载试用，欢迎通过issue方式向我们报Bug与提建议

# 概述
PaConvert全称是 **代码转换工具**，能自动将其它深度学习框架训练或推理的**代码**，转换为PaddlePaddle的**代码**，方便快速自动地 **模型代码迁移**。

目前支持自动转换Pytorch代码，其它深度学习框架的支持后续新增中，其原理是通过Python AST语法树分析，将输入代码生成为抽象语法树，对其进行解析、遍历、匹配、编辑、替换、插入等各种操作，然后得到基于PaddlePaddle的抽象语法树，最后生成Paddle的代码。

转换会尽量保持原代码的风格与结构，将代码中其它深度学习框架的接口转换为调用PaddlePaddle的接口。

转换时会尽可能保证原代码的行数不变，但某些情形下原来的1行代码会转换成多行。例如：

转换前：
```
import torch
y = torch.transpose(image, 1, 0)
```

转换后：
```
import paddle
x = image
perm_0 = list(range(x.ndim))
perm_0[1] = 0
perm_0[0] = 1
y = paddle.transpose(x=x, perm=perm_0)
```

这是由于两者API的用法差异，无法通过一行代码来完成，需要增加若干辅助行来实现相同功能。

转换过程中不会改动原文件，会将原项目文件一一转换到 `out_dir` 指定的文件夹中，方便前后对比。对不同类型的文件的处理逻辑分别为：

- Python代码文件：识别代码中调用其它深度学习框架的接口并转换
- requirements.txt： 替换其中的安装依赖为 `paddlepaddle-gpu`
- 其他文件：原样拷贝

# 安装与使用

由于使用了一些较新的Python语法树特性，你需要使用>=python3.8的解释器。
1. 使用pip安装

```bash
python3.8 -m pip install -U paconvert
paconvert --in_dir torch_project [--out_dir paddle_project] [--exclude_dirs exclude_dirs] [--log_dir log_dir] [--log_level "DEBUG"] [--run_check 1]
```

2. 使用源码安装

```bash
git clone https://github.com/PaddlePaddle/PaConvert.git
python3.8 paconvert/main.py --in_dir torch_project [--out_dir paddle_project] [--exclude_dirs exclude_dirs] [--log_dir log_dir] [--log_level "DEBUG"] [--run_check 1]
```

**参数介绍**

```
--in_dir        输入torch项目文件，可以为单个文件或文件夹
--out_dir       可选，输出paddle项目文件，可以为单个文件或文件夹，默认在当前目录下创建./paddle_project/
--exclude_dirs  可选，排除转换的文件或文件夹，排除多项时请用逗号分隔，默认不排除
--log_dir       可选，输出日志的路径，默认会在终端上打印日志
--log_level     可选，打印log等级，仅支持"INFO" "DEBUG"，默认"INFO"
--run_check     可选，工具自检
```


# 转换示例

以下面Pytorch代码为例，转换前：
```
import torch
import torch.nn as nn
import torch.optim as optim
import torch.nn.Linear as Linear
import torch.nn.functional as F

class MyNet(nn.Module):
    test = "str"

    def __init__(self):
        self._fc1 = torch.nn.Linear(10, 10)
        self._fc2 = nn.Linear(10, 10)
        self._fc3 = Linear(10, 10)

    @torch.no_grad()
    def forward(self, x):
        x = self._fc1(x)
        x = self._fc2(x)
        x = self._fc3(x)
        y = torch.add(x, x)
        return F.relu(y)

net = MyNet()

sgd = optim.SGD(net.parameters(), lr=0.1, momentum=0.9)
lr = optim.lr_scheduler.MultiStepLR(sgd, milestones=[2, 4, 6], gamma=0.8)
```

转换后：
```
import paddle


class MyNet(paddle.nn.Layer):
    test = 'str'

    def __init__(self):
        self._fc1 = paddle.nn.Linear(in_features=10, out_features=10)
        self._fc2 = paddle.nn.Linear(in_features=10, out_features=10)
        self._fc3 = paddle.nn.Linear(in_features=10, out_features=10)

    @paddle.no_grad()
    def forward(self, x):
        x = self._fc1(x)
        x = self._fc2(x)
        x = self._fc3(x)
        y = paddle.add(x=x, y=x)
        return paddle.nn.functional.relu(x=y)


net = MyNet()
>>>>>>sgd = torch.optim.SGD(net.parameters(), lr=0.1, momentum=0.9)
>>>>>>lr = torch.optim.lr_scheduler.MultiStepLR(sgd, milestones=[2, 4, 6], gamma=0.8)
```

打印信息如下：

```txt
===========================================
PyTorch to Paddle Convert Start ------>:
===========================================
Start convert /workspace/test_code.py --> /workspace/PaConvert/paddle_project/test_code.py
[test_code.py:1] remove 'import torch'
[test_code.py:2] remove 'import torch.nn as nn'
[test_code.py:3] remove 'import torch.optim as optim'
[test_code.py:4] remove 'import torch.nn.Linear as Linear'
[test_code.py:5] remove 'import torch.nn.functional as F'
[test_code.py] add 'import paddle' in first line
[test_code.py:25] [Not Support] convert torch.optim.SGD to Paddle is not supported currently
[test_code.py:26] [Not Support] convert torch.optim.lr_scheduler.MultiStepLR to Paddle is not supported currently
Finish convert /workspace/test_code.py --> /workspace/PaConvert/paddle_project/test_code.py


========================================
Convert Summary:
========================================
There are 10 Pytorch APIs in this Project:
 8  Pytorch APIs have been converted to Paddle successfully!
 2  Pytorch APIs are not supported to convert to Paddle currently!
 Convert Rate is: 80.000%

For these 2 Pytorch APIs that do not support to Convert now, which have been marked by >>>>>> before the line,
please refer to https://www.paddlepaddle.org.cn/documentation/docs/zh/develop/guides/model_convert/convert_from_pytorch/pytorch_api_mapping_cn.html
and convert it by yourself manually. In addition, these APIs will be supported in future.

Thank you to use Paddle Code Convert Tool. You can make any suggestions to us.

```

转换完成后，会打印 **转换总结** ，包含 **API总数、转换成功数、未转换数、转换率** 。如未指定 `out_dir` ，则会在当前目录下 `./paddle_project/` 并输出到此目录。如未指定 `log_dir` ，则会在终端打印日志。

例如，上述代码里一共有10个Pytorch API，其中8个被成功转换，因此转换率为 `80.00%` ，如果项目中有多个python文件，则会统计所有文件的累计数据。

**对于转换成功的API**：代码风格上会略有变化，会 **补全API全名、补全参数关键字、移除注释、移除多余空行** 。因为在 `源码->语法树->源码` 的过程中，会采用标准写法来生成代码，而 `注释、空行` 等代码无法被语法树识别，将被移除。

**对于不支持转换的API**：将 **补全为Pytorch API全名**，同时在行前通过 `>>>>>>` 的形式加以标记，用户必须对该API进行人工手动转换，然后删除标记，否则代码无法运行。


# 贡献代码

欢迎你向我们贡献代码，详细开发步骤请参考 [贡献代码教程](docs/CONTRIBUTING.md)
