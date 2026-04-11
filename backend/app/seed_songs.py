# -*- coding: utf-8 -*-
"""Seed song data for harmonica app."""


def get_seed_data():
    return [
        *_children_songs(),
        *_pop_songs(),
        *_folk_songs(),
        *_foreign_classics(),
    ]


def _children_songs():
    # Paddy Richter C 中音区: C5=4吹 D5=4吸 E5=5吹 F5=5吸 G5=6吹 A5=6吸 B5=7吸 C6=7吹
    return [
        {
            "title": '小星星', "artist": '儿歌', "key": 'C', "ts": '4/4', "bpm": 100, "difficulty": 1,
            "notes": [
                # 一闪一闪亮晶晶 (完整两段 + 结尾)
                (1,1,'C5','quarter'),(1,2,'C5','quarter'),(1,3,'G5','quarter'),(1,4,'G5','quarter'),
                (2,1,'A5','quarter'),(2,2,'A5','quarter'),(2,3,'G5','half'),
                (3,1,'F5','quarter'),(3,2,'F5','quarter'),(3,3,'E5','quarter'),(3,4,'E5','quarter'),
                (4,1,'D5','quarter'),(4,2,'D5','quarter'),(4,3,'C5','half'),
                (5,1,'G5','quarter'),(5,2,'G5','quarter'),(5,3,'F5','quarter'),(5,4,'F5','quarter'),
                (6,1,'E5','quarter'),(6,2,'E5','quarter'),(6,3,'D5','half'),
                (7,1,'G5','quarter'),(7,2,'G5','quarter'),(7,3,'F5','quarter'),(7,4,'F5','quarter'),
                (8,1,'E5','quarter'),(8,2,'E5','quarter'),(8,3,'D5','half'),
                # 再唱一遍主歌
                (9,1,'C5','quarter'),(9,2,'C5','quarter'),(9,3,'G5','quarter'),(9,4,'G5','quarter'),
                (10,1,'A5','quarter'),(10,2,'A5','quarter'),(10,3,'G5','half'),
                (11,1,'F5','quarter'),(11,2,'F5','quarter'),(11,3,'E5','quarter'),(11,4,'E5','quarter'),
                (12,1,'D5','quarter'),(12,2,'D5','quarter'),(12,3,'C5','half'),
            ],
        },
        {
            "title": '生日快乐', "artist": '儿歌', "key": 'C', "ts": '3/4', "bpm": 120, "difficulty": 1,
            "notes": [
                # Happy birthday to you (完整一遍)
                (1,1,'G5','eighth'),(1,2,'G5','eighth'),(1,3,'A5','quarter'),(1,4,'G5','quarter'),
                (2,1,'C6','quarter'),(2,2,'B5','half'),
                (3,1,'G5','eighth'),(3,2,'G5','eighth'),(3,3,'A5','quarter'),(3,4,'G5','quarter'),
                (4,1,'D6','quarter'),(4,2,'C6','half'),
                (5,1,'G5','eighth'),(5,2,'G5','eighth'),(5,3,'G6','quarter'),(5,4,'E6','quarter'),
                (6,1,'C6','quarter'),(6,2,'B5','quarter'),(6,3,'A5','quarter'),
                (7,1,'F6','eighth'),(7,2,'F6','eighth'),(7,3,'E6','quarter'),(7,4,'C6','quarter'),
                (8,1,'D6','quarter'),(8,2,'C6','half'),
            ],
        },
        {
            "title": '两只老虎', "artist": '儿歌', "key": 'C', "ts": '4/4', "bpm": 120, "difficulty": 1,
            "notes": [
                # 完整四段
                (1,1,'C5','quarter'),(1,2,'D5','quarter'),(1,3,'E5','quarter'),(1,4,'C5','quarter'),
                (2,1,'C5','quarter'),(2,2,'D5','quarter'),(2,3,'E5','quarter'),(2,4,'C5','quarter'),
                (3,1,'E5','quarter'),(3,2,'F5','quarter'),(3,3,'G5','half'),
                (4,1,'E5','quarter'),(4,2,'F5','quarter'),(4,3,'G5','half'),
                (5,1,'G5','eighth'),(5,2,'A5','eighth'),(5,3,'G5','eighth'),(5,4,'F5','eighth'),(5,5,'E5','quarter'),(5,6,'C5','quarter'),
                (6,1,'G5','eighth'),(6,2,'A5','eighth'),(6,3,'G5','eighth'),(6,4,'F5','eighth'),(6,5,'E5','quarter'),(6,6,'C5','quarter'),
                (7,1,'D5','quarter'),(7,2,'G5','quarter'),(7,3,'C5','half'),
                (8,1,'D5','quarter'),(8,2,'G5','quarter'),(8,3,'C5','half'),
            ],
        },
        {
            "title": '找朋友', "artist": '儿歌', "key": 'C', "ts": '2/4', "bpm": 108, "difficulty": 1,
            "notes": [
                # 找啊找啊找朋友 (完整两遍)
                (1,1,'G5','quarter'),(1,2,'E5','quarter'),
                (2,1,'G5','quarter'),(2,2,'E5','quarter'),
                (3,1,'A5','quarter'),(3,2,'A5','quarter'),
                (4,1,'G5','half'),
                (5,1,'F5','quarter'),(5,2,'F5','quarter'),
                (6,1,'E5','quarter'),(6,2,'E5','quarter'),
                (7,1,'D5','quarter'),(7,2,'D5','quarter'),
                (8,1,'C5','half'),
                # 第二遍
                (9,1,'G5','quarter'),(9,2,'E5','quarter'),
                (10,1,'G5','quarter'),(10,2,'E5','quarter'),
                (11,1,'A5','quarter'),(11,2,'A5','quarter'),
                (12,1,'G5','half'),
                (13,1,'F5','quarter'),(13,2,'F5','quarter'),
                (14,1,'E5','quarter'),(14,2,'E5','quarter'),
                (15,1,'D5','quarter'),(15,2,'D5','quarter'),
                (16,1,'C5','half'),
            ],
        },
        {
            "title": '粉刷匠', "artist": '儿歌', "key": 'C', "ts": '2/4', "bpm": 112, "difficulty": 1,
            "notes": [
                # 我是一个粉刷匠 (完整)
                (1,1,'E5','eighth'),(1,2,'E5','eighth'),(1,3,'F5','eighth'),(1,4,'G5','eighth'),
                (2,1,'G5','eighth'),(2,2,'G5','eighth'),(2,3,'G5','quarter'),
                (3,1,'A5','eighth'),(3,2,'G5','eighth'),(3,3,'F5','eighth'),(3,4,'E5','eighth'),
                (4,1,'D5','half'),
                (5,1,'C5','eighth'),(5,2,'C5','eighth'),(5,3,'D5','eighth'),(5,4,'E5','eighth'),
                (6,1,'E5','eighth'),(6,2,'D5','eighth'),(6,3,'D5','quarter'),
                (7,1,'C5','eighth'),(7,2,'C5','eighth'),(7,3,'D5','eighth'),(7,4,'E5','eighth'),
                (8,1,'D5','eighth'),(8,2,'C5','eighth'),(8,3,'C5','quarter'),
                # 第二段
                (9,1,'E5','eighth'),(9,2,'E5','eighth'),(9,3,'F5','eighth'),(9,4,'G5','eighth'),
                (10,1,'G5','eighth'),(10,2,'G5','eighth'),(10,3,'G5','quarter'),
                (11,1,'A5','eighth'),(11,2,'G5','eighth'),(11,3,'F5','eighth'),(11,4,'E5','eighth'),
                (12,1,'D5','half'),
                (13,1,'C5','eighth'),(13,2,'D5','eighth'),(13,3,'E5','eighth'),(13,4,'D5','eighth'),
                (14,1,'C5','eighth'),(14,2,'D5','eighth'),(14,3,'E5','quarter'),
                (15,1,'D5','eighth'),(15,2,'E5','eighth'),(15,3,'D5','eighth'),(15,4,'C5','eighth'),
                (16,1,'C5','half'),
            ],
        },
        {
            "title": '小毛驴', "artist": '儿歌', "key": 'C', "ts": '2/4', "bpm": 120, "difficulty": 1,
            "notes": [
                # 我有一只小毛驴 (完整)
                (1,1,'C5','eighth'),(1,2,'C5','eighth'),(1,3,'C5','eighth'),(1,4,'D5','eighth'),
                (2,1,'E5','eighth'),(2,2,'E5','eighth'),(2,3,'E5','quarter'),
                (3,1,'D5','eighth'),(3,2,'D5','eighth'),(3,3,'D5','eighth'),(3,4,'E5','eighth'),
                (4,1,'D5','half'),
                (5,1,'C5','eighth'),(5,2,'C5','eighth'),(5,3,'C5','eighth'),(5,4,'D5','eighth'),
                (6,1,'E5','eighth'),(6,2,'E5','eighth'),(6,3,'E5','quarter'),
                (7,1,'D5','eighth'),(7,2,'E5','eighth'),(7,3,'D5','eighth'),(7,4,'C5','eighth'),
                (8,1,'C5','half'),
                # 第二段：我心里真得意
                (9,1,'D5','eighth'),(9,2,'D5','eighth'),(9,3,'D5','eighth'),(9,4,'D5','eighth'),
                (10,1,'D5','eighth'),(10,2,'E5','eighth'),(10,3,'F5','quarter'),
                (11,1,'E5','eighth'),(11,2,'E5','eighth'),(11,3,'E5','eighth'),(11,4,'E5','eighth'),
                (12,1,'E5','eighth'),(12,2,'F5','eighth'),(12,3,'G5','quarter'),
                (13,1,'C5','eighth'),(13,2,'C5','eighth'),(13,3,'C5','eighth'),(13,4,'D5','eighth'),
                (14,1,'E5','eighth'),(14,2,'E5','eighth'),(14,3,'E5','quarter'),
                (15,1,'D5','eighth'),(15,2,'E5','eighth'),(15,3,'D5','eighth'),(15,4,'C5','eighth'),
                (16,1,'C5','half'),
            ],
        },
        {
            "title": '数鸭子', "artist": '儿歌', "key": 'C', "ts": '2/4', "bpm": 116, "difficulty": 1,
            "notes": [
                # 门前大桥下 游过一群鸭 (完整)
                (1,1,'G5','eighth'),(1,2,'A5','eighth'),(1,3,'G5','eighth'),(1,4,'E5','eighth'),
                (2,1,'D5','quarter'),(2,2,'E5','quarter'),
                (3,1,'G5','eighth'),(3,2,'A5','eighth'),(3,3,'G5','eighth'),(3,4,'E5','eighth'),
                (4,1,'D5','half'),
                (5,1,'G5','eighth'),(5,2,'G5','eighth'),(5,3,'A5','eighth'),(5,4,'G5','eighth'),
                (6,1,'E5','quarter'),(6,2,'G5','quarter'),
                (7,1,'D5','eighth'),(7,2,'D5','eighth'),(7,3,'E5','eighth'),(7,4,'D5','eighth'),
                (8,1,'C5','half'),
                # 快来快来数一数 二四六七八
                (9,1,'C5','eighth'),(9,2,'D5','eighth'),(9,3,'E5','eighth'),(9,4,'G5','eighth'),
                (10,1,'A5','quarter'),(10,2,'G5','quarter'),
                (11,1,'E5','eighth'),(11,2,'G5','eighth'),(11,3,'A5','eighth'),(11,4,'G5','eighth'),
                (12,1,'E5','half'),
                (13,1,'D5','eighth'),(13,2,'E5','eighth'),(13,3,'D5','eighth'),(13,4,'C5','eighth'),
                (14,1,'D5','quarter'),(14,2,'E5','quarter'),
                (15,1,'D5','eighth'),(15,2,'E5','eighth'),(15,3,'D5','eighth'),(15,4,'C5','eighth'),
                (16,1,'C5','half'),
            ],
        },
        {
            "title": '拔萝卜', "artist": '儿歌', "key": 'C', "ts": '2/4', "bpm": 108, "difficulty": 1,
            "notes": [
                # 拔萝卜拔萝卜 (完整)
                (1,1,'C5','quarter'),(1,2,'E5','quarter'),
                (2,1,'G5','quarter'),(2,2,'E5','quarter'),
                (3,1,'F5','quarter'),(3,2,'D5','quarter'),
                (4,1,'E5','half'),
                (5,1,'E5','quarter'),(5,2,'G5','quarter'),
                (6,1,'A5','quarter'),(6,2,'G5','quarter'),
                (7,1,'F5','quarter'),(7,2,'E5','quarter'),
                (8,1,'C5','half'),
                # 嘿哟嘿哟拔不动
                (9,1,'D5','quarter'),(9,2,'D5','quarter'),
                (10,1,'E5','quarter'),(10,2,'F5','quarter'),
                (11,1,'E5','quarter'),(11,2,'D5','quarter'),
                (12,1,'C5','half'),
                (13,1,'E5','quarter'),(13,2,'G5','quarter'),
                (14,1,'A5','quarter'),(14,2,'G5','quarter'),
                (15,1,'F5','quarter'),(15,2,'E5','quarter'),
                (16,1,'C5','half'),
            ],
        },
    ]


