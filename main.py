import argparse
import pandas as pd


def main(no_questions):
    """
    :param no_questions (int): The number of quiz questions wanted
    :return (array): An array of question_ids
    """
    questions = pd.read_csv('questions.csv')  # Importing the question data

    random_sampled = pd.DataFrame([])

    # Separating the questions by strand_id
    q1 = questions[questions['strand_id'] == 1]
    q2 = questions[questions['strand_id'] == 2]

    # Getting the questions
    sdf = pd.concat([
        q1.groupby(['standard_id']).sample(n=(no_questions // 2), random_state=1, replace=True).drop_duplicates(
            'standard_name').head(no_questions // 2),
        q2.groupby(['standard_id']).sample(n=(no_questions // 2), random_state=1, replace=True).drop_duplicates(
            'standard_name').head(no_questions // 2)])

    diff = no_questions - len(sdf)

    if diff >= 1:
        random_sampled = questions.sample(n=diff, random_state=1)
    return pd.concat([sdf, random_sampled]).sort_values(by=['difficulty'])['question_id'].to_list()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Please enter the number of questions for the quiz.")
    parser.add_argument("num_questions", type=int, help="any number greater than zero")
    args = parser.parse_args()
    ques_no = args.num_questions

    assert ques_no > 0, 'Only numbers greater than 0'
    assert isinstance(ques_no, int), 'only integers are allowed'

    print(main(ques_no))
