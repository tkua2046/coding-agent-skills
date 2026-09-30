import importlib.util
from pathlib import Path
spec = importlib.util.spec_from_file_location("subject", Path.cwd()/"session.py")
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)
for cursor, selection in [(4,"open"), (-7,"closed"), (10,"custom")]:
    for command, delta in [("next",1),("previous",-1),("bogus",None),("",None)]:
        state=module.Session(); state.cursor=cursor; state.selection=selection
        if delta is None:
            try: state.apply(command)
            except ValueError: pass
            else: raise AssertionError("unknown command accepted")
            assert (state.cursor,state.selection)==(cursor,selection), "invalid command mutates state"
        else:
            state.apply(command)
            assert (state.cursor,state.selection)==(cursor+delta,"closed"), "valid command regressed"
print("Session contract: rejected-state preservation and valid transitions verified")
