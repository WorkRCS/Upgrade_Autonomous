# EDITH upgrade status

All implementation remains on `ui/edith-interface`. Do not merge this branch into
`main` until the owner has tested a pull of the branch and explicitly requests merge.

## Current UI after owner feedback

- Restore the layout, desktop palette and remote page appearance from `938ffe5`,
  before the two UI redesign commits `8219027` and `7eb2ab4`.
- Play the user-selected bundled video in a silent infinite loop with soft edge blending;
  retain independent real input/output feedback and activity labels.
- Retain native OS window controls and screen-aware startup geometry; remove duplicate
  in-app window buttons.
- Retain confirmation expiry/serialization, selected-file clearing, newer remote
  command/pairing behavior and Neuron Intelligence product metadata.
- Remove the Apple light theme and separate conversation/context-tab layout.
- This is a forward UI restoration commit, not a branch reset or a merge to main.

## Remaining stages

Audio/runtime reliability implementation has started. Generated narration now uses
a lossless PCM FIFO, a dedicated device writer, startup/rebuffer prefill and explicit
underrun diagnostics. Tool execution no longer blocks the audio receiver. Startup
news waits for generation **and** hardware playback to finish instead of a fixed
delay. See [NARRATION_RELIABILITY.md](NARRATION_RELIABILITY.md) for the failure,
implementation boundaries and target-device checks. This stage does not implement
the later provider, voice approval or device-control features.

| Stage | Implementation and acceptance gate |
| --- | --- |
| Full branch audit | Inventory both branches and every tool/sub-command; reproduce failures; record dependencies, supported OS and real execution evidence. Earlier UI tests are not a full runtime certification. |
| Narration reliability — implemented, device test pending | Byte-for-byte burst/jitter tests, ordered tool execution while audio receive continues, speaker recovery and interruption checks pass with simulated streams. Confirm long spoken responses with the owner's actual API key, network and speaker. |
| Task/session control | Explicit Working, Awaiting approval, Stopping and Sleeping lifecycle; accept stop/clarification/approval while rejecting unrelated new tasks during a job; verify cancellation semantics. |
| Voice approval | Bind a spoken reply to one pending action and target; exclude assistant output and untrusted content; expiry, rejection and microphone-unavailable behavior; destructive tests only with disposable targets. Existing local confirmation remains active until this is implemented and verified. |
| Provider adapters | Separate Gemini, Ollama, Anthropic, xAI and OpenAI settings and runtime adapters. Preserve existing Ollama settings. Real key/response/voice/tool tests per provider; no unsupported native audio capability claims. |
| Memory | Transactional storage, structured project/task facts, summaries, retrieval, provenance and migration from the bounded JSON store. |
| Device/tool coverage | Hardware/network diagnostics, multi-monitor/window targeting, terminal/code workflows and authorized security diagnostics; OS capability/permission reporting and post-action verification. |
| Latency and resilience | Measure input, first audio, tool start and verified completion separately; p50/p95 benchmarks, network interruptions, hardware recovery and duplicate-action handling. |
| Release | Target Windows/macOS/Linux and phone-browser checks, user's pull/test feedback, fixes, then explicit authorization before merging into main. |

API-provider access, real microphones, cameras, screen permissions and OS window
managers must be tested on target devices. Headless GUI tests validate application
behavior; they do not certify those external integrations. No universal sub-second
task-completion or unrestricted access to arbitrary devices is claimed.
