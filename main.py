# Libraries
import string
from time import sleep
from random import randint
 
# Files
import outcomes
import phrase_list
""" TODO:   
"""

class fortune_game():
    """ Class for the Fortune Game """
    def __init__(self) -> None:
        self.alphabet = string.ascii_lowercase # Alphabet in a string; "abc...xyz"
        self.alph_list = list(string.ascii_lowercase) # To play with computer
        self.current_player = 0
        self.playing = False # Used to determine if player 1 has played at leaset once| 
        self.newGameCalled = False # Used to determine if a new game is to be set up
        self.yes = ['y','yes']
        self.no = ['n', 'no']
        self.invalids = ['', ' ', '+', '-', '/', '*'] # Invalid entries answer if guessing the phrase
        self.match_list = [] # To collect the indexes of matching letters
        self.used_chars = [] # To collect all given guessed letters
        self.customize_name = False
        self.player1_name = ''
        self.player2_name = ''
        self.player = 0
        self.player_points = 0
        self.player_1_wins = 0
        self.player_1_points = 0
        self.player_2_wins = 0
        self.player_2_points = 0
        self.spacer = ' ' *  20
        self.hidden_phrase = ''
        self.temp = ''
        self.phrases = phrase_list.phrases
        self.outcome = outcomes.outcomes
        self.rand_num_phrase = randint(0, len(self.phrases)-1)
        self.chosen_phrase = self.phrases[self.rand_num_phrase]
        self.with_computer = False # Playing against computer (I.e: random choice of index in alphabet list)
        
    def pick_player(self, newgame: bool = False) -> int:
        """ Switch the player  """
        if newgame: # Set to 0 in order to start with player 1 in the new game
            self.current_player = 0
        # current_player is initally set to 0 when program first runs in order to start the game with player 1 instead of 2
        if self.current_player == 0:
            self.current_player = 1
        else: # Game is running
            if self.current_player == 1:
                self.current_player = 2 
            elif self.current_player == 2:
                self.current_player = 1
        self.player = self.current_player
        return self.current_player

    def AI(self) -> None:
        """ Determine whether player will play against computer """
        with_AI = input('Play against the computer? [y/n]: ')
        if with_AI in self.yes:
            self.with_computer = True

    def hide_phrase(self) ->  str:
        """ Hide the chosen phrase with dashes (-) """
        self.hidden_phrase = ''
        for char in self.chosen_phrase.lower():
            if char == ' ':
                self.hidden_phrase += ' '
            elif char == "'":
                pass
            elif char == '-':
                pass
            elif char in self.alphabet:
                self.hidden_phrase += '-'
        return self.hidden_phrase
        
    def custom_name(self) -> bool:
        """ Determine if the game will use custom names """
        ask = input('Used custom names? [y/n]: ')
        if ask in self.yes:
            self.player1_name = input("Player 1's name: ")
            self.player2_name = input("Player 2's name: ")
            return True
        else:
            return False
            
    def display_labels(self, customized: 'If the player has chosen custom names or not') -> None:
        """ Display the player, used characters, and points/wins """
        if customized:
            self.custom_player_name = self.player1_name if self.player == 1 else self.player2_name
            print('='*60+f"\n{self.custom_player_name}'s Turn" + ' '*6 + f'Used characters: {self.used_chars}')
            print(f'{self.spacer} {self.player1_name}: {self.player_1_points} | Wins: {self.player_1_wins}\n{self.spacer} {self.player2_name}: {self.player_2_points} | Wins: {self.player_2_wins}')
        else:
            print('='*60 + f"\nPlayer {self.player}'s Turn" + ' '*6 + f'Used characters: {self.used_chars}')
            print(f'{self.spacer} Player 1: {self.player_1_points} | Wins: {self.player_1_wins}\n{self.spacer} Player 2: {self.player_2_points} | Wins: {self.player_2_wins}')

    def new_game(self) -> None:
        """ Start a new game """
        self.newGameCalled = True
        self.current_player = 0
        self.pick_player(newgame=True)
        self.new_phrase(newgame=True)
        self.player_1_points = 0
        self.player_2_points = 0
        del self.match_list[:]
        del self.used_chars[:]

    def new_phrase(self, newgame: bool = False) -> str:
        """ Set new phrase after a game ends """
        if newgame:
            self.temp = ''
        self.phrase_randNum = randint(0, len(self.phrases)-1)
        self.chosen_phrase = self.phrases[self.phrase_randNum]
        return self.hide_phrase()

    def spin(self) -> str or int:
        """ Returns the value chosen by the randint from outcomes list"""
        if self.with_computer:
            self.spin_randNum = randint(0, len(self.outcome)-1)
            return self.outcome[self.spin_randNum]
        else:
            user = input('Press [ENTER] to spin: ')
            if user == '' or 'spin':
                self.spin_randNum = randint(0, len(self.outcome)-1)
                return self.outcome[self.spin_randNum]

    def guess_whole_phrase(self, decision: str) -> None:
        """ Allow the user to guess the whole phrase """
        self.playing = True
        if decision in self.yes:
            # print the dashed sentence with a spacer to align the user's guess
            print('\n' + (' ' * 8) + self.temp)
            user_guess = input('Phrase: ')

            if user_guess.lower() == self.chosen_phrase.lower(): # Guessed correctly
                if self.customize_name:
                    print(f'Correct!\n{self.custom_player_name} wins!\n')
                else:
                    print(f'Correct!\nPlayer {self.player} wins!\n')
                # Figure out the player and add one (1) to the right variable then, execute new_game()
                if self.player == 1:
                    self.player_1_wins += 1
                    self.new_game()

                else:
                    self.player_2_wins += 1
                    self.new_game()
            else:
                print('Incorrect')
                del self.match_list[:]
                self.pick_player()
            
        elif decision in self.no: # Same game; next player. Empty match list and pick the other player
                del self.match_list[:]
                self.pick_player()
    
    def char_swap(self, input_char: 'Character to insert', str_to_mod: 'String to iterate over', output_str: str, indexes: 'Indexes to place char at' = []) -> str:
        """ Returns a string with the substitutions of the given character at the given indeces """
        output_str = '' # Set to empty string to function properly after game has been going on.
        for index, dash in enumerate(str_to_mod):
            if index in indexes:
                output_str += input_char
            else:
                output_str += dash
        self.temp = output_str
        self.hidden_phrase = self.temp
        output_str = ''
        return self.temp

    def update_points(self, player, multiplier) -> None:
        """ Updates the player's points [param: player] by the given number [param: multiplier] """
        if player == 1:
            self.player_1_points += multiplier * len(self.match_list)
        elif player == 2:
            self.player_2_points += multiplier * len(self.match_list)
    
    def cleanup(self) -> None:
        """ Empty lists and switch player """
        self.used_chars.remove(self.player_char)
        del self.match_list[:]
        self.pick_player()

    def check_N_run(self):
        """ Check given letter and have it go through 'tests' to make sure its a valid input """
        if  0 < len(self.player_char) <= 1 and (self.player_char in self.alphabet): # Check that user guess is 1 letter only and its a letter in the alphabet
            if self.player_char not in self.used_chars: # if character has not been used
                self.used_chars.append(self.player_char) # Add it to the list > self.match_list
                if self.player_char in self.chosen_phrase.lower(): # Check the length (len) of the list is 0 ->  User guessed no letter
                    for player_letter in self.player_char: # Check letter that user picked and compare it to the letters in the phrase
                        for index, char in enumerate(self.chosen_phrase.lower()): # Check for match(s) and save matching indexes to list
                            self.match_list.append(index) if char == player_letter else None

                    # determine outcome based on returned spin
                    self.logistics(self.spin())
                else:
                    print(f"\n[-] '{self.player_char}' is not in the phrase\n")
                    self.pick_player()
            else:
                print(f"[-] '{self.player_char}' already used. Use another")
        else:
            if self.player_char not in self.alphabet:
                print(f"[-] '{self.player_char}' not a valid character")
            else:
                print('\n[-] Input can only be one (1) character\n')

    def logistics(self, spin: 'returned value from self.spin()') -> None:
        """ Determine what to do for each case of the outcome """
        if spin == self.outcome[8] or spin == self.outcome[9]: # Bankrupt or Lost turn
            if spin == self.outcome[8]: # Bankrupt
                if self.player == 1:
                    self.player_1_points = 0
                    print('Bankrupt')
                else:
                    self.player_2_points = 0
            elif spin == self.outcome[9]: # Lost turn
                print('Lost your turn')
                
            self.cleanup()

        else:
            # Calculate player's winnings
            self.update_points(self.player, spin)
            word = self.player_1_points if self.player == 1 else self.player_2_points

            # Display the right name if custom names are being used
            if self.customize_name:
                print(f'\n\n[+] {self.custom_player_name} spun: {spin}\n[+] {len(self.match_list)} matches >> {spin} * {len(self.match_list)}\n[+] Your points are {word}\n')
            else:
                print(f'\n\n[+] Player {self.player} spun: {spin}\n[+] {len(self.match_list)} matches >> {spin} * {len(self.match_list)}\n[+] Your points are {word}\n')
            
            # Display new sentence with guessed letters in place
            print(f'\n{self.char_swap(self.player_char, self.hidden_phrase, self.temp, self.match_list)}\n')

            # Check if dashed phrase == plain phrase
            if self.compare():
                self.new_game()
            else: # Allow user to guess the phrase
                
                if self.with_computer: # If the user playing against a computer
                    if self.player == 2:
                        self.guess_whole_phrase(decision='n')
                    elif self.player == 1:
                        guess = input('Want to guess the phrase? [y/n]: ')
                        if guess in self.invalids:
                            guess = 'n'
                        else:
                            self.guess_whole_phrase(guess.lower())
                else:
                    guess = input('Want to guess the phrase? [y/n]: ')
                    if guess in self.invalids:
                        guess = 'n'
                    else:
                        self.guess_whole_phrase(guess.lower())

    def compare(self) -> bool:
        """ Check if the dashed phrase is the same are the plain phrase """
        if self.hidden_phrase.lower() == self.chosen_phrase.lower(): # Dashed sentence == phrase
            if self.customize_name:
                self.custom_player_name = self.player1_name if self.player == 1 else self.player2_name
                print(f'{self.custom_player_name} Guessed the last correct letter\n{self.custom_player_name} wins')
            else:
                print(f'Player {self.player} guessed the last correct letter\nPlayer {self.player} wins\n')

            if self.player == 1:
                self.player_1_wins += 1
                return True
            elif self.player == 2:
                self.player_2_wins += 1
                return True
        else:
            return False

    def main(self) -> None:
        """ Main function; runs the game"""

        print("\nType 'quit' to terminate program\n")

        self.pick_player() # To initially set player at beginning of first game
        self.AI() # Ask if playing against computer
        self.hidden_phrase = self.hide_phrase()
        self.customize_name = self.custom_name() # self.custom_name() returns a bool; saved to variable
        
        # The following is essentially a "controlled infite loop". While the dahsed phrase doesn't equal the (plain) chosen word: the following.
        # What makes it a controlled infinte loop if that if the dashed and plain one equal each other, the function {self.compare()} will be executed;
        # Changing the dashed and plain phrase, hence the "controlled infite loop"
        while self.hidden_phrase.lower() != self.chosen_phrase.lower():

            self.display_labels(self.customize_name)
            
            if self.playing:
                if self.newGameCalled:
                    print(f'\n{self.hidden_phrase}\n')
                else:
                    if self.temp != '':
                        self.temp = ''
                    print(f'\n{self.hidden_phrase}\n')
            else: # Display dashed sentence
                print(f'\n{self.hidden_phrase}\n')
            
            if self.with_computer: # Playing against computer; only player one guesses letters, player 2 (computer)'s choice will be randomized [a-z]
                if self.player == 2:
                    self.comp_rand_num = randint(0, len(self.alph_list)-1) # Randomize the computers choice of letters
                    self.player_char = self.alph_list[self.comp_rand_num]
                    print(f'\nComputer chose: {self.player_char}')
                    sleep(3)
                else: # player = 1
                    self.player_char = input(f'Pick a letter: ').lower()
            else: # Player vs Player; let each player guess a letter
                    self.player_char = input(f'Pick a letter: ').lower()
 
            if self.player_char == 'quit': # quit the program by raising [SystemExit] exception
                raise SystemExit
            else:
                self.check_N_run()

if __name__ == '__main__':
    fortune_game().main()
    
    