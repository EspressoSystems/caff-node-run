#!/usr/bin/env python3
"""
Chain Configuration Validator

Validates chain configuration files against rules derived from schema.json.

Exit Codes:
    0 - Validation passed (may have warnings)
    1 - Validation failed (has errors)
"""

import json
import sys
from pathlib import Path
from typing import List, Tuple, Optional
from dataclasses import dataclass

CAFF_NODE_REQUIRED_KEYS = {
    "hotshot-url",
    "namespace",
    "hotshot-polling-interval",
    "sgx-verifier-addr",
    "batch-poster-addr",
}

STREAMER_REQUIRED_KEYS = {
    "hotshot-block",
    "address-monitor-start-l1",
}


@dataclass
class ValidationResult:
    rule_name: str
    passed: bool
    message: str
    severity: str = "error"  # error | warning | info


class ConfigValidator:
    def __init__(self, config_path: str):
        self.config_path = Path(config_path)
        self.config = None
        self.errors: List[ValidationResult] = []
        self.warnings: List[ValidationResult] = []
        self.info: List[ValidationResult] = []

    # ---------- helpers ----------

    def _validate_no_extra_keys(self, obj, allowed_keys, path):
        # Support both dicts (objects) and lists (arrays).
        if isinstance(obj, dict):
            for key in obj.keys():
                if key not in allowed_keys:
                    self.errors.append(
                        ValidationResult(
                            rule_name="additional_properties",
                            passed=False,
                            message=f"Unexpected key '{path}.{key}'",
                        )
                    )
        elif isinstance(obj, list):
            for idx, item in enumerate(obj):
                # If list contains objects, validate their keys.
                if isinstance(item, dict):
                    for key in item.keys():
                        if key not in allowed_keys:
                            self.errors.append(
                                ValidationResult(
                                    rule_name="additional_properties",
                                    passed=False,
                                    message=f"Unexpected key '{path}[{idx}].{key}'",
                                )
                            )
                else:
                    # For lists of primitive values (e.g. allowed string entries),
                    # ensure the value itself is allowed.
                    if item not in allowed_keys:
                        self.errors.append(
                            ValidationResult(
                                rule_name="additional_properties",
                                passed=False,
                                message=f"Unexpected value '{path}[{item}]'",
                            )
                        )

    def _validate_required_keys_present(self, obj, required_keys, path):
        for key in required_keys:
            if key not in obj:
                self.errors.append(
                    ValidationResult(
                        rule_name="missing_required_key",
                        passed=False,
                        message=f"Missing required key '{path}.{key}'",
                    )
                )

    def _is_uri(self, value: str) -> bool:
        return isinstance(value, str) and value.startswith(("http://", "https://"))

    # ---------- loading ----------

    def load_config(self, verbose: bool = True) -> bool:
        try:
            with open(self.config_path, "r") as f:
                self.config = json.load(f)
            if verbose:
                print(f"✓ Loaded {self.config_path}")
            return True
        except Exception as e:
            print(f"Error loading {self.config_path}: {e}")
            return False

    # ---------- validation entry ----------

    def validate_all(self) -> Tuple[int, int, int]:
        self.errors.clear()
        self.warnings.clear()
        self.info.clear()

        if not isinstance(self.config, dict):
            self.errors.append(
                ValidationResult(
                    rule_name="root",
                    passed=False,
                    message="Root config must be an object",
                )
            )
            return len(self.errors), 0, 0

        self._validate_structure()
        self._validate_chain()
        self._validate_execution()
        self._validate_http()
        self._validate_ws()
        self._validate_node()
        self._validate_persistent()

        return len(self.errors), len(self.warnings), len(self.info)

    # ---------- rules ----------

    def _validate_structure(self):
        required = {"chain", "execution", "http", "ws", "node", "persistent"}

        for key in required:
            if key not in self.config:
                self.errors.append(
                    ValidationResult(
                        rule_name="structure",
                        passed=False,
                        message=f"Missing required section '{key}'",
                    )
                )

        self._validate_no_extra_keys(self.config, required, "root")

    def _validate_chain(self):
        chain = self.config.get("chain")
        if not isinstance(chain, dict):
            return

        self._validate_no_extra_keys(chain, {"name", "info-json"}, "chain")

        if "name" in chain and not isinstance(chain["name"], str):
            self.errors.append(
                ValidationResult(
                    rule_name="chain.name",
                    passed=False,
                    message="chain.name must be a string",
                )
            )

    def _validate_execution(self):
        execution = self.config.get("execution")
        if not isinstance(execution, dict):
            return

        self._validate_no_extra_keys(
            execution, {"caching", "forwarding-target", "sequencer"}, "execution"
        )

        if "forwarding-target" in execution:
            if not self._is_uri(execution["forwarding-target"]):
                self.errors.append(
                    ValidationResult(
                        rule_name="execution.forwarding-target",
                        passed=False,
                        message="execution.forwarding-target must be a valid URI",
                    )
                )

        caching = execution.get("caching")
        if caching:
            self._validate_no_extra_keys(caching, {"archive"}, "execution.caching")

        sequencer = execution.get("sequencer")
        if sequencer:
            self._validate_no_extra_keys(sequencer, {"enable"}, "execution.sequencer")

    def _validate_http(self):
        http = self.config.get("http")
        if not isinstance(http, dict):
            return

        self._validate_no_extra_keys(
            http, {"addr", "port", "corsdomain", "vhosts", "api"}, "http"
        )
        http_api = http.get("api")
        self._validate_no_extra_keys(
            http_api, {"eth", "net", "web3", "arb", "txpool"}, "http.api"
        )

        if "api" in http and not all(isinstance(x, str) for x in http["api"]):
            self.errors.append(
                ValidationResult(
                    rule_name="http.api",
                    passed=False,
                    message="http.api must be an array of strings",
                )
            )

    def _validate_ws(self):
        ws = self.config.get("ws")
        if not isinstance(ws, dict):
            return

        self._validate_no_extra_keys(ws, {"addr", "port", "api"}, "ws")

        ws_api = ws.get("api")
        self._validate_no_extra_keys(
            ws_api, {"eth", "net", "web3", "arb", "txpool"}, "ws.api"
        )

    def _validate_node(self):
        node = self.config.get("node")
        if not isinstance(node, dict):
            return

        self._validate_required_keys_present(
            node,
            {
                "batch-poster",
                "espresso",
                "dangerous",
                "data-availability",
                "delayed-sequencer",
                "feed",
                "seq-coordinator",
                "sequencer",
                "staker",
            },
            "node",
        )

        espresso = node.get("espresso")
        if espresso:
            self._validate_no_extra_keys(
                espresso, {"caff-node", "streamer"}, "node.espresso"
            )

            caff = espresso.get("caff-node")
            if caff:

                if caff.get("enable"):
                    self._validate_required_keys_present(
                        caff, CAFF_NODE_REQUIRED_KEYS, "node.espresso.caff-node"
                    )

                    if "hotshot-url" in caff and not self._is_uri(caff["hotshot-url"]):
                        self.errors.append(
                            ValidationResult(
                                rule_name="caff_node.hotshot-url",
                                passed=False,
                                message="hotshot-url must be a valid URI",
                            )
                        )

                    if caff.get("dangerous"):
                        self.warnings.append(
                            ValidationResult(
                                rule_name="caff_node_dangerous",
                                passed=True,
                                severity="warning",
                                message="Caff-node is enabled with dangerous settings",
                            )
                        )

            streamer = espresso.get("streamer")
            if streamer:
                self._validate_required_keys_present(
                    streamer, STREAMER_REQUIRED_KEYS, "node.espresso.streamer"
                )

    def _validate_persistent(self):
        persistent = self.config.get("persistent")
        if not isinstance(persistent, dict):
            return

        self._validate_no_extra_keys(persistent, {"chain"}, "persistent")

        if "chain" not in persistent:
            self.errors.append(
                ValidationResult(
                    rule_name="persistent.chain",
                    passed=False,
                    message="persistent.chain must be set",
                )
            )

    def has_issues(self) -> bool:
        return bool(self.errors or self.warnings)

    def print_results(self) -> bool:
        if self.errors:
            print(f"\n❌ Errors ({len(self.errors)}):")
            for e in self.errors:
                print(f"  • {e.message}")

        if self.warnings:
            print(f"\n⚠️  Warnings ({len(self.warnings)}):")
            for w in self.warnings:
                print(f"  • {w.message}")

        return not self.errors


def find_config_files(pattern: Optional[str] = None) -> List[Path]:
    if pattern:
        p = Path(pattern)
        if p.exists():
            return [p]
        return list(Path(".").rglob(pattern))
    return list(Path(".").rglob("nodeConfig.json"))


def main():
    pattern = sys.argv[1] if len(sys.argv) > 1 else None
    files = find_config_files(pattern)

    if not files:
        print("No config files found")
        sys.exit(1)

    total_errors = 0
    total_warnings = 0
    success = True

    for path in sorted(files):
        v = ConfigValidator(str(path))
        if not v.load_config(verbose=False):
            success = False
            continue

        errors, warnings, _ = v.validate_all()
        total_errors += errors
        total_warnings += warnings

        if v.has_issues():
            print(f"\n📄 {path}")
            print("-" * len(str(path)))
            if not v.print_results():
                success = False
        else:
            print(f"✅ {path}")

    if len(files) > 1:
        print("\n" + "─" * 70)
        print(f"Validated {len(files)} file(s)")
        print(f"❌ {total_errors} error(s)")
        print(f"⚠️  {total_warnings} warning(s)")

    sys.exit(0 if success and total_errors == 0 else 1)


if __name__ == "__main__":
    main()
