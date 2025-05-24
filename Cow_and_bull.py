import random
import time
from datetime import datetime
import json
import os

class BullsAndCowsGame:
    def __init__(self):
        self.stats_file = "bulls_cows_stats.json"
        self.load_stats()
        self.difficulties = {
            'easy': {'digits': 3, 'max_tries': 12},
            'medium': {'digits': 4, 'max_tries': 10},
            'hard': {'digits': 5, 'max_tries': 8},
            'expert': {'digits': 6, 'max_tries': 6}
        }
        
    def load_stats(self):
        try:
            if os.path.exists(self.stats_file):
                with open(self.stats_file, 'r') as f:
                    self.stats = json.load(f)
            else:
                self.stats = {
                    'games_played': 0,
                    'games_won': 0,
                    'total_attempts': 0,
                    'best_score': None,
                    'average_attempts': 0,
                    'difficulty_stats': {}
                }
        except:
            self.stats = {
                'games_played': 0,
                'games_won': 0,
                'total_attempts': 0,
                'best_score': None,
                'average_attempts': 0,
                'difficulty_stats': {}
            }
    
    def save_stats(self):
        try:
            with open(self.stats_file, 'w') as f:
                json.dump(self.stats, f, indent=2)
        except:
            pass
    
    def get_digits(self, num):
        return [int(i) for i in str(num)]
    
    def no_duplicates(self, num):
        num_li = self.get_digits(num)
        return len(num_li) == len(set(num_li))
    
    def generate_num(self, digits):
        while True:
            min_num = 10**(digits-1)
            max_num = 10**digits - 1
            num = random.randint(min_num, max_num)
            if self.no_duplicates(num):
                return num
    
    def num_of_bulls_cows(self, secret, guess):
        secret_digits = self.get_digits(secret)
        guess_digits = self.get_digits(guess)
        
        bulls = 0
        cows = 0
        
        # Count bulls (exact position matches)
        for i in range(len(secret_digits)):
            if secret_digits[i] == guess_digits[i]:
                bulls += 1
        
        # Count cows (digit exists but wrong position)
        for digit in guess_digits:
            if digit in secret_digits:
                cows += min(secret_digits.count(digit), guess_digits.count(digit))
        
        # Remove bulls from cows count
        cows -= bulls
        
        return bulls, cows
    
    def validate_guess(self, guess, digits):
        try:
            guess = int(guess)
        except ValueError:
            return False, "Please enter a valid number."
        
        if guess < 10**(digits-1) or guess > 10**digits - 1:
            return False, f"Please enter a {digits}-digit number."
        
        if not self.no_duplicates(guess):
            return False, "Number should not have repeated digits."
        
        return True, guess
    
    def display_header(self):
        print("\n" + "="*60)
        print("ENHANCED BULLS AND COWS GAME")
        print("="*60)
        print("Rules:")
        print("• Bull: Correct digit in correct position")
        print("• Cow: Correct digit in wrong position")
        print("• Numbers have no repeated digits")
        print("="*60)
    
    def display_stats(self):
        print("\nGAME STATISTICS")
        print("-" * 30)
        print(f"Games Played: {self.stats['games_played']}")
        print(f"Games Won: {self.stats['games_won']}")
        if self.stats['games_played'] > 0:
            win_rate = (self.stats['games_won'] / self.stats['games_played']) * 100
            print(f"Win Rate: {win_rate:.1f}%")
        
        if self.stats['best_score']:
            print(f"Best Score: {self.stats['best_score']['attempts']} attempts "
                  f"({self.stats['best_score']['difficulty']} difficulty)")
        
        if self.stats['games_won'] > 0:
            avg_attempts = self.stats['total_attempts'] / self.stats['games_won']
            print(f"Average Attempts (Won Games): {avg_attempts:.1f}")
        
        print("-" * 30)
    
    def choose_difficulty(self):
        print("\nChoose Difficulty Level:")
        print("1. Easy (3 digits, 12 tries)")
        print("2. Medium (4 digits, 10 tries)")
        print("3. Hard (5 digits, 8 tries)")
        print("4. Expert (6 digits, 6 tries)")
        
        while True:
            try:
                choice = input("\nEnter your choice (1-4): ").strip()
                difficulty_map = {'1': 'easy', '2': 'medium', '3': 'hard', '4': 'expert'}
                if choice in difficulty_map:
                    return difficulty_map[choice]
                else:
                    print("Invalid choice. Please enter 1, 2, 3, or 4.")
            except KeyboardInterrupt:
                print("\nGame interrupted. Goodbye!")
                exit()
    
    def display_game_progress(self, attempts, max_tries, guess_history):
        print(f"\nAttempts: {attempts}/{max_tries}")
        if guess_history:
            print("\nPrevious Guesses:")
            for i, (guess, bulls, cows) in enumerate(guess_history[-5:], 1):
                print(f"  {len(guess_history)-5+i}. {guess} -> {bulls} bulls, {cows} cows")
    
    def give_hint(self, secret, attempts, max_tries):
        if attempts > max_tries // 2:
            secret_digits = self.get_digits(secret)
            hint_digit = random.choice(secret_digits)
            print(f"Hint: The number contains the digit {hint_digit}")
    
    def play_game(self):
        difficulty = self.choose_difficulty()
        digits = self.difficulties[difficulty]['digits']
        max_tries = self.difficulties[difficulty]['max_tries']
        
        secret_num = self.generate_num(digits)
        attempts = 0
        guess_history = []
        start_time = time.time()
        
        print(f"\nStarting {difficulty.upper()} game!")
        print(f"Guess the {digits}-digit number with no repeated digits.")
        print(f"You have {max_tries} attempts. Good luck!")
        
        while attempts < max_tries:
            self.display_game_progress(attempts, max_tries, guess_history)
            
            if attempts > 0 and attempts % (max_tries // 3) == 0:
                self.give_hint(secret_num, attempts, max_tries)
            
            try:
                guess_input = input(f"\nEnter your {digits}-digit guess: ").strip()
                
                if guess_input.lower() == 'quit':
                    print("Game abandoned. Thanks for playing!")
                    return
                elif guess_input.lower() == 'hint':
                    self.give_hint(secret_num, attempts, max_tries)
                    continue
                elif guess_input.lower() == 'stats':
                    self.display_stats()
                    continue
                
                is_valid, result = self.validate_guess(guess_input, digits)
                
                if not is_valid:
                    print(f"Error: {result}")
                    continue
                
                guess = result
                attempts += 1
                bulls, cows = self.num_of_bulls_cows(secret_num, guess)
                guess_history.append((guess, bulls, cows))
                
                if bulls == digits:
                    end_time = time.time()
                    game_duration = round(end_time - start_time, 2)
                    
                    print("\nCONGRATULATIONS!")
                    print(f"You guessed {secret_num} correctly!")
                    print(f"Attempts: {attempts}/{max_tries}")
                    print(f"Time: {game_duration} seconds")
                    print(f"Difficulty: {difficulty.upper()}")
                    
                    self.update_stats(True, attempts, difficulty)
                    
                    if (not self.stats['best_score'] or 
                        attempts < self.stats['best_score']['attempts']):
                        self.stats['best_score'] = {
                            'attempts': attempts,
                            'difficulty': difficulty,
                            'date': datetime.now().strftime("%Y-%m-%d")
                        }
                        print("NEW BEST SCORE!")
                    
                    break
                else:
                    print(f"Result: {bulls} bulls, {cows} cows")
                    
                    if bulls > 0:
                        print(f"Great! You have {bulls} digit(s) in the right position!")
                    if cows > 0:
                        print(f"You have {cows} correct digit(s) in wrong position(s)!")
                    
                    remaining = max_tries - attempts
                    if remaining <= 2:
                        print(f"Warning: Only {remaining} attempt(s) left!")
            
            except KeyboardInterrupt:
                print("\nGame interrupted. Goodbye!")
                return
        
        else:
            print(f"\nGame Over! You've used all {max_tries} attempts.")
            print(f"The secret number was: {secret_num}")
            self.update_stats(False, attempts, difficulty)
        
        self.save_stats()
    
    def update_stats(self, won, attempts, difficulty):
        self.stats['games_played'] += 1
        if won:
            self.stats['games_won'] += 1
            self.stats['total_attempts'] += attempts
        
        if difficulty not in self.stats['difficulty_stats']:
            self.stats['difficulty_stats'][difficulty] = {
                'played': 0, 'won': 0, 'total_attempts': 0
            }
        
        self.stats['difficulty_stats'][difficulty]['played'] += 1
        if won:
            self.stats['difficulty_stats'][difficulty]['won'] += 1
            self.stats['difficulty_stats'][difficulty]['total_attempts'] += attempts
    
    def main_menu(self):
        while True:
            self.display_header()
            print("\nMAIN MENU")
            print("1. Play Game")
            print("2. View Statistics")
            print("3. How to Play")
            print("4. Exit")
            
            try:
                choice = input("\nEnter your choice (1-4): ").strip()
                
                if choice == '1':
                    self.play_game()
                    input("\nPress Enter to continue...")
                elif choice == '2':
                    self.display_stats()
                    input("\nPress Enter to continue...")
                elif choice == '3':
                    self.show_instructions()
                    input("\nPress Enter to continue...")
                elif choice == '4':
                    print("\nThanks for playing Bulls and Cows! Goodbye!")
                    break
                else:
                    print("Invalid choice. Please enter 1, 2, 3, or 4.")
            
            except KeyboardInterrupt:
                print("\nGoodbye!")
                break
    
    def show_instructions(self):
        print("\nHOW TO PLAY BULLS AND COWS")
        print("-" * 40)
        print("OBJECTIVE:")
        print("  Guess the secret number with no repeated digits")
        print()
        print("DIFFICULTY LEVELS:")
        for level, config in self.difficulties.items():
            print(f"  {level.title()}: {config['digits']} digits, {config['max_tries']} attempts")
        print()
        print("SCORING:")
        print("  Bull: Correct digit in correct position")
        print("  Cow: Correct digit in wrong position")
        print()
        print("SPECIAL COMMANDS (during game):")
        print("  'hint' - Get a helpful hint")
        print("  'stats' - View current statistics")
        print("  'quit' - Exit current game")
        print()
        print("TIPS:")
        print("  • Use process of elimination")
        print("  • Pay attention to bulls vs cows")
        print("  • Try different digit combinations")
        print("  • Use hints when stuck")

def main():
    try:
        game = BullsAndCowsGame()
        game.main_menu()
    except Exception as e:
        print(f"An error occurred: {e}")
        print("Please try running the game again.")

if __name__ == "__main__":
    main()