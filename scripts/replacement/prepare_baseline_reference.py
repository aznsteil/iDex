"""Package unchanged baseline tensors for identical validation calibration tooling."""
import hashlib
import json
from pathlib import Path
import torch
from model import make_model,LABELS

root=Path('artifacts/replacement');file=root/'baseline-reference.pt'
if file.exists():raise ValueError('Preserve the existing baseline reference')
torch.set_num_threads(6);model=make_model('baseline').eval()
manifest=root/'data/manifest.jsonl'
state=dict(model=model.state_dict(),config=dict(arch='baseline',size=224,manifest=str(manifest)),labels=json.loads(LABELS.read_text()),manifest_sha256=hashlib.sha256(manifest.read_bytes()).hexdigest(),source_checkpoint_sha256='58e54044ed3ff747a26717313570e4c0b0f2204e7bdfcef7351d011861b2defe')
torch.save(state,file)
(root/'baseline-reference.json').write_text(json.dumps(dict(sha256=hashlib.sha256(file.read_bytes()).hexdigest(),parameters=sum(p.numel() for p in model.parameters()),source_sha256=state['source_checkpoint_sha256'],purpose='Unchanged source tensors; same calibration search as candidate; never modifies app model'),indent=2))
print('Unchanged baseline tensor reference packaged')
