# Ordered implementation ledger

Only published, integrated changes count as implementation. Mocked OS results do
not certify physical hardware. Keep the owner's reference video and layout.

| Step | State | Evidence / next gate |
| --- | --- | --- |
| Audit/plan documents | Published | AUDIT.md, PLAN.md, CAPABILITY_MATRIX.md; full real-device tool certification remains open |
| Narration and CI repair | Published | Previous 191 regressions and push/PR CI pass; owner audio/Windows validation pending |
| 5. Platform interface/adapters | Implemented | SystemController structured results, runtime factory, Windows/macOS/Linux/generic; mocked OS tests. Unified telemetry uses this layer. Existing model tools not all migrated yet. |
| 6. Telemetry collector and UI cache | Implemented | Fault-isolated CPU/per-core/frequency/load/RAM/swap/disk/I/O/network/battery/uptime/process count, optional GPU/temp; Qt reads cache only. Physical sensor validation pending. Process list is available via controller. |
| 7. Unified shell integration | Implemented (scoped) | `core/execution.py` now owns confirmed, streamed argv/shell execution with cwd, timeout, cancellation, source hashing and redacted receipts. `code_helper`, `dev_agent`, desktop generated code and code-file processing use it; 9 integration regressions plus the full 220-test suite pass. Media/FFmpeg and unrelated legacy subprocesses remain for later tool-by-tool migration. |
| 8. Permission tiers integration | Implemented (dispatcher scope) | `tool_tier` now gives every legacy dispatch a backend floor; Tier 2/3 calls require local approval, redacted previews and broker enforcement. Dispatcher-owned approval context prevents duplicate prompts in controlled shell/code workers. 14 permission/execution regressions plus the full 225-test suite pass. Native OS elevation and every independent legacy subprocess remain later migration work. |
| 9. Global kill switch | Pending | Owned controller subprocess cancellation primitive exists; connect all running/queued agent work and legacy child ownership to ESC |
| 10. Complete audit stream | Pending | Controller receipts exist; all tools and UI stream/redaction integration remain |
| 11. Keychain | Pending | Unpublished prototype; no migration in the running release |
| 12–13. Glass UI/live theme | Pending | No prototype UI published; original video/layout unchanged; controller theme probe is not yet live UI theming |
| 14–15. Busy gate / voice approval | Pending | Existing scheduler and manual confirmation remain; voice approvals are not implemented |
| 16–18. Providers/memory/device/HexStrike | Pending upgrades | Existing Gemini/Ollama and tools retained; no claim of new complete adapters/integration |
| 19–20. Performance/release verification | Pending | Need target-device evidence, p50/p95 and full acceptance report |
| 21. Main merge | Not authorized | Owner tests branch first, then explicitly requests merge |

The next implementation task is step 7, then 8, then 9. Do not repeat completed
primitives or call later stages complete simply because a prototype exists.
