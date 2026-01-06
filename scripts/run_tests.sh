#!/bin/bash

# Comprehensive test runner
# Runs all tests with coverage and reporting

set -e

echo "======================================"
echo "Running Comprehensive Test Suite"
echo "======================================"
echo ""

# Colors
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

function run_test_suite {
    echo -e "${YELLOW}▶ $1${NC}"
    python3 "$2"
    echo -e "${GREEN}✓ Completed${NC}"
    echo ""
}

# Activate virtual environment if it exists
if [ -d "venv" ]; then
    source venv/bin/activate
fi

# Install test dependencies
echo "Installing test dependencies..."
pip install pytest pytest-asyncio pytest-cov -q
echo ""

# Run unit tests
run_test_suite "Orchestrator Tests" "tests/test_orchestrator.py"
run_test_suite "Revenue Engine Tests" "tests/test_revenue_engine.py"
run_test_suite "Self-Healing Tests" "tests/test_self_healing.py"

# Run integration tests
run_test_suite "Integration Tests" "tests/integration_test.py"

# Run performance benchmarks
run_test_suite "Performance Benchmarks" "debug/performance_test.py"

echo "======================================"
echo "All Tests Passed! ✓"
echo "======================================"
