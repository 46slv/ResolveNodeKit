# Host checkpoint - Semantic Arrange user install PASS - 2026-09-06

Status: `PASS`. Semantic Arrange is installed into the user-scoped Fusion environment with verified hashes and a Resolve-side import proof. No project mutation, no save.

## Layout (canonical)

- Entry: `%APPDATA%\\Blackmagic Design\\DaVinci Resolve\\Support\\Fusion\\Scripts\\Comp\\ResolveNodeKit_Arrange.py` (byte-identical to repo source)
- Package: `%APPDATA%\\...\\Fusion\\ResolveNodeKit\\src\\resolve_node_kit\\...` (10 files, hashes match repo)
- Manifest: `%APPDATA%\\...\\Fusion\\ResolveNodeKit\\install_manifest.json` (tool, version 1, repo commit, per-file sha256 plus bytes)

Only ResolveNodeKit-owned paths are written. Foreign Comp entries are refused, never overwritten. Backups precede owned-file replacement unless `-Force`.

## Bootstrap (repo-checkout independent)

The installed entry resolves its package in order: `$RNK_SUPPORT_ROOT/ResolveNodeKit/src`, then `<Fusion Support>/ResolveNodeKit/src` found by walking up from its own path, then the repo `src` fallback. `main()` runs only under `__main__`, so the file imports safely. Proven offline by subprocess tests against stub trees with no repo on the path.

## Installer plus tests

- `scripts/install_resolve_user.ps1`: install, manifest write, hash re-verification (fail-closed), backup on owned drift, `-Uninstall` limited to manifest-listed files plus marker-checked entry, foreign-file refusal.
- `tests/test_install_layout.py`: 7 tests (install plus verify, idempotence, repair with backup, uninstall scope, foreign refusal, env-override bootstrap, upward-search precedence), all sandbox-scoped to temp dirs.
- PowerShell 5.1 compat fixes from test failures: no `GetRelativePath`, no `Get-FileHash`; pure .NET hashing and manual relative paths.
- Offline suite 72/72 plus `compileall`.

## Resolve-side verification (worker rnk-installcheck, read-only)

- Single GUI launch, no human gate; Studio 21.0.3.7; project PSD2Fusion observed only.
- Installed-tree import: `sys.path[0]` set to the installed src, `resolve_node_kit.fusion` loaded from the installed tree with `arrange_comp`, `ArrangeDialogState`, `FusionHostError` present. Raw events reference the installed tree 5 times and the repo tree 0 times.
- Comp category listing contains `ResolveNodeKit_Arrange.py`. On-screen menu rendering itself remains for the dialog human gate; no Resolve restart was performed.
- No arrange, no dialog, no graph, timeline, or project mutation. No save, no quit.

## Remaining

- Dialog human gate with the user at the machine.
- Ungroup stays fail-closed until exact restoration is proven on a disposable fixture.
