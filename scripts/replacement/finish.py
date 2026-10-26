"""Validation-only research selection, then one frozen public comparison.

Recoverable: rerunning reuses the immutable selection, never retunes on test.
No production promotion, Core ML claim, upload or remote mutation occurs.
"""
import os
os.environ['OPENBLAS_NUM_THREADS']='1'
os.environ['OMP_NUM_THREADS']='1'
os.environ['MKL_NUM_THREADS']='1'
import hashlib
import json
import subprocess
import sys
from pathlib import Path
from metrics import load_rows,metrics,compare_models

root=Path('artifacts/replacement');labels=json.loads(Path('iDex/Recognition/pokemon_labels.json').read_text())
manifest=root/'data/manifest.jsonl';manifest_sha=hashlib.sha256(manifest.read_bytes()).hexdigest()
policies=root/'policies';policies.mkdir(exist_ok=True)


def stage(name):
    (root/'finish_state.json').write_text(json.dumps(dict(stage=name,selection_frozen=(root/'selection.json').exists()),indent=2))
    print(name,flush=True)


def run(script,*args):
    subprocess.run([sys.executable,f'scripts/replacement/{script}',*map(str,args)],check=True)


def predict(name,arch,checkpoint,split,final=False):
    path=root/'predictions'/f'{name}.jsonl';receipt=path.with_suffix('.metadata.json')
    expected=hashlib.sha256(checkpoint.read_bytes()).hexdigest()
    if path.exists() and receipt.exists():
        meta=json.loads(receipt.read_text())
        if meta.get('checkpoint_sha256')==expected and meta['manifest_sha256']==manifest_sha and meta.get('predictions_sha256')==hashlib.sha256(path.read_bytes()).hexdigest():return path
        raise ValueError(f'Existing prediction provenance mismatch: {path}')
    args=['predict','--arch',arch,'--checkpoint',checkpoint,'--split',split,'--out',path]
    if final:args+=['--final']
    run('train.py',*args);return path


def calibrate(name,checkpoint,predictions):
    out=policies/f'{name}.json'
    if not out.exists():run('choose_candidate.py','--checkpoint',checkpoint,'--predictions',predictions,'--out',out)
    record=json.loads(out.read_text())
    if record['checkpoint_sha256']!=hashlib.sha256(checkpoint.read_bytes()).hexdigest() or record['manifest_sha256']!=manifest_sha or record['validation_predictions_sha256']!=hashlib.sha256(predictions.read_bytes()).hexdigest():raise ValueError('policy provenance mismatch')
    return record


def write(file,data):file.write_text(json.dumps(data,indent=2,allow_nan=False),encoding='utf-8')


