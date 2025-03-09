#!/usr/bin/env python3
import os

def handler(args):
    if os.path.isfile(args.log_path):
        # Use the Darshan handler.
        from handle_darshan import handler as darshan_handler
        return darshan_handler() or {}
    elif os.path.isdir(args.log_path):
        tau_trace = os.path.join(args.log_path, "traces.otf2")
        if os.path.exists(tau_trace):
            # Use the TAU handler.
            from handle_tau import handler as tau_handler
            return tau_handler() or {}
        else:
            # Use the Recorder handler.
            from handle_recorder import handler as recorder_handler
            return recorder_handler() or {}
    else:
        print("Invalid log path provided. Must be either a file or a directory.")
        return {}
