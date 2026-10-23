# Personal AI Assistant

A desktop voice assistant with real-time audio, optional screen/camera awareness, local computer controls, plugins, persistent memory, and an optional remote dashboard. It uses the existing Google Gemini Live API integration.

## Features

- Real-time voice conversation using Gemini Live API
- Female voice preset (Kore) and male voice preset (Orus), selectable by voice command or the Controls panel
- API-key settings with real Gemini Live connection testing before save; saving triggers session reconnection
- Keyboard and microphone input
- OS-aware installed desktop-app discovery and launching from Windows Start Menu shortcuts, macOS `.app` bundles, Linux `.desktop` entries, and known PATH executables
- Visible foreground desktop control across native apps and browsers, with a live Activity Log and screen-based verification before native-app interactions
- Local application, browser, file, and system-control tools
- Optional screen and camera context
- Plugin discovery and manager
- Session memory and optional startup briefing
- Optional mobile/remote dashboard with access-code pairing
- CPU, memory, network, GPU, and temperature indicators where supported

## Cross-app desktop control

EDITH is designed to work across the user's desktop rather than being limited to YouTube or a single browser. Example voice/text commands include:

- "List installed desktop apps."
- "Find MongoDB Compass."
- "Open Android Studio and inspect the screen."
- "Open Telegram and show me the current window."
- "Open Postman and help me inspect this request."

The app inventory is best-effort: Windows Start Menu shortcuts, macOS application bundles, Linux desktop-entry metadata, and known executables on PATH are searched. An app installed without a standard launcher may not appear in the inventory. Discovery reads metadata only; it does not execute commands from shortcut or desktop-entry files.

Desktop interactions use the real foreground window so the user can see the app being controlled. The Activity Log records action starts and outcomes while omitting typed text, message bodies, clipboard contents, credentials, and file contents. EDITH should inspect the screen after launching an app and after important UI changes. A launch is not reported as verified unless the foreground-window label matches; when the OS does not expose a usable label, the result is marked unverified and screen inspection is required.

This foundation does not guarantee that every workflow in every third-party application works automatically. Apps may need to be installed and signed in, GUI controls differ by version, OS permissions may be required, and workflows involving databases, sending messages, deleting data, publishing code, or other high-impact changes require appropriate confirmation.

Actual response time depends on network conditions, API availability, the requested action, and the local system. Long-running actions such as web searches, downloads, or application startup cannot be guaranteed to finish within a fixed number of seconds.

## Requirements

- Windows 10/11, macOS, or Linux
- Python 3.11 or 3.12
- A working microphone for voice interaction
- Google Gemini API key
- Some operating-system-specific dependencies may require extra setup

## Local setup

Clone the repository branch containing the UI refresh and enter the project directory:

```powershell
git clone -b ui/edith-interface https://github.com/WorkRCS/Upgrade_Autonomous.git
cd Upgrade_Autonomous
py -3.11 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
python main.py
```

If PowerShell blocks environment activation for the current terminal, use this session-only workaround and activate again:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
.\.venv\Scripts\Activate.ps1
```

On macOS or Linux, create and activate the environment with:

```bash
python3.11 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
pip install -r requirements.txt
python main.py
```

If `py -3.11` is unavailable on Windows, install Python 3.11 through the Windows Python Install Manager or the official Python installer. Verify with `py -3.11 --version` before creating the environment.

## Initial configuration

On first launch, enter a Gemini API key in the setup screen. Configuration is stored locally in `config/api_keys.json`. Never commit API keys or personal configuration to source control.

The optional remote dashboard requires compatible browser and network access. Use the access code displayed by the desktop application. Keep the dashboard on a trusted network and do not expose it to the public internet without reviewing its security configuration.

## Project structure

```text
main.py                  # Live API session, audio I/O, tool dispatch
ui.py                    # Desktop UI, HUD, panels, customization
core/prompt.txt          # Assistant behaviour and tool-routing rules
core/plugin_loader.py    # Plugin discovery and validation
actions/                 # Computer, browser, file, search and utility actions
dashboard/               # Optional remote dashboard and static assets
memory/                  # Session and long-term memory handling
config/                  # Local settings and generated app resources
```

## Troubleshooting

- **Python runtime missing:** install Python 3.11 or 3.12 and confirm the launcher detects it.
- **Microphone unavailable:** check operating-system microphone permissions and select a working input device.
- **API connection or key error:** open Controls → Gemini API Key, test the key against Gemini Live, then save and reconnect.
- **Missing optional module:** activate the virtual environment, then install the missing supported dependency.
- **Hardware metrics show N/A:** GPU and temperature metrics depend on the hardware, driver, and platform.

## License

See [LICENSE](LICENSE) for the terms that apply to this repository.
