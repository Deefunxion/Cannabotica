import os
import sys

SCRIPT_DIR = os.path.dirname(__file__)
ROOT_DIR = os.path.dirname(SCRIPT_DIR)
sys.path.extend([SCRIPT_DIR, ROOT_DIR])

import orchestrator
import visualize

def main():
    orchestrator.main()
    visualize.main()

if __name__ == "__main__":
    main()