def _pop_songs():
    return [
        {
            "title": '欢乐颂', "artist": '贝多芬', "key": 'C', "ts": '4/4', "bpm": 120, "difficulty": 2,
            "notes": [
                # 欢乐颂完整主旋律 (C5八度)
                (1,1,'E5','quarter'),(1,2,'E5','quarter'),(1,3,'F5','quarter'),(1,4,'G5','quarter'),
                (2,1,'G5','quarter'),(2,2,'F5','quarter'),(2,3,'E5','quarter'),(2,4,'D5','quarter'),
                (3,1,'C5','quarter'),(3,2,'C5','quarter'),(3,3,'D5','quarter'),(3,4,'E5','quarter'),
                (4,1,'E5','quarter',1),(4,2,'D5','eighth'),(4,3,'D5','half'),
                (5,1,'E5','quarter'),(5,2,'E5','quarter'),(5,3,'F5','quarter'),(5,4,'G5','quarter'),
                (6,1,'G5','quarter'),(6,2,'F5','quarter'),(6,3,'E5','quarter'),(6,4,'D5','quarter'),
                (7,1,'C5','quarter'),(7,2,'C5','quarter'),(7,3,'D5','quarter'),(7,4,'E5','quarter'),
                (8,1,'D5','quarter',1),(8,2,'C5','eighth'),(8,3,'C5','half'),
                # B段
                (9,1,'D5','quarter'),(9,2,'D5','quarter'),(9,3,'E5','quarter'),(9,4,'C5','quarter'),
                (10,1,'D5','quarter'),(10,2,'E5','eighth'),(10,3,'F5','eighth'),(10,4,'E5','quarter'),(10,5,'C5','quarter'),
                (11,1,'D5','quarter'),(11,2,'E5','eighth'),(11,3,'F5','eighth'),(11,4,'E5','quarter'),(11,5,'D5','quarter'),
                (12,1,'C5','quarter'),(12,2,'D5','quarter'),(12,3,'G5','half'),
                # 再现A段
                (13,1,'E5','quarter'),(13,2,'E5','quarter'),(13,3,'F5','quarter'),(13,4,'G5','quarter'),
                (14,1,'G5','quarter'),(14,2,'F5','quarter'),(14,3,'E5','quarter'),(14,4,'D5','quarter'),
                (15,1,'C5','quarter'),(15,2,'C5','quarter'),(15,3,'D5','quarter'),(15,4,'E5','quarter'),
                (16,1,'D5','quarter',1),(16,2,'C5','eighth'),(16,3,'C5','half'),
            ],
        },
        {
            "title": '世上只有妈妈好', "artist": '儿歌', "key": 'C', "ts": '4/4', "bpm": 88, "difficulty": 2,
            "notes": [
                (1,1,'G4','quarter'),(1,2,'E4','quarter'),(1,3,'G4','quarter'),(1,4,'A4','quarter'),
                (2,1,'G4','quarter'),(2,2,'E4','quarter'),(2,3,'G4','half'),(3,1,'A4','quarter'),
                (3,2,'G4','quarter'),(3,3,'E4','quarter'),(3,4,'G4','quarter'),(4,1,'D4','half'),
                (4,2,'E4','quarter'),(4,3,'D4','quarter'),(5,1,'C4','quarter'),(5,2,'D4','quarter'),
                (5,3,'E4','quarter'),(5,4,'G4','quarter'),(6,1,'A4','half'),(6,2,'G4','half'),
                (7,1,'E4','quarter'),(7,2,'G4','quarter'),(7,3,'A4','quarter'),(7,4,'G4','quarter'),
                (8,1,'C4','whole'),
            ],
        },
        {
            "title": '月亮代表我的心', "artist": '邓丽君', "key": 'C', "ts": '4/4', "bpm": 72, "difficulty": 3,
            "notes": [
                (1,1,'E4','quarter'),(1,2,'E4','eighth'),(1,3,'F4','eighth'),(1,4,'G4','half'),
                (2,1,'G4','quarter'),(2,2,'A4','quarter'),(2,3,'G4','quarter'),(2,4,'E4','quarter'),
                (3,1,'C4','quarter'),(3,2,'D4','quarter'),(3,3,'E4','half'),(4,1,'D4','whole'),
                (5,1,'E4','quarter'),(5,2,'E4','eighth'),(5,3,'F4','eighth'),(5,4,'G4','half'),
                (6,1,'C5','quarter'),(6,2,'B4','quarter'),(6,3,'A4','quarter'),(6,4,'G4','quarter'),
                (7,1,'F4','quarter'),(7,2,'G4','quarter'),(7,3,'A4','half'),(8,1,'G4','whole'),
            ],
        },
        {
            "title": '甜蜜蜜', "artist": '邓丽君', "key": 'C', "ts": '4/4', "bpm": 108, "difficulty": 2,
            "notes": [
                (1,1,'E4','quarter'),(1,2,'G4','quarter'),(1,3,'A4','quarter'),(1,4,'G4','quarter'),
                (2,1,'E4','half'),(2,2,'G4','half'),(3,1,'A4','quarter'),(3,2,'G4','quarter'),
                (3,3,'E4','quarter'),(3,4,'D4','quarter'),(4,1,'C4','whole'),(5,1,'E4','quarter'),
                (5,2,'G4','quarter'),(5,3,'A4','quarter'),(5,4,'C5','quarter'),(6,1,'B4','half'),
                (6,2,'A4','half'),(7,1,'G4','quarter'),(7,2,'A4','quarter'),(7,3,'G4','quarter'),
                (7,4,'E4','quarter'),(8,1,'G4','whole'),
            ],
        },
        {
            "title": '朋友', "artist": '周华健', "key": 'C', "ts": '4/4', "bpm": 88, "difficulty": 3,
            "notes": [
                (1,1,'G4','quarter'),(1,2,'A4','quarter'),(1,3,'G4','quarter'),(1,4,'E4','quarter'),
                (2,1,'D4','half'),(2,2,'E4','quarter'),(2,3,'D4','quarter'),(3,1,'C4','quarter'),
                (3,2,'D4','quarter'),(3,3,'E4','quarter'),(3,4,'G4','quarter'),(4,1,'A4','whole'),
                (5,1,'G4','quarter'),(5,2,'A4','quarter'),(5,3,'G4','quarter'),(5,4,'E4','quarter'),
                (6,1,'D4','half'),(6,2,'C4','half'),(7,1,'E4','quarter'),(7,2,'G4','quarter'),
                (7,3,'A4','quarter'),(7,4,'G4','quarter'),(8,1,'G4','whole'),
            ],
        },
        {
            "title": '童年', "artist": '罗大佑', "key": 'C', "ts": '4/4', "bpm": 120, "difficulty": 2,
            "notes": [
                (1,1,'C4','quarter'),(1,2,'E4','quarter'),(1,3,'G4','quarter'),(1,4,'A4','quarter'),
                (2,1,'G4','half'),(2,2,'E4','half'),(3,1,'F4','quarter'),(3,2,'G4','quarter'),
                (3,3,'A4','quarter'),(3,4,'G4','quarter'),(4,1,'E4','whole'),(5,1,'C4','quarter'),
                (5,2,'E4','quarter'),(5,3,'G4','quarter'),(5,4,'A4','quarter'),(6,1,'C5','half'),
                (6,2,'B4','half'),(7,1,'A4','quarter'),(7,2,'G4','quarter'),(7,3,'F4','quarter'),
                (7,4,'E4','quarter'),(8,1,'C4','whole'),
            ],
        },
        {
            "title": '同桌的你', "artist": '老狼', "key": 'C', "ts": '4/4', "bpm": 96, "difficulty": 2,
            "notes": [
                (1,1,'E4','quarter'),(1,2,'G4','quarter'),(1,3,'A4','quarter'),(1,4,'G4','quarter'),
                (2,1,'E4','half'),(2,2,'D4','half'),(3,1,'C4','quarter'),(3,2,'D4','quarter'),
                (3,3,'E4','quarter'),(3,4,'G4','quarter'),(4,1,'A4','whole'),(5,1,'G4','quarter'),
                (5,2,'A4','quarter'),(5,3,'G4','quarter'),(5,4,'E4','quarter'),(6,1,'D4','half'),
                (6,2,'E4','half'),(7,1,'F4','quarter'),(7,2,'E4','quarter'),(7,3,'D4','quarter'),
                (7,4,'C4','quarter'),(8,1,'G4','whole'),
            ],
        },
        {
            "title": '晴天', "artist": '周杰伦', "key": 'C', "ts": '4/4', "bpm": 116, "difficulty": 3,
            "notes": [
                (1,1,'G4','eighth'),(1,2,'A4','eighth'),(1,3,'G4','quarter'),(1,4,'E4','quarter'),
                (1,5,'D4','quarter'),(2,1,'C4','half'),(2,2,'D4','quarter'),(2,3,'E4','quarter'),
                (3,1,'G4','eighth'),(3,2,'A4','eighth'),(3,3,'G4','quarter'),(3,4,'E4','quarter'),
                (3,5,'D4','quarter'),(4,1,'E4','whole'),(5,1,'A4','eighth'),(5,2,'B4','eighth'),
                (5,3,'A4','quarter'),(5,4,'G4','quarter'),(5,5,'E4','quarter'),(6,1,'G4','half'),
                (6,2,'A4','half'),(7,1,'G4','quarter'),(7,2,'E4','quarter'),(7,3,'D4','quarter'),
                (7,4,'C4','quarter'),(8,1,'G4','whole'),
            ],
        },
        {
            "title": '小幸运', "artist": '田馥甸', "key": 'C', "ts": '4/4', "bpm": 96, "difficulty": 3,
            "notes": [
                (1,1,'E4','quarter'),(1,2,'G4','quarter'),(1,3,'A4','quarter'),(1,4,'G4','quarter'),
                (2,1,'E4','half'),(2,2,'G4','half'),(3,1,'A4','quarter'),(3,2,'B4','quarter'),
                (3,3,'A4','quarter'),(3,4,'G4','quarter'),(4,1,'E4','whole'),(5,1,'G4','quarter'),
                (5,2,'A4','quarter'),(5,3,'B4','quarter'),(5,4,'A4','quarter'),(6,1,'G4','half'),
                (6,2,'E4','half'),(7,1,'F4','quarter'),(7,2,'G4','quarter'),(7,3,'A4','quarter'),
                (7,4,'G4','quarter'),(8,1,'C5','whole'),
            ],
        },
        {
            "title": '后来', "artist": '刘若英', "key": 'C', "ts": '4/4', "bpm": 72, "difficulty": 3,
            "notes": [
                (1,1,'G4','quarter'),(1,2,'A4','quarter'),(1,3,'G4','quarter'),(1,4,'E4','quarter'),
                (2,1,'D4','half'),(2,2,'E4','half'),(3,1,'C4','quarter'),(3,2,'E4','quarter'),
                (3,3,'G4','quarter'),(3,4,'A4','quarter'),(4,1,'G4','whole'),(5,1,'A4','quarter'),
                (5,2,'B4','quarter'),(5,3,'A4','quarter'),(5,4,'G4','quarter'),(6,1,'E4','half'),
                (6,2,'G4','half'),(7,1,'A4','quarter'),(7,2,'G4','quarter'),(7,3,'E4','quarter'),
                (7,4,'D4','quarter'),(8,1,'C4','whole'),
            ],
        },
        {
            "title": '平凡之路', "artist": '朴树', "key": 'C', "ts": '4/4', "bpm": 88, "difficulty": 3,
            "notes": [
                (1,1,'C4','quarter'),(1,2,'E4','quarter'),(1,3,'G4','quarter'),(1,4,'E4','quarter'),
                (2,1,'D4','half'),(2,2,'C4','half'),(3,1,'E4','quarter'),(3,2,'G4','quarter'),
                (3,3,'A4','quarter'),(3,4,'G4','quarter'),(4,1,'E4','whole'),(5,1,'G4','quarter'),
                (5,2,'A4','quarter'),(5,3,'G4','quarter'),(5,4,'E4','quarter'),(6,1,'D4','half'),
                (6,2,'E4','half'),(7,1,'C4','quarter'),(7,2,'D4','quarter'),(7,3,'E4','quarter'),
                (7,4,'G4','quarter'),(8,1,'C5','whole'),
            ],
        },
        {
            "title": '夜空中最亮的星', "artist": '逃跑计划', "key": 'C', "ts": '4/4', "bpm": 108, "difficulty": 3,
            "notes": [
                (1,1,'E4','quarter'),(1,2,'G4','quarter'),(1,3,'A4','quarter'),(1,4,'G4','quarter'),
                (2,1,'E4','half'),(2,2,'D4','half'),(3,1,'C4','quarter'),(3,2,'E4','quarter'),
                (3,3,'G4','quarter'),(3,4,'A4','quarter'),(4,1,'G4','whole'),(5,1,'A4','quarter'),
                (5,2,'G4','quarter'),(5,3,'E4','quarter'),(5,4,'G4','quarter'),(6,1,'A4','half'),
                (6,2,'B4','half'),(7,1,'C5','quarter'),(7,2,'B4','quarter'),(7,3,'A4','quarter'),
                (7,4,'G4','quarter'),(8,1,'E4','whole'),
            ],
        },
        {
            "title": '成都', "artist": '赵雷', "key": 'C', "ts": '4/4', "bpm": 80, "difficulty": 3,
            "notes": [
                (1,1,'G4','quarter'),(1,2,'E4','quarter'),(1,3,'D4','quarter'),(1,4,'C4','quarter'),
                (2,1,'D4','half'),(2,2,'E4','half'),(3,1,'G4','quarter'),(3,2,'A4','quarter'),
                (3,3,'G4','quarter'),(3,4,'E4','quarter'),(4,1,'D4','whole'),(5,1,'E4','quarter'),
                (5,2,'G4','quarter'),(5,3,'A4','quarter'),(5,4,'G4','quarter'),(6,1,'E4','half'),
                (6,2,'D4','half'),(7,1,'C4','quarter'),(7,2,'D4','quarter'),(7,3,'E4','quarter'),
                (7,4,'G4','quarter'),(8,1,'A4','whole'),
            ],
        },
    ]


