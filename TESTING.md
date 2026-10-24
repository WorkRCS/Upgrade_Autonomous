# EDITH — Full Verification Checklist

This checklist separates automated repository checks from manual tests that must be run on the computer where EDITH will be used. Passing CI does **not** prove every OS-specific GUI action works on every machine.

## Phase 1 release gate — complete before Phase 2

Phase 1 is **not complete** until the repository checks pass **and** the user
verifies the following on their actual Windows installation. Do not start Phase 2
until the user explicitly confirms this release gate passed.

1. Update **only** `ui/edith-interface` using `git fetch origin`,
   `git checkout ui/edith-interface`, and `git pull --ff-only origin ui/edith-interface`.
   Do not create any new branch or merge the PR during testing.
2. Activate the existing Python virtual environment (or create one) and run
   `python -m pip install -r requirements.txt` followed by
   `python -m core.startup_check`. Verify the previously reported
   `sounddevice` startup problem no longer occurs.
3. Run the full automated commands in section 2. Start with `python main.py`;
   verify the **existing** EDITH design opens with the dedicated EDITH window
   and taskbar icon. No UI layout redesign is part of Phase 1.
4. In EDITH, click **CREATE DESKTOP SHORTCUT**. Check the desktop contains
   `EDITH.lnk`, it uses the EDITH icon, and launching it opens EDITH. Old
   shortcuts are removed automatically **only** if their target is positively
   identified as this installation's `main.py`; verify any remaining old
   shortcuts manually before removing them. Do not delete unknown shortcuts.
5. Toggle Auto-start on and off once. Use the Windows Task Manager Startup
   Apps page or inspect
   `HKCU:\Software\Microsoft\Windows\CurrentVersion\Run`. A new
   entry must be named `EDITH`, not the former product name. Existing
   auto-start data is migrated only if it matches this installation.
6. Open Remote Control, then check that `Downloads/EDITH Uploads` is used
   for phone uploads. If the former uploads directory existed, its files
   must survive migration. A same-name file collision must **not** overwrite
   either file. If permissions or existing symlinks prevent migration, inspect
   both folders and retain the old one until data has been checked.
7. Check file screenshots, new reminders, generated projects, browser profiles,
   notifications and optional scheduled game updates create **EDITH**-named
   artifacts. Existing scheduled reminders must continue to work; their old
   scheduling records may remain until they fire or are removed safely.
8. Test the current cloud **Gemini Live** key and **Local LLM** inference
   separately in settings. Confirm the saved `llm_provider`, `llm_url`,
   `llm_model`, and `gemini_api_key` were not unexpectedly modified.
9. Restart EDITH, repeat shortcut launch and API/Local LLM checks, then
   report **PASS/FAIL** for each item. A Windows-level failure keeps Phase 1
   open even when GitHub Actions passes.

Do **not** post config secrets, browser cookies, microphone samples or private
files with a bug report. Sanitized stack traces and shortcut targets are enough.

## 0. Before you start

- Use a computer you control, with Python 3.11 or 3.12.
- Keep a backup of important data.
- Do not use valuable files, work databases, real recipients, or an important project for destructive-action tests.
- Have a test app available (for example, Calculator or a blank text editor) and a test messaging account/recipient only if you plan to check messaging.
- Keep credentials/API keys private. Do not paste them into issue comments, logs, screenshots, or this checklist.

## 1. Get the current branch

From a terminal:

```bash
git clone -b ui/edith-interface https://github.com/WorkRCS/Upgrade_Autonomous.git
cd Upgrade_Autonomous
```

If the repository is already cloned, protect any uncommitted work first, then run:

```bash
git status
git fetch origin
git checkout ui/edith-interface
git pull --ff-only origin ui/edith-interface
```

Windows PowerShell setup:

```powershell
py -3.11 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
```

macOS/Linux setup:

```bash
python3.11 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
pip install -r requirements.txt
```

