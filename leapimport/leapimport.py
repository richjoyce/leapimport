# -*- coding: utf-8 -*-
import Leap
import struct
import ctypes

# Need to call this before running any Leap functions
Leap.Controller()

def leap_frames(filename):
    """List generator of `Leap.Frame` from raw LeapMotion binary file."""
    with open(filename, 'rb') as file_:
        frame_size_data = file_.read(4)
        while frame_size_data:
            frame_size = struct.unpack('i', frame_size_data)[0]
            frame_data = Leap.byte_array(frame_size)
            frame_data_ptr = frame_data.cast().__long__()
            ctypes.memmove(frame_data_ptr, file_.read(frame_size), frame_size)
            frame = Leap.Frame()
            frame.deserialize((frame_data, frame_size))
            frame_size_data = file_.read(4)
            yield frame

def leap_frames_to_hand_dataframe(filename, fingers=[0, 1, 2, 3, 4], palm=True):
    """
    Convert binary LeapMotion data from `filename` to a dataframe with
    palm and fingertip information from each LeapMotion frame. Columns are:
    `timestamp, confidence, id, type, palm_x, palm_y, ...`

    One row corresponds to one hand, so frames with multiple hands will
    have multiple rows.

    frames: list of `Leap.Frame`
    fingers: list of  `Leap.Finger` types to parse, defaults to all.
    palm: include palm or not
    """
    import pandas as pd
    import collections
    hand_data = collections.defaultdict(list)
    # this array is accessed using the finger.type attribute which translates from 0-4
    type_to_string = [ 'thumb', 'index', 'middle', 'ring', 'pinky' ]

    for frame in leap_frames(filename):
        frame_processed_hands = []
        for hand in frame.hands:
            if hand.id in frame_processed_hands:
                continue
            if palm:
                hand_data['palm_x'].append(hand.palm_position.x)
                hand_data['palm_y'].append(hand.palm_position.y)
                hand_data['palm_z'].append(hand.palm_position.z)
            for finger_type in fingers:
                finger = hand.fingers.finger_type(finger_type)[0]
                hand_data[type_to_string[finger.type]+'_x'].append(finger.tip_position.x)
                hand_data[type_to_string[finger.type]+'_y'].append(finger.tip_position.y)
                hand_data[type_to_string[finger.type]+'_z'].append(finger.tip_position.z)
            hand_data['timestamp'].append(frame.timestamp)
            hand_data['confidence'].append(hand.confidence)
            hand_data['id'].append(hand.id)
            hand_data['type'].append("right" if hand.is_right else "left")
            frame_processed_hands.append(hand.id)
    return pd.DataFrame.from_dict(hand_data)
