import random
import time
import json
import os

class NumberGuessingGame:
    def __init__(self):
        self.DIFFICULTY_LEVELS = {
            'easy': 10,
            'medium': 5,
            'hard': 3
        }
    
    def select_difficulty(self):
        """Allow user to select difficulty level."""
        print("\nSelect Difficulty Level:")
        for i, (level, chances) in enumerate(self.DIFFICULTY_LEVELS.items(), 1):
            print(f"{i}. {level.capitalize()} ({chances} chances)")
        
        while True:
            try:
                choice = int(input("Enter your choice (1-3): "))
                if 1 <= choice <= 3:
                    difficulty = list(self.DIFFICULTY_LEVELS.keys())[choice - 1]
                    return difficulty
                else:
                    print("Invalid choice. Please enter 1, 2, or 3.")
            except ValueError:
                print("Please enter a valid number.")
    
    def play_round(self, difficulty):
        """Play a single round of the game."""
        target_number = random.randint(1, 100)
        max_attempts = self.DIFFICULTY_LEVELS[difficulty]
        attempts = 0
        
        print(f"\nGreat! You have selected the {difficulty.capitalize()} difficulty level.")
        print(f"You have {max_attempts} chances to guess the correct number.")
        
        start_time = time.time()
        
        while attempts < max_attempts:
            try:
                remaining_attempts = max_attempts - attempts
                print(f"\nRemaining attempts: {remaining_attempts}")
                
                guess = int(input("Enter your guess (1-100): "))
                
                if guess < 1 or guess > 100:
                    print("Please enter a number between 1 and 100.")
                    continue
                
                attempts += 1
                
                if guess == target_number:
                    end_time = time.time()
                    time_taken = round(end_time - start_time, 2)
                    print(f"\n🎉 Congratulations! You guessed the correct number {target_number} in {attempts} attempts!")
                    print(f"Time taken: {time_taken} seconds")
                    return attempts, time_taken
                
                if guess < target_number:
                    print("Incorrect! The number is HIGHER than your guess.")
                else:
                    print("Incorrect! The number is LOWER than your guess.")
            
            except ValueError:
                print("Please enter a valid number.")
        
        print(f"\n😔 Game Over! The number was {target_number}.")
        return attempts, None

class HighScoreManager:
    def __init__(self, filename='high_scores.json'):
        self.filename = filename
        self.high_scores = self.load_high_scores()
    
    def load_high_scores(self):
        """Load high scores from JSON file."""
        if not os.path.exists(self.filename):
            return {
                'easy': {'attempts': float('inf'), 'time': float('inf')},
                'medium': {'attempts': float('inf'), 'time': float('inf')},
                'hard': {'attempts': float('inf'), 'time': float('inf')}
            }
        
        with open(self.filename, 'r') as f:
            return json.load(f)
    
    def update_high_score(self, difficulty, attempts, time_taken):
        """Update high score if current performance is better."""
        current_high_score = self.high_scores[difficulty]
        
        if attempts < current_high_score['attempts'] or \
           (attempts == current_high_score['attempts'] and time_taken < current_high_score['time']):
            current_high_score['attempts'] = attempts
            current_high_score['time'] = time_taken
            
            with open(self.filename, 'w') as f:
                json.dump(self.high_scores, f, indent=4)
            
            print(f"\n🏆 New high score for {difficulty} difficulty!")
            return True
        return False
    
    def display_high_scores(self):
        """Display current high scores."""
        print("\n--- High Scores ---")
        for difficulty, score in self.high_scores.items():
            if score['attempts'] != float('inf'):
                print(f"{difficulty.capitalize()} Difficulty: "
                      f"{score['attempts']} attempts in {score['time']:.2f} seconds")
            else:
                print(f"{difficulty.capitalize()} Difficulty: No high score yet")

def main():
    game = NumberGuessingGame()
    high_score_manager = HighScoreManager()
    
    while True:
        print("\n" + "=" * 40)
        print("🎲 Welcome to the Number Guessing Game! 🎲")
        print("=" * 40)
        
        print("\nMenu:")
        print("1. Start New Game")
        print("2. View High Scores")
        print("3. Quit")
        
        try:
            choice = input("Enter your choice (1-3): ")
            
            if choice == '1':
                difficulty = game.select_difficulty()
                attempts, time_taken = game.play_round(difficulty)
                high_score_manager.update_high_score(difficulty, attempts, time_taken or float('inf'))
                
                play_again = input("\nDo you want to play again? (yes/no): ").lower()
                if play_again != 'yes':
                    break
            
            elif choice == '2':
                high_score_manager.display_high_scores()
                input("\nPress Enter to continue...")
            
            elif choice == '3':
                print("Thanks for playing! Goodbye!")
                break
            
            else:
                print("Invalid choice. Please try again.")
        
        except Exception as e:
            print(f"An error occurred: {e}")
    
    # Add a pause to keep the window open
    input("\nPress Enter to exit...")

if __name__ == "__main__":
    main()