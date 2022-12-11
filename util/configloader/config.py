import yaml
from types import SimpleNamespace
import util


def load_config(file: str) -> SimpleNamespace:
    with open(file, "r") as f:
        ns: SimpleNamespace = SimpleNamespace(**yaml.safe_load(f))
        ns.LANG, ns.GEO, ns.TZ = util.get_c_code_lang_and_offset()
        return ns
