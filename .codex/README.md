# Codex MCP and skill registration

Repository-backed STDIO MCP servers use two Codex configuration layers:

- `~/.codex/config.toml` owns machine-specific transport: absolute `command`,
  absolute script arguments, absolute `cwd`, and `enabled = false`.
- This repository's `.codex/config.toml` owns activation and project policy:
  `enabled`, `required`, tool allowlists, timeouts, and approval rules.

Codex merges trusted project configuration over user configuration. The split
keeps local paths out of Git and prevents the server from starting in unrelated
projects. See the [official Codex configuration reference](https://learn.chatgpt.com/docs/config-file/config-reference)
for the supported MCP fields and configuration scopes.

## Required `cc002` machine registration

Before opening or resuming a Codex task in this checkout, merge
[`cc002.user.example.toml`](cc002.user.example.toml) into
`~/.codex/config.toml` and replace all placeholder paths with absolute local
paths.

The project table is intentionally not standalone-valid. Without the
machine-level transport, Codex rejects `mcp_servers.cc002` before a task can
start. Do not work around that refusal by committing local paths, changing
`required`, or falling back to a shell command.

Codex `0.149.0-alpha.4.1` also rejects this policy-only project table when
started with `--strict-config`, before it merges the user transport. Normal
Codex Desktop and CLI startup do merge the layers. Verify the resolved table
and a normal startup as shown below; do not duplicate the transport in Git to
silence strict validation.

After changing either layer, run these checks:

```bash
cd /
codex mcp get cc002 --json
cd /absolute/path/to/malleus-dev
codex mcp get cc002 --json
```

The first result must show `enabled: false`. The second must show
`enabled: true`, `cc002_acquire` and `cc002_verify_offline`, and absolute
values for `command`, the adapter script argument, and `cwd`. Restart Codex
after registration changes so new and resumed tasks initialize from the
resolved configuration.

## Mandatory rule for new MCP servers and dependent skills

Any change that adds a repository-backed MCP server, or a skill that requires
one, must include all of the following in the same change:

1. A user-config example with an absolute executable, absolute repository
   script path, absolute repository working directory, and `enabled = false`.
2. Project configuration containing activation and policy only. Never commit
   `cwd = "."`, a relative repository script, or a local absolute path there.
3. A launch test whose caller starts in `/` and completes the actual STDIO
   discovery sequence: `initialize`, `notifications/initialized`, then a
   metadata-bearing `tools/list`. Parsing TOML or stopping after `initialize`
   is not a launch test. MCP request `_meta` is protocol metadata and must not
   be rejected as a tool argument.
4. A skill preflight that names the required MCP server and tools, points to
   this document, and fails with the missing registration or tool name. It must
   not silently use a shell or legacy fallback.
5. An explicit decision about `required`. Set it only when startup must fail
   closed and the registration test passes.

Codex Desktop's app server can run with `/` as its process working directory.
Relative MCP paths therefore depend on ambient process state and are forbidden
for repository-backed servers.
