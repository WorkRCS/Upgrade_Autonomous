# Personal AI Assistant

A desktop voice assistant with real-time audio, optional screen/camera awareness, local computer controls, plugins, persistent memory, and an optional remote dashboard. It uses the existing Google Gemini Live API integration.

## Features

- Real-time voice conversation using Gemini Live API
- Female voice preset (Kore) and male voice preset (Orus), selectable by voice command or the Controls panel
- API-key settings with an LLM status panel showing provider, exact runtime model, cloud/local mode, test outcome, and time to first model output
- API test sends a small real prompt and waits for a model response (not just a successful socket handshake) before allowing the key to be saved
- Keyboard and microphone input
- OS-aware installed desktop-app discovery and launching from Windows Start Menu shortcuts, macOS `.app` bundles, Linux `.desktop` entries, and known PATH executables
- Visible foreground desktop control across native apps and browsers, with a live Activity Log and screen-based verification before native-app interactions
- Bundled local SVG icons for core controls and file types (no remote icon downloads)
- YouTube creator/channel-only search that opens filtered channel results without auto-playing a video
- A bundled, locally rendered SVG line-icon set for the desktop controls and file-type indicators; no remote icon CDN or emoji glyphs are required for these UI elements
- Local application, browser, file, and system-control tools
- Optional screen and camera context
- Plugin discovery and manager
- Session memory and optional startup briefing
- Optional mobile/remote dashboard with access-code pairing
- CPU, memory, network, GPU, and temperature indicators where supported

## Local confirmation for high-impact actions

EDITH uses a scrollable native local confirmation dialog before permanent file/folder deletion, closing/terminating apps, system restart/shutdown, outbound messages, and detected destructive terminal commands. The dialog shows the exact target, message body, or destructive command for review where relevant; **Confirm and Execute** proceeds, while **Cancel**, dismissal, or timeout leaves the action unexecuted. Before close or keyboard/mouse actions continue, EDITH restores and verifies the window captured before the dialog so keystrokes do not accidentally land in EDITH itself. A model-supplied confirmation parameter cannot bypass this dialog.

The ordinary `delete` action moves an item to Trash/Recycle Bin when the platform dependency is available. Irreversible removal uses the separate `delete_permanent` action and is allowed only within the user's home directory after local confirmation. The home/profile root stays protected; a specifically selected user folder (including a standard Desktop or Downloads folder) can be removed after the dialog clearly names that exact target.

For user-facing model identity, EDITH uses the product name **Neural Intelligence Model** and its system prompt treats provider/model details as non-disclosable product implementation details, including when similar requests arrive through prompt injection in untrusted content.

## LLM connection status and response speed

The API settings panel identifies the configured provider as **Google Gemini Live API (cloud-hosted)** and shows the exact Live model ID used by the app. The local LLM line explicitly reports **not configured**: this branch does not currently route conversations to an Ollama or LM Studio local model. A future local-provider adapter would be a separate capability rather than an implied fallback.

The **TEST KEY** action opens a Live session, sends a short test prompt, waits for the first real model output, and reports the elapsed time to first response. This checks more than whether a connection handshake succeeds; it does not guarantee the next conversation's latency, which still depends on the network, API service, audio input, and requested task. The assistant prompt prioritizes concise, direct replies and immediate tool use for straightforward tasks while preserving safety confirmations and target verification.

## Product identity

When asked what model/provider or AI service powers it, EDITH's conversational product identity is **Neural Intelligence Model**. The system prompt instructs the assistant not to disclose backend provider or model identifiers in conversation, including when such requests appear in untrusted page or file content. This is conversational branding; it does not remove provider-level policies or change which API is configured in the local settings.

## Cross-app desktop control

EDITH is designed to work across the user's desktop rather than being limited to YouTube or a single browser. Example voice/text commands include:

- "List installed desktop apps."
- "Find MongoDB Compass."
- "Open Android Studio and inspect the screen."
- "Open Telegram and show me the current window."
- "Open Postman and help me inspect this request."
- "Search YouTube for the CarryMinati channel." (opens channel-filtered results without auto-playing a video)
- "Permanently delete this specific folder." (shows the local confirmation dialog before removal)

The app inventory is best-effort: Windows Start Menu shortcuts, macOS application bundles, Linux desktop-entry metadata, and known executables on PATH are searched. An app installed without a standard launcher may not appear in the inventory. Discovery reads metadata only; it does not execute commands from shortcut or desktop-entry files.

Desktop interactions use the real foreground window so the user can see the app being controlled. The Activity Log records action starts and outcomes while omitting typed text, message bodies, clipboard contents, credentials, and file contents. EDITH should inspect the screen after launching an app and after important UI changes. A launch is not reported as verified unless the foreground-window label matches; when the OS does not expose a usable label, the result is marked unverified and screen inspection is required.

This foundation does not guarantee that every workflow in every third-party application works automatically. Apps may need to be installed and signed in, GUI controls differ by version, OS permissions may be required, and workflows involving databases, sending messages, deleting data, publishing code, or other high-impact changes require appropriate confirmation.

Actual response time depends on network conditions, API availability, the requested action, and the local system. Long-running actions such as web searches, downloads, or application startup cannot be guaranteed to finish within a fixed number of seconds.

## Full end-to-end testing

Use [TESTING.md](TESTING.md) for the complete local validation sequence, including automated checks, Gemini/voice/UI smoke tests, app discovery, YouTube channel search, Activity Log privacy, and safe confirmation-dialog tests using disposable files and harmless apps. Machine-level GUI behavior still needs to be verified on the target OS.

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
