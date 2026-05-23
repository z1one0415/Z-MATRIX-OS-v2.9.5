"""v2.9.6 Daily Operations Workflow"""
import sys, os, argparse
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))

def main():
    p = argparse.ArgumentParser()
    p.add_argument('--stage', default='premarket', choices=['premarket','intraday','tail','review'])
    args = p.parse_args()
    
    stages = {'premarket': 'Z-G02', 'intraday': 'Z-G03', 'tail': 'Z-G04', 'review': 'Z-G05'}
    print(f"v2.9.6 daily_ops: {args.stage} → {stages[args.stage]}")
    # Pipeline calls would go here
    print("✅ daily_ops workflow loaded")

if __name__ == '__main__': main()
