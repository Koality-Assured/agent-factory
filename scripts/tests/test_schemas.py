import unittest
import json
import os
from pathlib import Path

try:
    import jsonschema
    HAS_JSONSCHEMA = True
except ImportError:
    HAS_JSONSCHEMA = False

ROOT = Path(__file__).resolve().parents[2]

class TestSchemas(unittest.TestCase):
    def setUp(self):
        self.run_spec_schema_path = ROOT / "docs" / "standards" / "run-spec.schema.json"
        self.finding_schema_path = ROOT / "docs" / "standards" / "finding.schema.json"
        
        with open(self.run_spec_schema_path, "r", encoding="utf-8") as f:
            self.run_spec_schema = json.load(f)
            
        with open(self.finding_schema_path, "r", encoding="utf-8") as f:
            self.finding_schema = json.load(f)

    @unittest.skipUnless(HAS_JSONSCHEMA, "jsonschema not installed")
    def test_run_spec_valid(self):
        example = {
            "run_id": "run-001",
            "target": "$TARGET_CHECKOUT",
            "pack_id": "example-web-app",
            "mode": "read-only",
            "promotion_target": "example-org/example-app",
            "proof_mode": "local-replay",
            "objective": "both"
        }
        jsonschema.validate(instance=example, schema=self.run_spec_schema)

    @unittest.skipUnless(HAS_JSONSCHEMA, "jsonschema not installed")
    def test_finding_valid(self):
        example = {
            "id": "run-001-f-03",
            "persona": "priya",
            "target": "$TARGET_CHECKOUT",
            "objective": "problems",
            "what_they_tried": "Followed the documented path to create a page.",
            "reproduction": "1. Open the target. 2. Click New page. 3. Submit with title only.",
            "expected_result": "Page is created and listed.",
            "actual_result": "Form returns a validation error with no field highlighted.",
            "class": "defect",
            "triage_status": "open"
        }
        jsonschema.validate(instance=example, schema=self.finding_schema)

if __name__ == "__main__":
    unittest.main()

