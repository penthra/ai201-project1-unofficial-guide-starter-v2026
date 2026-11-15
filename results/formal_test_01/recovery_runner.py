from datetime import datetime, timezone
import hashlib
import importlib.util
import json
from pathlib import Path

root=Path.cwd()/'results/formal_test_01'
manifest=json.loads((root/'manifest.json').read_text())
for name,expected in manifest['source_sha256_normalized_newlines'].items():
    assert hashlib.sha256(Path(name).read_bytes().replace(b'\r\n',b'\n')).hexdigest()==expected,name
spec=importlib.util.spec_from_file_location('frozen_formal_runner',root/'runner.py')
runner=importlib.util.module_from_spec(spec)
spec.loader.exec_module(runner)
output=root/'trial_3.recovery.client.jsonl'
assert not output.exists(), 'Do not overwrite recovery evidence'
output.touch(exist_ok=False)
commands=root/'trial_3.recovery.commands.sh'
runner.save_json(root/'protocol_clarifications.jsonl',{'timestamp':datetime.now(timezone.utc).isoformat(),'trial':3,'user_correction':'User says service may not have been online when restart completion was reported; asks to try again.','authorized_action':'One separately recorded recovery warm-up on unchanged deployment, then remaining C1/C2/C4/C5 if successful.','initial_http_502_preserved':True,'initial_server_record_http_200_supplied':True,'initial_client_server_id_match_verified':False,'C3_final_verdict_needs_eligibility_review':True})
inputs=json.loads((root/'inputs.json').read_text())
def send(step,criteria,condition,payload=None):
    return runner.send(inputs['url'],3,step,criteria,condition,output,commands,payload)
health=send('recovery_health',['C3'],'after_user_corrected_restart_confirmation')
if not (health.get('response') or {}).get('index_ready'):
    raise SystemExit('Recovery readiness failed; preserve evidence and stop.')
first=send('recovery_answer_and_excluded_warmup',['C3'],'separate_recovery_after_initial_502_excluded_from_C1',{'question':inputs['restart_question']})
if first['http_status']!=200 or (first.get('response') or {}).get('refused') is not False or not first.get('request_id'):
    raise SystemExit('Recovery warm-up unsuccessful; no remaining trials sent.')
for number,entry in enumerate(inputs['in_corpus'],1):
    send(f'project_question_{number}',['C1','C2'],'warm_after_user_authorized_recovery',{'question':entry['question']})
send('invalid_non_string',['C4'],'same_running_service',inputs['invalid_payload'])
send('valid_after_invalid',['C4'],'immediately_after_invalid',{'question':inputs['recovery_question']})
for number,question in enumerate(inputs['out_of_scope'],1):
    send(f'out_of_scope_{number}',['C5'],'warm_after_user_authorized_recovery',{'question':question})
print('Trial 3 remaining requests complete; original 502 and separate recovery preserved. Export matching logs before final scoring.',flush=True)
