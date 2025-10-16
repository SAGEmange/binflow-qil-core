from dataclasses import dataclass, field
from typing import Dict, Callable, Any
import time, json, os, hashlib
from pathlib import Path

BINFLOW_STATES = ["F","S","L","P","T"]  # Focus, Stress, Loop, Pause, Transition

@dataclass
class PatternNode:
    id: str
    state: str = "F"
    payload: Dict[str, Any] = field(default_factory=dict)
    update_fn: Callable[["PatternNode","PatternWorld",float], None] = None

    def tick(self, world:"PatternWorld", dt:float):
        if self.update_fn:
            self.update_fn(self, world, dt)

class PatternWorld:
    def __init__(self):
        self.nodes: Dict[str, PatternNode] = {}
        self.time = 0.0

    def add(self, node:PatternNode):
        self.nodes[node.id] = node

    def step(self, dt:float=0.1):
        self.time += dt
        for n in list(self.nodes.values()):
            n.tick(self, dt)

    def snapshot(self)->Dict[str,Any]:
        return {
            "t": self.time,
            "nodes": {k: {"state":v.state, "payload":v.payload} for k,v in self.nodes.items()}
        }

class DataPass:
    @staticmethod
    def export(world:PatternWorld, out_dir="data_passes")->str:
        os.makedirs(out_dir, exist_ok=True)
        snap = world.snapshot()
        raw = json.dumps(snap, sort_keys=True).encode("utf-8")
        digest = hashlib.sha256(raw).hexdigest()
        ts = int(time.time())
        path = Path(out_dir)/f"datapass_{ts}_{digest[:8]}.json"
        with open(path, "w", encoding="utf-8") as f:
            json.dump({"snapshot": snap, "sha256": digest, "timestamp": ts}, f, indent=2)
        return str(path)
