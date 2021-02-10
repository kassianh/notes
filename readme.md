# Notes

Notes is a small text editing notes app made in PyQT5. The app only has the ability for storing one note but has been set up to be easily extended.

## Installation

For easy installation use virtualenv and ```pip install -r requirements.txt```

- Used python version 3.9.1


## Assumptions and decisions

- The  requirements mentioned a standalone application with persistent storage. One option that presented itself was to use text files to make a text file reader. I chose to use the SQLite database instead because I believe databases will be more common for future applications I will work on. SQLite was chosen because it natively comes with python and PyQT5, and PyQT5 has dedicated drivers for easy integration.
- I only included the barebones of the application with what I think is required. I chose not to extend it (though I had many ideas) because I did not want it to become too much to read/comprehend. More focus was put on doing everything properly.
- An MVC pattern was chosen since that is QT's recommended approach. The model is an QSqlTableModel which uses QDataWidgetMapper to map the text data to the QTexEdit field. All formatting options are stored in other columns and extracted as needed.

## Problems I came across and how I overcame them

- Lack of python specific documentation - Many problems I came across were due to lack of python specific documentation for the recommended way of approaching problems. One of such was the QSqlTableModel. The QT documentation recommends setting up the model and using the QDataMapperWidget. Some familiarization with the official QT docs was needed to overcome this.
- Which database to choose - Initially I was not aware of SQLite being standalone and was looking for databases that were. One tutorial pointed out that SQLite comes natively with python and PYQT5 as it is only an imported C Library rather than a full on database (since it does not have client/server capabilities).

## Things I would add

For larger applications and with a bit more time and experience I would add unit tests and logging.