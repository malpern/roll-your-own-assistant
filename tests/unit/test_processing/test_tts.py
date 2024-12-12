from openai import OpenAI
import os
from dotenv import load_dotenv
import time
import httpx

def verify_api_key():
    """Verify the OpenAI API key works with a simple models list request."""
    try:
        client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))
        _ = client.models.list()  # Using _ to indicate we don't use the return value
        return True
    except Exception as e:
        print(f"API Key verification failed: {str(e)}")
        return False

def test_tts(text="Hello, testing text to speech."):
    """Test OpenAI's text-to-speech functionality."""
    print("1. Starting OpenAI TTS test...")
    
    # Load environment variables
    print("2. Loading environment variables...")
    load_dotenv()
    api_key = os.getenv('OPENAI_API_KEY')
    if not api_key:
        print("Error: OPENAI_API_KEY not found in environment variables")
        return False
    print("3. API key loaded successfully")
    
    # Verify API key works
    print("4. Verifying API key...")
    if not verify_api_key():
        return False
    print("5. API key verified")
    
    try:
        # Initialize OpenAI client with timeout
        print("6. Initializing OpenAI client...")
        timeout = httpx.Timeout(30.0, connect=20.0)
        client = OpenAI(
            api_key=api_key,
            http_client=httpx.Client(timeout=timeout)
        )
        print("7. Client initialized")
        
        # Generate speech
        print(f"8. Converting text to speech: '{text}'")
        print("   This may take a few seconds...")
        start_time = time.time()
        
        with client.audio.speech.create(
            model="tts-1",
            voice="alloy",
            input=text
        ).with_streaming_response() as response:
            # Save to file
            print("10. Saving to file...")
            output_file = "tts_output.mp3"
            with open(output_file, 'wb') as f:
                for chunk in response.iter_bytes():
                    f.write(chunk)
            
        duration = time.time() - start_time
        print(f"9. Speech generated in {duration:.2f} seconds")
        print(f"11. Audio saved to {output_file}")
        
        return True
        
    except Exception as e:
        print(f"\nError during text-to-speech conversion: {str(e)}")
        return False

if __name__ == "__main__":
    test_tts() 