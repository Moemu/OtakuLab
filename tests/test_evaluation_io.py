import copy
import hashlib
import json
from pathlib import Path
import tempfile
import unittest

from scripts.evaluation_io import (
    CHARACTERS, MODELS, align_metric_pairs, evaluation_paths, read_paired_metrics,
    save_generations, validate_generations, validate_metric_pairs, write_run_manifest,
)


class EvaluationIntegrityTests(unittest.TestCase):
    def setUp(self):
        self.samples = [{"subset": "test", "neutral": text} for text in ("first", "second")]
        self.records = [
            {"model": model, "character": character, "neutral": sample["neutral"], "output": "response"}
            for model in MODELS for character in CHARACTERS for sample in self.samples
        ]
        self.metrics = {}
        for model in MODELS:
            semantic = [0.75, 0.8] * len(CHARACTERS)
            style = [0.6] * len(semantic)
            self.metrics[model] = {
                "semantic": semantic, "style": style,
                "h_score": [2*se*st/(se+st+1e-9) for se,st in zip(semantic,style)],
                "valid_style": [0.06, 0.6] * len(CHARACTERS),
                "per_char": {ch: {"semantic": [0.75,0.8], "style": [0.6,0.6]} for ch in CHARACTERS},
            }

    def test_duplicate_wrong_input_and_failed_generation_rejected(self):
        for mutation in ("duplicate", "wrong_input", "failed"):
            records = copy.deepcopy(self.records)
            if mutation == "duplicate":
                records.append(records[0])
            elif mutation == "wrong_input":
                records[0]["neutral"] = "other"
            else:
                records[0]["output"] = "<error>"
            with self.subTest(mutation=mutation), self.assertRaises(ValueError):
                validate_generations(records, self.samples)

    def test_exact_threshold_uses_point_one_penalty(self):
        validate_metric_pairs(self.metrics,self.records,self.samples)
        self.metrics[MODELS[0]]["valid_style"][0] = 0
        with self.assertRaises(ValueError):
            validate_metric_pairs(self.metrics,self.records,self.samples)

    def test_pair_alignment_preserves_values_across_different_orders(self):
        records = copy.deepcopy(self.records)
        metrics = copy.deepcopy(self.metrics)
        model = MODELS[-1]
        for i in range(len(records)-16,len(records),2):
            records[i],records[i+1]=records[i+1],records[i]
        for key in ("semantic","style","h_score","valid_style"):
            values=metrics[model][key]
            for i in range(0,len(values),2):
                values[i],values[i+1]=values[i+1],values[i]
        for ch in CHARACTERS:
            metrics[model]["per_char"][ch]["semantic"].reverse()
        aligned=align_metric_pairs(metrics,records,self.samples)
        self.assertEqual(aligned[model]["semantic"],aligned[MODELS[0]]["semantic"])
        self.assertEqual(metrics[model]["semantic"][:2],[0.8,0.75])

    def test_rerun_replaces_groups_instead_of_appending(self):
        with tempfile.TemporaryDirectory() as directory:
            path=Path(directory)/'generations.jsonl'
            for model in MODELS:
                save_generations(path,[r for r in self.records if r["model"]==model],self.samples)
            rerun=[dict(r,output="new") for r in self.records if r["model"]==MODELS[0]]
            save_generations(path,rerun,self.samples)
            rows=[json.loads(line) for line in path.read_text(encoding="utf-8").splitlines()]
            self.assertEqual(len(rows),len(self.records))
            self.assertTrue(all(r["output"]=="new" for r in rows if r["model"]==MODELS[0]))

    def test_statistics_uses_saved_generations_until_new_metrics_exist(self):
        with tempfile.TemporaryDirectory() as directory:
            root=Path(directory)
            paths=evaluation_paths(root,'paper')
            paths.test_file.parent.mkdir()
            paths.test_file.write_text(''.join(json.dumps(s)+'\n' for s in self.samples),encoding='utf-8')
            save_generations(paths.saved_generations,self.records,self.samples)
            paths.saved_metrics.write_text(json.dumps(self.metrics),encoding='utf-8')
            # A partially generated run must not contaminate saved-result statistics.
            save_generations(paths.generation_output,[r for r in self.records if r["model"]==MODELS[0]],self.samples)
            read_paired_metrics(paths)
            save_generations(paths.generation_output,self.records,self.samples)
            paths.metric_output.write_text(json.dumps(self.metrics),encoding='utf-8')
            write_run_manifest(paths.run_dir/'metric-manifest.json',paths.test_file,paths.generation_output,{
                'metric_sha256':hashlib.sha256(paths.metric_output.read_bytes()).hexdigest(),
            })
            read_paired_metrics(paths)
            changed=[dict(r,output="changed") for r in self.records]
            save_generations(paths.generation_output,changed,self.samples)
            with self.assertRaises(ValueError):
                read_paired_metrics(paths)

    def test_routes_preserve_supplied_snapshots(self):
        root=Path('/repo')
        for variant in ('paper','expanded'):
            paths=evaluation_paths(root,variant)
            self.assertNotEqual(paths.saved_generations,paths.generation_output)
            self.assertNotEqual(paths.saved_metrics,paths.metric_output)
        with self.assertRaises(ValueError):
            evaluation_paths(root,'unknown')

    def test_published_snapshot_hash_mismatch_stops_statistics(self):
        with tempfile.TemporaryDirectory() as directory:
            root=Path(directory)
            paths=evaluation_paths(root,'paper')
            paths.saved_metrics.parent.mkdir()
            (paths.saved_metrics.parent/'evaluation-snapshots.json').write_text(json.dumps({
                'snapshots':{'paper':{'files':[
                    {'path':'outputs/evaluate_result.jsonl','sha256':'wrong'},
                ]}},
            }),encoding='utf-8')
            paths.saved_metrics.write_text('{}',encoding='utf-8')
            with self.assertRaises(ValueError):
                read_paired_metrics(paths)


if __name__ == '__main__':
    unittest.main()
