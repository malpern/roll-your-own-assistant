from audio_player import AudioPlayer
import time

def test_audio_player():
    print("\n🧪 Testing Audio Player...")
    
    # Create player instance
    player = AudioPlayer()
    
    # Test with a sample response file
    # You can use any .mp3 file in your responses/ directory
    # If none exists, we'll print available files
    from pathlib import Path
    responses_dir = Path("responses")
    
    if not responses_dir.exists():
        print("❌ No responses directory found")
        return
        
    response_files = list(responses_dir.glob("*.mp3"))
    
    if not response_files:
        print("❌ No response files found in responses/")
        print("Please run the main application first to generate a response")
        return
        
    # Play the most recent response file
    latest_response = max(response_files, key=lambda x: x.stat().st_mtime)
    print(f"\n▶️  Playing: {latest_response}")
    
    # Test playback
    player.play_file(latest_response)
    
    print("\n✅ Audio player test complete")

if __name__ == "__main__":
    test_audio_player() 