#!/usr/bin/env python3
"""
Stress test script for OFChat
Tests performance, reliability, and response quality under load
"""
import sys
import time
from pathlib import Path
from statistics import mean, median, stdev

# Add src to path
sys.path.insert(0, str(Path(__file__).parent))

from src.config import Config
from src.llm.groq_client import GroqClient


class StressTest:
    """Stress testing for OFChat"""

    def __init__(self):
        """Initialize stress test"""
        self.client = GroqClient(
            api_key=Config.GROQ_API_KEY,
            model=Config.LLM_MODEL
        )
        self.results = {
            'total_requests': 0,
            'successful': 0,
            'failed': 0,
            'response_times': [],
            'errors': []
        }

    def test_message(self, message: str, message_type: str = "master") -> dict:
        """
        Test a single message

        Args:
            message: Test message
            message_type: Type of prompt

        Returns:
            Test result dict
        """
        start_time = time.time()

        try:
            response = self.client.generate_response(
                user_message=message,
                message_type=message_type,
                use_history=False
            )

            response_time = time.time() - start_time

            return {
                'success': True,
                'response': response,
                'response_time': response_time,
                'error': None
            }

        except Exception as e:
            response_time = time.time() - start_time

            return {
                'success': False,
                'response': None,
                'response_time': response_time,
                'error': str(e)
            }

    def run_basic_tests(self):
        """Run basic functionality tests"""
        print("\n" + "="*70)
        print("  TEST 1: Basic Functionality")
        print("="*70)

        test_messages = [
            ("Hey! How are you today? 😊", "simple"),
            ("I loved your latest post! You look absolutely stunning!", "compliment"),
            ("When are you going live next? I don't want to miss it!", "question"),
            ("Hey beautiful! Just wanted to say you're amazing 😍", "first"),
            ("What kind of content do you enjoy creating the most?", "question"),
        ]

        for i, (message, msg_type) in enumerate(test_messages, 1):
            print(f"\n📨 Test {i}/{len(test_messages)}: {msg_type.upper()}")
            print(f"   Input: \"{message[:60]}{'...' if len(message) > 60 else ''}\"")

            result = self.test_message(message, msg_type)
            self.results['total_requests'] += 1

            if result['success']:
                self.results['successful'] += 1
                self.results['response_times'].append(result['response_time'])
                print(f"   ✅ Response: \"{result['response'][:60]}...\"")
                print(f"   ⏱️  Time: {result['response_time']:.2f}s")
            else:
                self.results['failed'] += 1
                self.results['errors'].append(result['error'])
                print(f"   ❌ Error: {result['error']}")

    def run_load_test(self, num_requests: int = 20):
        """Run load test with rapid requests"""
        print("\n" + "="*70)
        print(f"  TEST 2: Load Test ({num_requests} rapid requests)")
        print("="*70)

        test_message = "Hey! Love your content, keep it up! 💕"

        print(f"\n🔥 Sending {num_requests} requests as fast as possible...")
        start_time = time.time()

        successful = 0
        failed = 0

        for i in range(num_requests):
            result = self.test_message(test_message)
            self.results['total_requests'] += 1

            if result['success']:
                successful += 1
                self.results['successful'] += 1
                self.results['response_times'].append(result['response_time'])
                print(f"   [{i+1}/{num_requests}] ✅ {result['response_time']:.2f}s")
            else:
                failed += 1
                self.results['failed'] += 1
                self.results['errors'].append(result['error'])
                print(f"   [{i+1}/{num_requests}] ❌ {result['error'][:50]}")

        total_time = time.time() - start_time

        print(f"\n📊 Load Test Results:")
        print(f"   Total Time: {total_time:.2f}s")
        print(f"   Successful: {successful}/{num_requests}")
        print(f"   Failed: {failed}/{num_requests}")
        print(f"   Avg Time/Request: {total_time/num_requests:.2f}s")

    def run_edge_cases(self):
        """Test edge cases and challenging inputs"""
        print("\n" + "="*70)
        print("  TEST 3: Edge Cases")
        print("="*70)

        edge_cases = [
            ("hi", "Very short message"),
            ("Hey " * 50, "Very long message"),
            ("🔥💕😍❤️✨💋", "Only emojis"),
            ("HELLO HOW ARE YOU TODAY??????", "All caps with punctuation"),
            ("I love you so much can we meet up what's your number where do you live", "Multiple questions"),
            ("你好 beautiful! Comment ça va? 😊", "Mixed languages"),
        ]

        for i, (message, description) in enumerate(edge_cases, 1):
            print(f"\n🧪 Test {i}/{len(edge_cases)}: {description}")
            print(f"   Input: \"{message[:60]}{'...' if len(message) > 60 else ''}\"")

            result = self.test_message(message)
            self.results['total_requests'] += 1

            if result['success']:
                self.results['successful'] += 1
                self.results['response_times'].append(result['response_time'])
                print(f"   ✅ Response: \"{result['response'][:60]}...\"")
                print(f"   ⏱️  Time: {result['response_time']:.2f}s")
            else:
                self.results['failed'] += 1
                self.results['errors'].append(result['error'])
                print(f"   ❌ Error: {result['error']}")

    def run_conversation_history_test(self):
        """Test conversation history feature"""
        print("\n" + "="*70)
        print("  TEST 4: Conversation History")
        print("="*70)

        conversation = [
            "Hey! Love your content!",
            "What kind of content do you post?",
            "That sounds amazing! Do you take requests?",
            "How can I support you more?",
        ]

        print("\n💬 Testing context-aware responses...")

        for i, message in enumerate(conversation, 1):
            print(f"\n   Message {i}: \"{message}\"")

            result = self.test_message(message)
            self.results['total_requests'] += 1

            if result['success']:
                self.results['successful'] += 1
                self.results['response_times'].append(result['response_time'])
                print(f"   Response: \"{result['response'][:60]}...\"")
                print(f"   Time: {result['response_time']:.2f}s")
            else:
                self.results['failed'] += 1
                self.results['errors'].append(result['error'])
                print(f"   ❌ Error: {result['error']}")

    def print_summary(self):
        """Print comprehensive test summary"""
        print("\n" + "="*70)
        print("  STRESS TEST SUMMARY")
        print("="*70)

        # Overall stats
        print(f"\n📊 Overall Statistics:")
        print(f"   Total Requests: {self.results['total_requests']}")
        print(f"   Successful: {self.results['successful']} ({self.results['successful']/self.results['total_requests']*100:.1f}%)")
        print(f"   Failed: {self.results['failed']} ({self.results['failed']/self.results['total_requests']*100:.1f}%)")

        # Response time stats
        if self.results['response_times']:
            times = self.results['response_times']
            print(f"\n⏱️  Response Time Statistics:")
            print(f"   Mean: {mean(times):.2f}s")
            print(f"   Median: {median(times):.2f}s")
            print(f"   Min: {min(times):.2f}s")
            print(f"   Max: {max(times):.2f}s")
            if len(times) > 1:
                print(f"   Std Dev: {stdev(times):.2f}s")

        # Error summary
        if self.results['errors']:
            print(f"\n❌ Errors Encountered:")
            error_counts = {}
            for error in self.results['errors']:
                error_type = error.split(':')[0] if ':' in error else error[:50]
                error_counts[error_type] = error_counts.get(error_type, 0) + 1

            for error_type, count in error_counts.items():
                print(f"   - {error_type}: {count} time(s)")

        # Performance rating
        success_rate = self.results['successful'] / self.results['total_requests'] * 100
        avg_time = mean(self.results['response_times']) if self.results['response_times'] else 0

        print(f"\n🎯 Performance Rating:")

        if success_rate >= 95 and avg_time < 3:
            print("   ⭐⭐⭐⭐⭐ EXCELLENT - Production Ready!")
        elif success_rate >= 90 and avg_time < 5:
            print("   ⭐⭐⭐⭐ GOOD - Minor optimizations recommended")
        elif success_rate >= 80:
            print("   ⭐⭐⭐ FAIR - Some issues need attention")
        else:
            print("   ⭐⭐ NEEDS IMPROVEMENT - Significant issues detected")

        print("\n" + "="*70)


def main():
    """Run stress tests"""
    print("\n" + "="*70)
    print("  OFChat - Stress Test Suite")
    print("="*70)
    print("\n🔧 Initializing tests...")

    # Validate configuration
    try:
        Config.validate()
        print("✅ Configuration valid")
    except Exception as e:
        print(f"❌ Configuration error: {e}")
        return

    # Initialize stress test
    stress_test = StressTest()

    # Test API connection
    print("🔌 Testing API connection...")
    if not stress_test.client.test_connection():
        print("❌ Cannot connect to Groq API")
        return
    print("✅ API connection successful")

    # Run all tests
    try:
        stress_test.run_basic_tests()
        stress_test.run_load_test(num_requests=20)
        stress_test.run_edge_cases()
        stress_test.run_conversation_history_test()

        # Print summary
        stress_test.print_summary()

    except KeyboardInterrupt:
        print("\n\n⚠️  Test interrupted by user")
        stress_test.print_summary()

    except Exception as e:
        print(f"\n❌ Test suite error: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
