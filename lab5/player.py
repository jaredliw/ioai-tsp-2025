import time
import re
import random
from typing import Dict, List, Optional
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate


class AIPlayer:
    def __init__(self, name: str, llm, prompt_prefix: str = ""):
        self.name = name
        self.llm = llm

        # The example shows how to store variable names in the prompt
        # Refer to self.system_chain.invoke()'s parameters for variables
        # TODO: Modify this!
        self.system_prompt = ChatPromptTemplate.from_template(prompt_prefix + """
            You are {player_name} playing Liar's Dice. Your goal is to win the game with the best strategy played.

            GAME RULES:
            1. Each player rolls hidden dice with faces from 1 to 6.
            2. The game is played in turns.
            3. On each turn, a player may either:
               - Make a higher bid (as per the bid hierarchy).
               - Make a challenge, that is, call the previous player's bluff.
            4. Bid hierarchy increases first by quantity, then by face value. Example:
               - 2 fives < 2 sixes < 3 ones < 3 twos < ... < 4 sixes.
            5. A new bid must be strictly higher than the previous bid.
            6. When "CHALLENGE" is called, all dice are rerevealed, and the total number of the face value in the last bid is counted.
               - If the bid is valid (at least that many dice), the caller loses one die.
               - If the bid is false, the bidder loses one die.
            7. All dice are rerolled after each "CHALLENGE".
            
            In each round, YOUR INPUT will include:
            - Your hidden dice
            - Current bid or challenge (or None if you're starting)
            - Game history
            - Total dice counts
            After receiving the input, think on the game and decide what is the next move. Output your reasoning and make your decision.

            DO NOT make random bids. Use reasoning based on your own dice and the total dice count.
            DO NOT assume knowledge of other players' dice. You may deduce over other player's dice, but they are merely your guesses.
            DO follow the output format exactly.
            NEVER break the rules.
            Stay focused and dedicated to your goals. Your consistent efforts will lead to outstanding achievements.
            Take pride in your work and give it your best.
            
            The game will start now. Please acknowledge this message with "OK".
        """)  # Hmmmm, does emotion prompting work?

        # TODO: Modify this!
        # Ensure that the output is either just "CHALLENGE"
        # or "BID <num of dice> <dice face value>"
        self.decision_prompt = ChatPromptTemplate.from_template(prompt_prefix + """
            There are total {total_dice} dice in the game now. Your private dice is {my_dice}.

            The current bid is: {current_bid}.

            Full game history:
            {game_history}

            Think through the game. Give your thoughts in detailed and end your output with the decision format specified above.
            
            Output your decision in a separate line. Your output must be one of the following:
            - To make a bid: "BID <num of dice> <dice face value>"
            - To challenge: "CHALLENGE"
            You can't call liar when there is not current bid.
            The final line should not contain leading or trailing spaces, or other characters than the format specified.
            The final line should start with BID or CHALLENGE without any markdown formatting.

            These are BAD decision examples:
            - Decision: BID 3 4
            - **CHALLENGE**
            - BID 2 dice show 6
            - bid two six
            - BID CHALLENGE
            - CHALLENGE 6 2
            - I choose to challenge.
            - **BID 1 5**
            - BID 4 6.
            Giving such outputs will disqualify you immediately.

            These are GOOD decision examples:
            - BID 3 4
            - CHALLENGE
            - BID 4 6
            - BID 2 1
        """)

        self.system_chain = self.system_prompt | self.llm | StrOutputParser()
        self.decision_chain = self.decision_prompt | self.llm | StrOutputParser()

        self._init_llm()

    def make_decision(
        self,
        my_dice: List[int],
        total_dice: int,
        current_bid: Optional[Dict],
        game_history: List[str],
    ) -> Dict:
        """
        Given information about the game, get LLMs to decide what to do next!
        """
        current_bid_str = (
            "None (you start)"
            if not current_bid
            else f"{current_bid['quantity']} dice show {current_bid['face_value']}"
        )
        history_str = (
            "\n".join(game_history[-10:]) if game_history else "Game just started"
        )

        try:
            # TODO: Modify this!
            output = self.decision_chain.invoke({
                "total_dice": total_dice,
                "my_dice": my_dice,
                "current_bid": current_bid_str,
                "game_history": history_str
            })
            print(f"[{self.name}] Player's thoughts: {output}")
    
            decision = self._parse_decision(output)
            return decision
        except Exception as e:
            print(f"[{self.name}] ❌ An error occured: {e}")
            return self._fallback_decision(current_bid)

    def _init_llm(self):
        """
        Feed system prompt to LLM.
        """
        output = self.system_chain.invoke({"player_name": self.name})
        print(f"[{self.name}] LLM initialized with system prompt. Response: {output}")

    def _parse_decision(self, response: str) -> Dict:
        """
        Parse the LLM's decision response.
                
        Valid return output examples:

        {"action": "challenge"}
        {"action": "bid", "quantity": 3, "face_value": 4}
        {"action": "bid", "quantity": 4, "face_value": 2}
        """
        # TODO: Modify this!
        decision = list(re.finditer(r"\bBID\s+(\d+)\s+(\d+)\b|\bCHALLENGE\b", response))
        if not decision:  # No matches
            raise RuntimeError("Fail to parse decision")
        decision = decision[-1]  # Take the last one if there are multiple matches
        
        if decision.group(0) == "CHALLENGE":
            return {"action": "challenge"}
        else:
            quantity, face_value = int(decision.group(1)), int(decision.group(2))
            return {"action": "bid", "quantity": quantity, "face_value": face_value}

    def _fallback_decision(self, current_bid: Optional[Dict]) -> Dict:
        """
        Intelligent fallback decision based on game state.
        This is implemented for you in advance.
        """
        if not current_bid:
            return {
                "action": "bid",
                "quantity": random.randint(1, 2),
                "face_value": random.randint(2, 6),
            }

        # More likely to challenge high bids
        bid_aggression = current_bid["quantity"] / 10.0  # Rough aggression metric
        challenge_probability = min(0.6, bid_aggression)

        if random.random() < challenge_probability:
            return {"action": "challenge"}
        else:
            # Make a reasonable increase
            if current_bid["face_value"] < 6:
                return {
                    "action": "bid",
                    "quantity": current_bid["quantity"],
                    "face_value": current_bid["face_value"] + 1,
                }
            else:
                return {
                    "action": "bid",
                    "quantity": current_bid["quantity"] + 1,
                    "face_value": 2,
                }