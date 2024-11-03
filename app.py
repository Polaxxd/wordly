from flask import Flask
from flask import render_template, request, redirect, url_for
import re

app = Flask(__name__)

word_length = 0
possible_words = []

letter_frequency = [    ['a', 8.91],    ['ą', 0.99],    ['b', 1.47],    ['c', 3.96],    ['ć', 0.40],    ['d', 3.25],    ['e', 7.66],    ['ę', 1.11],    ['f', 0.30],    ['g', 1.42],    ['h', 1.08],    ['i', 8.21],    ['j', 2.28],    ['k', 3.51],    ['l', 2.10],    ['ł', 1.82],    ['m', 2.80],    ['n', 5.52],    ['ń', 0.20],    ['o', 7.75],    ['ó', 0.85],    ['p', 3.13],    ['q', 0.14],    ['r', 4.69],    ['s', 4.32],    ['ś', 0.66],    ['t', 3.98],    ['u', 2.50],    ['v', 0.04],    ['w', 4.65],    ['x', 0.02],    ['y', 3.76],    ['z', 5.64],    ['ź', 0.06],    ['ż', 0.83]]

def create_set_of_popular_letters_words(set_of_X_letter_words):
    popular_letters_words = []
    for elem in set_of_X_letter_words:
        score = 0
        letters_in_word = []
        for letter in elem:
            for em in letter_frequency:
                if (letter == em[0] and letter not in letters_in_word):
                    score += em[1]
                    letters_in_word.append(letter)
        popular_letters_words.append([elem, score])
    sorted_popular_letters_words_frequency = [ x[0] for x in sorted(popular_letters_words, key=lambda k: k[1], reverse=True)]

    # print(sorted_popular_letters_words_frequency[:20])
    return sorted_popular_letters_words_frequency


@app.route('/')
def home():
    return render_template('home.html')

@app.route('/game_start/<int:number>')
def game_start(number):
    word_length = number
    file_name = "len" + str(word_length) + ".txt"
    with open(file_name) as file:
        for line in file:
            possible_words.append(line.strip())

    word_list = list(create_set_of_popular_letters_words(possible_words))

    return render_template('suggestions.html', number=number, word_list = word_list[:20])

@app.route('/word_input', methods=["GET", "POST"])
def word_input():
    feedback = []
    if request.method == "POST":

        for i in range(word_length):
            letter_feedback = request.form.get(f'feedback-{i}')
            feedback.append(letter_feedback)
            print("User feedback:", feedback)


    return render_template('word_input.html', word_list = possible_words, word_length=word_length, feedback=feedback)



if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True, port=12014)
