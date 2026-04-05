"""
ResearchBrain 端到端测试 — 验证开源包的完整功能
在临时目录中模拟一个全新用户的使用流程。
"""
import sys, os, tempfile, shutil

# 确保导入的是本地包
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from research_brain import brain, quick_log, ResearchSession, track_experiment, lint

PASS = 0
FAIL = 0

def check(name, condition):
    global PASS, FAIL
    if condition:
        print(f"  ✅ {name}")
        PASS += 1
    else:
        print(f"  ❌ {name}")
        FAIL += 1

# 在临时目录中测试
test_dir = os.path.join(os.path.dirname(__file__), "_test_workspace")
if os.path.exists(test_dir):
    shutil.rmtree(test_dir)
os.makedirs(test_dir)
os.chdir(test_dir)

print("\n🧪 ResearchBrain 端到端测试\n")

# ============================================================
print("1️⃣  rb init — 初始化")
fp = brain.init(path=test_dir, project="TestProject", metric="accuracy")
check("RESEARCH_BRAIN.md 已创建", fp.exists())
check("文件名正确", fp.name == "RESEARCH_BRAIN.md")

# ============================================================
print("\n2️⃣  load — 加载数据")
data = brain.load(fp)
check("config.project", data["config"]["project"] == "TestProject")
check("config.metric", data["config"]["metric"] == "accuracy")
check("experiments 为空", len(data["experiments"]) == 0)
check("pain_points 为空", len(data["pain_points"]) == 0)
check("log 为空", len(data["log"]) == 0)

# ============================================================
print("\n3️⃣  add_experiment — 添加实验")
exp1 = brain.add_experiment(data, {
    "title": "Random Forest Baseline",
    "metrics": {"accuracy": 0.72},
    "code": "train_rf.py",
    "findings": ["Feature importance matters"],
    "failed": ["SVM too slow"],
})
check("实验已添加", len(data["experiments"]) == 1)
check("自动标记 SOTA", exp1["status"] == "🏆")
check("Log 已追加", len(data["log"]) == 1)
check("Log 包含 experiment", "experiment" in data["log"][0])

# 添加第二个更好的实验
exp2 = brain.add_experiment(data, {
    "title": "XGBoost Tuned",
    "metrics": {"accuracy": 0.85},
    "based_on": ["Random Forest Baseline"],
    "insights": ["Gradient boosting wins"],
})
check("第二个实验已添加", len(data["experiments"]) == 2)
check("新 SOTA 自动检测", exp2["status"] == "🏆")
check("旧 SOTA 自动降级", data["experiments"][1]["status"] == "📦")

# 添加更差的实验
exp3 = brain.add_experiment(data, {
    "title": "Linear Regression",
    "metrics": {"accuracy": 0.55},
})
check("差实验不抢 SOTA", exp3["status"] == "🔄")

# ============================================================
print("\n4️⃣  add_pain — 添加痛点")
brain.add_pain(data, {
    "title": "OOM on 100K samples",
    "severity": "P0",
    "trigger": "当加载超过 50K 样本时",
    "failed_attempts": ["直接加载", "float32"],
    "workaround": "Chunking 10K/batch",
})
brain.add_pain(data, {
    "title": "CCA numerical instability",
    "severity": "P1",
    "trigger": "特征维度超过 5K 时",
})
check("痛点已添加", len(data["pain_points"]) == 2)
check("Log 记录痛点", any("pain" in e for e in data["log"]))

# ============================================================
print("\n5️⃣  resolve_pain — 解决痛点")
result = brain.resolve_pain(data, "CCA", "加正则化 reg=0.1")
check("痛点已解决", result is not None)
check("降级为 P2", result["severity"] == "P2")
check("Log 记录 resolve", any("resolve" in e for e in data["log"]))

# ============================================================
print("\n6️⃣  add_decision — 添加决策")
brain.add_decision(data, "选择 XGBoost 作为主模型",
    alternatives="RF, SVM, MLP",
    reason="准确率最高且训练快",
    impact="后续优化基于 XGBoost")
check("决策已添加", len(data["decisions"]) == 1)

# ============================================================
print("\n7️⃣  save & reload — 保存并重新加载")
brain.save(data, fp)
data2 = brain.load(fp)
check("实验数量一致", len(data2["experiments"]) == 3)
check("痛点数量一致", len(data2["pain_points"]) == 2)
check("决策数量一致", len(data2["decisions"]) == 1)
check("Log 数量一致", len(data2["log"]) == len(data["log"]))
check("SOTA 正确", brain.get_sota(data2)["title"] == "XGBoost Tuned")
check("SOTA 指标正确", brain.get_sota(data2)["metrics"]["accuracy"] == 0.85)

# ============================================================
print("\n8️⃣  search — 搜索")
results = brain.search(data2, "XGBoost")
check("搜索到实验", len(results) > 0)
results2 = brain.search(data2, "OOM")
check("搜索到痛点", len(results2) > 0)
results3 = brain.search(data2, "nonexistent_xyz")
check("搜索无结果", len(results3) == 0)

# ============================================================
print("\n9️⃣  get_context — AI 上下文生成")
ctx_compact = brain.get_context(data2)
check("精简版包含 SOTA", "XGBoost" in ctx_compact)
check("精简版包含痛点", "OOM" in ctx_compact)
check("精简版包含排行", "排行" in ctx_compact)
check("精简版不含时间线", "最近活动" not in ctx_compact)

ctx_detail = brain.get_context(data2, detail=True)
check("完整版包含时间线", "最近活动" in ctx_detail)
check("完整版包含失败", "SVM" in ctx_detail)

ctx_focus = brain.get_context(data2, focus="OOM")
check("焦点搜索生效", "OOM" in ctx_focus and "相关" in ctx_focus)

# ============================================================
print("\n🔟  lint — 健康检查")
issues = brain.lint(data2)
check("Lint 返回结果", len(issues) > 0)
# P0 未解决应该被检测到
has_p0_warning = any("P0" in msg for _, msg in issues)
check("检测到 P0 未解决", has_p0_warning)

# ============================================================
print("\n1️⃣1️⃣  Schema 注释")
content = fp.read_text(encoding="utf-8")
check("包含 Schema 注释", "ResearchBrain Schema" in content)
check("包含格式说明", "Pain Points" in content)

# ============================================================
print("\n1️⃣2️⃣  Log 时间线")
check("Log 有内容", len(data2["log"]) > 0)
check("Log 格式正确", all("[" in e and "]" in e for e in data2["log"]))

# ============================================================
print("\n1️⃣3️⃣  quick_log — 一行记录")
os.chdir(test_dir)
quick_log("Quick Test", {"accuracy": 0.99}, pain="过拟合")
data3 = brain.load(fp)
check("quick_log 已记录", len(data3["experiments"]) == 4)
check("quick_log 新 SOTA", brain.get_sota(data3)["title"] == "Quick Test")

# ============================================================
# 清理
os.chdir(os.path.dirname(test_dir))
shutil.rmtree(test_dir)

# 汇总
print(f"\n{'='*50}")
print(f"🧪 测试完成: {PASS} 通过, {FAIL} 失败")
if FAIL == 0:
    print("🎉 全部通过！可以放心开源。")
else:
    print("⚠️ 有失败项，请检查。")
print(f"{'='*50}\n")

sys.exit(FAIL)
