#!/usr/bin/env python3
"""Synthetic record tests only. No web server, HTTP client, or attack execution."""
import copy
import json
from datetime import datetime, timezone
from pathlib import Path
from new_ledger import generate
from validate_ledger import ROOT, validate

checks=0
NOW=datetime(2030,1,1,0,0,1,tzinfo=timezone.utc)
def valid(d): return validate(d,NOW)['valid']
def check(condition,name):
    global checks
    assert condition,name
    checks+=1

def active_example():
    d=generate();d['exampleOnly']=True;d['tests']=d['tests'][:2]
    d['gate'].update(decision='Yes',decidedAt='2030-01-01T00:00:00Z',decidedBy='Example owner')
    d['scopeApproved']=True
    s=d['scope'];s.update(project='Synthetic record fixture',releaseArtifact='fixture-only',environment='local',authorizationReference='Example only; no real permission',approvedBy='Example owner',approvedAt='2030-01-01T00:00:00Z',validFrom='2030-01-01T00:00:00Z',validUntil='2030-01-01T00:01:00Z',targets=[{'id':'fixture','origin':'http://127.0.0.1:9999','environment':'local','ownedBy':'Example owner','authorizationReference':'Example only','allowedPathPrefixes':['/fixture/']}],testAccounts=[{'id':'synthetic-user','role':'tester','tenant':'synthetic','synthetic':True}],allowedMethods=['bounded synthetic fixture checks'],syntheticDataPlan='Synthetic fixture only',evidenceLocation='private example',stopConditions=['Stop on any unexpected side effect or error'],emergencyContact='Example owner',cleanupPlan='No actual resources exist')
    s['backups']['rationale']='Record-only fixture; no state changes exist'
    d['globalBudget'].update(maxRequests=20,maxRequestsPerSecond=2,maxConcurrency=2,maxDurationSeconds=60,maxRequestBytes=1024,maxResponseBytes=4096)
    c=d['coordination'];c.update(singleWriter='coordinator',revision=1,startedAt='2030-01-01T00:00:00Z',deadlineAt='2030-01-01T00:01:00Z')
    for i,t in enumerate(d['tests']):
        t.update(activity='active_test',applicability='Applicable',targetId='fixture',target='http://127.0.0.1:9999/fixture/item',releaseArtifact='fixture-only',owner='Example owner',assignedAgent='worker-'+str(i),status='Ready',approvalReference='Example only',leaseId='lease-'+str(i),budget={'requests':10,'requestsPerSecond':1,'concurrency':1,'seconds':30})
        t['timestamps']['plannedAt']='2030-01-01T00:00:00Z'
        c['activeLeases'].append({'leaseId':t['leaseId'],'testId':t['id'],'assignedAgent':t['assignedAgent'],'issuedAt':'2030-01-01T00:00:00Z','expiresAt':'2030-01-01T00:00:30Z','budget':copy.deepcopy(t['budget']),'remainingRequests':10})
    return d

def mutation(name,change):
    d=active_example();change(d);check(not valid(d),name)

