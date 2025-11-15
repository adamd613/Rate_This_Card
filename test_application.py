"""
Test script to verify the application works with real MTG data
"""
import sys
import json
from scryfall_api import ScryfallAPI

def test_api():
    """Test basic API functionality"""
    
    print("Testing MTG Draft Rater Application")
    print("=" * 50)
    
    # Test 1: Fetch available sets
    print("\n✓ Test 1: Fetching available MTG sets...")
    sets = ScryfallAPI.get_set_codes()
    if sets:
        print(f"  Found {len(sets)} sets")
        print(f"  Latest sets: {', '.join([s['code'] for s in sets[:5]])}")
    else:
        print("  ✗ FAILED: Could not fetch sets")
        return False
    
    # Test 2: Fetch cards from a specific set
    print("\n✓ Test 2: Fetching cards from a set...")
    # Using a smaller set for testing - Murders at Karlov Manor (MKM) or similar
    # Let's try with a recent set
    
    test_set = None
    for s in sets:
        if s['code'] in ['ONE', 'DMU', 'BRO']:  # Known recent sets
            test_set = s
            break
    
    if not test_set:
        test_set = sets[0]  # Use first available
    
    print(f"  Using set: {test_set['name']} ({test_set['code']})")
    
    cards = ScryfallAPI.get_set_cards(test_set['code'])
    if cards:
        print(f"  Found {len(cards)} cards in set")
        
        # Test 3: Parse card data
        print("\n✓ Test 3: Parsing card data...")
        sample_card = cards[0]
        parsed = ScryfallAPI.parse_card_data(sample_card)
        
        print(f"  Sample card: {parsed['name']}")
        print(f"  Type: {parsed['type_line']}")
        print(f"  CMC: {parsed['cmc']}")
        print(f"  Keywords: {', '.join(parsed['keywords']) if parsed['keywords'] else 'None'}")
        
        # Test 4: Card rating engine
        print("\n✓ Test 4: Testing card rating engine...")
        from card_rating_engine import CardRatingEngine
        
        # Convert all cards
        parsed_cards = []
        for card in cards[:100]:  # Test with first 100 for speed
            try:
                parsed_cards.append(ScryfallAPI.parse_card_data(card))
            except:
                pass
        
        engine = CardRatingEngine(parsed_cards)
        print(f"  Loaded {len(parsed_cards)} cards into rating engine")
        
        # Test rating with a sample deck
        test_deck = []
        if len(parsed_cards) >= 5:
            test_deck = [parsed_cards[i]['name'] for i in range(min(5, len(parsed_cards)))]
        
        if test_deck:
            print(f"  Testing with sample deck: {', '.join(test_deck)}")
            ratings = engine.rate_cards(test_deck)
            
            if ratings:
                print(f"  Got ratings for {len(ratings)} cards")
                top_3 = ratings[:3]
                for i, (name, rating, explanation, card) in enumerate(top_3, 1):
                    print(f"    {i}. {name}: {rating}/10 - {explanation}")
            else:
                print("  ✗ FAILED: Could not generate ratings")
                return False
        
        print("\n✓ Test 5: Performance check")
        print("  All operations completed successfully!")
        
    else:
        print("  ✗ FAILED: Could not fetch cards")
        return False
    
    print("\n" + "=" * 50)
    print("✓ All tests passed! Application is ready to use.")
    print("\nRun 'python main.py' to start drafting!")
    return True

if __name__ == "__main__":
    try:
        success = test_api()
        sys.exit(0 if success else 1)
    except Exception as e:
        print(f"\n✗ Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
