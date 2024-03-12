import tensorflow as tf
import keras
import numpy as np
import operator

# Load model
model = keras.saving.load_model("./rps_model.keras")

# Initial prediction input
one_hot_input = tf.constant(np.array(
    [[0, 0, 0]]).astype('int32'))
winner_input = tf.constant(np.array([0]))

# One hot encoding array
encoding_arr = ['P', 'R', 'S']

# Playing status
playing = True

# Playing loop
while playing == True:
    # Predict the probability of P, R, S for the next round based on the last round
    pred = model.predict({'one_hot_input': one_hot_input,
                         'winner_input': winner_input})
    print(pred)

    # Select the highest probability of the predicted player choice
    max_probability = 0
    for probability in pred[0]:
        if operator.gt(probability, max_probability):
            max_probability = probability
    print('The highest probability in the given array is:', max_probability)

    # Get the encoding index and encode the predicted player choice
    probability_index = np.where(pred[0] == max_probability)
    enc_probability = encoding_arr[int(probability_index[0])]

    # Select the choice which will win against the predicted player choice
    if enc_probability == 'R':
        computer_choice = 'P'
    elif enc_probability == 'S':
        computer_choice = 'R'
    elif enc_probability == 'P':
        computer_choice = 'S'

    # Let the user make a choice
    player_choice = input("Enter R, P or S: ").upper()

    # Determine the winner
    print("The model chooses: " + computer_choice)
    print("The player chooses: " + player_choice)
    if player_choice == computer_choice:
        print('Tie')
        winner_input = tf.constant(np.array([0]))
        if player_choice == 'R':
            one_hot_input = tf.constant(
                np.array([[0, 1, 0]]).astype('int32'))  # ['P', 'R', 'S']
        elif player_choice == 'S':
            one_hot_input = tf.constant(
                np.array([[0, 0, 1]]).astype('int32'))  # ['P', 'R', 'S']
        elif player_choice == 'P':
            one_hot_input = tf.constant(
                np.array([[1, 0, 0]]).astype('int32'))  # ['P', 'R', 'S']
    elif player_choice == 'R':
        one_hot_input = tf.constant(
            np.array([[0, 1, 0]]).astype('int32'))  # ['P', 'R', 'S']
        if computer_choice == 'P':
            print('Player lose')
            winner_input = tf.constant(np.array([-1]))
        if computer_choice == 'S':
            print('Player win')
            winner_input = tf.constant(np.array([1]))
    elif player_choice == 'S':
        one_hot_input = tf.constant(
            np.array([[0, 0, 1]]).astype('int32'))  # ['P', 'R', 'S']
        if computer_choice == 'R':
            print('Player lose')
            winner_input = tf.constant(np.array([-1]))
        if computer_choice == 'P':
            print('Player win')
            winner_input = tf.constant(np.array([1]))
    elif player_choice == 'P':
        one_hot_input = tf.constant(
            np.array([[1, 0, 0]]).astype('int32'))  # ['P', 'R', 'S']
        if computer_choice == 'S':
            print('Player lose')
            winner_input = tf.constant(np.array([-1]))
        if computer_choice == 'R':
            print('Player win')
            winner_input = tf.constant(np.array([1]))

    # Let user input a choice
    next_round = input("Do you want to play another round? (Y/n): ").lower()
    if (next_round == 'n'):
        playing = False