def main():
    assert json.loads((root/'runs/efficientnet224-oe/run_status.json').read_text())['status']=='completed'
    base_checkpoint=root/'baseline-reference.pt'
    if not (root/'selection.json').exists():
        stage('calibrate-baseline-validation')
        base_val=predict('baseline-policy-val','baseline',base_checkpoint,'val,ood_val')
        baseline=calibrate('baseline',base_checkpoint,base_val)
        base_summary=metrics(load_rows(base_val),labels)
        variants=[('mobilenet','mobilenet_v3_large',root/'runs/mobilenet224/best.pt',root/'predictions/mobilenet-val.jsonl'),
                  ('efficientnet','efficientnet_b0',root/'runs/efficientnet224/best.pt',root/'predictions/efficientnet-val.jsonl'),
                  ('full','efficientnet_b0',root/'runs/efficientnet224-continued/best.pt',root/'predictions/efficientnet-full-val.jsonl')]
        for epoch in range(1,5):
            name=f'oe-{epoch}';checkpoint=root/f'runs/efficientnet224-oe/epoch-{epoch}.pt'
            stage(f'validation-{name}');pred=predict(f'{name}-val','efficientnet_b0',checkpoint,'val,ood_val')
            variants.append((name,'efficientnet_b0',checkpoint,pred))
        candidates=[]
        for name,arch,checkpoint,pred in variants:
            record=calibrate(name,checkpoint,pred);summary=metrics(load_rows(pred),labels)
            policy=record['policy'];utility=0 if policy.get('abstain_all') else policy['validation_known_coverage']*policy['validation_known_accuracy']
            candidates.append(dict(name=name,arch=arch,checkpoint=str(checkpoint),predictions=str(pred),top1=summary['top1'],macro_recall=summary['macro_recall'],original_unknown_far=summary['unknown_far'],correct_accepted_coverage=utility,policy_file=str(policies/f'{name}.json'),record=record))
        floor=max(base_summary['top1'],max(x['top1'] for x in candidates)-.005)
        eligible=[x for x in candidates if x['top1']>=floor]
        if not eligible:raise ValueError('No candidate matches baseline validation accuracy; keep all candidates unpromoted for diagnosis')
        winner=max(eligible,key=lambda x:(x['correct_accepted_coverage'],x['top1'],-Path(x['checkpoint']).stat().st_size))
        selection=winner['record'];selection.update(research_selection=True,promotion=False,selected_variant=winner['name'],validation_accuracy_floor=floor,
            selection_rule='Validation only: require top1>=baseline and within0.5pp of best candidate; maximize correctly accepted known coverage at separately source-constrained5%FAR and95%accepted-knownprecision. Baseline receives identical calibration. Production still requires independent accuracy and useful coverage evidence.',
            alternatives=[{k:v for k,v in x.items() if k!='record'} for x in candidates],baseline_policy_file=str(policies/'baseline.json'),baseline_val_top1=base_summary['top1'],evaluation_scope_sha256=hashlib.sha256((root/'evaluation_scope.json').read_bytes()).hexdigest())
        write(root/'selection.json',selection)
    selection=json.loads((root/'selection.json').read_text());basepolicy=json.loads((policies/'baseline.json').read_text())['policy'];candpolicy=selection['policy']
    stage('selection-frozen-test-prediction')
    base_test=predict('baseline-test','baseline',base_checkpoint,'test_public,ood_test_public',True)
    cand_test=predict('selected-test',selection['arch'],Path(selection['checkpoint']),'test_public,ood_test_public',True)
    a,b=load_rows(base_test),load_rows(cand_test)
    stage('paired-public-diagnostics')
    write(root/'reports/comparison-all-public.json',compare_models(a,b,labels,baseline_temperature=1,temperature=1,replicates=1000))
    scope=json.loads((root/'evaluation_scope.json').read_text());assert scope['manifest_sha256']==manifest_sha
    ids=set(scope['sha256s']);pa=[r for r in a if r['sha256'] in ids];pb=[r for r in b if r['sha256'] in ids]
    assert len(pa)==len(ids)==len(pb)
    for name,rows in [('baseline-public-unknown',pa),('candidate-public-unknown',pb)]:
        (root/'predictions'/f'{name}.jsonl').write_text(''.join(json.dumps(r)+'\n' for r in rows),encoding='utf-8')
    write(root/'reports/comparison-public-unknown-exposure.json',compare_models(pa,pb,labels,baseline_temperature=1,temperature=1,replicates=1000))
    if not basepolicy.get('abstain_all') and not candpolicy.get('abstain_all'):
        write(root/'reports/comparison-frozen-policies.json',compare_models(a,b,labels,confidence=candpolicy['confidence'],margin=candpolicy['margin'],temperature=candpolicy['temperature'],baseline_confidence=basepolicy['confidence'],baseline_margin=basepolicy['margin'],baseline_temperature=basepolicy['temperature'],replicates=1000))
    run('analyze_predictions.py','--baseline',base_test,'--candidate',cand_test,'--manifest',manifest,'--labels','iDex/Recognition/pokemon_labels.json','--out',root/'reports/final-analysis','--selection',root/'selection.json')
    stage('prepare-private-mac-handoff')
    if not (root/'handoff/bundle_receipt.json').exists():run('prepare_handoff.py')
    stage('completed-windows-pending-independent-camera-and-apple')


if __name__=='__main__':main()
