from datetime import datetime, timezone
import hashlib
import importlib.util
import json
from pathlib import Path

root=Path.cwd()/'results/formal_test_01'
manifest=json.loads((root/'manifest.json').read_text())
for name,expected in manifest['source_sha256_normalized_newlines'].items():
    assert hashlib.sha256(Path(name).read_bytes().replace(b'\r\n',b'\n')).hexdigest()==expected,name
spec=importlib.util.spec_from_file_location('frozen_runner',root/'runner.py')
runner=importlib.util.module_from_spec(spec)
spec.loader.exec_module(runner)
output=root/'c3_final.client.jsonl'
assert not output.exists(), 'Final observation must not be overwritten or repeated.'
output.touch(exist_ok=False)
commands=root/'c3_final.commands.sh'
inputs=json.loads((root/'inputs.json').read_text())
runner.save_json(root/'c3_final.confirmation.jsonl',{'timestamp':datetime.now(timezone.utc).isoformat(),'restart_finished_and_Render_Live_explicitly_confirmed_by_user':True,'original_target_unchanged':True,'score_once_without_retry':True,'deployed_commit_user_attested':manifest['deployed_commit']})
runner.send(inputs['url'],3,'final_confirmed_restart_health',['C3'],'after_explicitly_confirmed_completed_restart',output,commands)
runner.send(inputs['url'],3,'final_confirmed_restart_parking',['C3'],'first_question_after_explicitly_confirmed_completed_restart',output,commands,{'question':inputs['restart_question']})
print('Final C3 observation saved; no retries.',flush=True)
