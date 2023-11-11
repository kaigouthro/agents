# -*- coding: utf-8 -*-
import copy
import time
import re
from tree import construct_tree, tree2xml, tree2dict
import json

def extract_tag_names(text):

    pattern = r'<([^<>]+)>'


    matches = re.findall(pattern, text)


    stack = []
    answer = []
    for item in matches:
        if item[0] != '/':
            stack.append(item)
        elif item[1:] in stack:
            while stack[-1] != item[1:]:
                stack.pop()
            answer.append(stack.pop())
    return answer

def print_log(message: str):
    print(f"[{time.ctime()}] {message}")

def simulation():
    content = ""
    content = f"{content} hello"
    return {
        'id': 'chatcmpl-6p9XYPYSTTRi0xEviKjjilqrWU2Ve',
        'object': 'chat.completion',
        'created': 1677649420,
        'model': 'gpt-3.5-turbo',
        'usage': {'prompt_tokens': 56, 'completion_tokens': 31, 'total_tokens': 87},
        'choices': [
            {
                'message': {
                    'role': 'assistant',
                    'content': content
                },
                'finish_reason': 'stop',
                'index': 0
            }
        ]
    }

def new_parse(content:str, labels: list, return_dict:bool=False):

    tree = construct_tree(content, add_root_label=True)
    tree.first_label = False
    if not labels or labels is None:
        return (
            tree2dict(tree)['root']
            if return_dict
            else "\n".join(tree2xml(tree).split('\n')[1:-1])
        )
    if return_dict:
        return tree2dict(tree, filter=labels, mode="remain")['root']
    tree_xml = tree2xml(tree, filter=labels, mode="remain")
    return "\n".join(tree_xml.split('\n')[1:-1])