## 2. Run automated checks first

Run these from the project root, in the activated environment:

```bash
python -m compileall -q main.py ui.py setup.py actions core dashboard memory plugins tests config
python -m unittest discover -s tests -v
python tests/check_inline_js.py
```

**Pass criteria:** all commands exit with code 0; the unit-test output ends with `OK`. If any command fails, stop here, save the error output with credentials and private text removed, and fix it before live testing.

The GitHub Actions Quality checks workflow runs these same checks on the branch.

## 3. Start the app and check basics

1. Start EDITH with `python main.py`.
2. Complete initial setup with your own API key in the local setup window. Keep the key private.
3. Open the API-key settings. Verify the panel shows the Gemini Live provider/model and also the local-agent provider, endpoint, and model read from the existing `llm_provider`, `llm_url`, and `llm_model` values in `config/api_keys.json`.
4. The local-agent connection check should run automatically. With the configured local server running and model installed, it should show the endpoint online and the configured model available. Stop Ollama (or the configured compatible server) and reopen Settings to verify it reports that the endpoint cannot be reached; then restart the server and reopen to verify recovery.
5. Click **TEST LOCAL LLM**. The test should make an actual short inference through `core.llm_client.call_llm` and show success plus response time. Check the configured model is the same one shown by the panel. If using `llm_provider=openai`, make sure the configured OpenAI-compatible server and model are running.
6. Run **TEST KEY**. The test should open a Gemini Live session, send a short prompt, wait for the first actual model output, and show the time to first response. A successful handshake without model output must not be reported as a passed test.
7. Save/reconnect only if the Gemini model-response test succeeds. The local status check must not overwrite existing local-LLM settings.
8. Confirm that the main EDITH UI opens, text input works, the microphone can be enabled/muted, the interrupt control responds, and the Activity Log remains visible.
9. Inspect the main controls and file cards: icons should render as line icons rather than emoji placeholders.
10. Close and restart EDITH normally once to check that the local configuration remains available.

## 4. Voice and identity

- Ask a harmless question and confirm EDITH answers.
- Request the female voice; verify the UI indicates the change and wait for the session to reconnect before judging the voice.
- Request the male voice and repeat.
- Ask what model/provider/engine powers EDITH. The conversational prompt asks it to respond with the product identity, **Neural Intelligence Model**. Treat this as a product-prompt behavior check, not a cryptographic guarantee that backend implementation details can never be disclosed.

## 5. Desktop app discovery and visible control

Use harmless apps first.

- Ask EDITH to list installed desktop apps.
- Search for a known installed app by name.
- Open a harmless app and check that its real foreground window appears.
- Ask EDITH to inspect the screen after launch. Verify it describes the visible app, not a guessed state.
- Try one harmless action such as scrolling or focusing a text field, and verify the screen again afterward.
- Repeat only for the OS/app combinations you actually use. Some apps may not be discoverable if they lack a standard launcher, and focus verification depends on OS permissions and available window tools.

## 6. YouTube channel search

- Ask EDITH to search for a known creator's **channel**.
- Expected: YouTube opens channel-filtered results; no video should auto-play from a channel-only request.
- Separately ask EDITH to play a specific video. Expected: the video-play action runs only for the play request.

## 7. Confirm/cancel behavior — use disposable targets only

Create a temporary test directory and a disposable text file inside your own user profile. Do not point these tests at Desktop, Downloads, a project, a database, or real work files.

For example, from Python:

```python
from pathlib import Path
import tempfile

root = Path(tempfile.mkdtemp(prefix="edith-safe-test-", dir=str(Path.home())))
test_file = root / "disposable-test.txt"
test_file.write_text("EDITH deletion test only", encoding="utf-8")
print("Temporary test folder:", root)
print("Temporary test file:", test_file)
```

Keep the printed path so you can identify the exact test target.

### A. Cancel a file deletion

