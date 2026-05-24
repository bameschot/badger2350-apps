# Badger 2350 — Repository Documentation

A MicroPython firmware framework for the [Pimoroni Badger 2350](https://shop.pimoroni.com/products/badger-2350) e-paper badge, built on the RP2350 microcontroller.

---

## Table of Contents

- [Repository Structure](#repository-structure)
- [board/](#board)
- [ci/](#ci)
- [examples/](#examples)
- [firmware/](#firmware)
  - [firmware/apps/](#firmwareapps)
  - [firmware/assets/](#firmwareassets)
  - [firmware/main.py](#firmwaremainpy)
  - [firmware/secrets.py](#firmwaresecretspy)
- [modules/](#modules)
  - [modules/c/](#modulesc)
  - [modules/common/](#modulescommon)
  - [modules/python/](#modulespython)
- [romfs/](#romfs)
- [Badgeware API Specification](#badgeware-api-specification)

---

## Repository Structure

```
badger2350/
├── board/              Board definition files (CMake, C headers, pin maps)
├── ci/                 CI scripts and tooling configuration
├── examples/           Minimal example sketches
├── firmware/           Default apps and assets flashed onto the device
│   ├── apps/           Individual app directories
│   └── assets/         Shared fonts, icons, and sprites
├── modules/            MicroPython modules frozen into the firmware
│   ├── c/              C/C++ native modules
│   ├── common/         Python modules available to all apps
│   └── python/         Python-only utility modules
└── romfs/              Read-only ROM filesystem (fonts)
```

---

## board/

Board definition for MicroPython build system.

| File | Description |
|------|-------------|
| `filesystem.cmake` | CMake rules for embedding the ROM filesystem |
| `manifest.py` | MicroPython frozen module manifest |
| `mpconfigboard.cmake` | Board-level CMake configuration |
| `mpconfigboard.h` | C-level MicroPython board configuration macros |
| `pimoroni_badger2350.h` | Hardware-specific pin and peripheral definitions |
| `pins.csv` | Pin-name-to-GPIO mapping table |
| `usermodules.cmake` | CMake includes for user C modules |

---

## ci/

Continuous integration helpers.

| File | Description |
|------|-------------|
| `micropython.sh` | Builds the MicroPython firmware image |
| `python.sh` | Runs Python linting via ruff |
| `ruff.toml` | Ruff linter configuration |
| `pico-sdk-crt0-startup-rosc.patch` | Patch applied to the Pico SDK crt0 startup for ROSC use |

---

## examples/

| File | Description |
|------|-------------|
| `main.py` | Placeholder/starter template for custom apps |

---

## firmware/

### firmware/apps/

Each app lives in its own directory and must contain at least `__init__.py` and `icon.png`.

#### badge/
Personal ID-card display app.

| File | Description |
|------|-------------|
| `__init__.py` | Main app logic; renders front/rear ID card, handles button input |
| `avatar.png` | Default avatar image |
| `icon.png` | Menu icon |
| `assets/socials/` | PNG icons for 35+ social network platforms |

#### clock/
Multi-style clock app with NTP sync.

| File | Description |
|------|-------------|
| `__init__.py` | Main app loop; dispatches to one of four clock renderers |
| `daylightsaving.py` | `DaylightSavingPolicy` and `DaylightSaving` classes for DST calculation |
| `usermessage.py` | Helper functions `user_message()`, `center_text()`, `stretch_text()` |
| `icon.png` | Menu icon |
| `assets/` | Sprite sheets and backgrounds for each clock style |

#### gallery/
Image gallery viewer.

| File | Description |
|------|-------------|
| `__init__.py` | App entry point |
| `ui.py` | Gallery UI rendering |
| `icon.png` | Menu icon |
| `images/` | Sample image files |

#### hydrate/
Hydration reminder app.

| File | Description |
|------|-------------|
| `__init__.py` | App entry point |
| `icon.png` | Menu icon |

#### list/
Scrollable checklist app.

| File | Description |
|------|-------------|
| `__init__.py` | App entry point |
| `icon.png` | Menu icon |
| `avatar.png` | Avatar image |
| `assets/` | Arrow and checkbox/cross UI icons |

#### mass_storage/
Mounts the badge as a USB mass storage device.

| File | Description |
|------|-------------|
| `__init__.py` | Triggers USB MSC mode |
| `icon.png` | Menu icon |

#### menu/
System launcher / home screen.

| File | Description |
|------|-------------|
| `__init__.py` | Menu entry point; loads installed apps, handles navigation and launch |
| `app.py` | `App` and `Apps` classes — icon loading, grid layout, activation |
| `ui.py` | Draws background, header, and decorative elements |

#### the_compendium/
Raycasting dungeon-crawler game.

| File | Description |
|------|-------------|
| `__init__.py` | Game entry point |
| `behaviours.py` | Enemy AI behaviour definitions |
| `cutscene.py` | Cutscene rendering |
| `dialogue.py` | Dialogue system |
| `level.py` | Level data and management |
| `monster.py` | Monster definitions |
| `raycaster.py` | Software raycaster renderer |
| `ui.py` | HUD and inventory rendering |
| `assets/` | Background, character, and UI sprites |

#### weather/
Weather forecast display.

| File | Description |
|------|-------------|
| `__init__.py` | App entry point; fetches and displays weather data |
| `ui.py` | Weather UI rendering |
| `icon.png` | Menu icon |
| `assets/` | Weather condition icons (cloud, rainy, snowy, sunny, thunderstorm) |

---

### firmware/assets/

| Path | Description |
|------|-------------|
| `fonts/*.ppf` | Pixel-font files (pimoroni pixel font format) |
| `fonts/*.af` | Anti-aliased vector font files (DynaPuff, IndieFlower, MonaSans) |
| `icons.png` | Shared system icon sprite sheet |
| `mona-sprites/` | Mona mascot animation frames (code, dance, dead, eating, heart, love, notify) |

---

### firmware/main.py

System launcher script. Reads the `menu` state to determine which app was last running, validates that the app still exists, then calls `launch(app)`. After the app exits, resets state to the menu and calls `reset()`.

---

### firmware/secrets.py

Template for user WiFi credentials. Loaded by `modules/common/secrets.py`. Must define `WIFI_SSID`, `WIFI_PASSWORD`, and optionally `REGION` and `TIMEZONE`.

---

## modules/

### modules/c/

Native C/C++ MicroPython modules compiled into the firmware.

| Module | Description |
|--------|-------------|
| `jpegdec/` | JPEG decoder (JPEGDEC library) |
| `picovector/` | 2D vector graphics engine — shapes, fonts, images, brushes, rasteriser |
| `pngdec/` | PNG decoder (PNGdec + zlib) |
| `powman/` | RP2350 power management: dormant sleep, wake reasons, wake buttons |
| `ssd1680/` | SSD1680 e-paper display driver |

---

### modules/common/

Python modules available to all apps, loaded by `boot.py` before any app runs.

| File | Description |
|------|-------------|
| `badgeware/` | Core badge framework — see [Badgeware API Specification](#badgeware-api-specification) |
| `board.py` | Imports all `machine.Pin.board.*` names into local scope |
| `boot.py` | Boot entry point: switches C++ allocator to MicroPython heap, imports `badgeware` |
| `easing.py` | 24 easing functions for animations (quad, cubic, quart, quint, sine, expo, circ, back, elastic, bounce) |
| `lsm6ds3.py` | Driver for the LSM6DS3 IMU (accelerometer + gyroscope + pedometer + tap detection) |
| `main.py` | Handles double-tap MSC boot, filesystem checks, and delegates to `/system/main` |
| `pimoroni.py` | Hardware utility classes: `Analog`, `AnalogMux`, `Button`, `RGBLED`, `PID`, `Buzzer`, `ShiftRegister`, `PWMLED` |
| `qwstpad.py` | Driver for the QwSTPad I2C game controller (10 buttons, 4 LEDs) |
| `secrets.py` | Secrets loader; imports from `/secrets.py` or `/system/secrets.py` and exposes `require()` |
| `wifi.py` | WiFi connection management with retry logic |

---

### modules/python/

| File | Description |
|------|-------------|
| `_msc.py` | Activates USB Mass Storage mode |
| `hardware_test.py` | Hardware self-test routine |

---

## romfs/

Read-only filesystem mounted at `/rom/fonts/`. Contains `.ppf` pixel-font files for all system fonts, including the two `badgeware`-specific fonts (`badgeware.ppf`, `badgewaremax.ppf`). Fonts are accessible via `rom_font.<name>`.

---

---

# Badgeware API Specification

The `badgeware` package (`modules/common/badgeware/`) is the core application framework. All symbols it exports are hoisted into `builtins` and are therefore available globally in every app without explicit imports.

---

## Module: `badgeware` (`__init__.py`)

Initialises the display, picovector, and all sub-modules. Exports the following global symbols and functions to `builtins`.

### Global Constants

Exposed via `picovector` bindings or set directly:

| Constant | Value | Description |
|----------|-------|-------------|
| `LORES` | `0b00` | Low-resolution display mode |
| `HIRES` | `0b01` | High-resolution display mode |
| `VSYNC` | `0b10` | VSync-enabled display mode |
| `FAST_UPDATE` | `3 << 4` | Fast e-paper partial refresh |
| `FULL_UPDATE` | `0 << 4` | Full e-paper refresh (clears ghosting) |
| `MEDIUM_UPDATE` | `2 << 4` | Medium-speed e-paper refresh |
| `DITHER` | `1 << 8` | Enable dithering on display update |
| `NON_BLOCKING` | `1 << 9` | Non-blocking display update mode |
| `OFF` | `image.OFF` | Anti-aliasing off |
| `X2` | `image.X2` | 2× anti-aliasing |
| `X4` | `image.X4` | 4× anti-aliasing |

Button pin references (`BUTTON_A`, `BUTTON_B`, `BUTTON_C`, `BUTTON_UP`, `BUTTON_DOWN`, `BUTTON_HOME`) are set in `badge.py` and exposed as `builtins`.

---

### `set_brightness(value)`

No-op stub. Brightness control is not implemented on the Badger hardware.

**Parameters:**
- `value` — ignored

---

### `reset()`

Safely resets the device. Waits until all buttons are released before calling `machine.reset()` to avoid accidentally entering bootloader mode via the HOME/BOOT button.

---

### `class _run`

Loop runner returned as `builtins.run`. Manages the main update loop for an app.

#### `_run(update, duration=None)`

Instantiating with a callable immediately invokes it as the loop function.

**Parameters:**
- `update` — callable called once per frame; return a non-`None` value to exit the loop
- `duration` — optional maximum duration in milliseconds

#### `_run.ticks` *(property)*

Returns milliseconds elapsed since the loop started.

#### `_run.progress` *(property)*

Returns a `float` in `[0.0, 1.0]` representing elapsed time as a fraction of `duration`. Returns `0` if `duration` is `None`.

#### `_run.__call__(update)`

Starts the loop. Calls `badge.poll()` once, then calls `update()` in a tight loop until `update()` returns non-`None` or `duration` is exceeded. Exceptions are caught and displayed via `fatal_error()`. Nested loops are supported via `builtins.loop` stack.

---

### `wait_for_button_or_alarm(timeout=30_000)`

Blocks until a button is pressed, an RTC alarm fires, or the timeout expires with USB disconnected (in which case the badge is put to sleep).

**Parameters:**
- `timeout` — milliseconds before sleeping; `None` disables the sleep timeout

---

### `clear_running()`

Resets the `menu` state so the next boot launches the menu app instead of the previously running app. Also clears the RTC alarm.

---

### `launch(path)`

Loads and runs an app from the given path. Sets up the HOME button interrupt to quit to the launcher. Cleans up `sys.path` and `sys.modules` after the app exits.

**Parameters:**
- `path` — absolute path string, e.g. `"/system/apps/clock"`

**Returns:** the return value of the app's `on_exit()` function, or `None`.

Calls `on_exit()` on the app module if defined, then garbage collects.

---

### `get_exception(e)`

Formats an exception into a traceback string (excluding the "Traceback" header line).

**Parameters:**
- `e` — exception object

**Returns:** `str`

---

### `message(title, msg, window=None)`

Renders a modal dialog box on screen with a title bar, drop shadow, body text, and an "Okay" button label. Does **not** call `display.update()`.

**Parameters:**
- `title` — `str` shown in the title bar
- `msg` — `str` body text, rendered via `text.draw()`
- `window` — optional `image` window; defaults to a full-screen window

---

### `fatal_error(title, error)`

Renders a `message()` dialog, flushes the display, waits for a button press, deletes the `menu` state, then reboots.

**Parameters:**
- `title` — `str` dialog title
- `error` — `str` or exception object

---

## Module: `badgeware.badge` → `builtins.badge`

Instantiates and exposes a single `Badge` instance as `builtins.badge`.

### Constants (set on `builtins`)

| Constant | Description |
|----------|-------------|
| `BUTTON_A` | `machine.Pin.board.BUTTON_A` |
| `BUTTON_B` | `machine.Pin.board.BUTTON_B` |
| `BUTTON_C` | `machine.Pin.board.BUTTON_C` |
| `BUTTON_UP` | `machine.Pin.board.BUTTON_UP` |
| `BUTTON_DOWN` | `machine.Pin.board.BUTTON_DOWN` |
| `BUTTON_HOME` | `machine.Pin.board.BUTTON_HOME` |

---

### `class Badge`

#### `Badge.__init__()`

Initialises default pen/clear colours based on model, sets up four case-light PWM channels at 500 Hz with 0% duty cycle.

---

#### `badge.ticks` *(property → int)*

Milliseconds since the last `badge.poll()` call, sourced from the `_input` native module.

---

#### `badge.ticks_delta` *(property → int)*

Millisecond delta between the last two `badge.poll()` calls.

---

#### `badge.poll()`

Reads all button inputs. Must be called once per frame (or before any `badge.pressed()` / `badge.held()` / `badge.released()` / `badge.changed()` checks) to update internal state.

---

#### `badge.resolution` *(property → tuple[int, int])*

Returns `(screen.width, screen.height)`.

---

#### `badge.clear()`

Fills the screen with `badge.default_clear` colour and resets the pen to `badge.default_pen`.

**Returns:** `True`

---

#### `badge.update()`

Flushes the screen buffer to the display. On the first call (Badger model), performs a full refresh to avoid ghosting; subsequent calls use the user-configured speed. If `DITHER` mode is set, applies dithering before update. Calls `badge.clear()` and `badge.poll()` after updating.

**Returns:** `True`

---

#### `badge.mode(mode=None)`

Gets or sets the display mode.

**Parameters:**
- `mode` — optional bitmask combining `LORES`/`HIRES`, `VSYNC`, `FAST_UPDATE`/`FULL_UPDATE`/`MEDIUM_UPDATE`, `DITHER`, `NON_BLOCKING`. Omit to read the current mode.

**Returns:** `None` when setting; the current mode `int` when reading.

**Side effects:** Configures the SSD1680 blocking/speed settings (Badger) or display resolution/vsync (Tufty); recreates `builtins.screen` as an `image` backed by the display buffer when needed.

---

#### `badge.battery_voltage()` → `float`

Returns the battery voltage in volts, averaged over 10 ADC samples and corrected against the internal 1.1 V reference.

---

#### `badge.usb_connected()` → `bool`

Returns `True` if a USB cable is connected (VBUS detected).

---

#### `badge.battery_level()` → `int`

Returns estimated battery percentage `[0, 100]` using a non-linear curve derived from battery voltage.

---

#### `badge.is_charging()` → `bool`

Returns `True` if a USB cable is connected and the battery is charging (CHARGE_STAT pin low).

---

#### `badge.disk_free(mountpoint="/system")` → `tuple[int, int, int]`

Returns `(total_bytes, used_bytes, free_bytes)` for the given filesystem mountpoint.

**Parameters:**
- `mountpoint` — filesystem path string, default `"/system"`

---

#### `badge.light_level()` → `int`

Returns raw u16 ADC reading from the light sensor. Only available on the Tufty model; raises `RuntimeError` on Badger/Blinky.

---

#### `badge.pressed(button=None)` → `bool | set`

**Parameters:**
- `button` — a `Pin` constant (e.g. `BUTTON_A`). If `None`, returns the full set of currently-pressed buttons.

**Returns:** `True` if the specified button was just pressed this frame; the set of all pressed buttons if no argument given.

---

#### `badge.held(button=None)` → `bool | set`

Same as `badge.pressed()` but for held (long-press) buttons.

---

#### `badge.released(button=None)` → `bool | set`

Same as `badge.pressed()` but for buttons released this frame.

---

#### `badge.changed(button=None)` → `bool | set`

Same as `badge.pressed()` but for any change in button state (press or release).

---

#### `badge.caselights(*args)` → `list[float]`

Gets or sets the four rear case-light brightness values.

**Parameters:**
- No args — returns current `[float, float, float, float]` brightness values `[0.0, 1.0]`
- One `float` — sets all four lights to the same brightness
- Four `float` values — sets each light individually

Applies gamma correction (exponent 2.2) before writing to the PWM duty cycle.

**Returns:** list of four brightness floats.

---

#### `badge.sleep(duration=None)`

Puts the device into deep sleep.

**Parameters:**
- `duration` — optional sleep duration in milliseconds. If `None`, sleeps indefinitely until a button wakes it.

Calls `powman.goto_dormant_for(duration)` or `powman.sleep()`.

---

#### `badge.wake_reason()` → `int`

Returns the wake reason code from `powman.get_wake_reason()`. Compare against `powman.WAKE_BUTTON_A`, `powman.WAKE_BUTTON_B`, etc.

---

#### `badge.woken_by_button()` → `bool`

Returns `True` if the device was woken from sleep by any of the five face/directional buttons.

---

#### `badge.pressed_to_wake(button)` → `bool`

Returns `True` if the specified button was the one that woke the device from sleep.

**Parameters:**
- `button` — a `Pin` constant

---

#### `badge.woken_by_reset()` → `bool`

Returns `True` if the device was woken by a reset event (`powman.get_wake_reason() == 255`).

---

## Module: `badgeware.filesystem`

Exports to `builtins`.

### `file_exists(path)` → `bool`

Returns `True` if a file or directory exists at `path`. Uses `os.stat()` internally; catches `OSError` for missing paths.

**Parameters:**
- `path` — filesystem path string

---

### `is_dir(path)` → `bool`

Returns `True` if `path` exists and is a directory (checks `stat` flags bit `0x4000`).

**Parameters:**
- `path` — filesystem path string

---

## Module: `badgeware.math`

Exports to `builtins`.

### `clamp(v, vmin, vmax)` → `number`

Returns `v` clamped to the range `[vmin, vmax]`.

**Parameters:**
- `v` — value to clamp
- `vmin` — minimum bound
- `vmax` — maximum bound

---

### `rnd(v1, v2=None)` → `int`

Returns a random integer.

**Parameters:**
- `rnd(n)` — random integer in `[0, n]`
- `rnd(a, b)` — random integer in `[a, b]`

---

### `frnd(v1, v2=None)` → `float`

Returns a random float.

**Parameters:**
- `frnd(n)` — random float in `[0.0, n]`
- `frnd(a, b)` — random float in `[a, b]`

---

## Module: `badgeware.memory`

Exports to `builtins`.

### `free(message="")` → `None`

Prints current free heap in kilobytes, plus the delta since the last call to `free()`. Forces a GC collect before measuring. Intended for debugging.

**Parameters:**
- `message` — optional prefix label for the output line

**Output example:** `my_label: 142kb (+12kb)`

---

## Module: `badgeware.rtc` → `builtins.rtc`

Instantiates and exposes an `RTC` instance as `builtins.rtc`. Wraps the `pcf85063a.PCF85063A` hardware RTC. On construction, synchronises MicroPython's software clock from the hardware RTC (or vice versa) if the year is ≥ 2025.

### `class RTC`

#### `rtc.datetime(dt=None)` → `tuple | None`

Gets or sets the hardware RTC date/time.

**Parameters:**
- `dt` — optional 7-tuple `(year, month, day, hour, minute, second, weekday)`. Omit to read.

**Returns:** `tuple` when reading, `None` when setting.

---

#### `rtc.localtime_to_rtc()`

Copies the current MicroPython `time.localtime()` into the hardware RTC.

---

#### `rtc.rtc_to_localtime()`

Reads the hardware RTC and writes it into `machine.RTC()` (the software clock).

---

#### `rtc.time_from_ntp()`

Syncs time from an NTP server using `ntptime.settime()`, then copies it to the hardware RTC via `localtime_to_rtc()`. Deletes the `ntptime` module after use to reclaim memory.

---

#### `rtc.set_timer(ticks, enable_interrupt=True)`

Configures the hardware countdown timer.

**Parameters:**
- `ticks` — timer tick count (unit depends on PCF85063A configuration)
- `enable_interrupt` — whether to enable the timer interrupt pin; default `True`

---

#### `rtc.timer_elapsed()` → `bool`

Returns `True` if the timer flag is set, then clears the flag.

---

#### `rtc.set_alarm(hours=0, minutes=0, seconds=0)`

Sets a one-shot alarm relative to the current time.

**Parameters:**
- `hours` — hours to add to the current time
- `minutes` — minutes to add
- `seconds` — seconds to add

Enables both alarm and timer interrupts, clears existing flags.

---

#### `rtc.clear_alarm()`

Disables the alarm interrupt, clears both alarm and timer flags, and unsets the alarm.

---

#### `rtc.alarm_status()` → `bool`

Returns `True` if the RTC alarm pin is currently asserted (active low: `board.RTC_ALARM.value() == 0`).

---

## Module: `badgeware.sprite`

Exports `SpriteSheet` and `AnimatedSprite` to `builtins`.

### `class SpriteSheet`

A grid-sliced image containing named sprites.

#### `SpriteSheet(file, columns, rows)`

Loads an image file and slices it into a `columns × rows` grid of equal-sized sprites.

**Parameters:**
- `file` — path to the image file
- `columns` — number of columns in the sprite grid
- `rows` — number of rows in the sprite grid

---

#### `SpriteSheet.sprite(x, y)` → `image`

Returns the sprite at grid position `(x, y)` (zero-indexed, column-major).

**Parameters:**
- `x` — column index
- `y` — row index

---

#### `SpriteSheet.animation(x=0, y=0, count=None, horizontal=True)` → `AnimatedSprite`

Creates an `AnimatedSprite` from a sequence of frames in this sheet.

**Parameters:**
- `x` — starting column
- `y` — starting row
- `count` — number of frames; defaults to the full width of the sheet in sprite-widths
- `horizontal` — if `True`, frames advance along columns; if `False`, along rows

---

### `class AnimatedSprite`

A sequence of frames drawn from a `SpriteSheet`.

#### `AnimatedSprite(spritesheet, x, y, count, horizontal=True)`

**Parameters:**
- `spritesheet` — the source `SpriteSheet`
- `x` — starting column
- `y` — starting row
- `count` — number of frames
- `horizontal` — if `True`, frames advance along columns; if `False`, along rows

---

#### `AnimatedSprite.frame(frame_index=0)` → `image`

Returns the `image` for the given frame. `frame_index` is wrapped modulo the total frame count and truncated to `int`.

**Parameters:**
- `frame_index` — frame number (float or int; wraps around)

---

#### `AnimatedSprite.count()` → `int`

Returns the total number of frames in the animation.

---

## Module: `badgeware.state` → `builtins.State`

JSON-based persistent state storage to the filesystem at `/state/<app>.json`.

### `class State`

All methods are `@staticmethod`.

#### `State.load(app, defaults)` → `bool`

Reads `/state/<app>.json` into `defaults` (in-place update). If the file does not exist or is invalid, saves `defaults` as the initial state.

**Parameters:**
- `app` — app name string (used as the filename stem)
- `defaults` — `dict` of default values; modified in-place with loaded data

**Returns:** `True` if state was loaded successfully, `False` if defaults were saved.

---

#### `State.save(app, data)`

Writes `data` to `/state/<app>.json` as JSON. Creates the `/state/` directory if it does not exist.

**Parameters:**
- `app` — app name string
- `data` — JSON-serialisable `dict`

---

#### `State.modify(app, data)`

Loads the existing state for `app`, merges `data` into it (shallow update), then saves it back.

**Parameters:**
- `app` — app name string
- `data` — `dict` of keys to update

---

#### `State.delete(app)`

Deletes `/state/<app>.json`. Silently ignores `OSError` if the file does not exist.

**Parameters:**
- `app` — app name string

---

## Module: `badgeware.text`

Exports `rom_font`, `load_font`, and `text` to `builtins`.

### `builtins.rom_font` — `ROMFonts`

Lazy-loading accessor for fonts stored in `/rom/fonts/`.

#### `rom_font.<name>` → `pixel_font`

Returns (and caches) a `pixel_font` loaded from `/rom/fonts/<name>.ppf`. Raises `AttributeError` if not found.

#### `dir(rom_font)` → `list[str]`

Returns the names of all `.ppf` fonts in `/rom/fonts/`.

---

### `load_font(font_file)` → `font | pixel_font`

Searches for a font by name across several standard paths and both `.af` (vector) and `.ppf` (pixel) extensions. First checks `rom_font` for a ROM-resident font.

**Search paths (in order):**
1. `rom_font.<font_file>` attribute
2. `/rom/fonts/<name>.ppf`
3. `/system/assets/fonts/<name>`
4. `/fonts/<name>`
5. `/assets/<name>`
6. `<name>` (relative)

**Parameters:**
- `font_file` — font name (with or without extension) or full path

**Returns:** `font` for `.af` files, `pixel_font` for `.ppf` files.

**Raises:** `OSError` if the font cannot be found.

---

### `class _text` — `builtins.text`

Static text rendering utilities. All methods are `@staticmethod`.

#### `text.tokenise(image, text, glyph_renderers=None, size=24)` → `list`

Tokenises `text` into a list of `(type, width, data)` tuples suitable for `text.draw()`. Handles words, spaces, line breaks, and inline escape codes of the form `[code:param1,param2]`.

Built-in escape code: `[pen:r,g,b]` — changes the current pen colour.

**Parameters:**
- `image` — target `image` (used for text measurement)
- `text` — source string
- `glyph_renderers` — optional `dict` mapping code names to renderer callables; merged with built-in renderers
- `size` — font size for vector fonts

**Token format:**
- Word: `(1, width_px, "word_string")`
- Space: `(2,)`
- Line break: `(3,)`
- Glyph: `(renderer_fn, width_px, (params...))`

---

#### `text.draw(image, text, bounds=None, line_spacing=1, word_spacing=1, size=24)` → `rect`

Renders wrapped text into an image, optionally clipped to `bounds`. Supports pre-tokenised input.

**Parameters:**
- `image` — target `image` to draw into
- `text` — `str` or pre-tokenised list from `text.tokenise()`
- `bounds` — optional `rect` to constrain rendering; defaults to the full image
- `line_spacing` — multiplier for line height; default `1`
- `word_spacing` — multiplier for inter-word space; default `1`
- `size` — font size for vector fonts

**Returns:** `rect` representing the bounding box of the rendered text.

---

#### `text.scroll(text, font_face=None, font_size=None, target=None, speed=25, gap=None, align="middle")` → `callable`

Returns an `update()` function that, when called repeatedly in a loop, draws horizontally-scrolling text. Designed to be passed to `run()`.

**Parameters:**
- `text` — string to scroll
- `font_face` — font object; defaults to `rom_font.sins`
- `font_size` — required for vector (`font`) faces; ignored for pixel fonts
- `target` — target `image`; defaults to `screen`
- `speed` — scroll speed in pixels per second; default `25`
- `gap` — `int` gap between repetitions; `None` uses the full target width
- `align` — vertical alignment: `"middle"` (default), `"bottom"`, or `int` pixel offset

**Returns:** a no-argument callable that draws one scroll frame and returns a `float` progress value `[0.0, 1.0]`.

---

## Additional Common Modules

### `modules/common/wifi.py`

WiFi connection management. Not exported to builtins; must be imported with `import wifi`.

#### `wifi.connect(ssid=None, psk=None, timeout=60, retries=5)` → `bool`

Initiates a WiFi connection. Reads credentials from `secrets.py` if not provided. Returns `True` if already connected.

**Parameters:**
- `ssid` — network SSID; reads `secrets.WIFI_SSID` if `None`
- `psk` — network password; reads `secrets.WIFI_PASSWORD` if `None`
- `timeout` — seconds before retrying; default `60`
- `retries` — number of retry attempts; default `5`

**Returns:** `True` if immediately connected, `False` if connection is in progress.

---

#### `wifi.tick()` → `bool`

Checks connection progress. Call in a loop until it returns `True`. Handles timeouts and errors, retrying as configured. Calls `fatal_error()` if all retries are exhausted.

**Returns:** `True` when connected.

---

#### `wifi.disconnect()`

Disconnects and deactivates the WLAN interface.

---

#### `wifi.is_connected()` → `bool`

Returns `True` if WLAN is connected.

---

#### `wifi.status()` → `tuple[int, str]`

Returns `(status_code, human_readable_status_string)`.

---

#### `wifi.ip()` / `wifi.ipv4()` → `str | None`

Returns the IPv4 address string, or `None` if not connected.

---

#### `wifi.ipv6()` → `str | None`

Returns the IPv6 address string, or `None` if not connected.

---

#### `wifi.subnet()` → `str | None`

Returns the subnet mask string.

---

#### `wifi.gateway()` → `str | None`

Returns the default gateway IP string.

---

#### `wifi.nameserver()` → `str | None`

Returns the DNS nameserver IP string.

---

### `modules/common/secrets.py`

Secrets loader. Imports from `/secrets.py` (user filesystem) or falls back to `/system/secrets.py`.

#### `secrets.require(*keys)`

Checks that each named secret in `keys` is set (non-`None`, non-empty). Calls `fatal_error()` with a disk-mode prompt if any are missing.

**Parameters:**
- `*keys` — variable number of secret name strings (e.g. `"WIFI_SSID"`, `"TIMEZONE"`)

---

### `modules/common/easing.py`

24 easing functions. All take a single `float x` in `[0.0, 1.0]` and return a `float` in approximately the same range.

| Function | Style |
|----------|-------|
| `linear(x)` | Linear |
| `easeInQuad(x)` | Quadratic in |
| `easeOutQuad(x)` | Quadratic out |
| `easeInOutQuad(x)` | Quadratic in-out |
| `easeInCubic(x)` | Cubic in |
| `easeOutCubic(x)` | Cubic out |
| `easeInOutCubic(x)` | Cubic in-out |
| `easeInQuart(x)` | Quartic in |
| `easeOutQuart(x)` | Quartic out |
| `easeInOutQuart(x)` | Quartic in-out |
| `easeInQuint(x)` | Quintic in |
| `easeOutQuint(x)` | Quintic out |
| `easeInOutQuint(x)` | Quintic in-out |
| `easeInSine(x)` | Sinusoidal in |
| `easeOutSine(x)` | Sinusoidal out |
| `easeInOutSine(x)` | Sinusoidal in-out |
| `easeInExpo(x)` | Exponential in |
| `easeOutExpo(x)` | Exponential out |
| `easeInOutExpo(x)` | Exponential in-out |
| `easeInCirc(x)` | Circular in |
| `easeOutCirc(x)` | Circular out |
| `easeInOutCirc(x)` | Circular in-out |
| `easeInBack(x)` | Back (overshoot) in |
| `easeOutBack(x)` | Back (overshoot) out |
| `easeInOutBack(x)` | Back (overshoot) in-out |
| `easeInElastic(x)` | Elastic in |
| `easeOutElastic(x)` | Elastic out |
| `easeInOutElastic(x)` | Elastic in-out |
| `easeInBounce(x)` | Bounce in |
| `easeOutBounce(x)` | Bounce out |
| `easeInOutBounce(x)` | Bounce in-out |

Not exported to builtins; must be imported with `from easing import *` or `import easing`.

---

### `modules/common/lsm6ds3.py` — `class LSM6DS3`

Driver for the ST LSM6DS3 6-axis IMU.

#### `LSM6DS3(i2c, address=0x6A, mode=NORMAL_MODE_104HZ)`

Initialises the sensor: sets gyro and accel mode, enables step counter, tap detection (X/Y/Z), and double-tap.

| Mode Constant | Description |
|---------------|-------------|
| `NORMAL_MODE_104HZ` | Normal power, 104 Hz ODR |
| `NORMAL_MODE_208HZ` | Normal power, 208 Hz ODR |
| `PERFORMANCE_MODE_416HZ` | High performance, 416 Hz ODR |
| `LOW_POWER_26HZ` | Low power, 26 Hz ODR |

#### `LSM6DS3.get_readings()` → `tuple[int, int, int, int, int, int]`

Returns `(ax, ay, az, gx, gy, gz)` as signed 16-bit integers (two's complement). Reads all 12 data bytes in a single I2C transaction.

#### `LSM6DS3.get_step_count()` → `int`

Returns the current pedometer step count.

#### `LSM6DS3.reset_step_count()`

Resets the step counter to zero and re-enables sensor functions.

#### `LSM6DS3.tilt_detected()` → `int`

Returns `1` if a tilt event is detected, else `0`.

#### `LSM6DS3.sig_motion_detected()` → `int`

Returns `1` if significant motion is detected, else `0`.

#### `LSM6DS3.single_tap_detected()` → `int`

Returns `1` if a single tap is detected this frame, else `0`.

#### `LSM6DS3.double_tap_detected()` → `int`

Returns `1` if a double tap is detected this frame, else `0`.

#### `LSM6DS3.freefall_detected()` → `int`

Returns non-zero if a freefall event is detected.

---

### `modules/common/pimoroni.py`

Hardware utility classes. Not exported to builtins.

#### `class Analog`

ADC voltage/current reader with gain, resistor shunt, and offset compensation.

- `Analog(pin, amplifier_gain=1, resistor=0, offset=0)`
- `read_voltage()` → `float` — voltage in volts
- `read_current()` → `float` — current in amps (requires `resistor > 0`)

#### `class AnalogMux`

Multiplexed ADC using up to 3 address pins and an optional enable pin.

- `AnalogMux(addr0, addr1=None, addr2=None, en=None, muxed_pin=None)`
- `select(address)` — selects the given mux channel
- `disable()` — disables the mux via the enable pin
- `configure_pull(address, pull=None)` — sets the pull mode for a channel
- `read()` → `int` — reads the value of the muxed pin

#### `class Button`

Debounced button with repeat and hold support.

- `Button(button, invert=True, repeat_time=200, hold_time=1000)`
- `read()` → `bool` — returns `True` on press/repeat events
- `raw()` → `bool` — raw pin state
- `is_pressed` *(property)* → `bool`

#### `class RGBLED`

PWM RGB LED driver.

- `RGBLED(r="LED_R", g="LED_G", b="LED_B", invert=True)`
- `set_rgb(r, g, b)` — sets colour with 0–255 per channel

#### `class PID`

Proportional-Integral-Derivative controller.

- `PID(kp, ki, kd, sample_rate)`
- `calculate(value, value_change=None)` → `float` — returns PID output

#### `class Buzzer`

PWM buzzer/speaker.

- `Buzzer(pin)`
- `set_tone(freq, duty=0.5)` → `bool` — sets frequency and duty cycle; returns `False` if `freq < 50`

#### `class ShiftRegister`

8-bit parallel-in shift register reader.

- `ShiftRegister(clk, lat, dat)`
- `read()` → `int` — reads 8-bit value
- `is_set(mask)` → `bool` — checks if all bits in `mask` are set
- `__iter__` — yields 8 individual bit values

#### `class PWMLED`

PWM-controlled LED with brightness, on/off, and toggle.

- `PWMLED(pin, invert=False)`
- `brightness(brightness)` — sets brightness `[0.0, 1.0]`
- `on()` — sets brightness to 1.0
- `off()` — sets brightness to 0.0
- `toggle()` — toggles between 0.0 and 1.0

---

### `modules/common/qwstpad.py` — `class QwSTPad`

Driver for the Pimoroni QwSTPad I2C game controller (TCA9555 I/O expander).

#### `QwSTPad(i2c, address=DEFAULT_ADDRESS, show_address=True)`

**Parameters:**
- `i2c` — `machine.I2C` instance
- `address` — one of `0x21`, `0x23`, `0x25`, `0x27`; raises `ValueError` for invalid addresses
- `show_address` — if `True`, illuminates the LED corresponding to the I2C address position

#### `QwSTPad.read_buttons()` → `OrderedDict`

Returns a dict mapping button name → `bool` for all 10 buttons: `A`, `B`, `X`, `Y`, `U` (up), `D` (down), `L` (left), `R` (right), `+`, `-`.

#### `QwSTPad.set_leds(states)`

Sets all 4 LEDs from a 4-bit bitmask.

**Parameters:**
- `states` — `int` bitmask (bits 0–3 correspond to LEDs 1–4)

#### `QwSTPad.set_led(led, state)`

Sets a single LED on or off.

**Parameters:**
- `led` — LED index `1`–`4`; raises `ValueError` for out-of-range
- `state` — `bool`

#### `QwSTPad.clear_leds()`

Turns off all four LEDs.

#### `QwSTPad.address_code()` → `int`

Returns a bitmask with the bit set that corresponds to this device's I2C address index (0–3).
