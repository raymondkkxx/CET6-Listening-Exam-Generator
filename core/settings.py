# -*- coding: utf-8 -*-
import os
from PyQt5.QtCore import QSettings

APP_NAME = "CET-6 Listening Studio"
APP_ORG = "KokoroTTS"
APP_SETTINGS_KEY = "CET6ListeningStudioV1"

DEFAULT_KOKORO_ROOT = r"C:\ProgramData\Microsoft\Windows\Start Menu\Programs\KokoroTTS"

SAMPLE_RATE = 24000
TARGET_RMS = 0.085
TRIM_SILENCE_THRESHOLD = 0.005

DEFAULT_CONFIG = {
    "device": "auto",
    "voice_male": "am_michael",
    "voice_female": "af_heart",
    "voice_examiner": "am_eric",
    "speech_rate": 1.0,
    "turn_gap_sec": 0.25,
    "section_gap_sec": 1.2,
    "pre_question_read_sec": 8.0,
    "post_question_answer_sec": 8.0,
    "enable_ding_chime": True,
    "ding_volume": 0.18,
    "always_on_top": False,
}

PRESET_VOICES = [
    "am_michael (US Michael - 饱满美音男声)",
    "am_eric (US Eric - 沉稳考官/男声)",
    "am_adam (US Adam - 深沉男声)",
    "am_fenrir (US Fenrir - 活力男声)",
    "am_liam (US Liam - 青年男声)",
    "am_onyx (US Onyx - 权威男声)",
    "af_heart (US Heart - 自然美音女声)",
    "af_bella (US Bella - 清晰女声)",
    "af_sarah (US Sarah - 播音女声)",
    "af_nicole (US Nicole - 柔和女声)",
    "af_nova (US Nova - 明亮女声)",
    "af_kore (US Kore - 冷静女声)",
    "bf_emma (UK Emma - 优雅英音女声)",
    "bf_alice (UK Alice - 清晰英音女声)",
    "bm_george (UK George - 经典英音男声)",
    "bm_lewis (UK Lewis - 播音英音男声)",
]

