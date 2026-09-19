"""Synthetic negative protocol tests only; no Codex, Resolve, network, or fake host PASS."""
import copy
import json
from pathlib import Path
import unittest
from check_contract import validate, BINDINGS, EVIDENCE

BASE = json.loads(Path(__file__).with_name('acceptance.json').read_text(encoding='utf-8'))


def fixture():
    data = copy.deepcopy(BASE)
    data['status'] = 'READY_FOR_RUNTIME_PREFLIGHT'
    binding = {key: f'synthetic-{key}' for key in BINDINGS}
    binding.update(repository='46slv/ResolveNodeKit', branch=data['canonical_branch'], first_task='SO-00')
    data['handoff_state'] = {
        'phase': 'EXECUTION_CONFIRMED', 'mode': 'NEW_OWNER', 'handoff_id': 'synthetic-only',
        'planner_thread_id': 'test-planner', 'sol_thread_id': 'test-sol', 'sol_turn_id': 'test-turn',
        'expected': binding, 'observed': dict(binding),
        'receipt': {'handoff_id': 'synthetic-only', 'thread_id': 'test-sol', 'turn_id': 'test-turn', 'read_only': True},
        'ownership': {'previous_owner': 'test-planner', 'owner': 'test-sol', 'previous_epoch': 4, 'epoch': 5,
                      'active_writers': ['test-sol'], 'cas_success': True, 'old_writer_fenced': True, 'sol_readback_epoch': 5},
        'first_task_start': {'thread_id': 'test-sol', 'task_id': 'SO-00', 'owner_epoch': 5},
        'evidence': {key: 'synthetic://shape-test-not-runtime/' + key for key in EVIDENCE},
        'initial_planner_done': True,
    }
    return data


class ContractTests(unittest.TestCase):
    def reject(self, mutate):
        data = fixture(); mutate(data)
        with self.assertRaises((ValueError, KeyError, TypeError)):
            validate(data)

    def test_initial_publication_has_no_handoff_or_product_proof(self):
        data = copy.deepcopy(BASE)
        data['status'] = 'READY_FOR_RUNTIME_PREFLIGHT'
        data['handoff_state'].update(phase='NOT_STARTED', initial_planner_done=False)
        result = validate(data)
        self.assertFalse(result['handoff_record_consistent'])
        self.assertFalse(result['product_completion_record_consistent'])
        self.assertFalse(result['runtime_evidence_authenticated'])

    def test_complete_synthetic_receipt_does_not_authenticate_runtime(self):
        result = validate(fixture())
        self.assertTrue(result['handoff_record_consistent'])
        self.assertFalse(result['runtime_evidence_authenticated'])

    def test_01_thread_created_is_not_initial_done(self):
        self.reject(lambda d: d['handoff_state'].update(phase='THREAD_CREATED'))

    def test_02_turn_started_is_not_initial_done(self):
        self.reject(lambda d: d['handoff_state'].update(phase='TURN_STARTED'))

    def test_03_plan_ready_is_not_initial_done(self):
        self.reject(lambda d: d['handoff_state'].update(phase='PLAN_READY'))

    def test_04_wrong_model_binding(self):
        self.reject(lambda d: d['handoff_state']['observed'].update(model='not-requested'))

    def test_05_wrong_repository(self):
        self.reject(lambda d: d['handoff_state']['observed'].update(repository='other/repo'))

    def test_06_wrong_plan(self):
        self.reject(lambda d: d['handoff_state']['observed'].update(plan_digest='stale'))

    def test_07_wrong_permissions(self):
        self.reject(lambda d: d['handoff_state']['observed'].update(permissions_digest='expanded'))

    def test_08_missing_binding(self):
        self.reject(lambda d: d['handoff_state']['observed'].pop('instruction_digest'))

    def test_09_null_expected_model(self):
        self.reject(lambda d: d['handoff_state']['expected'].update(model=None))

    def test_10_two_writers(self):
        self.reject(lambda d: d['handoff_state']['ownership'].update(active_writers=['test-planner','test-sol']))

    def test_11_no_transfer_fence(self):
        self.reject(lambda d: d['handoff_state']['ownership'].update(old_writer_fenced=False))

    def test_12_stale_epoch(self):
        self.reject(lambda d: d['handoff_state']['ownership'].update(sol_readback_epoch=4))

    def test_13_first_task_before_transfer(self):
        self.reject(lambda d: d['handoff_state']['first_task_start'].update(owner_epoch=4))

    def test_14_receipt_wrong_thread(self):
        self.reject(lambda d: d['handoff_state']['receipt'].update(thread_id='other-sol'))

    def test_15_missing_actual_start_evidence(self):
        self.reject(lambda d: d['handoff_state']['evidence'].pop('first_task_started'))

    def test_16_receipt_receiver_wrote_early(self):
        self.reject(lambda d: d['handoff_state']['receipt'].update(read_only=False))

    def test_17_advisor_cannot_change_authority(self):
        self.reject(lambda d: d['handoff_policy'].update(advisor_can_change_authority=True))

    def test_18_advisor_cannot_write_shared(self):
        self.reject(lambda d: d['handoff_policy'].update(advisor_can_write_shared_state=True))

    def test_19_required_flatten_cannot_be_demoted(self):
        self.reject(lambda d: d['gates'][3].update(required=False))

    def test_20_task_dependency_cycle(self):
        self.reject(lambda d: d['work_packages'][0].update(depends_on=['SO-90']))

    def test_21_bootstrap_does_not_complete_product(self):
        self.reject(lambda d: d.update(status='STRICT_LAYOUT_RELEASE_CANDIDATE',candidate_sha='test'))

    def test_22_main_merge_still_forbidden(self):
        self.reject(lambda d: d['completion'].update(main_merge_authorized=True))

    def test_23_source_and_product_contract_unchanged(self):
        self.assertEqual(14,len(BASE['gates']))
        self.assertEqual(1100,BASE['performance']['minimum_original_non_group_tools'])
        self.assertEqual(3,BASE['performance']['qualification_runs'])
        self.assertEqual(60,BASE['performance']['per_action_budget_seconds'])

    def test_25_existing_sol_amendment_preserves_owner(self):
        data = fixture()
        data['handoff_state']['mode'] = 'AMEND_EXISTING'
        data['handoff_state']['ownership']['previous_owner'] = 'test-sol'
        self.assertTrue(validate(data)['handoff_record_consistent'])

    def test_26_existing_sol_cannot_be_silently_replaced(self):
        self.reject(lambda d: d['handoff_state'].update(mode='AMEND_EXISTING'))

    def test_27_initial_owner_cannot_adopt_stale_lease(self):
        self.reject(lambda d: d['handoff_state']['ownership'].update(previous_owner='unrelated-live-owner'))

    def test_28_unknown_binding_contract(self):
        self.reject(lambda d: d['handoff_policy']['required_binding_fields'].remove('model'))

    def test_24_ambiguous_is_not_done(self):
        self.reject(lambda d: d['handoff_state'].update(phase='AMBIGUOUS'))


if __name__ == '__main__':
    unittest.main()
