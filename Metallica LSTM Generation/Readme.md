# Metallica LSTM generator

This project comes in three parts:
- First part was scraping a website to get all tabs from Metallica
- Second part consisted in preprocessing the data, which was specially complicated by the fact that there is no norm for the tablature format and each tab seemed to reinvent how to write them. 
- Third part was here to train the model, and be able to generate some tabs in the end. 

The generator takes the first hand position in input, which roughly enables us to chose whether we want to generate a solo or rythmic part. An example can be found under the name Metallica_LSTM_Tab.txt
It is possible that there is some overfitting: some parts really seem to come from known tablatures. This is probably the next thing to improve.
