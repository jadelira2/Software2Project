#ifndef MAINWINDOW_H
#define MAINWINDOW_H

#include <QMainWindow>
#include <string>
#include <cstring>
#include <cctype>
#include <QMessageBox>
#include <iostream>
#include <bitset>
#include <sstream>
#include <algorithm>

struct Position {
    int x;
    int y;
};

namespace Ui {
class MainWindow;
}

class MainWindow : public QMainWindow
{
    Q_OBJECT

public:
    explicit MainWindow(QWidget *parent = 0);
    ~MainWindow();

private slots:
    void on_EncryptionPushButton_clicked();
    void on_DecryptionPushButton_clicked();

    void on_Reset_triggered();
    void on_ClearPlainText_triggered();
    void on_CleaEncryptedText_triggered();

    void on_Exit_triggered();
    void on_actionAbout_Qt_triggered();

    void on_TypeComboBox_currentTextChanged(const QString &arg1);

private:

    Ui::MainWindow *ui;

    QString CaesarCipherE(QString plainText, int key);
    QString CaesarCipherD(QString encryptedText, int key);

    QString DESE(QString plainText, std::string key);
    QString iDESE(QString encryptedText, std::string key);

    std::vector<std::string> keyGeneration(std::string key);
    QString DESEncryption(std::string dataBlock, std::vector< std::string > keys);

    std::string Xor(std::string str1, std::string str2);
    std::string Function(std::string str1, std::string str2);
    std::string eBit(std::string str);

    QString DESD(QString plainText, std::string key);
    QString iDESD(QString encryptedText, std::string key);

    std::vector< std::string > BinaryAscii(std::string str);
    std::string BinaryAsciiToText(std::string str);
    std::string CharToBinaryAscii(char ch);
    char BinaryAsciiToChar(std::string binaryAscii);


};



#endif // MAINWINDOW_H
