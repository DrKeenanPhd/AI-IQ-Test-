# Dashboard & Results UI Plan

Purpose: Define a practical, scalable UI/UX for the Results and ongoing Dashboard experiences that leverages Abacus DeepAgent structured outputs and ChatGPT to guide users, generate solutions, and present contextual visualizations without overwhelming screen real estate.

---

1) UX goals
- Be a solutions engine: identify issues, organize remedies, and produce assets (scripts, emails, schemas, etc.).
- Keep the agent present but unobtrusive: minimized voice control, movable/minimizable transcription pod, contextual side panel.
- Make historical sessions easy to access: left sidebar with sessions; quick switch and comparison.
- Progressive disclosure: show a clean overview first; let the agent reveal detail as needed.
- Clear upgrade paths: basic vs premium features are visible but gated with helpful prompts.

2) Information architecture
- Global header: brand, user menu, subscription badge, actions (New Session, Upgrade, Help).
- Left sidebar: 
  - Sessions tab (default): searchable list of sessions with title/date and quick badges (score, tier).
  - Saved assets tab: generated content (scripts, emails, schema, checklists) with filters and export actions.
- Main content area (center):
  - Results/Overview tab: score, key metrics, top findings, quick recommendations.
  - Diagnostics tab: detailed findings grouped by category (website, social, search, AI readiness).
  - Solutions tab: curated playbooks and prioritized task lists, accept/apply CTA, versioned.
  - Build/Assets tab: generated assets (video scripts, emails, schema, etc.) with edit/approve/export.
  - Activity tab: timeline of events, agent notes, user actions, exports.
- Right contextual panel: agent-triggered side panel that shows charts, key metrics, checklists, or resource cards related to the current discussion; can be pinned, collapsed, or auto-hide.
- Floating voice agent control: compact toggle to start/stop; opens minimized controls; transcription appears in a draggable, resizable pod with download link after session.

3) Layout behavior
- Desktop: three-column when active (sidebar, main, contextual). Context panel can overlay or dock.
- Tablet: sidebar collapsible; context panel overlays with backdrop; voice/transcript floats.
- Mobile: top-level tabs; sidebar and contextual panel open as sheets; transcript pod becomes a bottom sheet.

4) DeepAgent output → UI mapping
- Expect structured payloads from Abacus DeepAgent and ChatGPT. Normalize into the following UI-ready types:
  - Metric: id, label, value, target, delta, unit, category.
  - Finding: id, category, severity, summary, evidence, related_metrics[].
  - Opportunity: id, impact, effort, rationale, linked_findings[].
  - Task: id, title, steps[], owner, est_time, prerequisites[], links[].
  - Playbook: id, title, tasks[], expected_outcomes, dependencies.
  - ContentAsset: id, type (video_script/email/schema/blog), title, body, metadata, status (draft/approved/published), version.
  - ChartSpec: id, type, labels[], series[], theme, caption.
  - Checklist: id, title, items[{text, done}], hint.
  - ResourceLink: id, title, url, source (YouTube/Article), thumbnail.
- Store raw agent payloads, and also the normalized forms for rendering.

5) Contextual side panel contract
- The agent can trigger panel updates via structured actions:
  - ui.show_panel { kind: "chart" | "checklist" | "metrics" | "resources", payload: ChartSpec | Checklist | Metric[] | ResourceLink[] }
  - ui.highlight { sectionId: "overview|diagnostics|solutions|assets" }
  - ui.switch_tab { tabId: "overview|diagnostics|solutions|assets|activity" }
  - ui.create_asset { asset: ContentAsset } (adds to Build/Assets and focuses the card)
  - ui.prompt_upgrade { feature: "session_history|assets|deep_diagnostics", requiredTier: "premium" }
- Frontend listens to agent messages, parses these actions, and updates UI without reflowing the chat.

6) Visualization layer
- Primary: Recharts or Nivo for in-app charts with a dark theme and brand colors.
- Secondary: QuickChart for server-generated images when pre-render is helpful (emails/exports/PDFs).
- The agent may return ChartSpec; renderer chooses library accordingly.

7) Voice agent + transcription UX
- Voice agent button: floating, minimal; shows status (idle/listening/thinking).
- Transcript pod: draggable, resizable, minimizable; opacity control; save/download (.txt) after session; store in session timeline.
- Accessibility: keyboard controls, captioning toggle.

8) Session history sidebar
- Sessions list: title, date, score, tier badge, duration; search and filters (range, category).
- Actions: rename, star, duplicate, archive. Premium: compare up to 2 sessions in split view.
- Clicking a session loads its data into center tabs; agent greets with session context.

9) Subscription gating
- Basic: Overview tab, limited Solutions (top 3 tasks), last session only, no Assets editing, transcript download only.
- Premium: Full Diagnostics, unlimited session history, Assets editor and export, compare sessions, advanced charts.
- Gating UX: show preview cards with lock icon and an Upgrade CTA; agent can trigger ui.prompt_upgrade.

10) Export & integration actions
- Asset cards: Approve, Export to GHL (email campaign, funnel copy, schema), Copy, Download.
- Charts: Export image, Add to report, Email summary.
- Tasks/Playbooks: Push to GHL tasks/pipelines; schedule reminders.

