"""
MTG Draft Rater GUI - Graphical User Interface
Built with tkinter for cross-platform compatibility
"""

import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext, simpledialog
import threading
import json
from datetime import datetime
from scryfall_api import ScryfallAPI
from card_rating_engine import CardRatingEngine


class MTGDraftRaterGUI:
    """Main GUI application class"""
    
    def __init__(self, root):
        self.root = root
        self.root.title("MTG Draft Deck Rating Engine")
        self.root.geometry("1400x900")
        
        # Configure style
        self.style = ttk.Style()
        self.style.theme_use('clam')
        
        # Application state
        self.current_set = None
        self.set_cards = []
        self.rating_engine = None
        self.selected_cards = []
        self.all_sets = []
        self.current_ratings = []
        
        # Create UI
        self._create_widgets()
        self._load_sets_async()
    
    def _create_widgets(self):
        """Create all UI widgets"""
        # Main container
        main_frame = ttk.Frame(self.root)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # TOP: Set Selection Panel
        self._create_set_panel(main_frame)
        
        # MIDDLE: Two-column layout
        middle_frame = ttk.Frame(main_frame)
        middle_frame.pack(fill=tk.BOTH, expand=True, pady=10)
        
        # Left column: Deck management
        self._create_deck_panel(middle_frame)
        
        # Right column: Recommendations
        self._create_recommendations_panel(middle_frame)
        
        # BOTTOM: Stats and controls
        self._create_stats_panel(main_frame)
    
    def _create_set_panel(self, parent):
        """Create set selection panel"""
        set_frame = ttk.LabelFrame(parent, text="Select MTG Set", padding=10)
        set_frame.pack(fill=tk.X, pady=(0, 10))
        
        # Search box
        search_frame = ttk.Frame(set_frame)
        search_frame.pack(fill=tk.X, pady=(0, 10))
        
        ttk.Label(search_frame, text="Search Set:").pack(side=tk.LEFT, padx=5)
        
        self.set_search_var = tk.StringVar()
        self.set_search_var.trace('w', self._filter_sets)
        search_entry = ttk.Entry(search_frame, textvariable=self.set_search_var, width=20)
        search_entry.pack(side=tk.LEFT, padx=5)
        
        # Set dropdown
        ttk.Label(search_frame, text="or Select:").pack(side=tk.LEFT, padx=20)
        
        self.set_combo_var = tk.StringVar()
        self.set_combo = ttk.Combobox(
            search_frame,
            textvariable=self.set_combo_var,
            state='readonly',
            width=40
        )
        self.set_combo.pack(side=tk.LEFT, padx=5, fill=tk.X, expand=True)
        self.set_combo.bind('<<ComboboxSelected>>', self._on_set_selected)
        
        ttk.Button(search_frame, text="Load Set", command=self._load_set_clicked).pack(side=tk.LEFT, padx=5)
        
        # Status
        self.set_status_var = tk.StringVar(value="Ready to select a set...")
        ttk.Label(set_frame, textvariable=self.set_status_var, foreground="blue").pack(fill=tk.X)
    
    def _create_deck_panel(self, parent):
        """Create deck management panel"""
        deck_frame = ttk.LabelFrame(parent, text="Your Deck", padding=10)
        deck_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 5))
        
        # Add card section
        add_frame = ttk.Frame(deck_frame)
        add_frame.pack(fill=tk.X, pady=(0, 10))
        
        ttk.Label(add_frame, text="Add Card:").pack(side=tk.LEFT, padx=5)
        
        self.card_entry_var = tk.StringVar()
        self.card_entry = ttk.Entry(add_frame, textvariable=self.card_entry_var, width=30)
        self.card_entry.pack(side=tk.LEFT, padx=5, fill=tk.X, expand=True)
        self.card_entry.bind('<Return>', lambda e: self._add_card_clicked())
        
        ttk.Button(add_frame, text="Add", command=self._add_card_clicked).pack(side=tk.LEFT, padx=2)
        ttk.Button(add_frame, text="Clear All", command=self._clear_deck).pack(side=tk.LEFT, padx=2)
        
        # Deck list
        list_frame = ttk.Frame(deck_frame)
        list_frame.pack(fill=tk.BOTH, expand=True)
        
        # Scrollbar for listbox
        scrollbar = ttk.Scrollbar(list_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.deck_listbox = tk.Listbox(
            list_frame,
            yscrollcommand=scrollbar.set,
            height=20
        )
        self.deck_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.config(command=self.deck_listbox.yview)
        
        # Deck controls
        control_frame = ttk.Frame(deck_frame)
        control_frame.pack(fill=tk.X, pady=10)
        
        ttk.Button(control_frame, text="Remove Selected", command=self._remove_card).pack(side=tk.LEFT, padx=2)
        ttk.Button(control_frame, text="Save Deck", command=self._save_deck).pack(side=tk.LEFT, padx=2)
        ttk.Button(control_frame, text="Load Deck", command=self._load_deck).pack(side=tk.LEFT, padx=2)
        
        # Deck size indicator
        self.deck_size_var = tk.StringVar(value="Deck: 0/40")
        ttk.Label(control_frame, textvariable=self.deck_size_var, foreground="green").pack(side=tk.RIGHT, padx=5)
    
    def _create_recommendations_panel(self, parent):
        """Create card recommendations panel"""
        rec_frame = ttk.LabelFrame(parent, text="Cards in Set", padding=10)
        rec_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        
        # Search and rate controls
        control_frame = ttk.Frame(rec_frame)
        control_frame.pack(fill=tk.X, pady=(0, 10))
        
        ttk.Label(control_frame, text="Search:").pack(side=tk.LEFT, padx=5)
        
        self.card_search_var = tk.StringVar()
        self.card_search_var.trace('w', self._update_card_list)
        search_entry = ttk.Entry(control_frame, textvariable=self.card_search_var, width=20)
        search_entry.pack(side=tk.LEFT, padx=5, fill=tk.X, expand=True)
        
        ttk.Button(control_frame, text="Rate Cards", command=self._rate_cards_clicked).pack(side=tk.LEFT, padx=5)
        
        # Results display with tree view for better card listing
        tree_frame = ttk.Frame(rec_frame)
        tree_frame.pack(fill=tk.BOTH, expand=True)
        
        # Create treeview
        scrollbar = ttk.Scrollbar(tree_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.card_tree = ttk.Treeview(
            tree_frame,
            columns=("Rating", "Mana", "Type"),
            height=25,
            yscrollcommand=scrollbar.set
        )
        self.card_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.config(command=self.card_tree.yview)
        
        # Configure columns
        self.card_tree.heading('#0', text='Card Name')
        self.card_tree.heading('Rating', text='Rating')
        self.card_tree.heading('Mana', text='Mana')
        self.card_tree.heading('Type', text='Type')
        
        self.card_tree.column('#0', width=200)
        self.card_tree.column('Rating', width=50, anchor='center')
        self.card_tree.column('Mana', width=50, anchor='center')
        self.card_tree.column('Type', width=100)
        
        # Store all cards and ratings
        self.all_card_list = []  # Full list of cards
        self.current_card_ratings = {}  # Map of card_name -> rating
        
        # Configure text tags for colors
        self.card_tree.tag_configure("excellent", foreground="#00AA00")  # Green
        self.card_tree.tag_configure("good", foreground="#0088FF")       # Blue
        self.card_tree.tag_configure("okay", foreground="#FFAA00")       # Orange
        self.card_tree.tag_configure("weak", foreground="#FF6600")       # Red
        
        self.card_tree.bind('<Double-1>', self._add_card_from_tree)
        
        # Info label
        self.card_info_var = tk.StringVar(value="Load a set to see cards")
        ttk.Label(rec_frame, textvariable=self.card_info_var, foreground="blue").pack(fill=tk.X, pady=(5, 0))
    
    def _create_stats_panel(self, parent):
        """Create statistics panel"""
        stats_frame = ttk.LabelFrame(parent, text="Deck Analysis", padding=10)
        stats_frame.pack(fill=tk.X, pady=10)
        
        # Stats display (use text widget for multi-line)
        self.stats_text = tk.Text(
            stats_frame,
            height=6,
            width=100,
            state=tk.DISABLED,
            wrap=tk.WORD,
            relief=tk.FLAT,
            bg="#f0f0f0"
        )
        self.stats_text.pack(fill=tk.BOTH, expand=True)
        
        # Refresh stats button
        ttk.Button(stats_frame, text="Refresh Statistics", command=self._update_stats).pack(pady=5)
    
    def _load_sets_async(self):
        """Load sets in background thread"""
        def load():
            self.set_status_var.set("Loading available sets...")
            self.root.update()
            
            sets = ScryfallAPI.get_set_codes()
            self.all_sets = sets
            
            if sets:
                set_names = [f"{s['name']} ({s['code']})" for s in sets]
                self.set_combo['values'] = set_names
                self.set_status_var.set(f"Ready! {len(sets)} sets available.")
            else:
                self.set_status_var.set("Failed to load sets. Check internet connection.")
                messagebox.showerror("Error", "Could not fetch sets from Scryfall API")
        
        thread = threading.Thread(target=load, daemon=True)
        thread.start()
    
    def _filter_sets(self, *args):
        """Filter sets based on search"""
        search_term = self.set_search_var.get().lower()
        if not search_term:
            if self.all_sets:
                set_names = [f"{s['name']} ({s['code']})" for s in self.all_sets]
                self.set_combo['values'] = set_names
            return
        
        filtered = [s for s in self.all_sets 
                   if search_term in s['name'].lower() or search_term in s['code'].lower()]
        
        if filtered:
            set_names = [f"{s['name']} ({s['code']})" for s in filtered]
            self.set_combo['values'] = set_names
    
    def _on_set_selected(self, event=None):
        """Handle set selection"""
        pass
    
    def _load_set_clicked(self):
        """Load the selected set"""
        if not self.set_combo_var.get():
            messagebox.showwarning("Warning", "Please select a set first")
            return
        
        # Find the selected set
        combo_text = self.set_combo_var.get()
        selected_set = None
        for s in self.all_sets:
            if f"{s['name']} ({s['code']})" == combo_text:
                selected_set = s
                break
        
        if not selected_set:
            messagebox.showerror("Error", "Set not found")
            return
        
        self.set_status_var.set(f"Loading {selected_set['name']}...")
        self.root.update()
        
        def load():
            cards = ScryfallAPI.get_set_cards(selected_set['code'])
            
            if cards:
                # Parse cards and deduplicate by name
                parsed_cards = []
                seen_cards = set()
                for card in cards:
                    try:
                        parsed = ScryfallAPI.parse_card_data(card)
                        card_name = parsed.get("name", "")
                        if card_name not in seen_cards:
                            seen_cards.add(card_name)
                            parsed_cards.append(parsed)
                    except:
                        pass
                
                self.set_cards = parsed_cards
                self.current_set = selected_set['name']
                self.rating_engine = CardRatingEngine(parsed_cards)
                self.selected_cards = []
                self.all_card_list = parsed_cards
                self.current_card_ratings = {}
                self.deck_listbox.delete(0, tk.END)
                self._update_deck_display()
                self._update_card_list()
                
                self.set_status_var.set(f"✓ Loaded {len(parsed_cards)} cards from {self.current_set}")
                self.card_info_var.set(f"{len(parsed_cards)} cards available")
            else:
                messagebox.showerror("Error", f"Could not load cards for {selected_set['code']}")
                self.set_status_var.set("Failed to load set")
        
        thread = threading.Thread(target=load, daemon=True)
        thread.start()
    
    def _add_card_clicked(self):
        """Add a card to the deck"""
        if not self.rating_engine:
            messagebox.showwarning("Warning", "Please load a set first")
            return
        
        card_name = self.card_entry_var.get().strip()
        if not card_name:
            messagebox.showwarning("Warning", "Please enter a card name")
            return
        
        if len(self.selected_cards) >= 40:
            messagebox.showwarning("Warning", "Deck is full (40 cards)")
            return
        
        # Find the card
        card_lookup = {card["name"].lower(): card["name"] for card in self.set_cards}
        
        if card_name.lower() in card_lookup:
            actual_name = card_lookup[card_name.lower()]
            if actual_name not in self.selected_cards:
                self.selected_cards.append(actual_name)
                self.card_entry_var.set("")
                self._update_deck_display()
                self._update_stats()
            else:
                messagebox.showinfo("Info", "Card already in deck")
        else:
            # Try fuzzy matching
            matching = [card["name"] for card in self.set_cards 
                       if card_name.lower() in card["name"].lower()]
            
            if len(matching) == 1:
                if matching[0] not in self.selected_cards:
                    self.selected_cards.append(matching[0])
                    self.card_entry_var.set("")
                    self._update_deck_display()
                    self._update_stats()
                else:
                    messagebox.showinfo("Info", "Card already in deck")
            elif len(matching) > 1:
                # Show dialog with options
                dialog = tk.Toplevel(self.root)
                dialog.title("Select Card")
                dialog.geometry("300x300")
                
                ttk.Label(dialog, text="Multiple matches found:").pack(padx=10, pady=10)
                
                listbox = tk.Listbox(dialog)
                listbox.pack(fill=tk.BOTH, expand=True, padx=10)
                
                for card in matching[:20]:
                    listbox.insert(tk.END, card)
                
                def select_card():
                    if listbox.curselection():
                        card = matching[listbox.curselection()[0]]
                        if card not in self.selected_cards:
                            self.selected_cards.append(card)
                            self.card_entry_var.set("")
                            self._update_deck_display()
                            self._update_stats()
                        dialog.destroy()
                
                ttk.Button(dialog, text="Select", command=select_card).pack(pady=10)
            else:
                messagebox.showerror("Error", "Card not found in set")
    
    def _remove_card(self):
        """Remove selected card from deck"""
        selection = self.deck_listbox.curselection()
        if selection:
            idx = selection[0]
            self.selected_cards.pop(idx)
            self._update_deck_display()
            self._update_stats()
    
    def _clear_deck(self):
        """Clear entire deck"""
        if messagebox.askyesno("Confirm", "Clear all cards from deck?"):
            self.selected_cards = []
            self._update_deck_display()
            self._update_stats()
    
    def _update_deck_display(self):
        """Update deck listbox display"""
        self.deck_listbox.delete(0, tk.END)
        for i, card in enumerate(self.selected_cards, 1):
            self.deck_listbox.insert(tk.END, f"{i:2}. {card}")
        
        self.deck_size_var.set(f"Deck: {len(self.selected_cards)}/40")
    
    def _rate_cards_clicked(self):
        """Rate cards based on current deck"""
        if not self.rating_engine:
            messagebox.showwarning("Warning", "Please load a set first")
            return
        
        if not self.selected_cards:
            messagebox.showwarning("Warning", "Add some cards first to get recommendations")
            return
        
        self.card_info_var.set("Rating cards...")
        self.root.update()
        
        def rate():
            ratings = self.rating_engine.rate_cards(self.selected_cards)
            self.current_card_ratings = {name: rating for name, rating, _, _ in ratings}
            self._update_card_list()
            
            # Count top recommendations
            top_count = len([r for r in ratings if r[1] >= 7])
            self.card_info_var.set(f"✓ Ratings updated! {top_count} excellent cards found")
        
        thread = threading.Thread(target=rate, daemon=True)
        thread.start()
    
    def _update_card_list(self, *args):
        """Update card list display with search and ratings"""
        search_term = self.card_search_var.get().lower()
        
        # Clear tree
        for item in self.card_tree.get_children():
            self.card_tree.delete(item)
        
        if not self.all_card_list:
            return
        
        # Filter cards
        filtered_cards = []
        for card in self.all_card_list:
            name = card.get("name", "")
            card_type = card.get("type_line", "")
            oracle_text = card.get("oracle_text", "")
            
            if search_term and not any(search_term in text.lower() for text in [name, card_type, oracle_text]):
                continue
            
            filtered_cards.append(card)
        
        # Sort: rated cards first, then by name
        def sort_key(card):
            name = card.get("name", "")
            rating = self.current_card_ratings.get(name, -1)
            # Sort by rating descending, then by name
            return (-rating, name)
        
        filtered_cards.sort(key=sort_key)
        
        # Add to tree
        for idx, card in enumerate(filtered_cards):
            name = card.get("name", "Unknown")
            mana_cost = card.get("mana_cost", "").replace("{", "[").replace("}", "]") or "—"
            card_type = card.get("type_line", "")[:30]  # Truncate long types
            rating = self.current_card_ratings.get(name, None)
            
            # Determine tag based on rating
            tag = ""
            if rating is not None:
                if rating >= 8:
                    tag = "excellent"
                elif rating >= 6:
                    tag = "good"
                elif rating >= 4:
                    tag = "okay"
                else:
                    tag = "weak"
            
            rating_str = f"{rating:.1f}" if rating is not None else "—"
            
            self.card_tree.insert(
                '',
                tk.END,
                text=name,
                values=(rating_str, mana_cost, card_type),
                tags=(tag,)
            )
        
        # Update info
        if not search_term:
            self.card_info_var.set(f"Showing all {len(filtered_cards)} cards (double-click to add)")
        else:
            self.card_info_var.set(f"Showing {len(filtered_cards)} of {len(self.all_card_list)} cards")
    
    def _add_card_from_tree(self, event):
        """Add card from tree view (double-click)"""
        selection = self.card_tree.selection()
        if not selection:
            return
        
        item = selection[0]
        card_name = self.card_tree.item(item, 'text')
        
        if len(self.selected_cards) >= 40:
            messagebox.showwarning("Warning", "Deck is full (40 cards)")
            return
        
        if card_name not in self.selected_cards:
            self.selected_cards.append(card_name)
            self._update_deck_display()
            self._update_stats()
        else:
            messagebox.showinfo("Info", "Card already in deck")
    
    def _update_stats(self):
        """Update deck statistics"""
        if not self.rating_engine or not self.selected_cards:
            self.stats_text.config(state=tk.NORMAL)
            self.stats_text.delete(1.0, tk.END)
            self.stats_text.config(state=tk.DISABLED)
            return
        
        deck_cards = self.rating_engine._parse_selected_cards(self.selected_cards)
        if not deck_cards:
            return
        
        analysis = self.rating_engine._analyze_deck(deck_cards)
        
        stats = f"Deck Size: {analysis['count']}/40  |  "
        stats += f"Creatures: {analysis['creatures']} ({analysis['creatures']*100//max(1, analysis['count'])}%)  |  "
        stats += f"Spells: {analysis['spells']}  |  "
        stats += f"Avg CMC: {analysis['avg_cmc']:.2f}  |  "
        
        if analysis['color_identity']:
            colors = ', '.join(sorted(list(analysis['color_identity'])))
            stats += f"Colors: {colors}"
        
        if analysis['synergies']:
            stats += f"\n\nThemes: {', '.join(analysis['synergies'][:5])}"
        
        self.stats_text.config(state=tk.NORMAL)
        self.stats_text.delete(1.0, tk.END)
        self.stats_text.insert(tk.END, stats)
        self.stats_text.config(state=tk.DISABLED)
    
    def _save_deck(self):
        """Save the current deck"""
        if not self.selected_cards:
            messagebox.showwarning("Warning", "No deck to save")
            return
        
        filename = simpledialog.askstring("Save Deck", "Enter filename (without extension):")
        if filename:
            import os
            cache_dir = "cache"
            if not os.path.exists(cache_dir):
                os.makedirs(cache_dir)
            
            filepath = os.path.join(cache_dir, f"{filename}.deck")
            
            deck_data = {
                "set": self.current_set,
                "cards": self.selected_cards,
                "date": datetime.now().isoformat()
            }
            
            try:
                with open(filepath, 'w', encoding='utf-8') as f:
                    json.dump(deck_data, f, indent=2)
                messagebox.showinfo("Success", f"Deck saved to {filepath}")
            except Exception as e:
                messagebox.showerror("Error", f"Could not save deck: {e}")
    
    def _load_deck(self):
        """Load a saved deck"""
        import os
        cache_dir = "cache"
        
        if not os.path.exists(cache_dir):
            messagebox.showwarning("Warning", "No saved decks found")
            return
        
        deck_files = [f for f in os.listdir(cache_dir) if f.endswith('.deck')]
        
        if not deck_files:
            messagebox.showwarning("Warning", "No saved decks found")
            return
        
        # Create dialog
        dialog = tk.Toplevel(self.root)
        dialog.title("Load Deck")
        dialog.geometry("300x300")
        
        ttk.Label(dialog, text="Select a deck:").pack(padx=10, pady=10)
        
        listbox = tk.Listbox(dialog)
        listbox.pack(fill=tk.BOTH, expand=True, padx=10)
        
        for f in deck_files:
            listbox.insert(tk.END, f[:-5])
        
        def load_selected():
            if listbox.curselection():
                filename = deck_files[listbox.curselection()[0]]
                filepath = os.path.join(cache_dir, filename)
                
                try:
                    with open(filepath, 'r', encoding='utf-8') as f:
                        deck_data = json.load(f)
                    
                    # Find and load the set
                    set_name = deck_data.get("set")
                    matching_set = next((s for s in self.all_sets if s['name'] == set_name), None)
                    
                    if matching_set:
                        self.set_combo_var.set(f"{matching_set['name']} ({matching_set['code']})")
                        self._load_set_clicked()
                        
                        # Schedule card loading after set loads
                        def load_cards():
                            import time
                            time.sleep(1)  # Wait for set to load
                            self.selected_cards = deck_data.get("cards", [])
                            self._update_deck_display()
                            self._update_stats()
                        
                        thread = threading.Thread(target=load_cards, daemon=True)
                        thread.start()
                        
                        messagebox.showinfo("Success", "Deck loaded!")
                    else:
                        messagebox.showerror("Error", f"Could not find set {set_name}")
                    
                    dialog.destroy()
                except Exception as e:
                    messagebox.showerror("Error", f"Could not load deck: {e}")
        
        ttk.Button(dialog, text="Load", command=load_selected).pack(pady=10)


def main():
    """Main entry point"""
    root = tk.Tk()
    app = MTGDraftRaterGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()
