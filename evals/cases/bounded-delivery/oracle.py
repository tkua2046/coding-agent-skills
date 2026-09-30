import json
import os
import sys
from pathlib import Path

sys.path.insert(0, os.getcwd())
from inventory import reserve
from batch import execute
orders=[{"id":"reject","items":[["a",1],["b",3]]},{"id":"accept","items":[["a",2],["b",1]]}]
stock={"a":2,"b":1}
expected=({"a":0,"b":0},[{"order_id":"reject","accepted":False},{"order_id":"accept","accepted":True}])
assert reserve(stock,orders)==expected
assert execute(stock,json.dumps(orders))==expected
assert stock=={"a":2,"b":1} and orders[0]["items"]==[["a",1],["b",3]]
assert reserve({"a":0},[{"id":"r","items":[["a",1]]}])==({"a":0},[{"order_id":"r","accepted":False}])
assert reserve({"a":1},[{"id":"empty","items":[]}])==({"a":1},[{"order_id":"empty","accepted":True}])
assert reserve({"a":1},[])==({"a":1},[])
depleting=[{"id":"first","items":[["a",1]]},{"id":"reject","items":[["a",1],["b",1]]},{"id":"later","items":[["b",2]]}]
depleted=({"a":0,"b":0},[{"order_id":"first","accepted":True},{"order_id":"reject","accepted":False},{"order_id":"later","accepted":True}])
assert reserve({"a":1,"b":2},depleting)==depleted
assert execute({"a":1,"b":2},json.dumps(depleting))==depleted
for p in ["reviews/design-current.json","reviews/code-current.json"]:
    assert json.loads(Path(p).read_text())["verdict"]=="ready", p
print("All-or-nothing rejection, continuation, APIs, input preservation, empty order and review readiness verified")
