"""
Dataset Curator for Cannabis Plant Health

Interactive tool to curate custom cannabis-specific training data
from web sources, user uploads, and community contributions.
"""

import os
import json
import base64
from pathlib import Path
from typing import List, Dict, Any, Optional
from dataclasses import dataclass, asdict
from datetime import datetime


@dataclass
class HealthExample:
    """Single training example for plant health."""
    image_path: str
    issue_type: str  # "deficiency", "pest", "disease", "stress"
    issue_name: str  # e.g., "Nitrogen Deficiency"
    severity: str  # "low", "medium", "high", "critical"
    affected_area: str
    description: str
    solutions: List[str]
    prevention: List[str]
    growth_stage: str
    source: str  # "web", "user", "expert"
    confidence: float
    created_at: str


class DatasetCurator:
    """
    Interactive dataset curation tool.
    
    Helps build high-quality cannabis-specific training data.
    """
    
    def __init__(self, dataset_dir: str = "./ml/datasets/custom_cannabis"):
        self.dataset_dir = Path(dataset_dir)
        self.dataset_dir.mkdir(parents=True, exist_ok=True)
        
        self.images_dir = self.dataset_dir / "images"
        self.images_dir.mkdir(exist_ok=True)
        
        self.examples: List[HealthExample] = []
        self.load_existing()
    
    def load_existing(self):
        """Load existing curated examples."""
        manifest_path = self.dataset_dir / "manifest.json"
        
        if manifest_path.exists():
            with open(manifest_path, 'r') as f:
                data = json.load(f)
                self.examples = [
                    HealthExample(**example) for example in data.get("examples", [])
                ]
            print(f"✅ Loaded {len(self.examples)} existing examples")
        else:
            print("📝 Starting new dataset")
    
    def add_example(
        self,
        image_path: str,
        issue_type: str,
        issue_name: str,
        severity: str,
        description: str,
        solutions: List[str],
        prevention: List[str],
        affected_area: str = "unspecified",
        growth_stage: str = "vegetative",
        source: str = "manual",
        confidence: float = 1.0,
    ) -> HealthExample:
        """Add a new training example."""
        
        # Copy image to dataset directory
        src_path = Path(image_path)
        if not src_path.exists():
            raise FileNotFoundError(f"Image not found: {image_path}")
        
        # Generate unique filename
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        ext = src_path.suffix
        new_filename = f"{issue_type}_{issue_name.replace(' ', '_')}_{timestamp}{ext}"
        dst_path = self.images_dir / new_filename
        
        # Copy image
        import shutil
        shutil.copy(src_path, dst_path)
        
        # Create example
        example = HealthExample(
            image_path=str(dst_path.relative_to(self.dataset_dir)),
            issue_type=issue_type,
            issue_name=issue_name,
            severity=severity,
            affected_area=affected_area,
            description=description,
            solutions=solutions,
            prevention=prevention,
            growth_stage=growth_stage,
            source=source,
            confidence=confidence,
            created_at=datetime.now().isoformat(),
        )
        
        self.examples.append(example)
        self.save()
        
        print(f"✅ Added example: {issue_name} ({severity})")
        return example
    
    def save(self):
        """Save dataset manifest."""
        manifest = {
            "version": "1.0",
            "created_at": datetime.now().isoformat(),
            "total_examples": len(self.examples),
            "examples": [asdict(ex) for ex in self.examples],
        }
        
        with open(self.dataset_dir / "manifest.json", 'w') as f:
            json.dump(manifest, f, indent=2)
        
        print(f"💾 Saved {len(self.examples)} examples to manifest")
    
    def export_for_training(self, output_path: str = None):
        """
        Export dataset in format ready for fine-tuning.
        
        Creates JSONL file with conversational format.
        """
        if output_path is None:
            output_path = self.dataset_dir / "training_data.jsonl"
        
        formatted_examples = []
        
        for example in self.examples:
            # Read and encode image
            image_path = self.dataset_dir / example.image_path
            with open(image_path, 'rb') as f:
                image_data = base64.b64encode(f.read()).decode('utf-8')
            
            # Build expected answer
            answer = f"""Analysis of plant in {example.growth_stage} stage:

Issue Identified: {example.issue_name}
Type: {example.issue_type}
Severity: {example.severity}
Affected Area: {example.affected_area}

Description: {example.description}

Solutions:
{chr(10).join(f"- {sol}" for sol in example.solutions)}

Prevention:
{chr(10).join(f"- {prev}" for prev in example.prevention)}"""
            
            # Format as conversation
            formatted = {
                "image": image_data,
                "messages": [
                    {
                        "role": "system",
                        "content": "You are an expert plant health advisor specializing in cannabis cultivation."
                    },
                    {
                        "role": "user",
                        "content": f"Analyze this plant photo for health issues. The plant is in {example.growth_stage} stage."
                    },
                    {
                        "role": "assistant",
                        "content": answer
                    }
                ]
            }
            
            formatted_examples.append(formatted)
        
        # Save as JSONL
        with open(output_path, 'w') as f:
            for example in formatted_examples:
                f.write(json.dumps(example) + '\n')
        
        print(f"✅ Exported {len(formatted_examples)} examples to {output_path}")
        return output_path
    
    def get_statistics(self) -> Dict[str, Any]:
        """Get dataset statistics."""
        stats = {
            "total_examples": len(self.examples),
            "by_issue_type": {},
            "by_severity": {},
            "by_growth_stage": {},
            "by_source": {},
        }
        
        for example in self.examples:
            # Count by issue type
            stats["by_issue_type"][example.issue_type] = \
                stats["by_issue_type"].get(example.issue_type, 0) + 1
            
            # Count by severity
            stats["by_severity"][example.severity] = \
                stats["by_severity"].get(example.severity, 0) + 1
            
            # Count by growth stage
            stats["by_growth_stage"][example.growth_stage] = \
                stats["by_growth_stage"].get(example.growth_stage, 0) + 1
            
            # Count by source
            stats["by_source"][example.source] = \
                stats["by_source"].get(example.source, 0) + 1
        
        return stats
    
    def print_statistics(self):
        """Print dataset statistics."""
        stats = self.get_statistics()
        
        print("\n📊 Dataset Statistics")
        print("=" * 50)
        print(f"Total Examples: {stats['total_examples']}\n")
        
        print("By Issue Type:")
        for issue_type, count in stats['by_issue_type'].items():
            print(f"  {issue_type}: {count}")
        
        print("\nBy Severity:")
        for severity, count in stats['by_severity'].items():
            print(f"  {severity}: {count}")
        
        print("\nBy Growth Stage:")
        for stage, count in stats['by_growth_stage'].items():
            print(f"  {stage}: {count}")
        
        print("\nBy Source:")
        for source, count in stats['by_source'].items():
            print(f"  {source}: {count}")
        print("=" * 50 + "\n")
    
    def interactive_add(self):
        """Interactive mode to add examples."""
        print("\n🌿 Cannabis Dataset Curator - Interactive Mode\n")
        
        while True:
            print("\n" + "-" * 50)
            image_path = input("Image path (or 'done' to finish): ").strip()
            
            if image_path.lower() == 'done':
                break
            
            if not Path(image_path).exists():
                print(f"❌ File not found: {image_path}")
                continue
            
            print("\nIssue Types: deficiency, pest, disease, stress")
            issue_type = input("Issue type: ").strip()
            
            issue_name = input("Issue name (e.g., 'Nitrogen Deficiency'): ").strip()
            
            print("\nSeverity: low, medium, high, critical")
            severity = input("Severity: ").strip()
            
            description = input("Description: ").strip()
            
            print("\nSolutions (one per line, empty line to finish):")
            solutions = []
            while True:
                sol = input("  - ").strip()
                if not sol:
                    break
                solutions.append(sol)
            
            print("\nPrevention tips (one per line, empty line to finish):")
            prevention = []
            while True:
                prev = input("  - ").strip()
                if not prev:
                    break
                prevention.append(prev)
            
            affected_area = input("Affected area (e.g., 'lower leaves'): ").strip() or "unspecified"
            growth_stage = input("Growth stage (seedling/vegetative/flowering): ").strip() or "vegetative"
            
            # Add example
            try:
                self.add_example(
                    image_path=image_path,
                    issue_type=issue_type,
                    issue_name=issue_name,
                    severity=severity,
                    description=description,
                    solutions=solutions,
                    prevention=prevention,
                    affected_area=affected_area,
                    growth_stage=growth_stage,
                )
            except Exception as e:
                print(f"❌ Error adding example: {e}")
        
        self.print_statistics()
        
        export = input("\nExport for training? (y/n): ").strip().lower()
        if export == 'y':
            output_path = self.export_for_training()
            print(f"\n✅ Training data ready at: {output_path}")


def main():
    """Main CLI entry point."""
    import argparse
    
    parser = argparse.ArgumentParser(description="Cannabis Plant Health Dataset Curator")
    parser.add_argument("--dataset-dir", default="./ml/datasets/custom_cannabis",
                       help="Dataset directory")
    parser.add_argument("--interactive", action="store_true",
                       help="Interactive mode")
    parser.add_argument("--stats", action="store_true",
                       help="Show dataset statistics")
    parser.add_argument("--export", action="store_true",
                       help="Export training data")
    
    args = parser.parse_args()
    
    curator = DatasetCurator(args.dataset_dir)
    
    if args.stats:
        curator.print_statistics()
    
    if args.export:
        curator.export_for_training()
    
    if args.interactive:
        curator.interactive_add()
    
    if not (args.stats or args.export or args.interactive):
        # Default: show stats
        curator.print_statistics()


if __name__ == "__main__":
    main()
