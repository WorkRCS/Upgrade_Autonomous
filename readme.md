# Personal AI Assistant

A desktop voice assistant with real-time audio, optional screen/camera awareness, local computer controls, plugins, persistent memory, and an optional remote dashboard. It uses the existing Google Gemini Live API integration.

## Professional desktop and remote workspace

The desktop now places the conversation and command composer in the main workspace.
A centered violet particle-ring animation and Activity, Files and System tabs keep diagnostics available
without squeezing the conversation. Existing voice, model, plugin and action integrations
continue through the `EdithUI` facade.

Setup, Connections, Preferences, Plugins and Remote Access use scrollable native modal
forms with consistent controls and persistent action footers. Preferences preview is
reverted on cancellation; attachment removal clears the selected-file state. Sensitive
action confirmations expire and concurrent requests are shown in order. The legacy
YouTube URL prompt now runs through Qt on the UI thread.

The phone dashboard shares the desktop visual palette, larger touch controls, accessible
labels and reduced-motion support. Pairing and command submissions expose their pending
state; repeated pairing clicks are guarded. Microphone startup failures restore the voice
control, and the file picker reports the existing 500 MB per-file server limit.

Run the existing test suite plus the new workspace behavior gates:

```bash
QT_QPA_PLATFORM=offscreen python -m unittest discover -s tests -v
python tests/check_inline_js.py
node tests/check_phase5_js.js
node tests/check_workspace_js.js
```

Real microphone/camera use, OS integration and phone-browser behavior still require
manual testing on the target devices. Earlier Phase 4 notes below describe the previous
layout; this workspace redesign supersedes those presentation details.

## Apple-inspired UI and upgrade stages

The desktop and remote UI use light grouped surfaces, rounded controls and bundled SVG
icons. Startup geometry fits the available work area to keep the title bar on screen.
Standard native title-bar controls are explicitly enabled. Close, Minimize and
Maximize/Restore are also available in the app header, including full-screen mode;
forms have an in-app Close action. Desktop styling does not require macOS or iOS.

The center ring follows the supplied violet/blue reference appearance with an eight-second
procedural loop, bounded shared raster cache, real microphone-driven scaling, mute and
reduced-motion states. The cache contains at most 32 frames (about 12.5 MiB), and hidden
windows reduce timer activity. There is no image download or additional dependency.

Product metadata is defined in `core/product_identity.py`: EDITH, Neuron Intelligence
(NL), application built by Sadik Laskar. This metadata is separate from provider IDs and
user memory; it is not displayed as an owner/model banner in the UI. Code-owned metadata
and prompt instructions do not constitute a guarantee of injection-proof model output.

See [docs/UPGRADE_STATUS.md](docs/UPGRADE_STATUS.md) for delivered work, remaining runtime
upgrades and the test-before-merge release gate.

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

For user-facing model identity, EDITH uses the product name **Neuron Intelligence** and its system prompt treats provider/model details as non-disclosable product implementation details, including when similar requests arrive through prompt injection in untrusted content.

## LLM connection status and response speed

The API settings panel shows two distinct paths. The real-time voice conversation uses **Google Gemini Live API (cloud-hosted)** and its exact Live model ID. Separately, EDITH's internal planning/code-agent tools use the already integrated `core/llm_client.py` adapter, which reads `llm_provider`, `llm_url`, and `llm_model` from `config/api_keys.json` (default provider: Ollama; OpenAI-compatible providers are also supported).

The **TEST KEY** action opens a Live session, sends a short test prompt, waits for the first real model output, and reports the elapsed time to first response. This checks more than whether a connection handshake succeeds; it does not guarantee the next conversation's latency, which still depends on the network, API service, audio input, and requested task.

When the settings panel opens, its local-LLM section reads the actual configured provider, endpoint, and model from `core.llm_client`, then checks whether the endpoint is reachable and whether the configured model appears available. **TEST LOCAL LLM** sends a real short inference request through that same `call_llm` client and reports its response time. These checks do not replace or overwrite the existing local-LLM configuration. The assistant prompt prioritizes concise, direct replies and immediate tool use for straightforward tasks while preserving safety confirmations and target verification.


## Phase 3 safe multitasking

EDITH uses a bounded asynchronous scheduler (core/task_scheduler.py) for Gemini
Live batches containing multiple tool calls. Up to four independent, explicitly
allowlisted **read-only** operations may run together. Results are returned to
Gemini in the original call order. Actions that manipulate the desktop,
files, messages, voice/session settings, external apps, or unknown plugins
remain serialized behind dependency barriers and retain the existing local
confirmation checks. Failed or cancelled prerequisites block dependent work.