def _folk_songs():
    return [
        {
            "title": '茅莉花', "artist": '民歌', "key": 'C', "ts": '3/4', "bpm": 80, "difficulty": 2,
            "notes": [
                (1,1,'E4','quarter'),(1,2,'G4','quarter'),(1,3,'A4','quarter'),(2,1,'G4','half'),
                (2,2,'E4','quarter'),(3,1,'C4','quarter'),(3,2,'D4','quarter'),(3,3,'E4','quarter'),
                (4,1,'G4','half'),(5,1,'A4','quarter'),(5,2,'G4','quarter'),(5,3,'E4','quarter'),
                (6,1,'D4','half'),(6,2,'E4','quarter'),(7,1,'C4','quarter'),(7,2,'D4','quarter'),
                (7,3,'E4','quarter'),(8,1,'C4','half'),
            ],
        },
        {
            "title": '康定情歌', "artist": '民歌', "key": 'C', "ts": '3/4', "bpm": 96, "difficulty": 2,
            "notes": [
                (1,1,'G4','quarter'),(1,2,'A4','quarter'),(1,3,'G4','quarter'),(2,1,'E4','half'),
                (2,2,'G4','quarter'),(3,1,'A4','quarter'),(3,2,'G4','quarter'),(3,3,'E4','quarter'),
                (4,1,'D4','half'),(5,1,'E4','quarter'),(5,2,'G4','quarter'),(5,3,'A4','quarter'),
                (6,1,'C5','half'),(6,2,'B4','quarter'),(7,1,'A4','quarter'),(7,2,'G4','quarter'),
                (7,3,'E4','quarter'),(8,1,'G4','half'),
            ],
        },
        {
            "title": '沂蒙山小调', "artist": '民歌', "key": 'C', "ts": '4/4', "bpm": 88, "difficulty": 2,
            "notes": [
                (1,1,'G4','quarter'),(1,2,'A4','quarter'),(1,3,'G4','quarter'),(1,4,'E4','quarter'),
                (2,1,'D4','half'),(2,2,'E4','half'),(3,1,'G4','quarter'),(3,2,'A4','quarter'),
                (3,3,'G4','quarter'),(3,4,'E4','quarter'),(4,1,'C4','whole'),(5,1,'E4','quarter'),
                (5,2,'G4','quarter'),(5,3,'A4','quarter'),(5,4,'G4','quarter'),(6,1,'E4','half'),
                (6,2,'D4','half'),(7,1,'C4','quarter'),(7,2,'D4','quarter'),(7,3,'E4','quarter'),
                (7,4,'G4','quarter'),(8,1,'A4','whole'),
            ],
        },
        {
            "title": '草原上升起不落的太阳', "artist": '民歌', "key": 'C', "ts": '4/4', "bpm": 96, "difficulty": 2,
            "notes": [
                (1,1,'C4','quarter'),(1,2,'E4','quarter'),(1,3,'G4','quarter'),(1,4,'A4','quarter'),
                (2,1,'G4','half'),(2,2,'E4','half'),(3,1,'G4','quarter'),(3,2,'A4','quarter'),
                (3,3,'G4','quarter'),(3,4,'E4','quarter'),(4,1,'D4','whole'),(5,1,'E4','quarter'),
                (5,2,'G4','quarter'),(5,3,'A4','quarter'),(5,4,'C5','quarter'),(6,1,'B4','half'),
                (6,2,'A4','half'),(7,1,'G4','quarter'),(7,2,'E4','quarter'),(7,3,'D4','quarter'),
                (7,4,'C4','quarter'),(8,1,'G4','whole'),
            ],
        },
        {
            "title": '在那遥远的地方', "artist": '民歌', "key": 'C', "ts": '3/4', "bpm": 80, "difficulty": 2,
            "notes": [
                (1,1,'G4','quarter'),(1,2,'A4','quarter'),(1,3,'G4','quarter'),(2,1,'E4','half'),
                (2,2,'G4','quarter'),(3,1,'A4','quarter'),(3,2,'G4','quarter'),(3,3,'E4','quarter'),
                (4,1,'D4','half'),(5,1,'C4','quarter'),(5,2,'D4','quarter'),(5,3,'E4','quarter'),
                (6,1,'G4','half'),(6,2,'A4','quarter'),(7,1,'G4','quarter'),(7,2,'E4','quarter'),
                (7,3,'D4','quarter'),(8,1,'C4','half'),
            ],
        },
    ]


