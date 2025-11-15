"""
Main MTG Draft Deck Rating Application
"""
import os
import json
from typing import List, Dict, Any
from colorama import Fore, Style, init
from scryfall_api import ScryfallAPI
from card_rating_engine import CardRatingEngine

# Initialize colorama for colored terminal output
init(autoreset=True)

class MTGDraftRater:
    """Main application class for MTG draft deck rating"""
    
    def __init__(self):
        self.current_set = None
        self.set_cards = []
        self.rating_engine = None
        self.selected_cards = []
        self.cache_dir = "cache"
        
        # Create cache directory if it doesn't exist
        if not os.path.exists(self.cache_dir):
            os.makedirs(self.cache_dir)
    
    def run(self):
        """Main application loop"""
        self._print_header()
        
        while True:
            print(f"\n{Fore.CYAN}=== MTG Draft Deck Rater ==={Style.RESET_ALL}")
            print("1. Select a set to draft from")
            print("2. Add/update selected cards")
            print("3. Rate remaining cards")
            print("4. View deck statistics")
            print("5. Save deck")
            print("6. Load deck")
            print("7. Exit")
            
            choice = input("\nEnter your choice (1-7): ").strip()
            
            if choice == "1":
                self._select_set()
            elif choice == "2":
                self._add_cards()
            elif choice == "3":
                self._rate_cards()
            elif choice == "4":
                self._view_statistics()
            elif choice == "5":
                self._save_deck()
            elif choice == "6":
                self._load_deck()
            elif choice == "7":
                print(f"\n{Fore.GREEN}Thanks for using MTG Draft Rater!{Style.RESET_ALL}")
                break
            else:
                print(f"{Fore.RED}Invalid choice. Please try again.{Style.RESET_ALL}")
    
    def _print_header(self):
        """Print application header"""
        print(f"\n{Fore.MAGENTA}")
        print("╔════════════════════════════════════════╗")
        print("║     MTG DRAFT DECK RATING ENGINE       ║")
        print("║                                        ║")
        print("║  Craft the perfect draft deck with AI  ║")
        print("║  card ratings based on synergy,        ║")
        print("║  mana curve, and metagame analysis     ║")
        print("╚════════════════════════════════════════╝")
        print(Style.RESET_ALL)
    
    def _select_set(self):
        """Select a MTG set to draft from"""
        print(f"\n{Fore.CYAN}Fetching available MTG sets...{Style.RESET_ALL}")
        
        sets = ScryfallAPI.get_set_codes()
        if not sets:
            print(f"{Fore.RED}Error: Could not fetch sets. Check your internet connection.{Style.RESET_ALL}")
            return
        
        # Display sets
        print(f"\n{Fore.YELLOW}Available sets:{Style.RESET_ALL}")
        for i, s in enumerate(sets[:30], 1):
            print(f"{i:2}. {s['name']:30} ({s['code']})")
        
        print("... and more")
        
        # Let user search or select
        while True:
            user_input = input("\nEnter set code (e.g., MOM) or search term: ").strip().upper()
            
            # Search for matching sets
            matching_sets = [s for s in sets if user_input in s['code'] or user_input.lower() in s['name'].lower()]
            
            if len(matching_sets) == 1:
                selected_set = matching_sets[0]
                self._load_set(selected_set)
                return
            elif len(matching_sets) > 1:
                print(f"\n{Fore.YELLOW}Found {len(matching_sets)} matching sets:{Style.RESET_ALL}")
                for i, s in enumerate(matching_sets[:10], 1):
                    print(f"{i}. {s['name']} ({s['code']})")
                
                try:
                    choice = int(input("Select set (number): "))
                    if 1 <= choice <= len(matching_sets):
                        self._load_set(matching_sets[choice - 1])
                        return
                except ValueError:
                    pass
                
                print(f"{Fore.RED}Invalid selection.{Style.RESET_ALL}")
            else:
                print(f"{Fore.RED}No matching sets found. Try again.{Style.RESET_ALL}")
    
    def _load_set(self, set_info: Dict[str, str]):
        """Load cards from a selected set"""
        set_code = set_info['code']
        
        # Check cache first
        cache_file = os.path.join(self.cache_dir, f"{set_code}.json")
        if os.path.exists(cache_file):
            print(f"{Fore.CYAN}Loading {set_info['name']} from cache...{Style.RESET_ALL}")
            try:
                with open(cache_file, 'r', encoding='utf-8') as f:
                    cards_data = json.load(f)
                    self.set_cards = cards_data
            except Exception as e:
                print(f"{Fore.YELLOW}Cache load failed: {e}. Fetching from Scryfall...{Style.RESET_ALL}")
                self._fetch_set(set_code, set_info, cache_file)
        else:
            self._fetch_set(set_code, set_info, cache_file)
        
        # Initialize rating engine
        self.current_set = set_info['name']
        self.rating_engine = CardRatingEngine(self.set_cards)
        self.selected_cards = []
        
        print(f"\n{Fore.GREEN}✓ Loaded {len(self.set_cards)} cards from {self.current_set}{Style.RESET_ALL}")
        print(f"Ready to build your deck! Start by adding cards.")
    
    def _fetch_set(self, set_code: str, set_info: Dict[str, str], cache_file: str):
        """Fetch set from Scryfall and cache it"""
        print(f"{Fore.CYAN}Fetching {set_info['name']} cards from Scryfall...{Style.RESET_ALL}")
        
        raw_cards = ScryfallAPI.get_set_cards(set_code)
        if not raw_cards:
            print(f"{Fore.RED}Error: Could not fetch cards for {set_code}{Style.RESET_ALL}")
            return
        
        # Parse cards
        self.set_cards = []
        for card in raw_cards:
            try:
                parsed = ScryfallAPI.parse_card_data(card)
                self.set_cards.append(parsed)
            except Exception as e:
                print(f"{Fore.YELLOW}Warning: Could not parse card {card.get('name', 'Unknown')}: {e}{Style.RESET_ALL}")
        
        # Cache the data
        try:
            with open(cache_file, 'w', encoding='utf-8') as f:
                json.dump(self.set_cards, f, indent=2, ensure_ascii=False)
        except Exception as e:
            print(f"{Fore.YELLOW}Warning: Could not cache set data: {e}{Style.RESET_ALL}")
    
    def _add_cards(self):
        """Add cards to the deck"""
        if not self.rating_engine:
            print(f"{Fore.RED}Please select a set first.{Style.RESET_ALL}")
            return
        
        print(f"\n{Fore.CYAN}Currently selected cards ({len(self.selected_cards)}/40):{Style.RESET_ALL}")
        if self.selected_cards:
            for i, card_name in enumerate(self.selected_cards, 1):
                print(f"  {i:2}. {card_name}")
        else:
            print("  (none)")
        
        print(f"\n{Fore.YELLOW}Commands:{Style.RESET_ALL}")
        print("  'add' - Add a card")
        print("  'remove N' - Remove card at position N")
        print("  'clear' - Clear all cards")
        print("  'done' - Return to main menu")
        
        while True:
            user_input = input("\nEnter command: ").strip()
            
            if user_input.lower() == "done":
                break
            elif user_input.lower() == "clear":
                self.selected_cards = []
                print(f"{Fore.GREEN}Deck cleared.{Style.RESET_ALL}")
            elif user_input.lower().startswith("remove"):
                try:
                    idx = int(user_input.split()[1]) - 1
                    if 0 <= idx < len(self.selected_cards):
                        removed = self.selected_cards.pop(idx)
                        print(f"{Fore.GREEN}✓ Removed {removed}{Style.RESET_ALL}")
                except (ValueError, IndexError):
                    print(f"{Fore.RED}Invalid command.{Style.RESET_ALL}")
            elif user_input.lower() == "add":
                self._add_single_card()
            else:
                print(f"{Fore.RED}Unknown command.{Style.RESET_ALL}")
    
    def _add_single_card(self):
        """Add a single card to the deck"""
        if len(self.selected_cards) >= 40:
            print(f"{Fore.YELLOW}Deck is full (40 cards).{Style.RESET_ALL}")
            return
        
        card_name = input("Enter card name: ").strip()
        if not card_name:
            return
        
        # Fuzzy match the card
        card_lookup = {card["name"].lower(): card["name"] for card in self.set_cards}
        
        if card_name.lower() in card_lookup:
            actual_name = card_lookup[card_name.lower()]
            if actual_name not in self.selected_cards:
                self.selected_cards.append(actual_name)
                print(f"{Fore.GREEN}✓ Added {actual_name}{Style.RESET_ALL}")
            else:
                print(f"{Fore.YELLOW}This card is already in your deck.{Style.RESET_ALL}")
        else:
            # Try fuzzy matching
            matching = [card["name"] for card in self.set_cards 
                       if card_name.lower() in card["name"].lower()]
            
            if len(matching) == 1:
                if matching[0] not in self.selected_cards:
                    self.selected_cards.append(matching[0])
                    print(f"{Fore.GREEN}✓ Added {matching[0]}{Style.RESET_ALL}")
                else:
                    print(f"{Fore.YELLOW}This card is already in your deck.{Style.RESET_ALL}")
            elif len(matching) > 1:
                print(f"{Fore.YELLOW}Found {len(matching)} matches:{Style.RESET_ALL}")
                for i, card in enumerate(matching[:10], 1):
                    print(f"  {i}. {card}")
                
                try:
                    choice = int(input("Select card (number): "))
                    if 1 <= choice <= len(matching):
                        card = matching[choice - 1]
                        if card not in self.selected_cards:
                            self.selected_cards.append(card)
                            print(f"{Fore.GREEN}✓ Added {card}{Style.RESET_ALL}")
                        else:
                            print(f"{Fore.YELLOW}This card is already in your deck.{Style.RESET_ALL}")
                except ValueError:
                    print(f"{Fore.RED}Invalid selection.{Style.RESET_ALL}")
            else:
                print(f"{Fore.RED}Card not found in set.{Style.RESET_ALL}")
    
    def _rate_cards(self):
        """Rate all remaining cards"""
        if not self.rating_engine:
            print(f"{Fore.RED}Please select a set first.{Style.RESET_ALL}")
            return
        
        if not self.selected_cards:
            print(f"{Fore.YELLOW}Add some cards first to get recommendations.{Style.RESET_ALL}")
            return
        
        print(f"\n{Fore.CYAN}Analyzing your deck and rating cards...{Style.RESET_ALL}")
        
        ratings = self.rating_engine.rate_cards(self.selected_cards)
        
        if not ratings:
            print(f"{Fore.RED}Error: Could not rate cards.{Style.RESET_ALL}")
            return
        
        # Display top rated cards
        print(f"\n{Fore.YELLOW}Top 20 recommendations for your deck:{Style.RESET_ALL}\n")
        
        for rank, (name, rating, explanation, card) in enumerate(ratings[:20], 1):
            color_code = self._get_rating_color(rating)
            mana_str = card.get("mana_cost", "").replace("{", "[").replace("}", "]") or "0"
            cmc = card.get("cmc", 0)
            card_type = card.get("type_line", "Unknown")
            
            print(f"{Fore.LIGHTBLACK_EX}{rank:2}.{Style.RESET_ALL} {color_code}{rating:4.1f}/10{Style.RESET_ALL} "
                  f"{name:25} {mana_str:15} {card_type:30}")
            print(f"      {Fore.LIGHTBLACK_EX}→ {explanation}{Style.RESET_ALL}")
        
        # Interactive browsing
        while True:
            print(f"\n{Fore.CYAN}Options: 'add N' (add card N), 'more' (show more), 'details N' (see card details), 'done'{Style.RESET_ALL}")
            user_input = input("Command: ").strip().lower()
            
            if user_input == "done":
                break
            elif user_input == "more":
                print(f"\n{Fore.YELLOW}Next 20 recommendations:{Style.RESET_ALL}\n")
                for rank, (name, rating, explanation, card) in enumerate(ratings[20:40], 21):
                    color_code = self._get_rating_color(rating)
                    mana_str = card.get("mana_cost", "").replace("{", "[").replace("}", "]") or "0"
                    print(f"{Fore.LIGHTBLACK_EX}{rank:2}.{Style.RESET_ALL} {color_code}{rating:4.1f}/10{Style.RESET_ALL} "
                          f"{name:25} {mana_str:15}")
                    print(f"      {Fore.LIGHTBLACK_EX}→ {explanation}{Style.RESET_ALL}")
            elif user_input.startswith("add"):
                try:
                    idx = int(user_input.split()[1]) - 1
                    if 0 <= idx < len(ratings):
                        card_name = ratings[idx][0]
                        if card_name not in self.selected_cards and len(self.selected_cards) < 40:
                            self.selected_cards.append(card_name)
                            print(f"{Fore.GREEN}✓ Added {card_name}. Deck: {len(self.selected_cards)}/40{Style.RESET_ALL}")
                        else:
                            print(f"{Fore.YELLOW}Card already in deck or deck is full.{Style.RESET_ALL}")
                except (ValueError, IndexError):
                    print(f"{Fore.RED}Invalid command.{Style.RESET_ALL}")
            elif user_input.startswith("details"):
                try:
                    idx = int(user_input.split()[1]) - 1
                    if 0 <= idx < len(ratings):
                        self._show_card_details(ratings[idx][3])
                except (ValueError, IndexError):
                    print(f"{Fore.RED}Invalid command.{Style.RESET_ALL}")
            else:
                print(f"{Fore.RED}Unknown command.{Style.RESET_ALL}")
    
    def _show_card_details(self, card: Dict[str, Any]):
        """Display detailed card information"""
        print(f"\n{Fore.CYAN}{'=' * 60}{Style.RESET_ALL}")
        print(f"{Fore.YELLOW}{card['name']}{Style.RESET_ALL}")
        print(f"{Fore.LIGHTBLACK_EX}{card['type_line']}{Style.RESET_ALL}")
        
        if card.get("mana_cost"):
            print(f"Mana Cost: {card['mana_cost'].replace('{', '[').replace('}', ']')}")
        
        if card.get("power") and card.get("toughness"):
            print(f"Power/Toughness: {card['power']}/{card['toughness']}")
        
        print(f"\n{Fore.LIGHTBLACK_EX}{card.get('oracle_text', 'No text')}{Style.RESET_ALL}")
        
        if card.get("keywords"):
            print(f"\n{Fore.YELLOW}Keywords:{Style.RESET_ALL} {', '.join(card['keywords'])}")
        
        print(f"{Fore.CYAN}{'=' * 60}{Style.RESET_ALL}\n")
    
    def _view_statistics(self):
        """Display deck statistics"""
        if not self.selected_cards or not self.rating_engine:
            print(f"{Fore.RED}No deck to analyze.{Style.RESET_ALL}")
            return
        
        # Get deck analysis
        deck_cards = self.rating_engine._parse_selected_cards(self.selected_cards)
        if not deck_cards:
            print(f"{Fore.RED}Could not analyze deck.{Style.RESET_ALL}")
            return
        
        analysis = self.rating_engine._analyze_deck(deck_cards)
        
        print(f"\n{Fore.CYAN}{'=' * 60}")
        print(f"DECK STATISTICS - {self.current_set}")
        print(f"{'=' * 60}{Style.RESET_ALL}\n")
        
        print(f"Deck Size: {Fore.YELLOW}{analysis['count']}{Style.RESET_ALL}/40 cards")
        print(f"Creatures: {Fore.YELLOW}{analysis['creatures']}{Style.RESET_ALL} ({analysis['creatures']*100//max(1, analysis['count'])}%)")
        print(f"Spells: {Fore.YELLOW}{analysis['spells']}{Style.RESET_ALL}")
        print(f"Average CMC: {Fore.YELLOW}{analysis['avg_cmc']:.2f}{Style.RESET_ALL}")
        
        print(f"\n{Fore.CYAN}Mana Curve:{Style.RESET_ALL}")
        for cmc in range(7):
            count = analysis['cmc_distribution'].get(cmc, 0)
            bar = "█" * count
            print(f"  {cmc}: {Fore.LIGHTGREEN_EX}{bar}{Style.RESET_ALL} ({count})")
        
        if analysis['color_identity']:
            colors = sorted(list(analysis['color_identity']))
            color_names = [self.rating_engine._color_name(c) for c in colors]
            print(f"\n{Fore.CYAN}Colors:{Style.RESET_ALL} {', '.join(color_names)}")
        
        if analysis['synergies']:
            print(f"\n{Fore.CYAN}Detected Themes/Synergies:{Style.RESET_ALL}")
            for synergy in analysis['synergies']:
                print(f"  • {synergy}")
        
        print(f"\n{Fore.CYAN}{'=' * 60}{Style.RESET_ALL}\n")
    
    def _save_deck(self):
        """Save the current deck to a file"""
        if not self.selected_cards:
            print(f"{Fore.YELLOW}No deck to save.{Style.RESET_ALL}")
            return
        
        filename = input("Enter filename (without extension): ").strip()
        if not filename:
            return
        
        filepath = os.path.join(self.cache_dir, f"{filename}.deck")
        
        deck_data = {
            "set": self.current_set,
            "cards": self.selected_cards
        }
        
        try:
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(deck_data, f, indent=2, ensure_ascii=False)
            print(f"{Fore.GREEN}✓ Deck saved to {filepath}{Style.RESET_ALL}")
        except Exception as e:
            print(f"{Fore.RED}Error saving deck: {e}{Style.RESET_ALL}")
    
    def _load_deck(self):
        """Load a saved deck from a file"""
        # List available decks
        deck_files = [f for f in os.listdir(self.cache_dir) if f.endswith('.deck')]
        
        if not deck_files:
            print(f"{Fore.YELLOW}No saved decks found.{Style.RESET_ALL}")
            return
        
        print(f"{Fore.YELLOW}Available decks:{Style.RESET_ALL}")
        for i, f in enumerate(deck_files, 1):
            print(f"  {i}. {f[:-5]}")
        
        try:
            choice = int(input("Select deck (number): ")) - 1
            if 0 <= choice < len(deck_files):
                filepath = os.path.join(self.cache_dir, deck_files[choice])
                
                with open(filepath, 'r', encoding='utf-8') as f:
                    deck_data = json.load(f)
                
                # Verify set is available
                set_name = deck_data.get("set")
                print(f"{Fore.CYAN}Loading {set_name}...{Style.RESET_ALL}")
                
                # Fetch set if needed
                sets = ScryfallAPI.get_set_codes()
                matching_set = next((s for s in sets if s['name'] == set_name), None)
                
                if matching_set:
                    self._load_set(matching_set)
                    self.selected_cards = deck_data.get("cards", [])
                    print(f"{Fore.GREEN}✓ Deck loaded: {len(self.selected_cards)} cards{Style.RESET_ALL}")
                else:
                    print(f"{Fore.RED}Could not find set {set_name}.{Style.RESET_ALL}")
        except (ValueError, json.JSONDecodeError):
            print(f"{Fore.RED}Error loading deck.{Style.RESET_ALL}")
    
    def _get_rating_color(self, rating: float) -> str:
        """Get color based on rating"""
        if rating >= 8:
            return Fore.LIGHTGREEN_EX
        elif rating >= 6:
            return Fore.GREEN
        elif rating >= 4:
            return Fore.YELLOW
        elif rating >= 2:
            return Fore.LIGHTRED_EX
        else:
            return Fore.RED


def main():
    """Entry point for the application"""
    app = MTGDraftRater()
    try:
        app.run()
    except KeyboardInterrupt:
        print(f"\n\n{Fore.YELLOW}Application interrupted.{Style.RESET_ALL}")
    except Exception as e:
        print(f"\n{Fore.RED}An error occurred: {e}{Style.RESET_ALL}")


if __name__ == "__main__":
    main()
