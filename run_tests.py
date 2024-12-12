#!/usr/bin/env python3
import unittest
import argparse
import sys
import signal
import atexit
import gc
import time


def run_tests(pattern, test_type=None):
    """Run test suite based on pattern and test type.
    
    Args:
        pattern: File pattern to match test files
        test_type: Type of tests to run ('unit' or 'all')
    """
    loader = unittest.TestLoader()
    
    if test_type == 'unit':
        # Assuming unit tests are in files that don't contain 'integration' or 'e2e'
        suite = loader.discover('tests/unit', pattern=pattern)
        # Filter out non-unit tests
        filtered_suite = unittest.TestSuite()
        for test in suite:
            if ('integration' not in str(test).lower() and 
                'e2e' not in str(test).lower()):
                filtered_suite.addTest(test)
        suite = filtered_suite
    else:
        # Run all tests
        suite = loader.discover('tests', pattern=pattern)
    
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    return result.wasSuccessful()


def cleanup_handler():
    """Clean up resources before exit."""
    print("\nPerforming final cleanup...")
    try:
        # Force garbage collection
        gc.collect()
        # Sleep to allow GC to finish
        time.sleep(0.1)
        
        # Try to clean up PyAudio if available
        try:
            from src.audio import cleanup_pa
            cleanup_pa()
        except ImportError:
            pass
            
        # Final sleep to allow PortAudio to clean up
        time.sleep(0.1)
    except Exception as e:
        print(f"Cleanup error: {e}")


def signal_handler(signum, frame):
    """Handle system signals for graceful shutdown."""
    print("\nCleaning up before exit...")
    cleanup_handler()
    sys.exit(0)


# Register signal handlers
signal.signal(signal.SIGABRT, signal_handler)
signal.signal(signal.SIGTERM, signal_handler)
signal.signal(signal.SIGINT, signal_handler)

# Register cleanup handler
atexit.register(cleanup_handler)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '--pattern', 
        default='test_*.py', 
        help='Pattern to match test files'
    )
    parser.add_argument(
        '--type',
        choices=['unit', 'all'],
        default='all',
        help='Type of tests to run'
    )
    
    args = parser.parse_args()
    
    success = run_tests(args.pattern, args.type)
    sys.exit(0 if success else 1)
