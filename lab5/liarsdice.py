from typing import List
import time
import random

class LiarsDiceGame:
    def __init__(self):
        self.players = {}
        self.current_bid = None
        self.history = []
        self.turn_order = []
        self.current_turn = 0
        self.round_count = 0
        
    def setup_game(self, ai_players: List, dice_per_player: int = 5):
        """Set up the Liar's Dice game"""
        player_names = [i.name for i in ai_players]
        self.turn_order = player_names
        self.total_dice = len(player_names) * dice_per_player
        
        for name, ai_player in zip(player_names, ai_players):
            self.players[name] = {
                'dice': [random.randint(1, 6) for _ in range(dice_per_player)],
                'num_dice': dice_per_player,
                'ai_player': ai_player
            }
        
        print("LIAR'S DICE!")
        print(f"Players: {', '.join(player_names)}")
        print(f"Total dice: {self.total_dice}")
        
        print("\nDICE (not visible to players):")
        for name, data in self.players.items():
            print(f"{name}: {data['dice']}")

    def display_game_state(self):
        """Display current game state"""
        print(f"\n{'='*60}")
        print(f"ROUND {self.round_count + 1} - GAME STATE")
        print('='*60)
        
        print("PLAYERS:")
        for name in self.turn_order:
            data = self.players[name]
            dice_display = f"{data['dice']} ({data['num_dice']} dice)"
            current_marker = " ← CURRENT TURN" if name == self.turn_order[self.current_turn] else ""
            print(f"   {name}: {dice_display}{current_marker}")
        
        if self.current_bid:
            print(f"\nCURRENT BID: {self.current_bid['quantity']} dice show {self.current_bid['face_value']} (by {self.current_bid['player']})")
        else:
            print("\nCURRENT BID: None (round start)")
        
        print(f"\n📊 TOTAL DICE IN PLAY: {self.total_dice}")
        
        if self.history:
            print(f"\n📜 RECENT HISTORY:")
            for action in self.history[-5:]:  # Show last 5 actions
                print(f"   • {action}")
    
    def is_valid_bid(self, quantity: int, face_value: int) -> bool:
        """Check if bid is higher than current bid"""
        if not self.current_bid:
            return quantity > 0 and 1 <= face_value <= 6
        
        current_q = self.current_bid['quantity']
        current_f = self.current_bid['face_value']
        
        return quantity > current_q or (quantity == current_q and face_value > current_f)
    
    def count_dice(self, face_value: int) -> int:
        """Count dice showing face_value (1s are wild)"""
        total = 0
        for player_data in self.players.values():
            for die in player_data['dice']:
                if die == face_value or die == 1:
                    total += 1
        return total
    
    def play_turn(self) -> bool:
        """Play one turn with enhanced display - returns False if game ends"""
        self.display_game_state()
        
        current_player = self.turn_order[self.current_turn]
        player_data = self.players[current_player]
        
        print(f"\n{current_player}'s turn")
        
        # Get AI decision with full context
        decision = player_data['ai_player'].make_decision(
            player_data['dice'],
            self.total_dice,
            self.current_bid,
            self.history,
        )
        
        if decision["action"] == "bid":
            quantity = decision["quantity"]
            face_value = decision["face_value"]
            
            if self.is_valid_bid(quantity, face_value):
                self.current_bid = {
                    'player': current_player,
                    'quantity': quantity,
                    'face_value': face_value
                }
                action_text = f"{current_player} bids {quantity} dice show {face_value}"
                print(f"✅ {action_text}")
                self.history.append(action_text)
            else:
                print(f"❌ Invalid bid from {current_player}! Auto-correcting...")
                # Force a valid bid
                if self.current_bid:
                    if self.current_bid['face_value'] < 6:
                        quantity = self.current_bid['quantity']
                        face_value = self.current_bid['face_value'] + 1
                    else:
                        quantity = self.current_bid['quantity'] + 1
                        face_value = 2
                else:
                    quantity, face_value = 1, 2
                
                self.current_bid = {
                    'player': current_player,
                    'quantity': quantity,
                    'face_value': face_value
                }
                action_text = f"{current_player} bids {quantity} dice show {face_value} (auto-corrected)"
                print(f"🔧 {action_text}")
                self.history.append(action_text)
                
        elif decision["action"] == "challenge":
            if not self.current_bid:
                print("❌ Can't challenge - no bid to challenge!")
                return True  # Continue game
            
            action_text = f"{current_player} challenges {self.current_bid['player']}'s bid"
            self.history.append(action_text)
            return self.resolve_challenge(current_player)
        
        # Next player
        self.current_turn = (self.current_turn + 1) % len(self.turn_order)
        return True
    
    def resolve_challenge(self, challenger: str) -> bool:
        """Resolve challenge with detailed analysis - returns True if game ends"""
        bid = self.current_bid
        actual_count = self.count_dice(bid['face_value'])
        
        print(f"\n{'🚨 CHALLENGE RESOLUTION 🚨':^60}")
        print(f"{challenger} challenges {bid['player']}'s bid:")
        print(f"BID: {bid['quantity']} dice show {bid['face_value']}")
        
        # Detailed count analysis
        print(f"\nCOUNTING DICE SHOWING {bid['face_value']}:")
        for name, data in self.players.items():
            player_count = sum(1 for die in data['dice'] if die == bid['face_value'] or die == 1)
            ones = data['dice'].count(1)
            targets = data['dice'].count(bid['face_value'])
            print(f"   {name}: {targets} natural {bid['face_value']}s + {ones} wilds = {player_count} total")
        
        print(f"\nFINAL COUNT: {actual_count} dice show {bid['face_value']}")
        print(f"BID CLAIMED: {bid['quantity']} dice show {bid['face_value']}")
        
        if actual_count >= bid['quantity']:
            print(f"✅ BID WAS TRUE! {challenger} loses a die!")
            loser = challenger
            winner = bid['player']
        else:
            print(f"❌ BID WAS FALSE! {bid['player']} loses a die!")
            loser = bid['player']
            winner = challenger
        
        # Remove die from loser
        self.players[loser]['num_dice'] -= 1
        if self.players[loser]['dice']:
            self.players[loser]['dice'].pop()
        
        print(f"{winner} wins the challenge!")
        print(f"{loser} now has {self.players[loser]['num_dice']} dice")
        
        result_text = f"Challenge: {challenger} vs {bid['player']} - {winner} wins"
        self.history.append(result_text)
        
        # Check elimination
        if self.players[loser]['num_dice'] == 0:
            print(f"{loser} is eliminated! 💀")
            self.turn_order.remove(loser)
            if len(self.turn_order) == 1:
                print(f"\n🎉 {self.turn_order[0]} WINS THE GAME! 🎉")
                return False
        
       # Re-roll ALL dice for new round and reset game state
        print(f"\nRolling new dice for next round...")
        for name, data in self.players.items():
            if data['num_dice'] > 0:  # Only re-roll for active players
                data['dice'] = [random.randint(1, 6) for _ in range(data['num_dice'])]
                print(f"   {name}: {data['dice']}")
        
        # Reset for next round
        self.current_bid = None
        self.current_turn = self.turn_order.index(winner)
        self.total_dice = sum(p['num_dice'] for p in self.players.values())
        self.round_count += 1
        
        print(f"\nNEW ROUND {self.round_count + 1}! {winner} starts with fresh dice")
        return True  # Continue game with new round