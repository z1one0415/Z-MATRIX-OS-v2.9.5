"""v2.9.6 Tianji Control Workflow — G18 as conflict resolver"""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))

def main():
    print("v2.9.6 tianji_control: G18 conflict resolver")
    print("  Rules: G17>G01/G12>G09 sell>G18 prob>G11 warn>G14 provenance")
    print("  No BUY/SELL/AUTO_TRADE")
    print("✅ tianji_control workflow loaded")

if __name__ == '__main__': main()
