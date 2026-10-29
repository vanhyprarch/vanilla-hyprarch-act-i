# SPDX-License-Identifier: GPL-2.0-only
"""Non-exclusive Home navigation. Never opens keyboard or mouse devices."""
import asyncio
import json
import sys
import time

import evdev
import pyudev

E = evdev.ecodes


class Navigation:
    """Per-controller input state, independently testable without hardware."""

    def __init__(self, vendor, ranges):
        self.confirm = E.BTN_EAST if vendor == 0x057E else E.BTN_SOUTH
        self.back = E.BTN_SOUTH if vendor == 0x057E else E.BTN_EAST
        self.ranges = ranges
        self.axes = {}
        self.raw_axes = {}
        self.pressed = set()
        self.home_since = None
        self.home_fired = False
        self.focused = False
        self.direction = 0
        self.next_repeat = None

    def set_focus(self, focused):
        self.focused = focused
        # A held stick must return to neutral before it can navigate on re-entry.
        self.next_repeat = None

    def axis_direction(self, code, value):
        if code in (E.ABS_HAT0X, E.ABS_HAT0Y):
            return (value > 0) - (value < 0)
        minimum, maximum = self.ranges.get(code, (-32767, 32767))
        center = (minimum + maximum) / 2
        radius = (maximum - minimum) / 2
        if radius <= 0 or abs(value - center) < radius * 0.35:
            return 0
        return 1 if value > center else -1

    def feed(self, event_type, code, value, now):
        if event_type == E.EV_KEY:
            was_pressed = code in self.pressed
            if code == E.BTN_MODE:
                if value == 1 and not was_pressed:
                    self.home_since = now
                    self.home_fired = False
                elif value == 0:
                    self.home_since = None
                    self.home_fired = False
            if value == 0:
                self.pressed.discard(code)
            elif value == 1:
                self.pressed.add(code)
                if self.focused and not was_pressed and E.BTN_MODE not in self.pressed:
                    if code == self.confirm:
                        return "select"
                    if code == self.back:
                        return "back"
            return None
        if event_type == E.EV_ABS:
            self.raw_axes[code] = value
        if event_type != E.EV_ABS or code not in (E.ABS_X, E.ABS_Y, E.ABS_HAT0X, E.ABS_HAT0Y):
            return None
        self.axes[code] = self.axis_direction(code, value)
        direction = next((self.axes.get(c, 0) for c in
                          (E.ABS_HAT0X, E.ABS_HAT0Y, E.ABS_X, E.ABS_Y)
                          if self.axes.get(c, 0)), 0)
        if direction == self.direction:
            return None
        self.direction = direction
        self.next_repeat = None
        if E.BTN_MODE in self.pressed:
            if code == E.ABS_HAT0X and value and not self.home_fired:
                self.home_fired = True
                return "app-next" if value > 0 else "app-previous"
            return None
        if self.focused and direction:
            self.next_repeat = now + 0.4
            return "next" if direction > 0 else "previous"
        return None

    def repeat(self, now):
        if self.home_since is not None and not self.home_fired and now - self.home_since >= 5:
            self.home_fired = True
            return "home"
        if E.BTN_MODE in self.pressed:
            return None
        if not self.focused or self.next_repeat is None or now < self.next_repeat:
            return None
        self.next_repeat = now + 0.16
        return "next" if self.direction > 0 else "previous"


    @property
    def neutral(self):
        return not self.pressed and not any(
            self.axis_direction(code, value) for code, value in self.raw_axes.items()
            if code in (E.ABS_X, E.ABS_Y, E.ABS_RX, E.ABS_RY, E.ABS_HAT0X, E.ABS_HAT0Y))


