---
project: My Research Project
metric: avg_correlation
higher_is_better: true
---
<!--
📜 ResearchBrain Schema v0.2
本文件是整个知识库。格式约定：
- ## 🏆 SOTA: 当前最优结果
- ## 🚧 Pain Points: 痛点（按 P0>P1>P2 排序）
- ## 📊 Experiments: 实验记录（最新在前）
- ## 📋 Decisions: 决策日志
- ## 📅 Log: 时间线（append-only，最新在前）
每条实验用 ### [状态] 标题 — 日期 格式
每条痛点用 ### EMOJI 严重度: 标题 格式
AI 操作时请遵循此格式，优先阅读 Pain Points 部分。
-->

# 🧠 Research Brain

> **项目**: My Research Project | **核心指标**: avg_correlation ↑ | **更新**: 2026-04-05

---

## 🏆 SOTA

**Baseline Ridge CV** — avg_correlation = **0.72** (2026-04-05)

---

## 🚧 Pain Points

### 🔴 P0: GPU OOM on large dataset

- **触发条件**: 当一次性加载超过 50K 样本到 GPU 时
- **现象**: CUDA out of memory / 进程被 kill
- **已试无效**: ❌ 直接加载全部数据 | ❌ float32 精度存储
- **方案**: 分批处理 (chunking) + 低精度 (bfloat16)
- **发现**: 2026-04-05

### 🟡 P1:  underperforms

- **触发条件**: 当使用简单 concatenation 拼接特征时
- **已试无效**: ❌ concatenation 拼接 | ❌ 增大隐藏层导致过拟合
- **方案**: 尝试 
- **发现**: 2026-04-05

---

## 📊 Experiments

### [🏆] CV — 2026-04-05

> 使用 5-fold CV 作为基准

- **指标**: avg_correlation=0.72, feature_dim=2048
- **代码**: `baseline.py`
- **参数**: model=ridge, folds=5, alpha=1.0
- **发现**: 💡 特征质量比模型复杂度更重要
- **失败**: ❌ SVM → 慢且无提升 | ❌ MLP 过拟合
- **下一步**: 尝试更好的特征提取方法

### [📦] Simple CNN — 2026-04-04

> 简单卷积网络直接回归

- **指标**: avg_correlation=0.65
- **代码**: `train_cnn.py`
- **失败**: ❌ 小数据集上过拟合严重

---

## 📋 Decisions

### 2026-04-05: 选择  CV 作为基线方法

- **备选**: SVM, MLP, Random Forest
- **理由**: 简单稳定，适合小数据集，计算快
- **影响**: 后续所有实验需要跟此基线对比

---

## 📅 Log

- [2026-04-05 12:00] experiment |  CV — avg_correlation=0.72
- [2026-04-04 18:00] experiment | Simple CNN — avg_correlation=0.65
- [2026-04-05 10:00] pain | GPU OOM on large dataset — [P0]
- [2026-04-05 10:30] decision | 选择 Ridge CV 作为基线方法