DEFAULT_AI_PROMPT_TEMPLATE = """你是一位资深的大学英语六级（CET-6）听力命题专家与声学语音脚本设计师。请根据我提供的【参考材料】以及可选的【本次重点攻克的薄弱点】，创作一套高仿六级听力 Section A（长对话）的平行模拟题，并严格以单个合法的 JSON 代码块输出。

### 一、 命题、节奏与防陷阱铁律
1. **题材迁移与防雷同**：保留参考材料的核心场景（如校园科研、职场项目、环保科技、社会现象等）与逻辑骨架，但**必须彻底更换具体事件、人物身份与核心语料**，严禁照搬原句。
2. **考场真实体量与非对称呼吸感**：
   - 总词数严格控制在 **360–430 词**（约 2.5–3 分钟音频时长），一男（`M`）一女（`F`）交替对话，共 **8–10 个话轮**。
   - **话轮必须长短交替（非对称）**：穿插 2–3 个 65–95 词的“背景铺垫/细节解释”长话轮，还原六级听力中“冗余信息巡航区”与“高密考点爆发区”交替的真实考场节奏。
3. **顺序铁律与“视听一致”陷阱设计（核心）**：
   - 命制 **4 道选择题**，4 道题的考点**必须严格按照 `dialogue` 从头到尾的时间顺序分布**（平均每 90–100 词出现 1 个考点），严禁乱序（如把开头细节放到第 4 题）。
   - **信号路标引导**：每道题的正确答案必须紧跟在明确的口语转折、强调或因果路标词之后（如 `Actually,`, `Well, the thing is,`, `Surprisingly,`, `What really matters is...`, `While..., ...`）。
   - **反直觉选项设计**：每题的 `A/B/C/D` 四个选项长度与句式必须高度平行对称。**至少 2 个干扰项必须直接借用对话中（尤其是转折词之前）出现的原文原词**（制造“视听一致”陷阱）；**正确选项必须避开原文核心实词，采用地道的高阶同义替换**。
   - **答案分布防偏置**：4 道题的 `answer` 必须在 `A/B/C/D` 中随机分布，严禁习惯性集中于 `B` 或 `C`。
4. **靶向痛点注入**：如果我在下方填写了【本次重点攻克的薄弱点】，请在对话和选项设计中重点强化该类考点的出现频率（若未填写，则默认均衡覆盖转折态度、细节推理与行动建议）。

### 二、 Kokoro-TTS 专用语音轨（`spoken_text`）强制规则
为了保证本地 Kokoro-TTS（Misaki G2P）零误读且韵律自然，每句台词和每道题干必须同时提供 `display_text`（正常拼写）和 `spoken_text`（纯语音拼写），`spoken_text` 必须严格遵守以下规则：
1. **数字与符号全展开**：将所有阿拉伯数字、年份、时间、百分比、货币、小数全部拼写成纯英文单词（例如：`2026` -> `twenty twenty-six`；`$45,000` -> `forty-five thousand dollars`；`90%` -> `ninety percent`；`3.5` -> `three point five`）。
2. **缩略词与生僻词处理**：逐字母念的缩写用空格隔开大写字母（如 `LED` -> `L E D`，`GPA` -> `G P A`）；易误读专有名词或连读缩写使用 `[原词](/IPA音标/)` 语法或展开为全称。
3. **韵律标点规范**：严禁使用 `<break>`、`[sigh]` 等标签，严禁使用双连字符 `--` 或结巴连字符（如 `W-what`）；统一使用逗号 `,`、句号 `.`、问号 `?` 以及前后带空格的省略号 ` ... ` 表示犹豫与自然换气停顿。
4. **题干不含序号前缀**：`questions` 中的 `spoken_text` 直接以疑问词开头（如 `"What does the man say about...?"`），**不要**添加 `"Question 1."` 或 `"Question one."`（本地合成引擎会自动播报题号）。

### 三、 输出格式（严禁输出 JSON 以外的任何解释文字）
\x60\x60\x60json
{
  "design_scratchpad": {
    "new_scenario": "简述迁移后的全新场景与核心冲突",
    "target_word_count": "预估总词数（需落在360-430词之间）",
    "question_blueprints": [
      {
        "q_id": 1,
        "signal_marker": "引导考点的转折/强调路标词",
        "paraphrase_pair": "原文核心表达 -> 正确选项同义替换表达",
        "audio_visual_trap": "干扰项借用了原文哪几个原词做视听一致陷阱"
      }
    ]
  },
  "title": "CET-6 Section A Simulation — [英文话题副标题]",
  "dialogue": [
    {
      "role": "M",
      "display_text": "正常拼写台词...",
      "spoken_text": "纯英文单词与Kokoro韵律标点处理后的语音台词..."
    },
    {
      "role": "F",
      "display_text": "正常拼写台词...",
      "spoken_text": "纯英文单词与Kokoro韵律标点处理后的语音台词..."
    }
  ],
  "questions": [
    {
      "id": 1,
      "display_text": "What does the man say about...?",
      "spoken_text": "What does the man say about...?",
      "options": {
        "A": "选项 A 文本",
        "B": "选项 B 文本",
        "C": "选项 C 文本",
        "D": "选项 D 文本"
      },
      "answer": "D",
      "explanation": "【信号路标】... -> 【原文定位】... -> 【同义替换】... -> 【干扰项陷阱】..."
    }
  ]
}
\x60\x60\x60

【本次重点攻克的薄弱点】：（可选，例如：转折词后的同义替换 / 数字与趋势对比 / 虚拟语气与委婉拒绝；留空则综合出题）
【参考材料】：
（在此处粘贴你的六级真题对话或文章）"""

AI_PROMPT_TEMPLATE = DEFAULT_AI_PROMPT_TEMPLATE


def get_project_root() -> str:
    return os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def get_default_output_dir() -> str:
    return os.path.join(get_project_root(), "output")


def get_tray_icon_path() -> str:
    return os.path.join(get_project_root(), ".icon", "cet.png")


def create_qsettings() -> QSettings:
    return QSettings(APP_ORG, APP_SETTINGS_KEY)


def get_ai_prompt() -> str:
    """读取用户自定义提示词，若未修改过则返回默认模板"""
    settings = create_qsettings()
    saved = settings.value("custom_ai_prompt", "", type=str)
    return saved.strip() if saved and saved.strip() else DEFAULT_AI_PROMPT_TEMPLATE


def save_ai_prompt(prompt_text: str):
    """保存用户自定义出题提示词"""
    settings = create_qsettings()
    settings.setValue("custom_ai_prompt", prompt_text.strip())
    settings.sync()


def reset_ai_prompt() -> str:
    """恢复默认出题提示词"""
    settings = create_qsettings()
    settings.remove("custom_ai_prompt")
    settings.sync()
    return DEFAULT_AI_PROMPT_TEMPLATE