"""Preserve the exact first-run source, verified against its pre-recorded hashes.

The launcher gained continuation and automatic source snapshots while run 1 was
already in memory. Reconstruct only that additive edit, never alter trained state.
Any unexpected source difference fails instead of claiming reproducibility.
"""
import hashlib
import json
from pathlib import Path

run=Path('artifacts/replacement/runs/mobilenet224')
env=json.loads((run/'environment.json').read_text())
dest=run/'source';dest.mkdir(exist_ok=True)
for filename,expected in env['code_hashes'].items():
    file=Path(filename);raw=file.read_bytes()
    if hashlib.sha256(raw).hexdigest()!=expected and file.name=='train.py':
        text=raw.decode('utf-8').replace('import shutil\n','')
        text=text.replace("    if args.init_checkpoint:\n        initial=torch.load(args.init_checkpoint,map_location='cpu',weights_only=True)\n        if initial['manifest_sha256']!=manifest_sha or initial['config']['arch']!=args.arch or initial['config']['size']!=args.size:\n            raise ValueError('Explicit continuation checkpoint contract mismatch')\n        model.load_state_dict(initial['model'],strict=True)\n",'')
        text=text.replace("    if args.init_checkpoint: config['init_checkpoint_sha256']=hashlib.sha256(args.init_checkpoint.read_bytes()).hexdigest()\n",'')
        text=text.replace("    (args.out/'source').mkdir(exist_ok=True)\n    for file in Path('scripts/replacement').glob('*.py'): shutil.copy2(file,args.out/'source'/file.name)\n",'')
        text=text.replace("p.add_argument('--checkpoint',type=Path); p.add_argument('--init-checkpoint',type=Path);", "p.add_argument('--checkpoint',type=Path);")
        raw=text.encode('utf-8')
    actual=hashlib.sha256(raw).hexdigest()
    if actual!=expected: raise ValueError(f'Cannot reconstruct {file}: expected {expected}, got {actual}')
    (dest/file.name).write_bytes(raw)
(dest/'receipt.json').write_text(json.dumps(dict(status='all source files match pre-recorded training hashes',hashes=env['code_hashes']),indent=2))
print('All first-run source hashes verified and preserved')