class Gamepads:
    def __init__(self, input_route=None):
        self.context = pyudev.Context()
        self.devices = {}
        self.focused = False
        self.stopping = False
        self.tasks = set()
        self.last_routing = None
        self.input_route = input_route
        self.routing_queue = asyncio.Queue(maxsize=1)

    @staticmethod
    def emit(message):
        print(json.dumps(message), flush=True)

    def action(self, action):
        if action:
            self.emit({"type": "action", "action": action})

    def routing(self):
        pads = [nav for _, nav in self.devices.values()]
        state = (any(E.BTN_MODE in pad.pressed for pad in pads), all(pad.neutral for pad in pads))
        if state != self.last_routing:
            self.last_routing = state
            if self.routing_queue.full():
                self.routing_queue.get_nowait()
            self.routing_queue.put_nowait(state)

    def scan(self):
        if self.stopping:
            return
        paths = {d.device_node for d in self.context.list_devices(subsystem="input")
                 if d.device_node and d.device_node.rsplit("/", 1)[-1].startswith("event")
                 and d.properties.get("ID_INPUT_JOYSTICK") == "1"}
        for path in paths - self.devices.keys():
            try:
                device = evdev.InputDevice(path)
                capabilities = device.capabilities()
                if E.EV_ABS not in capabilities or E.EV_KEY not in capabilities:
                    device.close()
                    continue
                ranges = {code: (info.min, info.max) for code, info in capabilities[E.EV_ABS]}
                navigation = Navigation(device.info.vendor, ranges)
                # Seed current axes so a held control cannot fire on focus entry.
                for code in (E.ABS_X, E.ABS_Y, E.ABS_RX, E.ABS_RY, E.ABS_HAT0X, E.ABS_HAT0Y):
                    info = device.absinfo(code) if code in ranges else None
                    if info is not None:
                        navigation.feed(E.EV_ABS, code, info.value, time.monotonic())
                navigation.pressed.update(device.active_keys())
                navigation.set_focus(self.focused)
                self.devices[path] = (device, navigation)
                task = asyncio.create_task(self.read(path, device, navigation))
                self.tasks.add(task)
                task.add_done_callback(self.tasks.discard)
            except OSError as error:
                print(f"Gamepad unavailable: {path}: {error.strerror}", file=sys.stderr, flush=True)
        self.emit({"type": "devices", "count": len(self.devices)})
        self.routing()

    async def read(self, path, device, navigation):
        try:
            async for event in device.async_read_loop():
                if event.type == E.EV_SYN and event.code == E.SYN_DROPPED:
                    raise OSError("Input stream lost synchronization")
                action = navigation.feed(event.type, event.code, event.value, time.monotonic())
                self.routing()
                self.action(action)
        except OSError:
            pass
        finally:
            self.devices.pop(path, None)
            device.close()
            self.routing()
            self.emit({"type": "devices", "count": len(self.devices)})
            if not self.stopping:
                asyncio.get_running_loop().call_later(1, self.scan)

    async def repeat(self):
        while True:
            for _, navigation in tuple(self.devices.values()):
                self.action(navigation.repeat(time.monotonic()))
            await asyncio.sleep(0.04)

    async def route_input(self):
        while True:
            reserved, neutral = await self.routing_queue.get()
            if self.input_route is not None:
                await asyncio.to_thread(self.input_route, reserved, neutral)

    async def run(self):
        loop = asyncio.get_running_loop()
        monitor = pyudev.Monitor.from_netlink(self.context)
        monitor.filter_by(subsystem="input")
        monitor.start()

        def hotplug():
            while monitor.poll(timeout=0) is not None:
                pass
            self.scan()

        loop.add_reader(monitor.fileno(), hotplug)
        reader = asyncio.StreamReader(limit=1024)
        transport, _ = await loop.connect_read_pipe(lambda: asyncio.StreamReaderProtocol(reader), sys.stdin)
        self.scan()
        repeat_task = asyncio.create_task(self.repeat())
        route_task = asyncio.create_task(self.route_input())
        try:
            while line := await reader.readline():
                try:
                    message = json.loads(line)
                    focused = message.get("focused")
                    if message.get("type") != "focus" or type(focused) is not bool:
                        continue
                except (ValueError, AttributeError):
                    continue
                if focused != self.focused:
                    self.focused = focused
                    for _, navigation in self.devices.values():
                        navigation.set_focus(focused)
        finally:
            self.stopping = True
            loop.remove_reader(monitor.fileno())
            transport.close()
            repeat_task.cancel()
            route_task.cancel()
            for task in tuple(self.tasks):
                task.cancel()
            await asyncio.gather(repeat_task, route_task, *self.tasks, return_exceptions=True)


def main():
    try:
        from adapters.catalog import load_catalog
        from adapters.jellyfin import route_input
        app = load_catalog()["jellyfin"]
        asyncio.run(Gamepads(lambda reserved, neutral:
            route_input(app.flatpak_id, reserved, neutral)).run())
    except (BrokenPipeError, KeyboardInterrupt):
        pass
