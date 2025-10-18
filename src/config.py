import os

import numpy as np
from ok import ConfigOption

version = "dev"


key_config_option = ConfigOption(
    "Game Settings",
    {
        "Game Language": "Chinese",
    },
    description="Game settings",
    config_type={
        "Game Language": {
            "type": "drop_down",
            "options": ["Chinese", "English"],
        }
    },
)


config = {
    'debug': False,  # Optional, default: False
    'use_gui': True,
    'config_folder': 'configs',
    'global_configs': [key_config_option],
    'gui_icon': 'icons/icon.png',
    'wait_until_before_delay': 0,
    'wait_until_check_delay': 0,
    'wait_until_settle_time': 0.2,
    'ocr': {
        'lib': 'onnxocr',
        'params': {
            'use_openvino': True,
        }
    },
    'windows': {  # required when supporting windows game
        'exe': ['Star.exe', 'BPSR.exe', 'BPSR_STEAM.exe'],
        # 'hwnd_class': 'UnrealWindow', # Increases duplicate name check accuracy
        'interaction': 'Pynput',
        'can_bit_blt': True,  # default false, opengl games do not support bit_blt
        'bit_blt_render_full': True,
        'check_hdr': False, # Warns user when AutoHDR is enabled, but does not prevent usage
        'force_no_hdr': False, # True = prevents usage when user has AutoHDR enabled
        'require_bg': True # Requires background screenshot
    },
    'start_timeout': 60,  # default 60
    'window_size': { # ok-script window size
        'width': 1200,
        'height': 800,
        'min_width': 600,
        'min_height': 450,
    },
    'supported_resolution': {
        'ratio': '16:9', # Supported game resolution
        'min_size': (1280, 720), # Minimum supported game resolution
        'resize_to': [(2560, 1440), (1920, 1080), (1600, 900), (1280, 720)], # If not 16:9, automatically rescale to resize_to
    },
    'analytics': {
        # 'report_url': 'http://report.ok-script.cn:8080/report', # Report daily active users, optional
    },
    'links': {
            'default': {
                'github': 'https://github.com/sanheiii/ok-star-resonance',
            }
        },
    'screenshots_folder': "screenshots", # Screenshot storage directory, cleared on each restart
    'gui_title': 'ok-star-resonance',  # Optional
    'template_matching': {
        'coco_feature_json': os.path.join('assets', 'result.json'), # COCO format annotation, requires PNG images. After running in debug mode, will crop images to keep only annotated parts to reduce image size
        'default_horizontal_variance': 0.002, # Default x offset, when searching without passing box, will offset box based on COCO coordinates and match
        'default_vertical_variance': 0.002, # Default y offset
        'default_threshold': 0.8, # Default threshold
    },
    'version': version, # Version
    'my_app': ['src.globals', 'Globals'], # Global singleton object, can store loaded models, call using og.my_app
    'onetime_tasks': [  # tasks to execute
        ["ok", "DiagnosisTask"],
    ],
    'trigger_tasks':[
        ["src.tasks.FishingTask", "FishingTask"],
        ["src.tasks.PickPassTask", "PickPassTask"],
        ["src.tasks.GatherTask", "GatherTask"]
    ]
}