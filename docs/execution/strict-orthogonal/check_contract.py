"""Read-only RNK plan/receipt shape guard; does not launch or authenticate a runtime."""
from __future__ import annotations
import argparse
import json
from pathlib import Path
from typing import Any

GATES = {f"G{i:02d}" for i in range(1, 15)}
BINDINGS = {
    "repository", "cwd", "worktree_identity", "branch", "source_revision",
    "dirty_fingerprint", "plan_digest", "model", "effort", "permissions_digest",
    "instruction_digest", "first_task", "verification_entry",
}
EVIDENCE = {
    "thread_created", "turn_started", "receipt_verified", "ownership_transfer",
    "owner_readback", "first_task_started", "independent_lifetime",
}


def require(condition: bool, message: str) -> None:
    if not condition:
        raise ValueError(message)


def text(value: Any) -> bool:
    return isinstance(value, str) and bool(value.strip())


def validate(data: dict[str, Any]) -> dict[str, Any]:
    """Check consistency, not the truth or authenticity of referenced evidence."""
    require(isinstance(data, dict), "contract must be an object")
    require(data.get("program") == "RNK-STRICT-ORTHOGONAL", "wrong program")
    completion = data["completion"]
    require(completion.get("main_merge_authorized") is False, "main merge unauthorized")
    require(completion.get("whole_project_mission_complete") is False, "wrong completion scope")
    gates = {g["id"]: g for g in data["gates"]}
    require(len(gates) == len(data["gates"]), "duplicate gate")
    require(set(gates) == set(completion["required_gate_ids"]) == GATES, "required gates changed")
    require(all(g.get("required") is True for g in gates.values()), "required gate demoted")
    tasks = {t["id"]: t for t in data["work_packages"]}
    require(len(tasks) == len(data["work_packages"]), "duplicate task")
    require(set(completion["required_task_ids"]) <= set(tasks), "missing required task")
    require(all(g["owner_task"] in tasks for g in gates.values()), "unknown gate owner")
    pending = {key: set(t["depends_on"]) for key, t in tasks.items()}
    require(all(deps <= set(tasks) for deps in pending.values()), "unknown dependency")
    done: set[str] = set()
    while pending:
        ready = {key for key, deps in pending.items() if deps <= done}
        require(bool(ready), "dependency cycle")
        done.update(ready)
        for key in ready:
            del pending[key]
    require(data["roles"]["shared_writers"] == data["roles"]["host_owners"] == 1, "multiple owners")
    policy = data["handoff_policy"]
    require(policy["shared_writer_limit"] == 1, "handoff multiple writers")
    require(policy["advisor_can_write_shared_state"] is False, "advisor writes state")
    require(policy["advisor_can_change_authority"] is False, "advisor changes authority")
    require(set(policy["required_binding_fields"]) == BINDINGS, "incomplete binding contract")
    state = data["handoff_state"]
    phase = state["phase"]
    require(state.get("mode") in {"NEW_OWNER", "AMEND_EXISTING"}, "unknown handoff mode")
    require(phase in policy["phases"] + policy["exception_states"], "unknown handoff phase")
    require(not state["initial_planner_done"] or phase == "EXECUTION_CONFIRMED", "premature bootstrap Done")
    verified = False
    if phase == "EXECUTION_CONFIRMED":
        for key in ("handoff_id", "planner_thread_id", "sol_thread_id", "sol_turn_id"):
            require(text(state.get(key)), f"missing {key}")
        require(state["sol_thread_id"] != state["planner_thread_id"], "same planner/owner context")
        expected, observed = state["expected"], state["observed"]
        require(isinstance(expected, dict) and isinstance(observed, dict), "missing bindings")
        for key in BINDINGS:
            require(text(expected.get(key)) and expected[key] == observed.get(key), f"binding mismatch: {key}")
        require(expected["repository"] == "46slv/ResolveNodeKit", "wrong receipt repo")
        require(expected["branch"] == data["canonical_branch"], "wrong receipt branch")
        receipt = state["receipt"]
        require(receipt["handoff_id"] == state["handoff_id"], "receipt handoff mismatch")
        require(receipt["thread_id"] == state["sol_thread_id"], "receipt sender mismatch")
        require(receipt["turn_id"] == state["sol_turn_id"], "receipt turn mismatch")
        require(receipt["read_only"] is True, "receiver wrote before transfer")
        owner = state["ownership"]
        previous = state["sol_thread_id"] if state["mode"] == "AMEND_EXISTING" else state["planner_thread_id"]
        require(owner["previous_owner"] == previous, "old owner mismatch")
        require(owner["owner"] == state["sol_thread_id"], "new owner mismatch")
        require(owner["active_writers"] == [state["sol_thread_id"]], "concurrent shared writers")
        require(type(owner["previous_epoch"]) is int and owner["previous_epoch"] >= 0, "bad previous epoch")
        require(type(owner["epoch"]) is int and owner["epoch"] == owner["previous_epoch"] + 1, "bad transfer epoch")
        require(owner["cas_success"] is True and owner["old_writer_fenced"] is True, "unfenced owner")
        require(owner["sol_readback_epoch"] == owner["epoch"], "stale owner readback")
        first = state["first_task_start"]
        require(first["thread_id"] == state["sol_thread_id"], "wrong first-task thread")
        require(first["task_id"] == expected["first_task"] and first["task_id"] in tasks, "wrong first task")
        require(first["owner_epoch"] == owner["epoch"], "first task before transfer")
        for key in EVIDENCE:
            require(text(state["evidence"].get(key)), f"missing evidence ref: {key}")
        verified = True
    product = data.get("status") == completion["output"]
    if product:
        require(verified, "product completion lacks handoff")
        require(text(data.get("candidate_sha")), "missing product candidate")
        for gate in gates.values():
            require(gate["status"] == "PASS", "product gate not PASS")
            require(gate["candidate_sha"] == data["candidate_sha"], "mixed product candidates")
            require(bool(gate["evidence"]), "missing product evidence")
    return {"contract_consistent": True, "handoff_record_consistent": verified,
            "product_completion_record_consistent": product,
            "runtime_evidence_authenticated": False, "host_tests_executed": False}


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("path", nargs="?", type=Path, default=Path(__file__).with_name("acceptance.json"))
    args = parser.parse_args()
    try:
        result = validate(json.loads(args.path.read_text(encoding="utf-8")))
    except (OSError, ValueError, KeyError, TypeError) as exc:
        print(json.dumps({"contract_consistent": False, "error": str(exc)}, ensure_ascii=False))
        raise SystemExit(1)
    print(json.dumps(result, ensure_ascii=False, indent=2))
