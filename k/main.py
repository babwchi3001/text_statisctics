import glob
import os
import csv

def run_program_loop(all_text_statistics):
    print("----------------------------------------------------------------------\nAvailable text files to analyse:")
    counter = 0
    word_to_inform = str
    for my_dict in all_text_statistics:
        print(counter, ": " + my_dict)
        counter = counter + 1

    print("Please choose a textfile by entering a number: ")
    given_input = str
    while 1:
        given_input = str(input())
        if given_input == "exit":
            return
        if not given_input.isnumeric():
            print("Please enter a number. Try Again!")
            continue
        if given_input.isnumeric():
            if(int(given_input) < 0 or int(given_input) > counter):
                print("Please enter a valid number. Try Again!")
            else:
                print("Please type the word you want information on: ")
                word_to_inform = str(input())
                break

    dict_to_check = list(all_text_statistics.items())[int(given_input)]
    chosen_word_value = 0
    counter_most_common_words = 0
    flag_check = 0
    while 1:
        if word_to_inform == "exit":
            return
        for stats_key, stats_value in dict_to_check[1].items():
            #print(stats_key)
            if word_to_inform == stats_key:
                chosen_word_value = stats_value
                flag_check = 1
        if flag_check:
            break
        else:
            print(word_to_inform,", is not present in",dict_to_check[0], ". Try Again!")
            word_to_inform = str(input())

    for stats_key, stats_value in dict_to_check[1].items():
        if stats_value >= chosen_word_value :
            counter_most_common_words = counter_most_common_words + 1
    print("In text",dict_to_check[0],"word",word_to_inform,"occurs",chosen_word_value, "time(s).", counter_most_common_words,"other words occur at least as often as",word_to_inform,"in this text.")

def run_text_statistics(datafolder, path_to_stopwords):

    print("----------------------------------------------------------------------\nWelcome to EasyText!\nType \"exit\" to exit the program at any time.\n----------------------------------------------------------------------\n")
    my_file = open(path_to_stopwords, "r")
    stopwords = my_file.read()
    my_file.close()
    counter = 0
    folder_dict = {}
    print("Calculating text statistics... please wait.\n")
    os.chdir(datafolder)
    for file in glob.glob("*.txt"):
        folder_dict[file] = {}
        folder_dict[file] = calculate_text_stats(file, stopwords)
        counter = counter + 1
        new_file = file[:-4]
        new_file = new_file + ".csv"
        write_text_stats_to_file(folder_dict[file], new_file)

    print("Finished calculating text statistics.")
    run_program_loop(folder_dict)
    print("----------------------------------------------------------------------\nThank you for using EasyText! Good bye!")

def calculate_text_stats(file, stopwords):
    file_to_analyze = open(file, "r")
    file_string = file_to_analyze.read()
    file_to_analyze.close()
    word_and_counter_array = []
    counter = 0
    stopwords_array = stopwords.split()
    for words in file_string.split():
        for character in words:
            if not character.isalnum():
                words = words.replace(character, '')
        word_and_counter_array.append(words)
        counter = counter + 1
    text_stats_dict = {}

    for word in word_and_counter_array:
        word_found_check = 0
        word = word.lower()
        for stopword in stopwords_array:
            if stopword == word:
                word_found_check = 1
                break
        if word_found_check == 1:
            continue

        word_counter = 0
        for word_inner in word_and_counter_array:
            word_inner = word_inner.lower()
            if word == word_inner:
                word_counter = word_counter + 1
        text_stats_dict[word] = word_counter
    return text_stats_dict

def write_text_stats_to_file(words_and_counts, filepath):
    filepath = "/home/babwchi/Desktop/ali/" + filepath
    with open(filepath, 'w') as csv_file:
        writer = csv.writer(csv_file)
        for key, value in words_and_counts.items():
            writer.writerow([key, value])
if __name__ == '__main__':
    datafolder = "/home/babwchi//Desktop/ali"
    path_to_stopwords = "/home/babwchi/Desktop/ali/stopwords.stop"
    run_text_statistics(datafolder, path_to_stopwords)