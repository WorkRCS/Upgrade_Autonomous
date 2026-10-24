# Platform capability matrix

Targets: Windows 10/11, macOS 13+, Ubuntu 22.04+; compatible Linux distributions
can use the same adapters. This matrix is a plan/capability contract, not proof of
physical testing. Mocked tests and actual local results are recorded in VERIFICATION.md.

| Feature | Windows | macOS | Linux | Fallback / prerequisite |
| --- | --- | --- | --- | --- |
| CPU total/per-core/frequency/load | psutil; load if available | psutil | psutil | Missing individual field is null/N/A |
| RAM/swap/disk/I/O/uptime/processes | psutil | psutil | psutil | AccessDenied/missing sensor does not crash collector |
| Network counters/throughput/interfaces | psutil | psutil | psutil | First throughput sample N/A; counters are not an Internet speed test |
| Battery | psutil | psutil | psutil | Desktop/no sensor: N/A |
| NVIDIA GPU utilization | pynvml → nvidia-smi/WMI | model inventory; no general Apple GPU utilization claim | pynvml → nvidia-smi → lspci/sysfs inventory | Inventory does not imply load percentage; N/A when absent |
| Temperature | LibreHardwareMonitor/WMI when exposed | psutil if exposed | psutil sensors/sysfs | N/A; no fabricated temperature |
| Shell streaming/cwd/timeout/exit code | PowerShell → cmd | zsh → bash | bash → sh | Missing shell returns structured error; all shell requests confirmed |
| Process list/kill | psutil | psutil | psutil | Kill sensitive; permissions may deny; never target EDITH itself |
| Files/new/read/list/trash/overwrite | pathlib/send2trash | pathlib/send2trash | pathlib/send2trash | Permission tiers; irreversible fallback is not automatic |
| App launch/installed inventory | Start Menu/PATH | .app bundles/open | desktop entries/PATH/gtk-launch | No matching launcher: error, never claim foreground success |
| Window list | Win32 | AppleScript System Events | wmctrl on X11 | Accessibility permission; Wayland unsupported unless compositor API exists |
| Clipboard | Qt/pyperclip | Qt/pyperclip | Qt/pyperclip with session | Headless/Wayland/backend denial: unavailable |
| Screenshot/multi-monitor | mss | mss + Screen Recording permission | mss on X11 | Wayland needs portal; return unavailable, not a black fake capture |
| Volume | pycaw | osascript | pactl/wpctl | Missing audio service: unsupported |
| Brightness | WMI supported displays | optional brightness utility | brightnessctl | External displays/no interface: N/A/unsupported; do not silently simulate dimming |
| Sleep/restart/shutdown | OS power/UAC | AppleScript OS authorization | logind/systemctl/polkit | Always critical confirmation; OS can deny |
| OS theme | winreg AppsUseLightTheme | defaults AppleInterfaceStyle | GNOME gsettings → KDE kdeglobals | Unknown dark; worker polls every 2s |
| Secure API secrets | keyring Windows Credential Manager | keyring Keychain | keyring Secret Service/KWallet | No unlocked secure backend: explicit error; no plaintext fallback |
| Glass desktop / local JS | Qt WebEngine | Qt WebEngine | Qt WebEngine | Platform Qt libraries/display session required; native compatibility fallback |
| Three.js sphere / GSAP | WebGL2 with supported driver | WebGL2 | WebGL2 | Static accessible orb if unavailable; no 60fps guarantee without measurement |
| Microphone/speaker | PortAudio | PortAudio + mic permission | PortAudio/PipeWire/Pulse/ALSA | Text/remote input survive absent hardware; exact 16/24k formats checked |
| Camera | OpenCV | OpenCV + camera permission | OpenCV/V4L | Missing camera: explicit unavailable |
| Full arbitrary device/kernel/vehicle control | No | No | No | Only documented, authorized OS/device APIs; never bypass safety controllers |

Power/elevation, native desktop and live provider tests must be performed on real
supported targets. OS version support depends on installed Qt/PortAudio/browser
runtime and distribution libraries. Do not interpret mocked adapter selection as
Windows/macOS/Linux production certification.
