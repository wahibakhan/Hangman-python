import random
from words import words
from Visual import lives_visual_dict
import string
import streamlit as st

def get_valid_word(words):
    word = random.choice(words)  # randomly chooses something from the list
    while '-' in word or ' ' in word:
        word = random.choice(words)
    return word.upper()

def initialize_game():
    # Initialize the game state
    st.session_state.word = get_valid_word(words)
    st.session_state.word_letters = set(st.session_state.word)
    st.session_state.used_letters = set()
    st.session_state.lives = 7
    st.session_state.game_over = False
    st.session_state.last_guess = None  # Track the last guessed letter
    st.session_state.feedback = None  # Track feedback for the last guess

def hangman():
    # Initialize game state if not already done
    if 'word' not in st.session_state:
        initialize_game()

    word = st.session_state.word
    word_letters = st.session_state.word_letters
    used_letters = st.session_state.used_letters
    lives = st.session_state.lives
    game_over = st.session_state.game_over
    last_guess = st.session_state.last_guess
    feedback = st.session_state.feedback

    # Display game status
    st.write(f'You have {lives} lives left and you have used these letters: ', ' '.join(used_letters))
    
    # Display the hangman visual
    st.code(lives_visual_dict[lives], language='text')  # Use st.code to preserve formatting
    
    # Display current word with guessed letters
    word_list = [letter if letter in used_letters else '-' for letter in word]
    st.write('Current word: ', ' '.join(word_list))

    # Display feedback for the last guess
    if feedback:
        st.write(feedback)

    # Check if the game is over
    if lives == 0 or len(word_letters) == 0:
        st.session_state.game_over = True
        if lives == 0:
            st.code(lives_visual_dict[lives], language='text')  # Display final hangman visual
            st.write(f'You died, sorry. The word was {word}.')
        else:
            st.write(f'YAY! You guessed the word {word}!!')
        
        # Add a button to restart the game
        if st.button('Play Again'):
            initialize_game()
        return

    # User input for guessing a letter
    user_letter = st.text_input('Guess a letter: ', max_chars=1, key='input').upper()

    if user_letter:
        if user_letter in set(string.ascii_uppercase) - used_letters:
            used_letters.add(user_letter)
            st.session_state.last_guess = user_letter  # Store the last guessed letter
            if user_letter in word_letters:
                word_letters.remove(user_letter)
                st.session_state.feedback = f'\nYour letter, {user_letter}, is in the word!'  # Set feedback
            else:
                lives -= 1  # takes away a life if wrong
                st.session_state.lives = lives
                st.session_state.feedback = f'\nYour letter, {user_letter}, is not in the word.'  # Set feedback
        elif user_letter in used_letters:
            st.session_state.feedback = '\nYou have already used that letter. Guess another letter.'  # Set feedback
        else:
            st.session_state.feedback = '\nThat is not a valid letter.'  # Set feedback

        # Update session state
        st.session_state.used_letters = used_letters
        st.session_state.word_letters = word_letters

if __name__ == '__main__':
    st.title('Hangman Game')
    hangman()