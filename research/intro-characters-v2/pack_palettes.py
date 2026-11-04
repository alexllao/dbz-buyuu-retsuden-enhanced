"""Exact palette union packing. Bank0 is fixed; banks1..3 have15 opaque slots."""
import time

def pack_exact(group_colors,fixed_words,max_nodes=1500000,max_seconds=20,free_banks=3):
 fixed=frozenset(fixed_words);sets=sorted(set(map(frozenset,group_colors)),key=lambda s:(-len(s),tuple(sorted(s))))
 maximal=[s for i,s in enumerate(sets) if not any(s<=t for t in sets[:i]) and not s<=fixed]
 all_colors=set().union(*sets);outside=all_colors-set(fixed)
 info=dict(uniqueTargetWords=len(all_colors),uniqueOutsideFixedG=len(outside),maximalGroups=len(maximal),largestGroup=max(map(len,sets),default=0),nodes=0)
 if len(outside)>15*free_banks or info['largestGroup']>15:info['status']='Impossible by unique-color or group-capacity bound';return None,info
 start=time.monotonic();seen=set();aborted=False
 def visit(bins):
  nonlocal aborted
  info['nodes']+=1
  if info['nodes']>max_nodes or time.monotonic()-start>max_seconds:aborted=True;return None
  missing=[s for s in maximal if not any(s<=b for b in bins)]
  if not missing:return bins
  key=tuple(sorted(tuple(sorted(b)) for b in bins[1:]))
  if key in seen:return None
  seen.add(key)
  choices=[]
  for s in missing:
   fits=[(len(s-b),i) for i,b in enumerate(bins[1:],1) if len(b|s)<=15]
   if not fits:return None
   choices.append((len(fits),-len(s),-min(n for n,i in fits),s,fits))
  _,_,_,s,fits=min(choices,key=lambda t:t[:3]);done=set()
  for n,i in sorted(fits):
   old=bins[i]
   if old in done:continue
   done.add(old);updated=list(bins);updated[i]=old|s
   answer=visit(tuple(updated))
   if answer:return answer
   if aborted:return None
  return None
 answer=visit(tuple([fixed]+[frozenset() for _ in range(free_banks)]));info['seconds']=time.monotonic()-start;info['status']='exact' if answer else ('search limit reached, not proof of impossibility' if aborted else 'Exhausted exact union search: infeasible for current native groups')
 return answer,info
