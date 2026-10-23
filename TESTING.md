# EDITH — Full Verification Checklist

This checklist separates automated repository checks from manual tests that must be run on the computer where EDITH will be used. Passing CI does **not** prove every OS-specific GUI action works on every machine.

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
python -m py_compile main.py ui.py setup.py
python -m unittest discover -s tests -v
python tests/check_inline_js.py
```

**Pass criteria:** all commands exit with code 0; the unit-test output ends with `OK`. If any command fails, stop here, save the error output with credentials and private text removed, and fix it before live testing.

The GitHub Actions Quality checks workflow runs the same three checks on the branch.

## 3. Start the app and check basics

1. Start EDITH with `python main.py`.
2. Complete initial setup with your own API key in the local setup window. Keep the key private.
3. Open the API-key settings and verify the panel shows **Google Gemini Live API (cloud-hosted)** and the configured model ID. The local LLM row should say it is not configured for this cloud-only branch.
4. Run **TEST KEY**. The test should open a Gemini Live session, send a short prompt, wait for the first actual model output, and show the time to first response. A successful handshake without model output must not be reported as a passed test.
5. Save/reconnect only if the model-response test succeeds.
4. Confirm that the main EDITH UI opens, text input works, the microphone can be enabled/muted, the interrupt control responds, and the Activity Log remains visible.
5. Inspect the main controls and file cards: icons should render as line icons rather than emoji placeholders.
6. Close and restart EDITH normally once to check that the local configuration remains available.

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
