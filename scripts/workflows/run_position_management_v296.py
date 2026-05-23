"""v2.9.6 Position Management Workflow"""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))

def main():
    from zmatrix.account.position_provider import load_positions
    pos = load_positions()
    print(f"v2.9.6 position_mgmt: {pos['count']} positions")
    for p in pos['positions']:
        print(f"  {p['ticker']} {p['name']}: {p['shares']}股 @{p['cost']}")

if __name__ == '__main__': main()
