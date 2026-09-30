"""Paths and integrity checks for paper and review evaluation artifacts."""

from dataclasses import dataclass
import hashlib
import json
import math
from pathlib import Path
from typing import NotRequired, TypedDict


MODELS = ("Ours(SFT)", "Ours(DPO)", "BaselineA", "BaselineB", "BaselineC")
CHARACTERS = ("沐雪", "神里绫华", "钟离", "胡桃", "凉宫春日", "李云龙", "谢尔顿", "孙悟空")


class NeutralSample(TypedDict):
    subset: str
    neutral: str


class GenerationRecord(TypedDict):
    model: str
    character: str
    neutral: str
    output: str


class CharacterMetrics(TypedDict):
    semantic: list[float]
    style: list[float]


class ModelMetrics(CharacterMetrics):
    h_score: list[float]
    valid_style: list[float]
    per_char: dict[str, CharacterMetrics]
    sample_ids: NotRequired[list[str]]


@dataclass(frozen=True)
class EvaluationPaths:
    variant: str
    test_file: Path
    saved_generations: Path
    saved_metrics: Path
    run_dir: Path

    @property
    def generation_output(self) -> Path:
        return self.run_dir / "batch_run_result.jsonl"

    @property
    def metric_output(self) -> Path:
        return self.run_dir / "evaluate_result.json"

    @property
    def generation_input(self) -> Path:
        return self.generation_output if self.generation_output.exists() else self.saved_generations

    @property
    def metric_input(self) -> Path:
        return self.metric_output if self.metric_output.exists() else self.saved_metrics


def evaluation_paths(root: Path, variant: str) -> EvaluationPaths:
    if variant not in ("paper", "expanded"):
        raise ValueError("Evaluation variant must be 'paper' or 'expanded'.")
    suffix = "" if variant == "paper" else "_extra"
    return EvaluationPaths(
        variant=variant,
        test_file=root / "data" / f"neutral_sentences_eval{suffix}.jsonl",
        saved_generations=root / "outputs" / f"batch_run_result{suffix}.jsonl",
        saved_metrics=root / "outputs" / f"evaluate_result{suffix}.jsonl",
        run_dir=root / "outputs" / "runs" / variant,
    )


def read_neutral_samples(path: Path) -> list[NeutralSample]:
    rows = [json.loads(line) for line in path.read_text(encoding="utf-8-sig").splitlines() if line.strip()]
    seen: set[str] = set()
    for row in rows:
        if not isinstance(row, dict) or not all(isinstance(row.get(k), str) for k in ("neutral", "subset")):
            raise ValueError(f"Invalid neutral sample in {path}")
        text = row["neutral"].strip()
        if not text or text in seen:
            raise ValueError(f"Empty or duplicate neutral input in {path}")
        seen.add(text)
    return rows


def validate_generations(records: list[GenerationRecord], samples: list[NeutralSample]) -> None:
    neutral_texts = {row["neutral"].strip() for row in samples}
    expected_pairs = {(character, text) for character in CHARACTERS for text in neutral_texts}
    by_model: dict[str, list[tuple[str, str]]] = {}
    for row in records:
        if not all(isinstance(row.get(k), str) for k in ("model", "character", "neutral", "output")):
            raise ValueError("Generation records require model, character, neutral, and output strings.")
        model = row["model"]
        if model not in MODELS:
            raise ValueError(f"Unknown main-evaluation model: {model}")
        if not row["output"].strip() or row["output"] == "<error>":
            raise ValueError(f"Missing or failed generation: {model}/{row['character']}")
        by_model.setdefault(model, []).append((row["character"], row["neutral"].strip()))
    if not by_model:
        raise ValueError("No generation records found.")
    for model, pairs in by_model.items():
        if len(pairs) != len(set(pairs)):
            raise ValueError(f"Duplicate sentence-character pairs for {model}")
        if set(pairs) != expected_pairs:
            raise ValueError(f"Incomplete or mismatched evaluation inputs for {model}")


def read_generations(path: Path, samples: list[NeutralSample]) -> list[GenerationRecord]:
    records = [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]
    validate_generations(records, samples)
    if {row["model"] for row in records} != set(MODELS):
        raise ValueError(f"Expected all five main systems in {path}")
    return records


def save_generations(path: Path, records: list[GenerationRecord], samples: list[NeutralSample]) -> None:
    """Replace complete system groups, so rerunning a cell cannot append duplicates."""
    validate_generations(records, samples)
    replaced_models = {row["model"] for row in records}
    existing: list[GenerationRecord] = []
    if path.exists():
        existing = [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]
        validate_generations(existing, samples)
    merged = [row for row in existing if row["model"] not in replaced_models] + records
    validate_generations(merged, samples)
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(path.suffix + ".tmp")
    temporary.write_text("".join(json.dumps(row, ensure_ascii=False) + "\n" for row in merged), encoding="utf-8")
    temporary.replace(path)


def sample_ids(records: list[GenerationRecord], samples: list[NeutralSample]) -> list[str]:
    indices = {row["neutral"].strip(): index for index, row in enumerate(samples)}
    return [f"{row['character']}:{indices[row['neutral'].strip()]}" for row in records]