1. Ask EDITH to delete only the disposable test file.
2. Verify the dialog names the correct target.
3. Choose **Cancel**.
4. Confirm the file still exists. If it disappeared, mark the test failed and stop further destructive tests.

### B. Approve a normal deletion

1. Ask EDITH to move the disposable file to the system Trash/Recycle Bin.
2. Read the dialog and confirm the correct path.
3. Choose **Confirm and Execute**.
4. Confirm the tool reports the result accurately. If the platform's Trash integration is unavailable, note the exact error; do not switch to permanent delete automatically.

### C. Permanent deletion (optional, disposable file only)

1. Create a new disposable file inside the temporary test folder.
2. Explicitly request **permanent** deletion of that exact file.
3. Check the dialog says this cannot be undone and displays the right target.
4. Choose **Cancel** first and confirm the file remains.
5. Repeat with a newly created disposable file; approve and verify that only that test file was removed.
6. Confirm EDITH refuses any attempt to delete the user-profile root.

Never test permanent deletion on a real app installation or a folder containing useful data.

### D. Close/terminate confirmation

1. Open a harmless test app (not EDITH) with no unsaved work.
2. Ask EDITH to close that named app.
3. Confirm the dialog identifies the intended target.
4. Cancel once and verify the app remains open.
5. Repeat and approve; verify the named app closes.
6. If EDITH cannot identify or verify the target window, it should stop instead of closing an arbitrary window.

### E. Outbound message confirmation (optional)

Use a test account or a consenting recipient. Ask EDITH to prepare a harmless message. Verify the local dialog displays the intended platform, recipient, and complete body. Cancel and verify no message is sent. Only repeat with approval if you are comfortable sending that exact message. Do not use a real sensitive conversation to test this.

### F. Destructive terminal command detection (optional)

Do not execute a destructive command against the real system. Test only with a disposable text editor or terminal sandbox, and cancel the confirmation dialog. Verify the dialog displays the exact command to be typed. Never approve a command that removes data, changes production resources, or affects another user's machine.

## 8. Activity Log and privacy

- Verify the log shows action start, confirmation requested/approved/cancelled, and outcome.
- Verify ordinary logs do not contain typed text, message bodies, API values, or arbitrary tool output.
- The local confirmation dialog intentionally previews the exact message/command so you can review it before execution; keep screenshots of that dialog private if it contains personal information.

## 9. Record the results

For each item mark **PASS**, **FAIL**, or **NOT TESTED**. Record OS/version, Python version, app name/version, and a short sanitized error when something fails. Do not include API keys, passwords, personal message bodies, or access tokens.

A full machine-level pass requires all relevant manual tests above to pass on the target OS. The automated CI suite alone is not a substitute for this machine-specific check.

## 10. Phase 2 — Fast Response Engine acceptance checks

**Phase 2 preserves both providers.** Gemini Live continues to handle the real-time
voice session; the configured local agent still uses the existing `llm_provider`,
`llm_url`, and `llm_model` settings. Do not replace one with the other.

### Automated tests

Run from the project root with the activated environment:

```powershell
python -m py_compile main.py ui.py core/llm_client.py core/realtime_audio.py tools/phase2_benchmark.py
python -m unittest discover -s tests -v
python tests/check_inline_js.py
```

**Pass:** all three commands succeed. The Phase 2 tests exercise the bounded audio
backlog and mocked Ollama/OpenAI-compatible text agents without internet access.

### On-device latency benchmark

1. Start your already-configured Ollama or OpenAI-compatible local server and ensure
   its configured model is available. Do not change `config/api_keys.json`.
2. Run `python tools/phase2_benchmark.py --iterations 3` on the actual PC.
   Record **first sentence** and **total** latency, without storing model output.
   First sentence is not first token. Repeat with the same local model/hardware
   settings when comparing improvements.
3. Start EDITH using `python main.py`. In the current UI's Activity Log find
   `PERF: Gemini Live session ready in ... ms`; this includes preparation
   and the cloud session handshake, not a response to a user message.
