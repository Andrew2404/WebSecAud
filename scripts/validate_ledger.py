#!/usr/bin/env python3
"""Check audit-record consistency. Never sends traffic or authorizes execution."""
from __future__ import annotations
import json
import math
from datetime import datetime, timezone
from pathlib import Path
import sys
from urllib.parse import urlsplit, unquote

ROOT = Path(__file__).resolve().parent.parent
STATUSES = {'Planned','Ready','Running','Passed','Failed','Blocked','Skipped','Not run','Retest pending','Retest passed','Retest failed'}
RESULTS = {'Passed','Failed','Retest pending','Retest passed','Retest failed'}
ACTIVE_STATES = RESULTS | {'Ready','Running'}
ACTIVITIES = {'offline_review','active_test','load_test'}
SEVERITIES = {'Unassessed','Low','Medium','High','Critical'}

def fresh_record(control):
    return {'id':'TEST-'+control['id'],'category':control['domain'],'controlIds':[control['id']],
      'activity':'active_test','applicability':'Unreviewed','targetId':'','target':'','releaseArtifact':'','owner':'','assignedAgent':'',
      'safeMethod':control['verify'],'expected':control['pass'],'status':'Planned',
      'reason':'Resolve applicability, activity, target, authority, identities and budget before execution.',
      'approvalReference':'','leaseId':None,'budget':{'requests':0,'requestsPerSecond':0,'concurrency':0,'seconds':0},
      'timestamps':{'plannedAt':None,'startedAt':None,'finishedAt':None,'updatedAt':None},'requestsUsed':0,
      'observed':'','evidence':[],'severity':'Unassessed',
      'remediation':{'recommendation':'','basis':'Uninspected','codeReferences':[],'owner':'','fixArtifact':''},
      'retest':{'status':'Not run','testIds':[],'releaseArtifact':'','evidence':[],'remainingRisk':''}}

def stamp(value):
    if not isinstance(value,str) or not value.endswith('Z'): raise ValueError('timestamp must be UTC ISO 8601 ending Z')
    return datetime.fromisoformat(value[:-1]+'+00:00')

def canonical_path(path):
    current=path
    for _ in range(5):
        decoded=unquote(current)
        if '\\' in decoded or any(part in {'.','..'} for part in decoded.split('/')): return False
        if decoded==current: return True
        current=decoded
    return False

