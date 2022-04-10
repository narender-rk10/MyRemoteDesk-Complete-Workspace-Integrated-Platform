import moni
import json
import sys

json_object = json.loads(sys.argv[1])

e_id = json_object["e_id"]
o_id = json_object["o_id"]

moni.mainRecord(e_id, o_id)