def _foreign_classics():
    return [
        {
            "title": 'Amazing Grace', "artist": 'Traditional', "key": 'C', "ts": '3/4', "bpm": 80, "difficulty": 2,
            "notes": [
                (1,1,'C4','quarter'),(1,2,'E4','quarter'),(1,3,'G4','quarter'),(2,1,'C5','half'),
                (2,2,'A4','quarter'),(3,1,'G4','half'),(3,2,'E4','quarter'),(4,1,'G4','half'),
                (5,1,'E4','quarter'),(5,2,'G4','quarter'),(5,3,'A4','quarter'),(6,1,'C5','half'),
                (6,2,'A4','quarter'),(7,1,'G4','quarter'),(7,2,'E4','quarter'),(7,3,'C4','quarter'),
                (8,1,'C4','half'),
            ],
        },
        {
            "title": 'Jingle Bells', "artist": 'Traditional', "key": 'C', "ts": '4/4', "bpm": 120, "difficulty": 1,
            "notes": [
                # Jingle Bells 完整副歌 + 主歌 (C5八度)
                # 副歌: Jingle bells, jingle bells, jingle all the way
                (1,1,'E5','quarter'),(1,2,'E5','quarter'),(1,3,'E5','half'),
                (2,1,'E5','quarter'),(2,2,'E5','quarter'),(2,3,'E5','half'),
                (3,1,'E5','quarter'),(3,2,'G5','quarter'),(3,3,'C5','quarter'),(3,4,'D5','quarter'),
                (4,1,'E5','whole'),
                (5,1,'F5','quarter'),(5,2,'F5','quarter'),(5,3,'F5','quarter'),(5,4,'F5','quarter'),
                (6,1,'F5','quarter'),(6,2,'E5','quarter'),(6,3,'E5','quarter'),(6,4,'E5','quarter'),
                (7,1,'E5','quarter'),(7,2,'D5','quarter'),(7,3,'D5','quarter'),(7,4,'E5','quarter'),
                (8,1,'D5','half'),(8,2,'G5','half'),
                # 副歌重复
                (9,1,'E5','quarter'),(9,2,'E5','quarter'),(9,3,'E5','half'),
                (10,1,'E5','quarter'),(10,2,'E5','quarter'),(10,3,'E5','half'),
                (11,1,'E5','quarter'),(11,2,'G5','quarter'),(11,3,'C5','quarter'),(11,4,'D5','quarter'),
                (12,1,'E5','whole'),
                (13,1,'F5','quarter'),(13,2,'F5','quarter'),(13,3,'F5','quarter'),(13,4,'F5','quarter'),
                (14,1,'F5','quarter'),(14,2,'E5','quarter'),(14,3,'E5','quarter'),(14,4,'E5','quarter'),
                (15,1,'G5','quarter'),(15,2,'G5','quarter'),(15,3,'F5','quarter'),(15,4,'D5','quarter'),
                (16,1,'C5','whole'),
            ],
        },
        {
            "title": 'Auld Lang Syne', "artist": 'Traditional', "key": 'C', "ts": '4/4', "bpm": 80, "difficulty": 2,
            "notes": [
                (1,1,'C4','quarter'),(1,2,'F4','quarter'),(1,3,'F4','quarter'),(1,4,'A4','quarter'),
                (2,1,'G4','half'),(2,2,'F4','quarter'),(2,3,'G4','quarter'),(3,1,'A4','quarter'),
                (3,2,'F4','quarter'),(3,3,'F4','quarter'),(3,4,'C4','quarter'),(4,1,'D4','whole'),
                (5,1,'C4','quarter'),(5,2,'F4','quarter'),(5,3,'F4','quarter'),(5,4,'A4','quarter'),
                (6,1,'C5','half'),(6,2,'A4','quarter'),(6,3,'G4','quarter'),(7,1,'A4','quarter'),
                (7,2,'G4','quarter'),(7,3,'F4','quarter'),(7,4,'D4','quarter'),(8,1,'F4','whole'),
            ],
        },
        {
            "title": 'Scarborough Fair', "artist": 'Traditional', "key": 'C', "ts": '3/4', "bpm": 72, "difficulty": 3,
            "notes": [
                (1,1,'A4','quarter'),(1,2,'G4','quarter'),(1,3,'E4','quarter'),(2,1,'A4','half'),
                (2,2,'A4','quarter'),(3,1,'C5','quarter'),(3,2,'B4','quarter'),(3,3,'A4','quarter'),
                (4,1,'G4','half'),(5,1,'E4','quarter'),(5,2,'G4','quarter'),(5,3,'A4','quarter'),
                (6,1,'G4','half'),(6,2,'E4','quarter'),(7,1,'D4','quarter'),(7,2,'E4','quarter'),
                (7,3,'G4','quarter'),(8,1,'A4','half'),
            ],
        },
        {
            "title": 'Danny Boy', "artist": 'Traditional', "key": 'C', "ts": '4/4', "bpm": 72, "difficulty": 3,
            "notes": [
                (1,1,'G4','quarter'),(1,2,'C5','quarter'),(1,3,'C5','quarter'),(1,4,'B4','quarter'),
                (2,1,'A4','half'),(2,2,'G4','half'),(3,1,'E4','quarter'),(3,2,'G4','quarter'),
                (3,3,'A4','quarter'),(3,4,'G4','quarter'),(4,1,'F4','whole'),(5,1,'G4','quarter'),
                (5,2,'C5','quarter'),(5,3,'C5','quarter'),(5,4,'B4','quarter'),(6,1,'A4','half'),
                (6,2,'G4','half'),(7,1,'E4','quarter'),(7,2,'G4','quarter'),(7,3,'A4','quarter'),
                (7,4,'G4','quarter'),(8,1,'C4','whole'),
            ],
        },
    ]