def validate(data, now=None):
    """Return errors plus a non-authoritative record summary; drafts may be valid."""
    errors=[]
    def require(ok,msg):
        if not ok: errors.append(msg)
    def nonempty(value): return isinstance(value,str) and bool(value.strip())
    def number(value): return type(value) in (int,float) and math.isfinite(value) and value>=0
    def time(value,label,required=False):
        if value is None:
            if required: errors.append(label+' is required')
            return None
        try: return stamp(value)
        except (ValueError,TypeError): errors.append(label+' is invalid'); return None
    now=now or datetime.now(timezone.utc)
    try:
        require(data['version']==1,'unsupported ledger version')
        require(type(data['exampleOnly']) is bool,'exampleOnly must be boolean')
        gate=data['gate']; scope=data['scope']; global_budget=data['globalBudget']; coord=data['coordination']; tests=data['tests']
        require(gate['prompt']=='Are you ready to get hacked?','exact gate prompt is missing')
        require(gate['decision'] in {'Pending','Yes','No'},'invalid gate decision')
        require(type(data['scopeApproved']) is bool,'scopeApproved must be boolean')
        require(type(scope['offlineReviewAuthorized']) is bool,'offline authorization must be boolean')
        if gate['decision']!='Pending':
            time(gate['decidedAt'],'gate.decidedAt',True); require(nonempty(gate['decidedBy']),'gate decision needs an owner')
        for k,v in global_budget.items(): require(number(v),'invalid global budget '+k)
        for k in ('maxRequests','maxConcurrency','maxDurationSeconds','maxRequestBytes','maxResponseBytes'):
            require(type(global_budget[k]) is int,'integer cap required: '+k)
        require(type(coord['revision']) is int and coord['revision']>=0,'invalid ledger revision')
        require(type(coord['stopRequested']) is bool,'stopRequested must be boolean')
        if coord['stopRequested']: require(nonempty(coord['stopReason']),'stop request needs a reason')
        start=time(coord['startedAt'],'campaign start'); deadline=time(coord['deadlineAt'],'campaign deadline')
        if start and deadline: require(0<(deadline-start).total_seconds()<=global_budget['maxDurationSeconds'],'campaign duration exceeds cap')
        require(type(coord['usedRequests']) is int and coord['usedRequests']>=0,'invalid cumulative request count')
        require(coord['usedRequests']<=global_budget['maxRequests'],'cumulative requests exceed cap')
        require(isinstance(tests,list),'tests must be a list')
        ids=[t['id'] for t in tests]; require(len(ids)==len(set(ids)),'duplicate test IDs')
        by_id={t['id']:t for t in tests}
        catalog=json.loads((ROOT/'references/controls.json').read_text(encoding='utf-8'))
        control_ids={c['id'] for c in catalog['controls']}
        target_ids=[t['id'] for t in scope['targets']]; require(len(target_ids)==len(set(target_ids)),'duplicate target IDs')
        targets={t['id']:t for t in scope['targets']}
        leases=coord['activeLeases']; history=coord['leaseHistory']; all_leases=leases+history
        lease_ids=[l['leaseId'] for l in all_leases]; require(len(lease_ids)==len(set(lease_ids)),'duplicate lease IDs')
        require(len([l['testId'] for l in leases])==len({l['testId'] for l in leases}),'multiple active leases for one test')
        lease_map={l['leaseId']:l for l in all_leases}
        for lease in all_leases:
            require(lease['testId'] in by_id,'lease references unknown test')
            require(nonempty(lease['assignedAgent']),'lease needs assigned agent')
            issued=time(lease['issuedAt'],'lease issue',True); expires=time(lease['expiresAt'],'lease expiry',True)
            b=lease['budget']
            for k in ('requests','requestsPerSecond','concurrency','seconds'): require(number(b[k]) and b[k]>0,'lease budget must be positive: '+k)
            require(type(b['requests']) is int and type(b['concurrency']) is int,'lease count/concurrency must be integers')
            if issued and expires:
                require(0<(expires-issued).total_seconds()<=b['seconds'],'lease duration exceeds allocation')
                if start and deadline: require(start<=issued<expires<=deadline,'lease exceeds fixed campaign window')
            if lease in leases:
                require(type(lease['remainingRequests']) is int and 0<=lease['remainingRequests']<=b['requests'],'invalid remaining reservation')
                if expires: require(expires>now,'active lease has expired; verify stop and reconcile it')
                test=by_id.get(lease['testId'])
                if test: require(lease['remainingRequests']+test['requestsUsed']==b['requests'],'spent and remaining lease requests do not reconcile')
            else:
                require(lease['state'] in {'Closed','Revoked','Uncertain'},'invalid historical lease state')
                time(lease['closedAt'],'lease closure',True)
                require(type(lease['requestsUsed']) is int and 0<=lease['requestsUsed']<=b['requests'],'invalid historical use')
                require(lease['state']!='Uncertain','uncertain worker must retain an active reservation until verified stopped')
                test=by_id.get(lease['testId'])
                if test: require(lease['requestsUsed']==test['requestsUsed'],'historical lease and case request use differ')
            test=by_id.get(lease['testId'])
            if test:
                for k in ('requests','requestsPerSecond','concurrency','seconds'):
                    require(test['budget'][k]<=b[k],test['id']+': case allocation exceeds lease '+k)
                require(test['requestsUsed']<=b['requests'],test['id']+': actual requests exceed lease')
        require(coord['usedRequests']+sum(l['remainingRequests'] for l in leases)<=global_budget['maxRequests'],'combined request reservations exceed cap')
        require(sum(l['budget']['requestsPerSecond'] for l in leases)<=global_budget['maxRequestsPerSecond'],'combined rates exceed cap')
        require(sum(l['budget']['concurrency'] for l in leases)<=global_budget['maxConcurrency'],'combined concurrency exceeds cap')
        require(sum(t['requestsUsed'] for t in tests)==coord['usedRequests'],'request totals must include every setup/test/retry/retest/cleanup record')
        active_records=[t for t in tests if t['activity']!='offline_review' and t['status'] in ACTIVE_STATES]
        if leases or active_records:
            require(gate['decision']=='Yes' and data['scopeApproved'],'active work requires Yes plus approved scope')
            for k in ('project','releaseArtifact','authorizationReference','approvedBy','syntheticDataPlan','evidenceLocation','emergencyContact','cleanupPlan'):
                require(nonempty(scope[k]),'active scope missing '+k)
            require(scope['catalogVersion']==catalog['version'],'scope catalog does not match this package')
            require(scope['environment'] in {'local','staging'},'active environment must be local/staging')
            require(nonempty(coord['singleWriter']),'single ledger writer is required')
            approved=time(scope['approvedAt'],'scope approval',True)
            valid_from=time(scope['validFrom'],'scope validFrom',True); valid_until=time(scope['validUntil'],'scope validUntil',True)
            if valid_from and valid_until: require(valid_from<valid_until,'invalid scope window')
            require(bool(scope['targets']) and bool(scope['testAccounts']) and bool(scope['allowedMethods']) and bool(scope['stopConditions']),'active targets/accounts/methods/stops required')
            for k in ('maxRequests','maxRequestsPerSecond','maxConcurrency','maxDurationSeconds','maxRequestBytes','maxResponseBytes'):
                require(global_budget[k]>0,'active cap must be positive: '+k)
            require(start is not None and deadline is not None,'fixed campaign start/deadline required')
            if valid_from and valid_until and start and deadline: require(valid_from<=start<deadline<=valid_until,'campaign outside authorized window')
            if start:
                if approved: require(approved<=start,'scope approval must precede campaign')
                decided=time(gate['decidedAt'],'gate decision',True)
                if decided: require(decided<=start,'Yes decision must precede campaign')
            for account in scope['testAccounts']:
                require(account['synthetic'] is True,'active accounts must be synthetic')
                for k in ('id','role','tenant'): require(nonempty(account[k]),'test account missing '+k)
            backups=scope['backups']; require(nonempty(backups['rationale']),'backup applicability rationale required')
            if backups['required']:
                time(backups['verifiedAt'],'backup verification',True)
                require(nonempty(backups['restorePlan']) and nonempty(backups['owner']),'verified restore plan/owner required')
            for target in scope['targets']:
                url=urlsplit(target['origin'])
                require(url.scheme in {'http','https'} and bool(url.hostname) and not url.username and not url.password and url.path in ('','/'),'target needs an explicit credential-free HTTP(S) origin')
                require(target['environment'] in {'local','staging'} and nonempty(target['ownedBy']) and nonempty(target['authorizationReference']),'target ownership/environment/authority missing')
                require(bool(target['allowedPathPrefixes']) and all(isinstance(x,str) and x.startswith('/') and canonical_path(x) for x in target['allowedPathPrefixes']),'explicit canonical allowed paths required')
        for test in tests:
            label=test['id']+': '
            require(nonempty(test['id']) and nonempty(test['category']) and nonempty(test['safeMethod']) and nonempty(test['expected']),label+'plan fields missing')
            require(bool(test['controlIds']) and all(x in control_ids for x in test['controlIds']),label+'unknown control IDs')
            require(test['activity'] in ACTIVITIES and test['status'] in STATUSES,label+'invalid activity/status')
            require(test['applicability'] in {'Unreviewed','Applicable','Not applicable'},label+'invalid applicability')
            require(test['severity'] in SEVERITIES,label+'invalid severity')
            require(type(test['requestsUsed']) is int and test['requestsUsed']>=0,label+'invalid request count')
            for k,v in test['budget'].items(): require(number(v),label+'invalid budget '+k)
            require(test['requestsUsed']<=test['budget']['requests'],label+'case request cap exceeded')
            if test['status'] in {'Blocked','Skipped','Not run'} or test['applicability']=='Not applicable': require(nonempty(test['reason']),label+'reason required')
            if test['status'] in ACTIVE_STATES:
                require(test['applicability']=='Applicable',label+'executed/ready case must be applicable')
                require(nonempty(test['owner']) and nonempty(test['assignedAgent']) and nonempty(test['approvalReference']) and nonempty(test['releaseArtifact']),label+'owner/agent/authority/artifact required')
                time(test['timestamps']['plannedAt'],label+'plannedAt',True)
                if test['activity']=='offline_review':
                    require(scope['offlineReviewAuthorized'] and nonempty(scope['authorizationReference']),label+'offline review not authorized')
                    require(test['requestsUsed']==0,label+'offline review cannot send requests')
                else:
                    target=targets.get(test['targetId']); require(target is not None,label+'unknown target')
                    lease=lease_map.get(test['leaseId']); require(lease is not None,label+'missing retained lease')
                    if target:
                        a=urlsplit(test['target']); b=urlsplit(target['origin'])
                        require(a.scheme==b.scheme and a.netloc==b.netloc and canonical_path(a.path) and any(a.path.startswith(p) for p in target['allowedPathPrefixes']),label+'target outside canonical approved origin/paths')
                    if lease: require(lease['testId']==test['id'] and lease['assignedAgent']==test['assignedAgent'],label+'lease assignment mismatch')
                    if test['status'] in {'Ready','Running'}:
                        require(not coord['stopRequested'],label+'stop requested; no dispatch permitted')
                        require(lease in leases,label+'Ready/Running needs outstanding lease')
                        if start and deadline: require(start<=now<deadline,label+'outside current campaign window')
                        if lease: require(stamp(lease['issuedAt'])<=now<stamp(lease['expiresAt']),label+'lease is not currently valid')
                    if test['activity']=='load_test':
                        approval=scope['loadTestApproval']
                        require(approval['approved'] is True and nonempty(approval['reference']) and nonempty(approval['approvedBy']) and bool(approval['healthStopConditions']),label+'separate load approval and health stops required')
                        load_approved=time(approval['approvedAt'],label+'load approval time',True)
                        if load_approved and lease: require(load_approved<=stamp(lease['issuedAt']),label+'separate load approval must precede lease/dispatch')
            if test['status'] in RESULTS:
                begun=time(test['timestamps']['startedAt'],label+'startedAt',True); finished=time(test['timestamps']['finishedAt'],label+'finishedAt',True)
                require(nonempty(test['observed']) and bool(test['evidence']),label+'observed result and evidence required')
                if begun and finished: require(begun<=finished,label+'timestamps reversed')
                if test['activity']!='offline_review' and test['leaseId'] in lease_map:
                    lease=lease_map[test['leaseId']]
                    if begun and finished: require(stamp(lease['issuedAt'])<=begun<=finished<=stamp(lease['expiresAt']),label+'execution outside lease window')
            if test['status']=='Running':
                begun=time(test['timestamps']['startedAt'],label+'startedAt',True)
                if begun:
                    require(begun<=now,label+'Running start is in future')
                    if test['activity']!='offline_review' and test['leaseId'] in lease_map:
                        lease=lease_map[test['leaseId']]
                        require(stamp(lease['issuedAt'])<=begun<stamp(lease['expiresAt']),label+'Running start outside lease')
            require(test['remediation']['basis'] in {'Uninspected','Inspected code','Conditional guidance'},label+'invalid fix basis')
            if test['remediation']['basis']=='Inspected code': require(bool(test['remediation']['codeReferences']),label+'exact fix requires inspected code references')
            require(test['retest']['status'] in STATUSES,label+'invalid retest status')
            require(all(x in by_id for x in test['retest']['testIds']),label+'unknown retest IDs')
            require(test['id'] not in test['retest']['testIds'],label+'retest must be a distinct case')
            if test['status'] in {'Retest passed','Retest failed'} or test['retest']['status'] in RESULTS:
                require(bool(test['retest']['testIds']) and nonempty(test['retest']['releaseArtifact']) and bool(test['retest']['evidence']),label+'retest artifact/case/evidence required')
                for linked_id in test['retest']['testIds']:
                    linked=by_id.get(linked_id)
                    if linked:
                        require(linked['status'] in RESULTS and bool(linked['evidence']) and linked['releaseArtifact']==test['retest']['releaseArtifact'],label+'linked retest lacks executed evidence/artifact')
                        if test['retest']['status'] in {'Passed','Retest passed'} or test['status']=='Retest passed':
                            require(linked['status'] in {'Passed','Retest passed'},label+'claimed successful retest links a non-pass')
        summary={'valid':not errors,'exampleOnly':data['exampleOnly'],'tests':len(tests),'statuses':{s:sum(t['status']==s for t in tests) for s in sorted(STATUSES)},'gate':gate['decision'],'scopeApproved':data['scopeApproved'],'errors':errors,'notice':'Record validation only: no traffic was sent, no authority verified, no test dispatched, and no security pass granted.'}
    except (KeyError,TypeError,ValueError,AttributeError) as exc:
        errors.append('Malformed ledger structure: '+str(exc)); summary={'valid':False,'errors':errors}
    return summary

if __name__=='__main__':
    try:
        path=Path(sys.argv[1])
        if path.stat().st_size>4*1024*1024: raise ValueError('ledger exceeds 4 MiB limit')
        result=validate(json.loads(path.read_text(encoding='utf-8')))
        print(json.dumps(result,indent=2)); raise SystemExit(0 if result['valid'] else 1)
    except (IndexError,OSError,ValueError,RecursionError) as exc:
        print('Usage: python scripts/validate_ledger.py LEDGER.json\n'+str(exc),file=sys.stderr); raise SystemExit(2)
