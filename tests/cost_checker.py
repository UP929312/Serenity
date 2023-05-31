import sys

if "pytest" not in sys.modules:
    from test_costs import test_open_ai_cost, test_deepgram_remaining_credits, test_elevenlabs_remaining_characters
    open_ai_cost = test_open_ai_cost()
    deepgram_remaining_credits = test_deepgram_remaining_credits()
    #elevenlabs_remaining_characters = test_elevenlabs_remaining_characters()
    print(f"OpenAI: {open_ai_cost}")
    print(f"Deepgram: {deepgram_remaining_credits}")
    #print(f"Eleven Labs: {elevenlabs_remaining_characters}")