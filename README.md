# 🧠 ResearchBrain

**科研 Vibe Coding 知识库 — 让每一次失败都成为 AI 的免疫力。**

> Inspired by [Karpathy's llm-wiki pattern](https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f), specialized for scientific research.

一个文件 `RESEARCH_BRAIN.md` 就是你的整个知识库。人和 AI 都能直接阅读和编辑。

## 🚀 30 秒上手

```bash
pip install research-brain       # 安装
cd your_project && rb init       # 创建 RESEARCH_BRAIN.md
rb log -t "实验标题" -v 0.85     # 记录实验（自动检测 SOTA）
rb status                        # 查看 SOTA + 排行 + 痛点
rb context                       # 生成 AI 上下文（精简版）
rb context --detail              # 生成 AI 上下文（完整版）
rb lint                          # 知识库健康检查
```

## 💡 Why

在 AI 辅助科研编程（Vibe Coding）中，最大的浪费不是重复代码——而是**重复失败**。

传统 RAG 每次从零推导，知识不累积。ResearchBrain 不同：

| | RAG | ResearchBrain |
|---|---|---|
| 知识存储 | 向量数据库 | **一个 Markdown 文件** |
| 更新方式 | 重新索引 | **增量更新** |
| 人可读 | ❌ | ✅ 打开就能看 |
| AI 可读 | 需要检索 | ✅ 直接读取 |
| 失败经验 | 不记录 | ✅ 带触发条件的痛点 |
| 知识复利 | ❌ | ✅ 每次实验都在积累 |

## 📄 实体文档

所有数据存储在项目根目录的 **`RESEARCH_BRAIN.md`** 中：

```
your_project/
├── RESEARCH_BRAIN.md    ← 知识库（就这一个文件）
├── train.py
└── ...
```

文档结构：

```markdown
## 🏆 SOTA          ← 当前最优结果
## 🚧 Pain Points   ← 痛点避坑指南（带触发条件）
## 📊 Experiments    ← 实验记录（最新在前）
## 📋 Decisions      ← 决策日志
## 📅 Log            ← 时间线（append-only）
```

## ✨ 核心特性

### 🎯 三种接入方式

```python
# 方式 A: 装饰器（最简洁）
from research_brain import track_experiment

@track_experiment(title="Ridge CV", based_on=["baseline"])
def train(lr=0.001):
    return {"avg_correlation": 0.85}  # 返回值自动记录

# 方式 B: 上下文管理器（最灵活）
from research_brain import ResearchSession

with ResearchSession("Fusion v3") as s:
    s.metric("avg_correlation", 0.85)
    s.pain("OOM", trigger="处理>50K图像时")
    s.insight("Patch >> FC by 7%")
    s.fail("concatenation 融合无提升")

# 方式 C: 一行搞定
from research_brain import quick_log
quick_log("L2正则化", {"avg_r": 0.72}, pain="过拟合")
```

### 🏆 自动 SOTA 追踪

每次记录实验，自动比较主要指标。超越当前 SOTA 时自动标记。

### 🚧 痛点触发条件

```bash
rb pain add "GPU OOM" -s P0 -t "处理>50K图像时" -w "使用chunking"
```

AI 编码前会读取痛点，遇到触发条件自动警告。

### 🔍 Lint 健康检查

```bash
rb lint
```

检查 7 类问题：无 SOTA、过期实验、P0 未解决、实验矛盾、缺失触发条件、缺失失败记录等。

### 📊 AI 上下文分级

```bash
rb context              # 精简版 (~1K tokens): SOTA + 痛点 + 排行
rb context --detail     # 完整版 (~3K tokens): + 实验详情 + 失败记录 + 时间线
rb context --save       # 将快照保存到 Log，知识复利
```

## 🔧 CLI 完整命令

| 命令 | 说明 |
|------|------|
| `rb init` | 创建 RESEARCH_BRAIN.md |
| `rb status` | SOTA + 排行 + 痛点 |
| `rb log -t "标题" -v 0.85` | 记录实验 |
| `rb context` | AI 上下文（精简版） |
| `rb context --detail --save` | AI 上下文（完整版 + 保存快照） |
| `rb lint` | 知识库健康检查 |
| `rb pain add "描述" -t "触发条件"` | 添加痛点 |
| `rb pain list` | 列出痛点 |
| `rb pain resolve "关键词"` | 解决痛点 |
| `rb search "关键词"` | 搜索 |
| `rb sync` | 同步到 Antigravity KI |

## 🏗️ 架构

```
3 个 Python 文件，2 个依赖，1 个实体文档。
```

| 文件 | 行数 | 职责 |
|------|------|------|
| `brain.py` | ~350 | 核心引擎：解析/渲染/CRUD/Lint/AI上下文 |
| `decorator.py` | ~130 | 非侵入 API: @track_experiment / ResearchSession |
| `cli.py` | ~250 | 命令行: rb init/status/log/context/lint/pain |

依赖：`pyyaml` + `click`。无数据库，无服务器，无账号。

## 🌍 可迁移性

```bash
pip install research-brain    # 一次安装
cd any_project && rb init     # 任意项目初始化
rb log -t "实验" -v 0.85      # 开始记录
```

知识库是纯 Markdown，可以用任何编辑器查看，建议纳入 Git 管理。


## License

MIT