4. Send a short **text** query and look for
   `PERF: Gemini Live first audio after text request: ... ms`. This measures
   the text-send to first-audio interval, not voice-to-voice latency.
5. Open the existing API settings and run **TEST KEY**. Confirm the live model
   actually responds. Then use **TEST LOCAL LLM** to confirm real local inference
   still succeeds on the configured backend.
6. Ask a question through the microphone and verify no clipped speech, doubled
   responses, or lost words during a normal connection.
7. Test network recovery on a disposable/no-risk session. Briefly disconnect
   and restore the network and verify status/reconnection are truthful. A slow
   network may force the input queue to discard **oldest unsent audio** to limit
   stale backlog; check whether speech becomes clipped under sustained overload.
8. Test typing several short prompts, camera/screen use, remote/phone input
   (if enabled), interrupt, and local agent tool calls. Confirm the UI remains
   responsive and all existing confirmation dialogs still appear when required.

### Phase 2 completion gate

Mark **PASS** only when automated checks pass **and** the user has verified
Gemini Live, Local LLM, desktop UI, and input/reconnection on their actual
machine. Report measured before/after latency for comparable conditions;
performance improvements are not guaranteed for every device or network.
Do not start Phase 3 until the user explicitly accepts Phase 2.


## Phase 3 — Autonomous multitasking release gate

Phase 3 extends the existing EDITH UI and Gemini Live tool-response path. It does
not replace or overwrite the Ollama/OpenAI-compatible local LLM configuration,
the Gemini Live model, or the sensitive-action confirmation rules.

### Automated checks

Run the existing three automated commands in section 2 on ui/edith-interface.
The new tests in tests/test_task_scheduler.py cover four simultaneous independent
jobs, worker limits, priorities, dependency barriers, queued cancellation,
failure propagation, missing prerequisites, read-only classification, and
opt-in safe retries. These are simulated tasks, not Windows GUI tests.

### Windows UI and live-operation checks

1. Start EDITH on the actual Windows PC. The **existing UI** should be retained.
   Above Activity Log, TASKS should start at zero running and zero waiting.
   CANCEL WAITING should be disabled initially.
2. Ask for four unrelated **read-only** lookups (four distinct web searches).
   If Gemini Live emits multiple function calls in one batch, check Activity Log
   for TASKS batch entries. Running actions must never exceed four. If the model
   issues one call per turn, mark simultaneous execution **NOT TESTED** rather
   than claiming the test passed.
3. With a batch larger than the available workers, click CANCEL WAITING.
   Only jobs not yet started may be cancelled. Running actions must continue;
   the UI must not claim they were stopped or undone.
4. Use a disposable folder. Request a listing, then creation of one specifically
   named disposable folder, then another listing. The creation must happen only
   after its prerequisite work; no folder may be created twice. Do not use
   valuable files for this test.
5. Request a harmless nonexistent-file read as a prerequisite to another task.
   If the prerequisite fails, the dependent task must not run or report success.
6. Check dangerous-action confirmation dialogs on disposable targets only, as
   documented in section 7; verify that cancellation prevents execution.
7. Re-run both TEST KEY (Gemini Live) and TEST LOCAL LLM. Check that the
   provider, model, endpoint and API key settings have not changed.
8. Restart EDITH, test text/voice input and optional phone dashboard. Note any
   stuck RUNNING indicator, duplicate action or wrong-window interaction.

### Phase 3 completion gate

CI must pass AND the user must report PASS on relevant Windows tests. Do not
start Phase 4 until the user explicitly approves Phase 3.

Limitations: this phase can parallelize independent read-only tool calls within
one Gemini Live batch; it does not execute four desktop mouse/keyboard operations
concurrently, nor four independent Live conversations. When a session disconnects
during an OS action, inspect the actual outcome before attempting it again.
