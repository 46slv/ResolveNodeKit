# Host checkpoint - dialog silent Bootstrap failure plus fix - 2026-09-06

Status: cause proven from log evidence; fix installed; one user click pending.

## Symptom

Menu showed `ResolveNodeKit_Arrange` but pressing it displayed nothing.

## Log evidence (`%TEMP%\\rnk-arrange-run.log`, 3 clicks)

- `start name=__main__ src=` repeated: the script body RAN under `__main__`, so menu-to-exec mapping and the entry guard were never the bug.
- `src=` empty on every run: no bootstrap candidate existed in the menu-exec context.
- `import-error ModuleNotFoundError("No module named resolve_node_kit")`, exit 4, Console-only print the user never saw.

Root cause: Resolve menu-exec provides no usable `__file__`, so path-walk bootstrap and the repo fallback both vanished. No Fusion logs directory was even created, which corroborates the missing root.

## Companion host facts (read-only worker, no dialog, no mutation)

- Resolve script Python is 3.12.10; comp bind works; `AskUser` exists with no doc.
- `AskUser()` with zero args and `AskUser("probe", 12345)` both return None without raising: bad shapes are silent, so shape handling must attempt in order and log each step.

## Fix (installed, backup retained)

- Host-native root discovery without `__file__`: explicit walk, then `fusion.MapPath("Scripts:")` or `"Comp:"` walked up to `Fusion`, then `%APPDATA%` fixed relative path, then repo fallback.
- `resolve.Fusion().GetCurrentComp()` comp fallback alongside `comp` and `fusion` globals.
- Unconditional entry with per-run file logging (entry `__name__`, bootstrap source, every exit path, traceback cap).
- Package-side `ask_arrange_options` tries list then dict controls and logs each attempt; only all-None concludes Cancel.
- Offline: 78/78 plus `compileall`; new host-context tests reproduce the missing-`__file__` exec shape and the APPDATA fallback in sandbox.
- Reinstalled with hash verification; entry byte-identical to repo; manifest commit `0eb9d13`.

## Next

One user menu press. The run log now records dialog attempts, so any remaining shape issue arrives with evidence instead of silence.