11) API surface (backend)
- GET /sessions (list by user)
- GET /sessions/{id} (detail)
- POST /sessions (create)
- POST /sessions/{id}/assets (create/update)
- GET /assets (list by user)
- POST /agent/events (log ui actions, optional)
- POST /export/ghl (push assets/tasks)
- GET /panel-content?topic=... (optional lazy content)
- Smart token endpoints (covered elsewhere): POST /tokens, POST /tokens/validate, POST /tokens/use

12) Data persistence (Supabase)
- tables: users, sessions, session_metrics, session_findings, session_tasks, assets, charts, transcripts, events, tokens.
- Store agent raw payloads in session_raw (jsonb) for traceability, plus normalized tables for performance.

13) Implementation phases
- Phase 1: UI skeleton
  - Header, sidebar (sessions), tabs scaffold, floating voice button, empty context panel; fake data.
- Phase 2: Data plumbing
  - Supabase schemas; FastAPI endpoints for sessions list/detail; render real data; theme charts.
- Phase 3: Agent event bridge
  - Parse agent actions (ui.show_panel, ui.switch_tab, etc.); display context panel content; basic checklist.
- Phase 4: Assets builder
  - ContentAsset cards; save/version in Supabase; export stubs to GHL.
- Phase 5: Transcription pod
  - Draggable/minimizable transcript; store and download; tie to session timeline.
- Phase 6: Subscription gating + smart tokens
  - Enforce Basic vs Premium; token validation on load; upgrade CTAs.
- Phase 7: Polish and exports
  - QuickChart integration for export-ready images; email/ PDF generation; performance, a11y.

14) Guardrails & best practices
- Keep the agent authoritative but not intrusive; panel should aid, not distract.
- Favor progressive disclosure; avoid clutter.
- Maintain a clear audit trail (raw agent outputs, user decisions, exports).
- Always sanitize any HTML/SVG returned by agents.
- Respect token/session limits and protect all data routes with token/user auth.

This plan aligns with the current stack (FastAPI backend, Supabase DB, Vercel frontend, GHL + Vapi integrations, Abacus/ChatGPT orchestration) and can be implemented incrementally without blocking on any single integration.

21) Scoring model and versioning
- Support configurable max score (default 200). Display badge as X/200 and normalize charts to 0–100%.
- Persist: results carry {schema_version, score_max, score_raw, score_norm, breakdown[]}.
- UI uses score_norm for visuals; copies can reference score_max dynamically.
- Allow multiple schema versions to coexist (v1 full test, v2 updated prompts); store mapping in code to keep UI stable.


15) Unified page strategy and test cadence
- Single route for both Results and Transformation: one page adapts to user state (visitor/free/basic/premium) and recency of tests.
- Top-left AI IQ score badge: shows latest monthly score, last updated date, delta vs prior month, and a tooltip with next eligible full test date.
- Full test policy: one full test every 30 days per account. Backend enforces via test_runs table (type="full"), with fields last_full_test_at and next_eligible_at derived.
- Individual diagnostics (mini-tests): unlimited for premium; limited for basic (e.g., 3 per week). Orchestrated by agent or user buttons.
- UI controls:
  - Primary CTA: "Run full test" (disabled with countdown until eligible; agent can explain).
  - Secondary: Quick diagnostics menu (Website, Social, Search, AI Readiness).
- Agent prompts: agent proposes when to run mini-tests and schedules the next full test; can queue tests in background and notify when ready.

16) Orchestration via Vapi widget (minimized)
- The Vapi widget runs minimized; a bridge listens to agent tool invocations or message tags and dispatches UI actions described in section 5.
- Define callable tools for the agent:
  - run_full_test(userId)
  - run_mini_test(userId, topic)
  - get_latest_results(userId)
  - show_panel(kind, payload)
  - create_asset(asset)
  - prompt_upgrade(feature, requiredTier)
- Implementation options:
  - Direct tool calling if Vapi supports function/tool APIs to your backend.
  - If not, the agent emits structured tags in messages; frontend parses and calls backend.
- Resilience: all tool calls are idempotent and return operation ids; UI polls job status.

17) Scheduling and background jobs
- Use Vercel Cron or Supabase pg_cron for monthly re-checks and reminders (e.g., nudge to run full test near eligibility).
- Long-running diagnostics run asynchronously:
  - POST creates a job (queued state), returns job_id.
  - Webhook or polling updates status; results written to test_runs and sessions.

18) Storage model additions
- test_runs: id, user_id, type(full|mini), topic, status(queued|running|complete|failed), started_at, completed_at, score, payload(jsonb), source(agent|ui), created_by, next_eligible_at(derived for full).
- iq_scores: id, user_id, score, period_month, computed_at, deltas.
- Enforce cadence by querying latest full run within 30 days; backend blocks and returns next_eligible_at.

19) Tier-based limits and UX
- Basic: Full test monthly, mini-tests limited; Solutions tab shows top 3 tasks; Assets read-only.
- Premium: Unlimited mini-tests, full diagnostics, asset editing/export, compare sessions.
- Clear gating with informative countdowns and agent explanations.

20) Practicality & risks
- Feasible: single-page adaptive UI reduces navigation overhead; agent-led orchestration increases engagement.
- Risks: widget–UI sync; mitigate with a strict action protocol and fallbacks; async job handling for long diagnostics; careful rate limits.
- Success metrics: completion of full tests monthly, mini-test engagement, asset approvals/exports, upgrade conversions.