The existing UI's Activity Log has a compact TASKS running/queued indicator and
a **CANCEL WAITING** button. This cancels queued actions only; in-progress OS
actions are not stopped or rolled back. Task status stores short action labels,
not raw parameters or file contents. Priorities, dependency tracking, and safe
opt-in retry support are included in the scheduler, while Live side-effect tools
are never automatically retried. See TESTING.md for the Phase 3 Windows release
gate. No provider selection, Gemini key, local model endpoint or model setting is
overwritten by this update.

## Phase 2 latency improvements

EDITH now schedules text input directly onto the existing Gemini Live event loop
without creating a new OS thread per text submission. Session preparation reads
memory/configuration off the event loop. The Live Activity Log reports the
session connection duration and **first-audio latency for text requests**;
these timings are measurements, not speed guarantees.

The microphone/remote input queue is bounded to about two seconds of audio.
Under severe network congestion EDITH discards the **oldest unsent chunk**
rather than accumulating a long queue of stale audio; very slow connections
can still cause missing words. These changes do not bypass security dialogs,
change the cloud model, or replace the configured Local LLM backend.

Local text-only agents retain their original 600-token response budget for
planning/coding tasks; concise chat calls keep their 150-token default.
To measure streaming response time with the **already configured** local
backend (Ollama or OpenAI-compatible), run:

```powershell
python tools/phase2_benchmark.py --iterations 3
```

This records first complete sentence and total response latency, but does
not print model output or API keys. The existing **TEST KEY** and
**TEST LOCAL LLM** controls continue to validate each backend separately.
Follow the Phase 2 section in [TESTING.md](TESTING.md) before considering
this phase accepted on your own machine.

## Product identity

When asked what model/provider or AI service powers it, EDITH's conversational product identity is **Neuron Intelligence**. The system prompt instructs the assistant not to disclose backend provider or model identifiers in conversation, including when such requests appear in untrusted page or file content. This is conversational branding; it does not remove provider-level policies or change which API is configured in the local settings.

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

## Phase 4 — Refinements to the existing EDITH desktop UI

The original EDITH HUD, layout, colors, chat/voice interaction, optional remote
dashboard, and cloud/local model configuration are retained—not replaced with
a new concept interface.

- **Task details:** expand the chevron beside TASKS to see up to four running,
  queued, or recently completed scheduler actions with real outcome labels.
  This is metadata only: tool arguments, outputs and API credentials are not
  sent to the task view. CANCEL WAITING still affects *queued tasks only*.
- **Faster Activity Log:** text is painted in bounded chunks instead of
  character-by-character; rendered history is bounded to protect long sessions.
  Controls → **REDUCED LOG ANIMATION** toggles near-immediate log updates.
  This display preference is stored separately using EDITH Qt settings; it
  does not change `config/api_keys.json`.
- **Keyboard and layout:** **Ctrl+K** focuses/selects the command field.
  Side panels adapt to narrower windows while retaining the same HUD and
  native desktop window.
- **Safer text entry:** when Gemini Live is offline before sending, typed
  commands are left in the input box. If asynchronous sending fails, the
  command is restored only when the input is still empty, preserving any
  newer draft.

GitHub CI exercises an offscreen Qt smoke test. A real Windows display,
microphone and dual-provider test remain required: see
[Phase 4 in TESTING.md](TESTING.md).

## Phase 5 — Cross-device and network resilience

The **existing** EDITH desktop HUD and phone remote dashboard remain in place.
The phone dashboard now reconnects its control WebSocket with bounded
exponential backoff (starting at 1 second, capped at 30 seconds), a ping/pong
heartbeat, and visible connection state. Reconnect does not clear the phone
conversation or replay old remote commands. Server event IDs let the phone skip
already displayed history after reconnect, while older clients can still read
the unchanged message types and authentication protocol.

**Command safety on unstable links:** phone text is kept until the HTTP server
confirms it accepted the command. If the acknowledgement is lost, EDITH reports
the delivery as **unconfirmed**; it never auto-resends potentially destructive
requests. When Gemini Live is disconnected, the phone gets an explicit
"not queued" response and retains the draft. Remote text commands still use
the existing Gemini Live session; local LLM agent routing and keys are unchanged.

