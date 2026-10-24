# EDITH upgrade status

All implementation remains on `ui/edith-interface`. Do not merge this branch into
`main` until the owner has tested a pull of the branch and explicitly requests merge.

## Delivered in this stage

- Initial geometry fits the available work area and screen origin, keeping the native
  title bar on screen on shorter displays.
- Explicit native title-bar Close, Minimize and Maximize flags, plus accessible
  in-app window controls that remain usable in full-screen mode.
- In-app dialog Close actions using the same cancel/preview-revert lifecycle as
  Escape and the native close button.
- Apple-inspired light grouped surfaces, rounded fields, blue accents, system
  typography, consistent SVG icons and remote dashboard styling.
- Missing chevron icon fixed; Activity, Files, System and command controls use
  explicit vector icons rather than falling back to generic file artwork.
- Centered violet particle-ring animation based on the supplied still-image
  reference. Eight-second periodic loop, bounded shared frame cache, PCM-driven
  input scaling, muted and reduced-motion states. A still image cannot specify
  the original animation's exact motion.
- Compact content/result view and camera-to-animation transitions retain access
  to the composer, diagnostics and dismiss action.
- Code-owned EDITH / Neuron Intelligence / NL / Sadik Laskar product metadata,
  appended to the runtime prompt including prompt-file failure fallback. This is
  a metadata foundation, not a guarantee of injection-proof model responses.

## Remaining stages

| Stage | Implementation and acceptance gate |
| --- | --- |
| Full branch audit | Inventory both branches and every tool/sub-command; reproduce failures; record dependencies, supported OS and real execution evidence. Earlier UI tests are not a full runtime certification. |
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