draft=generate()
check(valid(draft),'blank expanded ledger is a valid non-executing draft')
check(len(draft['tests'])==130 and all(t['status']=='Planned' and t['applicability']=='Unreviewed' for t in draft['tests']),'all 130 controls start unexecuted')
check(not draft['scopeApproved'] and draft['gate']['decision']=='Pending' and all(x==0 for x in draft['globalBudget'].values()),'defaults grant no permission or budget')
check(valid(active_example()),'consistent synthetic record validates; exampleOnly remains true')
mutation('Yes without approved scope rejected',lambda d:d.update(scopeApproved=False))
mutation('No blocks active work',lambda d:d['gate'].update(decision='No'))
mutation('Pending blocks active work',lambda d:d['gate'].update(decision='Pending'))
mutation('combined request reservations capped',lambda d:d['globalBudget'].update(maxRequests=19))
mutation('combined concurrency capped',lambda d:d['globalBudget'].update(maxConcurrency=1))
mutation('combined rates capped',lambda d:d['globalBudget'].update(maxRequestsPerSecond=1))
mutation('fixed campaign deadline enforced',lambda d:d['coordination'].update(deadlineAt='2030-01-01T00:02:00Z'))
mutation('expired worker lease rejected',lambda d:d['coordination']['activeLeases'][0].update(expiresAt='2029-12-31T23:59:59Z'))
mutation('real-account record rejected',lambda d:d['scope']['testAccounts'][0].update(synthetic=False))
mutation('production target rejected',lambda d:d['scope']['targets'][0].update(environment='production'))
mutation('outside target rejected',lambda d:d['tests'][0].update(target='https://outside.example.invalid/fixture/item'))
mutation('missing separate load approval rejected',lambda d:d['tests'][0].update(activity='load_test'))
mutation('stop prevents dispatch',lambda d:d['coordination'].update(stopRequested=True,stopReason='owner stop'))
mutation('duplicate assignment rejected',lambda d:d['coordination']['activeLeases'].append(copy.deepcopy(d['coordination']['activeLeases'][0])))
mutation('duplicate test ID rejected',lambda d:d['tests'][1].update(id=d['tests'][0]['id']))
mutation('pass without evidence rejected',lambda d:d['tests'][0].update(status='Passed'))
mutation('invalid applicability cannot pass',lambda d:d['tests'][0].update(applicability='Not applicable',status='Passed',reason='Not applicable'))
mutation('exact fix needs inspected source',lambda d:d['tests'][0]['remediation'].update(basis='Inspected code'))
mutation('boolean is not a numeric cap',lambda d:d['globalBudget'].update(maxRequests=True))
mutation('spent plus reserved reconciles',lambda d:d['coordination']['activeLeases'][0].update(remainingRequests=9))
mutation('case cannot exceed lease allocation',lambda d:d['tests'][0]['budget'].update(requests=100))
mutation('future-issued lease cannot dispatch',lambda d:d['coordination']['activeLeases'][0].update(issuedAt='2030-01-01T00:00:05Z'))
mutation('unsupported embedded retest pass rejected',lambda d:d['tests'][0]['retest'].update(status='Passed'))
mutation('self-linked retest rejected',lambda d:d['tests'][0]['retest'].update(testIds=[d['tests'][0]['id']]))
mutation('plain traversal target rejected',lambda d:d['tests'][0].update(target='http://127.0.0.1:9999/fixture/../admin'))
mutation('encoded traversal target rejected',lambda d:d['tests'][0].update(target='http://127.0.0.1:9999/fixture/%252e%252e/admin'))
d=active_example();d['tests'][0]['activity']='load_test'
d['scope']['loadTestApproval'].update(approved=True,reference='Example only',approvedBy='Example owner',approvedAt='2030-01-01T00:00:05Z',healthStopConditions=['Stop at first unexpected error'])
check(not valid(d),'separate load approval must precede dispatch')

example=json.loads((ROOT/'examples/ledger-dry-run.json').read_text(encoding='utf-8'))
check(valid(example),'No permits separately authorized offline review and retains unrun active cases')
check(example['exampleOnly'] is True and not any(t['status']=='Passed' for t in example['tests']),'example makes no runtime pass claim')
bad=copy.deepcopy(example);bad['scope']['offlineReviewAuthorized']=False
check(not valid(bad),'No does not authorize offline work by itself')
fixture=(ROOT/'examples/unsafe-checkout.txt').read_text(encoding='utf-8')
check('orders.markPaid(request.query.orderId)' in fixture,'example finding cites an actually inspected synthetic statement')
bad=copy.deepcopy(example);bad['tests'][1]['reason']=''
check(not valid(bad),'blocked test must retain exact reason')
print(json.dumps({'passed':checks,'scope':'Pure synthetic ledger consistency tests; no traffic or attacks; exampleOnly records are not authorization'}))