def validate_metric_pairs(metrics: dict[str, ModelMetrics], records: list[GenerationRecord], samples: list[NeutralSample]) -> None:
    """Check the pairing and formula of the five main systems before statistics."""
    validate_generations(records, samples)
    for model in MODELS:
        rows = [row for row in records if row["model"] == model]
        ids = sample_ids(rows, samples)
        if not rows:
            raise ValueError(f"Missing generation system: {model}")
        values = metrics[model]
        arrays = [values[key] for key in ("semantic", "style", "h_score", "valid_style")]
        if any(len(array) != len(rows) for array in arrays):
            raise ValueError(f"Metric count does not match generation count: {model}")
        if "sample_ids" in values and values["sample_ids"] != ids:
            raise ValueError(f"Metric sample IDs do not match generations: {model}")
        semantic, style, h_score, valid_style = arrays
        for se, st, h, vss in zip(semantic, style, h_score, valid_style):
            if not all(isinstance(x, (int, float)) and math.isfinite(x) for x in (se, st, h, vss)):
                raise ValueError(f"Invalid metric value: {model}")
            if not math.isclose(vss, st * (1 if se > 0.75 else 0.1), rel_tol=1e-8, abs_tol=1e-9):
                raise ValueError(f"VSS differs from the paper's 0.1 penalty: {model}")
        if "sample_ids" not in values:
            # Legacy files have per-character arrays but no explicit IDs.
            for character in CHARACTERS:
                indices = [i for i, row in enumerate(rows) if row["character"] == character]
                for key in ("semantic", "style"):
                    expected = [values[key][i] for i in indices]
                    if values["per_char"][character][key] != expected:
                        raise ValueError(f"Legacy per-character ordering differs: {model}/{character}")


def align_metric_pairs(metrics: dict[str, ModelMetrics], records: list[GenerationRecord],
                       samples: list[NeutralSample]) -> dict[str, ModelMetrics]:
    """Align metric arrays by character and neutral input without changing snapshots."""
    validate_metric_pairs(metrics, records, samples)
    ordered_ids = [f"{character}:{index}" for character in CHARACTERS for index in range(len(samples))]
    aligned: dict[str, ModelMetrics] = {}
    for model in MODELS:
        rows = [row for row in records if row["model"] == model]
        positions = {key: index for index, key in enumerate(sample_ids(rows, samples))}
        order = [positions[key] for key in ordered_ids]
        values = metrics[model]
        aligned[model] = {
            "semantic": [values["semantic"][i] for i in order],
            "style": [values["style"][i] for i in order],
            "h_score": [values["h_score"][i] for i in order],
            "valid_style": [values["valid_style"][i] for i in order],
            "per_char": values["per_char"], "sample_ids": ordered_ids.copy(),
        }
    return aligned


def read_paired_metrics(paths: EvaluationPaths) -> dict[str, ModelMetrics]:
    """Load the generation file bound to these metrics, then align paired arrays."""
    metric_path = paths.metric_input
    generation_path = paths.saved_generations
    if metric_path == paths.metric_output:
        manifest = json.loads((paths.run_dir / "metric-manifest.json").read_text(encoding="utf-8"))
        generation_path = Path(manifest["source_file"])
        allowed = {paths.saved_generations.resolve(), paths.generation_output.resolve()}
        if generation_path.resolve() not in allowed:
            raise ValueError("Metric manifest references a different evaluation route.")
        if hashlib.sha256(generation_path.read_bytes()).hexdigest() != manifest["source_sha256"]:
            raise ValueError("Generations changed after scoring; re-score before statistics.")
        if hashlib.sha256(paths.test_file.read_bytes()).hexdigest() != manifest["test_sha256"]:
            raise ValueError("Test inputs changed after scoring.")
        if hashlib.sha256(metric_path.read_bytes()).hexdigest() != manifest["settings"]["metric_sha256"]:
            raise ValueError("Metrics changed after their manifest was written.")
    else:
        snapshot_manifest = paths.saved_metrics.parent / "evaluation-snapshots.json"
        if snapshot_manifest.exists():
            snapshot = json.loads(snapshot_manifest.read_text(encoding="utf-8"))["snapshots"][paths.variant]
            root = paths.test_file.parent.parent
            for entry in snapshot["files"]:
                if hashlib.sha256((root / entry["path"]).read_bytes()).hexdigest() != entry["sha256"]:
                    raise ValueError(f"Published snapshot changed: {entry['path']}")
    metrics = json.loads(metric_path.read_text(encoding="utf-8"))
    samples = read_neutral_samples(paths.test_file)
    records = read_generations(generation_path, samples)
    return align_metric_pairs(metrics, records, samples)


def write_run_manifest(path: Path, test_file: Path, source_file: Path, settings: dict[str, str | float | int]) -> None:
    data = {
        "test_file": str(test_file),
        "test_sha256": hashlib.sha256(test_file.read_bytes()).hexdigest(),
        "source_file": str(source_file),
        "source_sha256": hashlib.sha256(source_file.read_bytes()).hexdigest(),
        "settings": settings,
    }
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
