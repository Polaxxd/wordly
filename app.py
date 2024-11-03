from flask import Flask, render_template, request, redirect, url_for, session
import os

app = Flask(__name__)
app.secret_key = 'supersecretkey'  # Required for session handling

possible_words_global = ['start']

letter_frequency = [
    ['a', 8.91], ['ą', 0.99], ['b', 1.47], ['c', 3.96], ['ć', 0.40],
    ['d', 3.25], ['e', 7.66], ['ę', 1.11], ['f', 0.30], ['g', 1.42],
    ['h', 1.08], ['i', 8.21], ['j', 2.28], ['k', 3.51], ['l', 2.10],
    ['ł', 1.82], ['m', 2.80], ['n', 5.52], ['ń', 0.20], ['o', 7.75],
    ['ó', 0.85], ['p', 3.13], ['q', 0.14], ['r', 4.69], ['s', 4.32],
    ['ś', 0.66], ['t', 3.98], ['u', 2.50], ['v', 0.04], ['w', 4.65],
    ['x', 0.02], ['y', 3.76], ['z', 5.64], ['ź', 0.06], ['ż', 0.83]
]

def create_set_of_popular_letters_words(set_of_X_letter_words):
    popular_letters_words = []
    for elem in set_of_X_letter_words:
        score = 0
        letters_in_word = []
        for letter in elem:
            for em in letter_frequency:
                if letter == em[0] and letter not in letters_in_word:
                    score += em[1]
                    letters_in_word.append(letter)
        popular_letters_words.append([elem, score])
    sorted_popular_letters_words_frequency = [x[0] for x in sorted(popular_letters_words, key=lambda k: k[1], reverse=True)]
    return sorted_popular_letters_words_frequency


def eliminate_words(feedback):
    global possible_words_global
    new_list_of_words = possible_words_global
    print(feedback)
    print(len(new_list_of_words))
    base_word = feedback[0].lower()
    for i in range(len(base_word)):
            if feedback[i+1] == 'green':
                possible_words = new_list_of_words
                new_list_of_words = []
                green_letter = base_word[i]
                green_place = i
                for elem in possible_words:
                    if (elem[green_place] == green_letter):
                        new_list_of_words.append(elem)
            elif feedback[i+1] == 'yellow':
                possible_words = new_list_of_words
                new_list_of_words = []
                yellow_letter = base_word[i]
                yellow_place = i
                for elem in possible_words:
                    if (elem[yellow_place] != yellow_letter and yellow_letter in elem):
                        new_list_of_words.append(elem)
            else:
                possible_words = new_list_of_words
                new_list_of_words = []
                grey_letter = base_word[i]
                for elem in possible_words:
                    if (grey_letter not in elem):
                        new_list_of_words.append(elem)
    print(new_list_of_words)

    return new_list_of_words


@app.route('/')
def home():
    return render_template('home.html')

@app.route('/game_start/<int:number>')
def game_start(number):
    global possible_words_global  # Add this line to specify the global variable

    # Clear possible_words_global to avoid accumulation across games
    possible_words_global.clear()

    # Set the word length in session
    session['word_length'] = number

    # Load possible words for the given length
    file_name = f"len{number}.txt"
    if os.path.exists(file_name):
        with open(file_name) as file:
            possible_words_global.extend(line.strip() for line in file)

    words_list = create_set_of_popular_letters_words(possible_words_global)
    possible_words_global = words_list
    title = "Proponuję te słowa:"
    return render_template('suggestions.html', number=number, words_list=words_list[:20], t = title)


@app.route('/word_input', methods=["GET", "POST"])
def word_input():
    global possible_words_global
    feedback = []

    # Retrieve word_length from session
    word_length = session.get('word_length', 0)

    if request.method == "POST":
        title = "Proponuję te słowa:"
        feedback.append(request.form.get(f'current_word'))
        for i in range(word_length):
            letter_feedback = request.form.get(f'feedback-{i}')
            feedback.append(letter_feedback)
        # print("User feedback:", feedback)

        # Here you can add additional processing for feedback if needed
        if len(feedback[0]) != word_length:
            return redirect(url_for('word_input'))
        else:
            words_list = eliminate_words(feedback)
            possible_words_global = words_list
            if len(words_list) == 1:
                title = "To musi być to słowo!"
            elif len(words_list) == 0:
                title = " Nie mam już pomysłów :c"
            return render_template('suggestions.html', words_list=words_list, t=title)

    return render_template('word_input.html', word_list=possible_words_global, word_length=word_length, feedback=feedback)

@app.route('/input_processing/<feedback>')
def input_processing(feedback):
    return render_template('gra.html', feedback=feedback)

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True, port=12014)
