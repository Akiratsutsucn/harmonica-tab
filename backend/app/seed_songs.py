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
    return [
        {
            "title": '小星星', "artist": '儿歌', "key": 'C', "ts": '4/4', "bpm": 100, "difficulty": 1,
            "notes": [
                (1,1,'C4','quarter'),(1,2,'C4','quarter'),(1,3,'G4','quarter'),(1,4,'G4','quarter'),
                (2,1,'A4','quarter'),(2,2,'A4','quarter'),(2,3,'G4','half'),(3,1,'F4','quarter'),
                (3,2,'F4','quarter'),(3,3,'E4','quarter'),(3,4,'E4','quarter'),(4,1,'D4','quarter'),
                (4,2,'D4','quarter'),(4,3,'C4','half'),(5,1,'G4','quarter'),(5,2,'G4','quarter'),
                (5,3,'F4','quarter'),(5,4,'F4','quarter'),(6,1,'E4','quarter'),(6,2,'E4','quarter'),
                (6,3,'D4','half'),(7,1,'G4','quarter'),(7,2,'G4','quarter'),(7,3,'F4','quarter'),
                (7,4,'F4','quarter'),(8,1,'E4','quarter'),(8,2,'E4','quarter'),(8,3,'D4','half'),
            ],
        },
        {
            "title": '生日快乐', "artist": '儿歌', "key": 'C', "ts": '3/4', "bpm": 120, "difficulty": 1,
            "notes": [
                (1,1,'C4','quarter'),(1,2,'C4','eighth'),(1,3,'D4','quarter',1),(2,1,'C4','quarter'),
                (2,2,'F4','quarter'),(2,3,'E4','half'),(3,1,'C4','quarter'),(3,2,'C4','eighth'),
                (3,3,'D4','quarter',1),(4,1,'C4','quarter'),(4,2,'G4','quarter'),(4,3,'F4','half'),
                (5,1,'C4','quarter'),(5,2,'C4','eighth'),(5,3,'C5','quarter',1),(6,1,'A4','quarter'),
                (6,2,'F4','quarter'),(6,3,'E4','quarter'),(7,1,'D4','quarter'),(7,2,'A4','eighth'),
                (7,3,'G4','quarter',1),(8,1,'F4','quarter'),(8,2,'F4','quarter'),(8,3,'F4','quarter'),
            ],
        },
        {
            "title": '两只老虎', "artist": '儿歌', "key": 'C', "ts": '4/4', "bpm": 120, "difficulty": 1,
            "notes": [
                (1,1,'C4','quarter'),(1,2,'D4','quarter'),(1,3,'E4','quarter'),(1,4,'C4','quarter'),
                (2,1,'C4','quarter'),(2,2,'D4','quarter'),(2,3,'E4','quarter'),(2,4,'C4','quarter'),
                (3,1,'E4','quarter'),(3,2,'F4','quarter'),(3,3,'G4','half'),(4,1,'E4','quarter'),
                (4,2,'F4','quarter'),(4,3,'G4','half'),(5,1,'G4','eighth'),(5,2,'A4','eighth'),
                (5,3,'G4','eighth'),(5,4,'F4','eighth'),(5,5,'E4','quarter'),(5,6,'C4','quarter'),
                (6,1,'G4','eighth'),(6,2,'A4','eighth'),(6,3,'G4','eighth'),(6,4,'F4','eighth'),
                (6,5,'E4','quarter'),(6,6,'C4','quarter'),(7,1,'C4','quarter'),(7,2,'G3','quarter'),
                (7,3,'C4','half'),(8,1,'C4','quarter'),(8,2,'G3','quarter'),(8,3,'C4','half'),
            ],
        },
        {
            "title": '找朋友', "artist": '儿歌', "key": 'C', "ts": '2/4', "bpm": 108, "difficulty": 1,
            "notes": [
                (1,1,'G4','quarter'),(1,2,'E4','quarter'),(2,1,'G4','quarter'),(2,2,'E4','quarter'),
                (3,1,'A4','quarter'),(3,2,'A4','quarter'),(4,1,'G4','half'),(5,1,'F4','quarter'),
                (5,2,'F4','quarter'),(6,1,'E4','quarter'),(6,2,'E4','quarter'),(7,1,'D4','quarter'),
                (7,2,'D4','quarter'),(8,1,'C4','half'),
            ],
        },
        {
            "title": '粉刷匠', "artist": '儿歌', "key": 'C', "ts": '2/4', "bpm": 112, "difficulty": 1,
            "notes": [
                (1,1,'E4','quarter'),(1,2,'G4','quarter'),(2,1,'E4','quarter'),(2,2,'G4','quarter'),
                (3,1,'A4','quarter'),(3,2,'G4','quarter'),(4,1,'E4','half'),(5,1,'G4','quarter'),
                (5,2,'E4','quarter'),(6,1,'G4','quarter'),(6,2,'A4','quarter'),(7,1,'G4','quarter'),
                (7,2,'E4','quarter'),(8,1,'C4','half'),
            ],
        },
        {
            "title": '小毛驴', "artist": '儿歌', "key": 'C', "ts": '2/4', "bpm": 120, "difficulty": 1,
            "notes": [
                (1,1,'C4','eighth'),(1,2,'D4','eighth'),(1,3,'E4','eighth'),(1,4,'C4','eighth'),
                (2,1,'E4','eighth'),(2,2,'C4','eighth'),(2,3,'E4','quarter'),(3,1,'F4','eighth'),
                (3,2,'G4','eighth'),(3,3,'A4','eighth'),(3,4,'F4','eighth'),(4,1,'G4','half'),
                (5,1,'E4','eighth'),(5,2,'F4','eighth'),(5,3,'G4','eighth'),(5,4,'E4','eighth'),
                (6,1,'G4','eighth'),(6,2,'E4','eighth'),(6,3,'G4','quarter'),(7,1,'A4','eighth'),
                (7,2,'G4','eighth'),(7,3,'F4','eighth'),(7,4,'E4','eighth'),(8,1,'C4','half'),
            ],
        },
        {
            "title": '数鸭子', "artist": '儿歌', "key": 'C', "ts": '2/4', "bpm": 116, "difficulty": 1,
            "notes": [
                (1,1,'G4','eighth'),(1,2,'G4','eighth'),(1,3,'A4','eighth'),(1,4,'G4','eighth'),
                (2,1,'E4','quarter'),(2,2,'G4','quarter'),(3,1,'D4','eighth'),(3,2,'D4','eighth'),
                (3,3,'E4','eighth'),(3,4,'D4','eighth'),(4,1,'C4','half'),(5,1,'G4','eighth'),
                (5,2,'A4','eighth'),(5,3,'G4','eighth'),(5,4,'E4','eighth'),(6,1,'D4','quarter'),
                (6,2,'E4','quarter'),(7,1,'C4','eighth'),(7,2,'D4','eighth'),(7,3,'E4','eighth'),
                (7,4,'G4','eighth'),(8,1,'C4','half'),
            ],
        },
        {
            "title": '拔萨卜', "artist": '儿歌', "key": 'C', "ts": '2/4', "bpm": 108, "difficulty": 1,
            "notes": [
                (1,1,'C4','quarter'),(1,2,'E4','quarter'),(2,1,'G4','quarter'),(2,2,'E4','quarter'),
                (3,1,'F4','quarter'),(3,2,'D4','quarter'),(4,1,'E4','half'),(5,1,'E4','quarter'),
                (5,2,'G4','quarter'),(6,1,'A4','quarter'),(6,2,'G4','quarter'),(7,1,'F4','quarter'),
                (7,2,'E4','quarter'),(8,1,'C4','half'),
            ],
        },
    ]


