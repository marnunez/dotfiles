#!/bin/python3
import bluetooth, subprocess, argparse, time
from parse import search


def scan_til_found(mac, timeout=10):
    res = " "
    while mac not in res:

        r = subprocess.run(
            ["bluetoothctl", "--timeout", str(timeout), "scan", "on",],
            check=True,
            capture_output=True,
        )
        res = str(r.stdout)
    return


def icon(mac):
    if status(mac)["connected"]:
        return ""
    else:
        return r"%{F#f00}%{F-}"


def status(mac):
    stat = {}
    res = subprocess.run(["bluetoothctl", "info", mac], capture_output=True)
    if res.returncode and "not available" in str(res.stdout):
        stat["found"] = stat["paired"] = stat["connected"] = False
    else:
        stat["found"] = True
        stat["paired"] = True if "Paired: yes" in str(res.stdout) else False
        stat["connected"] = True if "Connected: yes" in str(res.stdout) else False
        # print(str(res.stdout).splitlines())
        stat["name"] = search("\tName: {}\n", res.stdout.decode("UTF-8"))[0]
    return stat


def set_default_sink(code):
    sink = f"bluez_sink.{code.upper().replace(':','_')}.a2dp_sink"
    return subprocess.run(["pacmd", "set-default-sink", sink], check=True).returncode


def command(comm, mac):
    return subprocess.run(["bluetoothctl", comm, mac], check=True).returncode


def reconnect(code):
    if status(code)["found"]:
        command("remove", code)
    subprocess.run(["dunstify", "Put headphones on paring mode"])
    scan_til_found(code)
    command("pair", code)
    command("trust", code)
    command("connect", code)
    subprocess.run(["dunstify", f"Connected to {status(code)['name']}"])
    time.sleep(2)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--icon", help="return icon", action="store_true")
    parser.add_argument("-r", "--reconnect", help="reconnect", action="store_true")
    parser.add_argument(
        "-t", "--toggle", help="toggle connection state", action="store_true"
    )
    parser.add_argument("code")
    args = parser.parse_args()
    if args.icon:
        print(icon(args.code))
    elif args.reconnect:
        reconnect(args.code)
        set_default_sink(args.code)
        print(icon(args.code))
    elif args.toggle:
        if status(args.code)["connected"]:
            command("disconnect", args.code)
        else:
            command("connect", args.code)
            set_default_sink(args.code)
        print(icon(args.code))
