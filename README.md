# CheatChecker
### Project for BGU 2.0 Hackaton
in this project why tried to use the moodle answering system to determine if some student cheated.

## using the system
### Prerequisites

install dependencies:

    git clone https://github.com/CiTRuS93/CheatChecker.git
    cd CheatChecker/project
    pip install requirement.txt

we want to use bert pre-trained model which we can download from here:
https://github.com/hanxiao/bert-as-service#1-download-a-pre-trained-bert-model
export moodle answers:
in the moodle system export the students responses from the quiz:
In the quiz, Navigation block -> ... -> Quiz name -> Results -> Responses.

change the file pass in CheatChecker concept notebook to the new file.

## using the system

bert as service need to be alive so run:
	
    bert-serving-start -model_dir ./path_to_bert_model -num_worker=4

open jupyter notebook and run all cells and see the results.


