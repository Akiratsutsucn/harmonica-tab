# -*- coding: utf-8 -*-
"""7 new songs for harmonica app - batch import data."""

NEW_SONGS = [
    # ──────────────────────────────────────────────
    # 1. 千与千寻 (いつも何度でも / Always with Me)
    # ──────────────────────────────────────────────
    {
        "title": "千与千寻 (いつも何度でも)", "artist": "木村弓", "key": "C", "ts": "4/4", "bpm": 80, "difficulty": 3,
        "notes": [
            # A段 "呼ぶ声に 振り向いて"
            (1,1,'C5','eighth'),(1,2,'D5','eighth'),(1,3,'E5','quarter'),(1,4,'G5','quarter'),(1,5,'E5','quarter'),
            (2,1,'D5','quarter'),(2,2,'C5','quarter'),(2,3,'D5','half'),
            (3,1,'C5','eighth'),(3,2,'D5','eighth'),(3,3,'E5','quarter'),(3,4,'G5','quarter'),(3,5,'A5','quarter'),
            (4,1,'G5','whole'),
            # "何度も何度も 誓い合った"
            (5,1,'A5','quarter'),(5,2,'G5','quarter'),(5,3,'E5','quarter'),(5,4,'G5','quarter'),
            (6,1,'E5','quarter'),(6,2,'D5','quarter'),(6,3,'C5','quarter'),(6,4,'D5','quarter'),
            (7,1,'C5','eighth'),(7,2,'D5','eighth'),(7,3,'E5','quarter'),(7,4,'G5','quarter'),(7,5,'E5','quarter'),
            (8,1,'D5','whole'),
            # B段 "夢の中で ずっと続く"
            (9,1,'E5','quarter'),(9,2,'G5','quarter'),(9,3,'A5','quarter'),(9,4,'C6','quarter'),
            (10,1,'B5','quarter'),(10,2,'A5','quarter'),(10,3,'G5','quarter'),(10,4,'A5','quarter'),
            (11,1,'G5','quarter'),(11,2,'E5','quarter'),(11,3,'D5','quarter'),(11,4,'E5','quarter'),
            (12,1,'G5','half'),(12,2,'E5','half'),
            # A'段 回到主题
            (13,1,'C5','eighth'),(13,2,'D5','eighth'),(13,3,'E5','quarter'),(13,4,'G5','quarter'),(13,5,'E5','quarter'),
            (14,1,'D5','quarter'),(14,2,'C5','quarter'),(14,3,'D5','half'),
            (15,1,'C5','eighth'),(15,2,'D5','eighth'),(15,3,'E5','quarter'),(15,4,'G5','quarter'),(15,5,'A5','quarter'),
            (16,1,'G5','whole'),
            # 第二段变化
            (17,1,'A5','quarter'),(17,2,'G5','quarter'),(17,3,'E5','quarter'),(17,4,'G5','quarter'),
            (18,1,'E5','quarter'),(18,2,'D5','quarter'),(18,3,'C5','half'),
            (19,1,'E5','quarter'),(19,2,'G5','quarter'),(19,3,'A5','quarter'),(19,4,'G5','quarter'),
            (20,1,'E5','whole'),
            # 尾声
            (21,1,'E5','quarter'),(21,2,'G5','quarter'),(21,3,'A5','quarter'),(21,4,'C6','quarter'),
            (22,1,'B5','quarter'),(22,2,'A5','quarter'),(22,3,'G5','half'),
            (23,1,'E5','quarter'),(23,2,'D5','quarter'),(23,3,'C5','quarter'),(23,4,'D5','quarter'),
            (24,1,'C5','whole'),
        ],
    },
    # ──────────────────────────────────────────────
    # 2. 穿越时空的思念 (犬夜叉 OST)
    # ──────────────────────────────────────────────
    {
        "title": "穿越时空的思念", "artist": "和田薫", "key": "C", "ts": "4/4", "bpm": 72, "difficulty": 3,
        "notes": [
            # 主题 A
            (1,1,'E5','half'),(1,2,'G5','quarter'),(1,3,'A5','quarter'),
            (2,1,'G5','half'),(2,2,'E5','quarter'),(2,3,'D5','quarter'),
            (3,1,'C5','quarter'),(3,2,'D5','quarter'),(3,3,'E5','quarter'),(3,4,'G5','quarter'),
            (4,1,'E5','whole'),
            (5,1,'A5','half'),(5,2,'G5','quarter'),(5,3,'E5','quarter'),
            (6,1,'G5','quarter'),(6,2,'A5','quarter'),(6,3,'G5','half'),
            (7,1,'E5','quarter'),(7,2,'G5','quarter'),(7,3,'A5','quarter'),(7,4,'C6','quarter'),
            (8,1,'B5','quarter'),(8,2,'A5','quarter'),(8,3,'G5','half'),
            # 主题 B
            (9,1,'A5','half'),(9,2,'C6','quarter'),(9,3,'B5','quarter'),
            (10,1,'A5','half'),(10,2,'G5','half'),
            (11,1,'E5','quarter'),(11,2,'G5','quarter'),(11,3,'A5','quarter'),(11,4,'G5','quarter'),
            (12,1,'E5','whole'),
            (13,1,'C5','quarter'),(13,2,'D5','quarter'),(13,3,'E5','quarter'),(13,4,'G5','quarter'),
            (14,1,'A5','quarter'),(14,2,'G5','quarter'),(14,3,'E5','half'),
            (15,1,'D5','quarter'),(15,2,'E5','quarter'),(15,3,'G5','quarter'),(15,4,'E5','quarter'),
            (16,1,'C5','whole'),
            # 高潮段
            (17,1,'E5','quarter'),(17,2,'G5','quarter'),(17,3,'A5','quarter'),(17,4,'C6','quarter'),
            (18,1,'B5','half'),(18,2,'A5','half'),
            (19,1,'G5','quarter'),(19,2,'A5','quarter'),(19,3,'C6','quarter'),(19,4,'D6','quarter'),
            (20,1,'C6','whole'),
            (21,1,'A5','quarter'),(21,2,'C6','quarter'),(21,3,'B5','quarter'),(21,4,'A5','quarter'),
            (22,1,'G5','half'),(22,2,'E5','half'),
            (23,1,'D5','quarter'),(23,2,'E5','quarter'),(23,3,'G5','quarter'),(23,4,'E5','quarter'),
            (24,1,'C5','whole'),
        ],
    },
    # ──────────────────────────────────────────────
    # 3. 朋友别哭 - 吕方
    # ──────────────────────────────────────────────
    {
        "title": "朋友别哭", "artist": "吕方", "key": "C", "ts": "4/4", "bpm": 76, "difficulty": 3,
        "notes": [
            # 主歌 "有没有一扇窗 能让你不绝望"
            (1,1,'E5','quarter'),(1,2,'E5','quarter'),(1,3,'D5','quarter'),(1,4,'C5','quarter'),
            (2,1,'D5','half'),(2,2,'C5','half'),
            (3,1,'E5','quarter'),(3,2,'E5','quarter'),(3,3,'G5','quarter'),(3,4,'E5','quarter'),
            (4,1,'D5','whole'),
            (5,1,'C5','quarter'),(5,2,'C5','quarter'),(5,3,'D5','quarter'),(5,4,'E5','quarter'),
            (6,1,'G5','quarter'),(6,2,'E5','quarter'),(6,3,'D5','half'),
            (7,1,'C5','quarter'),(7,2,'D5','quarter'),(7,3,'E5','quarter'),(7,4,'D5','quarter'),
            (8,1,'C5','whole'),
            # 主歌2 "有没有一种爱 能让你不受伤"
            (9,1,'E5','quarter'),(9,2,'E5','quarter'),(9,3,'D5','quarter'),(9,4,'C5','quarter'),
            (10,1,'D5','half'),(10,2,'E5','half'),
            (11,1,'G5','quarter'),(11,2,'G5','quarter'),(11,3,'A5','quarter'),(11,4,'G5','quarter'),
            (12,1,'E5','whole'),
            (13,1,'C5','quarter'),(13,2,'D5','quarter'),(13,3,'E5','quarter'),(13,4,'G5','quarter'),
            (14,1,'A5','quarter'),(14,2,'G5','quarter'),(14,3,'E5','half'),
            (15,1,'D5','quarter'),(15,2,'E5','quarter'),(15,3,'D5','quarter'),(15,4,'C5','quarter'),
            (16,1,'C5','whole'),
            # 副歌 "朋友别哭 我依然是你心灵的归宿"
            (17,1,'G5','quarter'),(17,2,'G5','quarter'),(17,3,'A5','quarter'),(17,4,'G5','quarter'),
            (18,1,'E5','half'),(18,2,'D5','half'),
            (19,1,'G5','quarter'),(19,2,'G5','quarter'),(19,3,'A5','quarter'),(19,4,'G5','quarter'),
            (20,1,'E5','quarter'),(20,2,'D5','quarter'),(20,3,'C5','half'),
            (21,1,'E5','quarter'),(21,2,'G5','quarter'),(21,3,'A5','quarter'),(21,4,'C6','quarter'),
            (22,1,'B5','quarter'),(22,2,'A5','quarter'),(22,3,'G5','half'),
            (23,1,'A5','quarter'),(23,2,'G5','quarter'),(23,3,'E5','quarter'),(23,4,'D5','quarter'),
            (24,1,'C5','whole'),
            # 副歌延续 "朋友别哭 我会永远守护你"
            (25,1,'G5','quarter'),(25,2,'G5','quarter'),(25,3,'A5','quarter'),(25,4,'G5','quarter'),
            (26,1,'E5','half'),(26,2,'G5','half'),
            (27,1,'A5','quarter'),(27,2,'A5','quarter'),(27,3,'G5','quarter'),(27,4,'E5','quarter'),
            (28,1,'G5','half'),(28,2,'A5','half'),
            (29,1,'C6','quarter'),(29,2,'B5','quarter'),(29,3,'A5','quarter'),(29,4,'G5','quarter'),
            (30,1,'A5','half'),(30,2,'G5','half'),
            (31,1,'E5','quarter'),(31,2,'D5','quarter'),(31,3,'C5','quarter'),(31,4,'D5','quarter'),
            (32,1,'C5','whole'),
        ],
    },
    # ──────────────────────────────────────────────
    # 4. 万疆 - 李玉刚
    # ──────────────────────────────────────────────
    {
        "title": "万疆", "artist": "李玉刚", "key": "C", "ts": "4/4", "bpm": 80, "difficulty": 3,
        "notes": [
            # 主歌 "红日升在东方 其大道满霞光"
            (1,1,'G5','quarter'),(1,2,'A5','quarter'),(1,3,'C6','quarter'),(1,4,'A5','quarter'),
            (2,1,'G5','quarter'),(2,2,'E5','quarter'),(2,3,'G5','half'),
            (3,1,'E5','quarter'),(3,2,'G5','quarter'),(3,3,'A5','quarter'),(3,4,'G5','quarter'),
            (4,1,'E5','quarter'),(4,2,'D5','quarter'),(4,3,'C5','half'),
            # "我何其幸 生于你怀"
            (5,1,'D5','quarter'),(5,2,'E5','quarter'),(5,3,'G5','quarter'),(5,4,'E5','quarter'),
            (6,1,'D5','half'),(6,2,'C5','half'),
            (7,1,'D5','quarter'),(7,2,'E5','quarter'),(7,3,'G5','quarter'),(7,4,'A5','quarter'),
            (8,1,'G5','whole'),
            # "承一脉血流淌 千年的江山如画"
            (9,1,'A5','quarter'),(9,2,'C6','quarter'),(9,3,'A5','quarter'),(9,4,'G5','quarter'),
            (10,1,'A5','half'),(10,2,'G5','half'),
            (11,1,'E5','quarter'),(11,2,'G5','quarter'),(11,3,'A5','quarter'),(11,4,'C6','quarter'),
            (12,1,'A5','quarter'),(12,2,'G5','quarter'),(12,3,'E5','half'),
            # "万疆有你 在身旁"
            (13,1,'G5','quarter'),(13,2,'A5','quarter'),(13,3,'C6','quarter'),(13,4,'D6','quarter'),
            (14,1,'C6','half'),(14,2,'A5','half'),
            (15,1,'G5','quarter'),(15,2,'A5','quarter'),(15,3,'G5','quarter'),(15,4,'E5','quarter'),
            (16,1,'D5','quarter'),(16,2,'E5','quarter'),(16,3,'C5','half'),
            # 副歌 "万疆 万疆"
            (17,1,'C6','quarter'),(17,2,'D6','quarter'),(17,3,'C6','quarter'),(17,4,'A5','quarter'),
            (18,1,'G5','half'),(18,2,'A5','half'),
            (19,1,'C6','quarter'),(19,2,'A5','quarter'),(19,3,'G5','quarter'),(19,4,'E5','quarter'),
            (20,1,'G5','whole'),
            (21,1,'A5','quarter'),(21,2,'C6','quarter'),(21,3,'D6','quarter'),(21,4,'C6','quarter'),
            (22,1,'A5','half'),(22,2,'G5','half'),
            (23,1,'E5','quarter'),(23,2,'G5','quarter'),(23,3,'A5','quarter'),(23,4,'G5','quarter'),
            (24,1,'E5','quarter'),(24,2,'D5','quarter'),(24,3,'C5','half'),
            # 尾声
            (25,1,'D5','quarter'),(25,2,'E5','quarter'),(25,3,'G5','quarter'),(25,4,'A5','quarter'),
            (26,1,'G5','half'),(26,2,'E5','half'),
            (27,1,'D5','quarter'),(27,2,'E5','quarter'),(27,3,'D5','quarter'),(27,4,'C5','quarter'),
            (28,1,'C5','whole'),
        ],
    },
    # ──────────────────────────────────────────────
    # 5. 梦一场 - 那英
    # ──────────────────────────────────────────────
    {
        "title": "梦一场", "artist": "那英", "key": "C", "ts": "4/4", "bpm": 80, "difficulty": 3,
        "notes": [
            # 主歌 "我多么想见你 哪怕在梦里"
            (1,1,'E5','quarter'),(1,2,'E5','quarter'),(1,3,'D5','quarter'),(1,4,'E5','quarter'),
            (2,1,'G5','half'),(2,2,'E5','half'),
            (3,1,'D5','quarter'),(3,2,'D5','quarter'),(3,3,'C5','quarter'),(3,4,'D5','quarter'),
            (4,1,'E5','whole'),
            (5,1,'E5','quarter'),(5,2,'E5','quarter'),(5,3,'G5','quarter'),(5,4,'A5','quarter'),
            (6,1,'G5','quarter'),(6,2,'E5','quarter'),(6,3,'D5','half'),
            (7,1,'C5','quarter'),(7,2,'D5','quarter'),(7,3,'E5','quarter'),(7,4,'D5','quarter'),
            (8,1,'C5','whole'),
            # 主歌2 "我多么想抱你 哪怕是幻觉"
            (9,1,'E5','quarter'),(9,2,'E5','quarter'),(9,3,'D5','quarter'),(9,4,'E5','quarter'),
            (10,1,'G5','half'),(10,2,'A5','half'),
            (11,1,'G5','quarter'),(11,2,'G5','quarter'),(11,3,'E5','quarter'),(11,4,'G5','quarter'),
            (12,1,'A5','whole'),
            (13,1,'A5','quarter'),(13,2,'G5','quarter'),(13,3,'E5','quarter'),(13,4,'G5','quarter'),
            (14,1,'A5','quarter'),(14,2,'G5','quarter'),(14,3,'E5','half'),
            (15,1,'D5','quarter'),(15,2,'E5','quarter'),(15,3,'D5','quarter'),(15,4,'C5','quarter'),
            (16,1,'C5','whole'),
            # 副歌 "是不是梦一场 空欢喜一场"
            (17,1,'G5','quarter'),(17,2,'A5','quarter'),(17,3,'C6','quarter'),(17,4,'A5','quarter'),
            (18,1,'G5','half'),(18,2,'E5','half'),
            (19,1,'G5','quarter'),(19,2,'A5','quarter'),(19,3,'C6','quarter'),(19,4,'D6','quarter'),
            (20,1,'C6','whole'),
            (21,1,'A5','quarter'),(21,2,'G5','quarter'),(21,3,'E5','quarter'),(21,4,'G5','quarter'),
            (22,1,'A5','half'),(22,2,'G5','half'),
            (23,1,'E5','quarter'),(23,2,'D5','quarter'),(23,3,'C5','quarter'),(23,4,'D5','quarter'),
            (24,1,'C5','whole'),
            # 副歌延续 "爱了恨了伤了痛了"
            (25,1,'G5','quarter'),(25,2,'A5','quarter'),(25,3,'C6','quarter'),(25,4,'C6','quarter'),
            (26,1,'D6','half'),(26,2,'C6','half'),
            (27,1,'A5','quarter'),(27,2,'C6','quarter'),(27,3,'A5','quarter'),(27,4,'G5','quarter'),
            (28,1,'A5','half'),(28,2,'G5','half'),
            (29,1,'E5','quarter'),(29,2,'G5','quarter'),(29,3,'A5','quarter'),(29,4,'G5','quarter'),
            (30,1,'E5','half'),(30,2,'D5','half'),
            (31,1,'C5','quarter'),(31,2,'D5','quarter'),(31,3,'E5','quarter'),(31,4,'D5','quarter'),
            (32,1,'C5','whole'),
        ],
    },
    # ──────────────────────────────────────────────
    # 6. 太阳照常升起 (久石让)
    # ──────────────────────────────────────────────
    {
        "title": "太阳照常升起", "artist": "久石让", "key": "C", "ts": "4/4", "bpm": 76, "difficulty": 3,
        "notes": [
            # 主题 A
            (1,1,'E5','quarter'),(1,2,'G5','quarter'),(1,3,'A5','quarter'),(1,4,'G5','quarter'),
            (2,1,'E5','quarter'),(2,2,'D5','quarter'),(2,3,'C5','half'),
            (3,1,'D5','quarter'),(3,2,'E5','quarter'),(3,3,'G5','quarter'),(3,4,'A5','quarter'),
            (4,1,'G5','whole'),
            (5,1,'A5','quarter'),(5,2,'G5','quarter'),(5,3,'E5','quarter'),(5,4,'G5','quarter'),
            (6,1,'A5','half'),(6,2,'C6','half'),
            (7,1,'B5','quarter'),(7,2,'A5','quarter'),(7,3,'G5','quarter'),(7,4,'E5','quarter'),
            (8,1,'G5','whole'),
            # 主题 B
            (9,1,'C6','quarter'),(9,2,'B5','quarter'),(9,3,'A5','quarter'),(9,4,'G5','quarter'),
            (10,1,'A5','half'),(10,2,'G5','half'),
            (11,1,'E5','quarter'),(11,2,'G5','quarter'),(11,3,'A5','quarter'),(11,4,'G5','quarter'),
            (12,1,'E5','whole'),
            (13,1,'D5','quarter'),(13,2,'E5','quarter'),(13,3,'G5','quarter'),(13,4,'A5','quarter'),
            (14,1,'G5','quarter'),(14,2,'E5','quarter'),(14,3,'D5','half'),
            (15,1,'C5','quarter'),(15,2,'D5','quarter'),(15,3,'E5','quarter'),(15,4,'D5','quarter'),
            (16,1,'C5','whole'),
            # 再现 A'
            (17,1,'E5','quarter'),(17,2,'G5','quarter'),(17,3,'A5','quarter'),(17,4,'C6','quarter'),
            (18,1,'B5','quarter'),(18,2,'A5','quarter'),(18,3,'G5','half'),
            (19,1,'A5','quarter'),(19,2,'G5','quarter'),(19,3,'E5','quarter'),(19,4,'G5','quarter'),
            (20,1,'A5','whole'),
            (21,1,'C6','quarter'),(21,2,'B5','quarter'),(21,3,'A5','quarter'),(21,4,'G5','quarter'),
            (22,1,'E5','half'),(22,2,'G5','half'),
            (23,1,'D5','quarter'),(23,2,'E5','quarter'),(23,3,'D5','quarter'),(23,4,'C5','quarter'),
            (24,1,'C5','whole'),
        ],
    },
    # ──────────────────────────────────────────────
    # 7. 燃情岁月 (The Ludlows) - James Horner
    # ──────────────────────────────────────────────
    {
        "title": "燃情岁月 (The Ludlows)", "artist": "James Horner", "key": "C", "ts": "4/4", "bpm": 66, "difficulty": 3,
        "notes": [
            # 主题 A - 悠扬深情
            (1,1,'G5','half'),(1,2,'A5','quarter'),(1,3,'C6','quarter'),
            (2,1,'B5','half'),(2,2,'A5','half'),
            (3,1,'G5','quarter'),(3,2,'A5','quarter'),(3,3,'G5','quarter'),(3,4,'E5','quarter'),
            (4,1,'D5','whole'),
            (5,1,'E5','half'),(5,2,'G5','quarter'),(5,3,'A5','quarter'),
            (6,1,'G5','half'),(6,2,'E5','half'),
            (7,1,'D5','quarter'),(7,2,'E5','quarter'),(7,3,'G5','quarter'),(7,4,'E5','quarter'),
            (8,1,'C5','whole'),
            # 主题 B - 展开
            (9,1,'G5','half'),(9,2,'A5','quarter'),(9,3,'C6','quarter'),
            (10,1,'D6','half'),(10,2,'C6','half'),
            (11,1,'A5','quarter'),(11,2,'C6','quarter'),(11,3,'B5','quarter'),(11,4,'A5','quarter'),
            (12,1,'G5','whole'),
            (13,1,'A5','half'),(13,2,'C6','quarter'),(13,3,'D6','quarter'),
            (14,1,'C6','half'),(14,2,'A5','half'),
            (15,1,'G5','quarter'),(15,2,'A5','quarter'),(15,3,'G5','quarter'),(15,4,'E5','quarter'),
            (16,1,'D5','whole'),
            # 高潮/再现
            (17,1,'E5','half'),(17,2,'G5','quarter'),(17,3,'A5','quarter'),
            (18,1,'C6','half'),(18,2,'B5','half'),
            (19,1,'A5','quarter'),(19,2,'G5','quarter'),(19,3,'E5','quarter'),(19,4,'G5','quarter'),
            (20,1,'A5','whole'),
            (21,1,'C6','half'),(21,2,'D6','quarter'),(21,3,'C6','quarter'),
            (22,1,'A5','half'),(22,2,'G5','half'),
            (23,1,'E5','quarter'),(23,2,'D5','quarter'),(23,3,'C5','quarter'),(23,4,'D5','quarter'),
            (24,1,'C5','whole'),
        ],
    },
]
