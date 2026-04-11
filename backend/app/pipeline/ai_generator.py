"""AI jianpu generator using LLM."""
import json
import logging

from .llm_provider import get_provider
from .validator import validate_notes

logger = logging.getLogger(__name__)

PROMPT_TEMPLATE = """你是一个专业的口琴简谱编写者。请为以下歌曲生成完整主旋律的简谱数据。

歌曲: {title}
歌手: {artist}
{key_info}
拍号: {time_signature}

请严格按照以下JSON格式输出，不要包含任何其他文字：

{{
  "title": "歌名",
  "artist": "歌手",
  "key": "C",
  "time_signature": "4/4",
  "bpm": 120,
  "notes": [
    {{"measure": 1, "position": 1, "pitch": "C5", "duration": "quarter", "dot": false, "tie": false}},
    ...
  ]
}}

严格规则：
1. pitch 只能使用以下音（10孔Paddy Richter C调口琴可用音）：
   低音区: C4, D4, E4, G4, A4, B4（注意：没有F4）
   中音区: C5, D5, E5, F5, G5, A5, B5（完整音阶，推荐主要使用这个区域）
   高音区: C6, D6, E6, F6, G6, A6, C7（注意：没有B6）
2. duration 可选: whole(4拍), half(2拍), quarter(1拍), eighth(0.5拍), sixteenth(0.25拍)
3. dot 为 true 时时值变为1.5倍（附点四分=1.5拍，附点二分=3拍）
4. 每小节的音符时值总和必须严格等于拍号要求（4/4拍=4拍，3/4拍=3拍）。请仔细计算！
5. measure 从1开始，position 从1开始递增
6. 旋律应该是歌曲的完整主旋律（主歌+副歌），不要只写片段
7. 优先使用中音区(C5-C6)，必要时扩展到低音或高音区
8. 只输出JSON，不要其他文字
"""


async def generate_jianpu(params: dict) -> dict:
    """Generate jianpu via LLM. Returns dict with song data or error."""
    title = params.get("title", "")
    artist = params.get("artist", "")
    original_key = params.get("original_key", "")
    time_signature = params.get("time_signature", "4/4")

    key_info = f"原调: {original_key}" if original_key else ""

    prompt = PROMPT_TEMPLATE.format(
        title=title,
        artist=artist,
        key_info=key_info,
        time_signature=time_signature,
    )

    provider = get_provider()
    raw = await provider.generate(prompt)

    # Extract JSON from response
    try:
        # Try to find JSON block
        start = raw.find("{")
        end = raw.rfind("}") + 1
        if start == -1 or end == 0:
            return {"error": "LLM 未返回有效 JSON", "raw": raw[:500]}
        data = json.loads(raw[start:end])
    except json.JSONDecodeError as e:
        return {"error": f"JSON 解析失败: {e}", "raw": raw[:500]}

    notes = data.get("notes", [])
    if not notes:
        return {"error": "LLM 未生成任何音符"}

    # Validate
    errors = validate_notes(notes, data.get("time_signature", time_signature))
    if errors:
        logger.warning("AI generated notes have validation errors: %s", errors)

    return {
        "song": {
            "title": data.get("title", title),
            "artist": data.get("artist", artist),
            "key": data.get("key", "C"),
            "time_signature": data.get("time_signature", time_signature),
            "bpm": data.get("bpm", 120),
        },
        "notes": notes,
        "validation_errors": errors,
    }