**Audio on slower devices:** the phone mic keeps its original 16 kHz PCM16
format but bounds WebSocket buffering. Stale buffered audio is skipped instead
of building a long voice delay. The server also bounds its input queue and
prefers recent samples. Under severe congestion this can lose speech, so check
the transcribed request before allowing any important action.

**Pairing and compatibility:** a transient network failure does not erase a
saved paired-device token. Only an explicit authentication rejection removes
it. Original session keys, encryption salt, server routes and internal browser
storage identifiers are retained for compatibility; no legacy product name is
shown as the app name or shortcut. Remote access requires a reachable device
on a trusted local network or a separately configured trusted private tunnel.
EDITH does **not** magically connect across unrelated public internet networks,
and the dashboard should not be exposed directly to the open internet.

Phase 5 automated tests exercise authorized HTTP session probes, control
WebSocket ping/pong, replay IDs and offline Live command rejection, in addition
to the existing Python, UI and JavaScript suites. See the Phase 5 manual gate
in [TESTING.md](TESTING.md) for real phone/network verification.

## Phase 6 — Smart Agent Reliability

EDITH now keeps the same native UI, Gemini Live voice path, and existing local
Ollama/OpenAI-compatible LLM configuration. Phase 6 improves the **execution
protocol** rather than replacing an AI model or adding a redesigned dashboard.

- **Tool-call replay protection:** duplicate IDs for side-effecting actions
  (messaging, file writes, GUI controls, etc.) are suppressed within a running
  EDITH process. A conflicting ID is also rejected. Requests without an ID
  cannot be deduplicated reliably. An intentional new command with a new ID is
  not blocked just because it resembles an earlier one.
- **Truthful receipts:** the tool response carries `execution_verification`
  metadata. A handler reporting success is **not** independent confirmation
  of an external effect. For side effects EDITH marks follow-up observation
  as required; missing or ambiguous receipts block subsequent dependent
  operations. Cancelled actions remain distinguishable from actual failures.
- **Recovery without unsafe replay:** a local SQLite task journal records
  status and duration, never original prompts, arguments, filenames, paths,
  API secrets, messages or raw tool responses. When EDITH restarts, queued
  or running tasks from the previous process are marked **interrupted**;
  they are **not resumed automatically**. Task history is capped at 300
  terminal entries and can be queried through the read-only `task_history`
  tool. The journal is saved under `memory/agent_history.sqlite3`, which is
  ignored by Git.
- **Graceful storage failure:** if the journal cannot be created, EDITH reports
  that task history is unavailable while normal actions continue. Remote
  authentication and cloud/local API settings are unchanged.

These improvements do not prove that every action has been visually verified.
Use independent screen/OS checks before claiming a high-impact outcome, and
never re-send an external operation merely because its acknowledgment was lost.
See [Phase 6 testing in TESTING.md](TESTING.md). Windows release approval
still requires the user's on-device verification.

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
python -m pip install -r requirements.txt
python -m core.startup_check
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
python -m pip install -r requirements.txt
python -m core.startup_check
python main.py
```

If `py -3.11` is unavailable on Windows, install Python 3.11 through the Windows Python Install Manager or the official Python installer. Verify with `py -3.11 --version` before creating the environment.

## EDITH identity and compatibility (Phase 1)

EDITH keeps the existing native UI; there is no replacement dashboard design.
Use **CREATE DESKTOP SHORTCUT** in Controls to create `EDITH.lnk` on Windows,
`EDITH.app` on macOS, or `edith.desktop` on Linux. The app uses a dedicated
EDITH E-monogram icon in its window and desktop launcher.

Uploads are stored in **EDITH Uploads**. Existing files from the former
downloads folder are moved only with collision protection. Browser profiles
and generated projects migrate to EDITH-named directories when safe.
Never delete an old folder until its files and account sessions have been verified.
Old scheduled reminders can retain their original filesystem path to continue
firing; new reminders are EDITH-branded.

The cloud Gemini Live voice system and the configured local LLM remain separate
and intact. Phase 1 does **not** replace Ollama / LM Studio / OpenAI-compatible
local backends or overwrite `llm_provider`, `llm_url`, or `llm_model`.
The existing remote encryption/connection protocol retains its compatibility
keys internally; those are **not** application or shortcut names.

If EDITH reports missing packages such as `sounddevice`, run
`python -m pip install -r requirements.txt` with the **same Python** used to
start the app, then `python -m core.startup_check`.
Review the Phase 1 Windows checklist in [TESTING.md](TESTING.md) before
authorizing the start of Phase 2.

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

