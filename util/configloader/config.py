import yaml
from types import SimpleNamespace
import util


def load_config(file: str) -> SimpleNamespace:
    with open(file, "r") as f:
        ns: SimpleNamespace = SimpleNamespace(**yaml.safe_load(f))
        ns.LANG, ns.GEO, ns.TZ = util.get_c_code_lang_and_offset()
        ns.MicrosoftAccounts = list()
        for a in ns.accounts:
            account: util.MicrosoftAccount = util.MicrosoftAccount(
                email=a.get("email"),
                password=a.get("password")
            )
            ns.MicrosoftAccounts.append(account)
        return ns