def _pop_songs():
    return [
        {
            "title": '欢乐颂', "artist": '贝多芬', "key": 'C', "ts": '4/4', "bpm": 120, "difficulty": 2,
            "notes": [
                (1,1,'E4','quarter'),(1,2,'E4','quarter'),(1,3,'F4','quarter'),(1,4,'G4','quarter'),
                (2,1,'G4','quarter'),(2,2,'F4','quarter'),(2,3,'E4','quarter'),(2,4,'D4','quarter'),
                (3,1,'C4','quarter'),(3,2,'C4','quarter'),(3,3,'D4','quarter'),(3,4,'E4','quarter'),
                (4,1,'E4','quarter',1),(4,2,'D4','eighth'),(4,3,'D4','half'),(5,1,'E4','quarter'),
                (5,2,'E4','quarter'),(5,3,'F4','quarter'),(5,4,'G4','quarter'),(6,1,'G4','quarter'),
                (6,2,'F4','quarter'),(6,3,'E4','quarter'),(6,4,'D4','quarter'),(7,1,'C4','quarter'),
                (7,2,'C4','quarter'),(7,3,'D4','quarter'),(7,4,'E4','quarter'),(8,1,'D4','quarter',1),
                (8,2,'C4','eighth'),(8,3,'C4','half'),
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
                (1,1,'E4','quarter'),(1,2,'E4','quarter'),(1,3,'E4','half'),(2,1,'E4','quarter'),
                (2,2,'E4','quarter'),(2,3,'E4','half'),(3,1,'E4','quarter'),(3,2,'G4','quarter'),
                (3,3,'C4','quarter'),(3,4,'D4','quarter'),(4,1,'E4','whole'),(5,1,'F4','quarter'),
                (5,2,'F4','quarter'),(5,3,'F4','quarter'),(5,4,'F4','quarter'),(6,1,'F4','quarter'),
                (6,2,'E4','quarter'),(6,3,'E4','quarter'),(6,4,'E4','quarter'),(7,1,'E4','quarter'),
                (7,2,'D4','quarter'),(7,3,'D4','quarter'),(7,4,'E4','quarter'),(8,1,'D4','half'),
                (8,2,'G4','half'),
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

