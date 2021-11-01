#include "mainwindow.h"
#include "ui_mainwindow.h"

MainWindow::MainWindow(QWidget *parent)
    : QMainWindow(parent)
    , ui(new Ui::MainWindow)
{
    ui->setupUi(this);
}

MainWindow::~MainWindow()
{
    delete ui;
}

//When we ckick on the Encryption push button then we need to check the value of our index to what type we are using
void MainWindow::on_EncryptionPushButton_clicked()

{
    QString plainText = ui->plainTextEdit_plain->toPlainText();
    QString encryptedText = "to be implemented";

//When We select Ceaser Cipher
    if(ui->TypeComboBox->currentIndex() == 0)
    {
        int key = ui->lineEdit_CC_key->text().toInt();
        encryptedText = CaesarCipherE(plainText, key);
    }

//When we have selected DES in binary
    else if(ui->TypeComboBox->currentIndex() == 1)
    {
        QString key = ui->lineEdit_DES_key->text();
        encryptedText = DESE(plainText, key.toStdString());
    }

//When we have selected DES in Text
    else if(ui->TypeComboBox->currentIndex() == 2)
    {
        QString key = ui->lineEdit_DES_key->text();
        encryptedText = DESD(plainText, key.toStdString());
    }
    ui->plainTextEdit_encrypted->document()->setPlainText(encryptedText);
}

//When we ckick on the Decryption push button then we need to check the value of our index to what type we are using
void MainWindow::on_DecryptionPushButton_clicked()
{
    QString encryptedText = ui->plainTextEdit_encrypted->toPlainText();
    QString plainText = "to be implemented";

//When We select Ceaser Cipher
    if(ui->TypeComboBox->currentIndex() == 0)
    {
        int key = ui->lineEdit_CC_key->text().toInt();
        plainText = CaesarCipherD(encryptedText, key);
    }
//When we have selected DES in binary
    else if(ui->TypeComboBox->currentIndex() == 1)
    {
        QString key = ui->lineEdit_DES_key->text();
        plainText = iDESE(encryptedText, key.toStdString());
    }
//When we have selected DES in Text
    else if(ui->TypeComboBox->currentIndex() == 2)
    {
        QString key = ui->lineEdit_DES_key->text();
        plainText = iDESD(encryptedText, key.toStdString());
    }
    ui->plainTextEdit_plain->document()->setPlainText(plainText);
}

//Whenever we want evrything to Reset to start over
void MainWindow::on_Reset_triggered()
{
    ui->plainTextEdit_plain->clear();
    ui->plainTextEdit_encrypted->clear();
    ui->lineEdit_CC_key->clear();
}

//To clear only the Plain Text
void MainWindow::on_ClearPlainText_triggered()
{
    ui->plainTextEdit_plain->clear();
}

//To clear Encrypted Text
void MainWindow::on_CleaEncryptedText_triggered()
{
    ui->plainTextEdit_encrypted->clear();
}

//To Exit
void MainWindow::on_Exit_triggered()
{
    exit(0);
}

//QT Creator help
void MainWindow::on_actionAbout_Qt_triggered()
{
    QMessageBox::aboutQt(this);
}

//Check and see if of type of method has changed
void MainWindow::on_TypeComboBox_currentTextChanged(const QString &arg1)
{
    if(arg1 == "Caesar Cipher")
    {
        ui->stackedWidget->setCurrentIndex(0);
    }
    else if(arg1 == "DES")
    {
        ui->stackedWidget->setCurrentIndex(1);
    }
    else if(arg1 == "DES with Text")
    {
        ui->stackedWidget->setCurrentIndex(2);
    }
}

// This function receives text and shift and returns the encrypted text
QString MainWindow::CaesarCipherE(QString plainText, int key)
{

    std::string result = "";
    std::string plainStdText = plainText.toStdString();

    // Traverse text
    for (int i=0;i<plainText.length();i++)
    {
        //If plaintext is empty return blank
        if(plainStdText[i] == ' ')
        {
            result += ' ';
        }
        //Else there is a letter and we encrypt using the cypher formula
        else if(std::isalpha(plainStdText[i]))
        {
            // apply transformation to each character
            // Encrypt Uppercase letter
            if (std::isupper(plainStdText[i]))
                result += char(int(plainStdText[i]+key-65)%26 +65);
            //Encrypt Lowercase letter
            else
                result += char(int(plainStdText[i]+key-97)%26 +97);
        }
    }
    // Return the resulting string
    return QString::fromStdString(result);
}

//This function reverses the decrypted text and reveals the hidden plain text
QString MainWindow::CaesarCipherD(QString encryptedText, int key)
{
    //use the same function to decrypt, instead we’ll modify the shift value such that 26-key
    return CaesarCipherE(encryptedText, 26-key);
}


//DES Function Starts

//Function to Encrypt DES Text
QString MainWindow::DESE(QString plainText, std::string key)
{
    std::vector< std::string > keys = keyGeneration(key);

    QString encryptedText = DESEncryption(plainText.toStdString(), keys);

    return encryptedText;
}

//Function to Decrypt DES Text
QString MainWindow::DESD(QString encryptedText, std::string key)
{
    std::vector< std::string > keys = keyGeneration(key);

    std::reverse(keys.begin(), keys.end());

    QString plainText = DESEncryption(encryptedText.toStdString(), keys);

    return plainText;
}

//Function to Genarate keys for 16 rounds
std::vector< std::string > MainWindow::keyGeneration(std::string key)
{
    std::string permutationKey = "";

    // The PC1 table
    int pc1[56] = {
        57, 49, 41, 33, 25, 17, 9,
        1, 58, 50, 42, 34, 26, 18,
        10, 2, 59, 51, 43, 35, 27,
        19, 11, 3, 60, 52, 44, 36,
        63, 55, 47, 39, 31, 23, 15,
        7, 62, 54, 46, 38, 30, 22,
        14, 6, 61, 53, 45, 37, 29,
        21, 13, 5, 28, 20, 12, 4
    };

    //Compressing the key using the PC1 table
    for(int i=0;i<56; ++i)
    {
        permutationKey += key[pc1[i]-1];
    }

    //Now we will get 16 blocks( 1≤n≤16) by applying the number of cyclic left shifts
    int LeftShifts[16] = {1, 1, 2, 2, 2, 2, 2, 2, 1, 2, 2, 2, 2, 2, 2, 1};

    std::vector< std::pair<std::string, std::string> > keys;

    //Dividing the key into two equal halves
    std::string C0 = permutationKey.substr(0,28);
    std::string D0 = permutationKey.substr(28,56);

    keys.push_back(std::make_pair(C0, D0));

    for(int i=1 ; i<17 ; ++i)
    {
        std::string C = keys[i-1].first;
        std::string D = keys[i-1].second;

        //Apply left shifts for D and D
        C = C.substr(LeftShifts[i-1], C.length()) + C.substr(0, LeftShifts[i-1]);
        D = D.substr(LeftShifts[i-1], D.length()) + D.substr(0, LeftShifts[i-1]);

        //Combine both pairs back up
        keys.push_back(std::make_pair(C, D));
    }

    // The PC2 table
    int pc2[48] = {
        14, 17, 11, 24, 1, 5,
        3, 28, 15, 6, 21, 10,
        23, 19, 12, 4, 26, 8,
        16, 7, 27, 20, 13, 2,
        41, 52, 31, 37, 47, 55,
        30, 40, 51, 45, 33, 48,
        44, 49, 39, 56, 34, 53,
        46, 42, 50, 36, 29, 32
    };

    std::vector<std::string> finalKeys;

    //Traverse through the 16 rounds
    for(int i=0;i<16;++i)
    {
        std::string combinedkey = keys[i+1].first + keys[i+1].second;
        std::string roundkey = "";

        //Finally the PC2 table is used to transposethe key bits
        for(int j=0;j<48;++j)
        {
            roundkey += combinedkey[pc2[j]-1];
        }
        //Send final keys back
        finalKeys.push_back(roundkey);

    }
    //Lets user know Keys were succesfully generated staring with Round 0
    std::cout << std::endl << ">[BEGIN] Keys generated Successfully" << std::endl << std:: endl;

    //Print out the keys on Terminal
    for(size_t i=0; i<finalKeys.size(); ++i)
    {
        std::cout << "Key " << i+1 << ": " << finalKeys[i] << std::endl;
    }
    //Lets user know Keys were succesfully generated ending with Round 16
    std::cout << std::endl << ">[END] Keys generated Successfully" << std::endl << std:: endl;

    //Send keys back to user
    return finalKeys;
}

QString MainWindow::DESEncryption(std::string dataBlock, std::vector< std::string > keys)
{

    std::string permutationBlock = "";

    // Initial Permutation Table
    int initialPermutation[64] = {
        58,    50,   42,    34,    26,   18,    10,    2,
        60,    52,   44,    36,    28,   20,    12,    4,
        62,    54,   46,    38,    30,   22,    14,    6,
        64,    56,   48,    40,    32,   24,    16,    8,
        57,    49,   41,    33,    25,   17,     9,    1,
        59,    51,   43,    35,    27,   19,    11,    3,
        61,    53,   45,    37,    29,   21,    13,    5,
        63,    55,   47,    39,    31,   23,    15,    7
    };

    //For perform the initial pemutation
    for(int i=0 ; i<64 ; ++i)
    {
        permutationBlock += dataBlock[initialPermutation[i]-1];
    }
    //Split Left String and Right String
    std::string L0 = permutationBlock.substr(0, 32);
    std::string R0 = permutationBlock.substr(32, 64);

    //Print out L0 and R0
    std::cout << "L0 : " << L0 << std::endl;
    std::cout << "R0 : " << R0 << std::endl;

    //Combine into new pair and send to next round
    std::vector< std::pair<std::string, std::string> > data;
    data.push_back(std::make_pair(L0, R0));

    //16 rounds
    for(int i=1;i<17;++i)
    {
        //Next L is equal to previous Rn
        std::string L = data[i-1].second;

        std::string R = Xor(
            data[i-1].first,
            Function(eBit(data[i-1].second), keys[i-1])
        );

        data.push_back(std::make_pair(L, R));

        std::cout << "L" << i << " : " << L << std::endl;
        std::cout << "R" << i << " : " << R << std::endl;
    }

    std::string encryptedDataReversedKey = "";
    encryptedDataReversedKey += data[data.size()-1].second;
    encryptedDataReversedKey += data[data.size()-1].first;

    std::string finalPermutedBlock = "";

    int finalPermutation[64] = {
        40, 8, 48, 16, 56, 24, 64, 32,
        39, 7, 47, 15, 55, 23, 63, 31,
        38, 6, 46, 14, 54, 22, 62, 30,
        37, 5, 45, 13, 53, 21, 61, 29,
        36, 4, 44, 12, 52, 20, 60, 28,
        35, 3, 43, 11, 51, 19, 59, 27,
        34, 2, 42, 10, 50, 18, 58, 26,
        33, 1, 41,  9, 49, 17, 57, 25
    };

    for(int i=0 ; i<64 ; ++i)
    {
        finalPermutedBlock += encryptedDataReversedKey[finalPermutation[i]-1];
    }

    return QString(finalPermutedBlock.c_str());
}

//XOR Function to be called when encryption is happening
std::string MainWindow::Xor(std::string str1, std::string str2)
{
    //Checking to see if user entered correct number of strings
    if(str1.length() != str2.length())
        std::cout << "Error in XOR strings not equal" << std::endl;

    std::string result = "";
    //Traverse through the string and turn all 1 into 0's and 0 into 1's
    for(size_t i=0;i<str1.length();++i)
    {
        if(str1[i] == str2[i])
            result += '0';
        else
            result += '1';
    }
    //Send the string back for next step
    return result;
}

//Needs comments
std::string MainWindow::Function(std::string str1, std::string str2)
{
    // result is 48 bit
    std::string result = Xor(str1, str2);

    int sboxes[8][4][16] =
    {
        {
            { 14,  4,  13,  1,   2, 15,  11,  8,   3, 10,   6, 12,   5,  9,   0,  7 },
            {  0, 15,   7,  4,  14,  2,  13,  1,  10,  6,  12, 11,   9,  5,   3,  8 },
            {  4,  1,  14,  8,  13,  6,   2, 11,  15, 12,   9,  7,   3, 10,   5,  0 },
            { 15, 12,   8,  2,   4,  9,   1,  7,   5, 11,   3, 14,  10,  0,   6, 13 }
        },
        {
            { 15,  1,   8, 14,   6, 11,   3,  4,   9,  7,   2, 13,  12,  0,   5, 10 },
            {  3, 13,   4,  7,  15,  2,   8, 14,  12,  0,   1, 10,   6,  9,  11,  5 },
            {  0, 14,   7, 11,  10,  4,  13,  1,   5,  8,  12,  6,   9,  3,   2, 15 },
            { 13,  8,  10,  1,   3, 15,   4,  2,  11,  6,   7, 12,   0,  5,  14,  9 }
        },
        {
            { 10,  0,   9, 14,   6,  3,  15,  5,   1, 13,  12,  7,  11,  4,   2,  8 },
            { 13,  7,   0,  9,   3,  4,   6, 10,   2,  8,   5, 14,  12, 11,  15,  1 },
            { 13,  6,   4,  9,   8, 15,   3,  0,  11,  1,   2, 12,   5, 10,  14,  7 },
            {  1, 10,  13,  0,   6,  9,   8,  7,   4, 15,  14,  3,  11,  5,   2, 12 }
        },
        {
            {  7, 13,  14,  3,   0,  6,   9, 10,   1,  2,   8,  5,  11, 12,   4, 15 },
            { 13,  8,  11,  5,   6, 15,   0,  3,   4,  7,   2, 12,   1, 10,  14,  9 },
            { 10,  6,   9,  0,  12, 11,   7, 13,  15,  1,   3, 14,   5,  2,   8,  4 },
            {  3, 15,   0,  6,  10,  1,  13,  8,   9,  4,   5, 11,  12,  7,   2, 14 }
        },
        {
            {  2, 12,   4,  1,   7, 10,  11,  6,   8,  5,   3, 15,  13,  0,  14,  9 },
            { 14, 11,   2, 12,   4,  7,  13,  1,   5,  0,  15, 10,   3,  9,   8,  6 },
            {  4,  2,   1, 11,  10, 13,   7,  8,  15,  9,  12,  5,   6,  3,   0, 14 },
            { 11,  8,  12,  7,   1, 14,   2, 13,   6, 15,   0,  9,  10,  4,   5,  3 }
        },
        {
            { 12,  1,  10, 15,   9,  2,   6,  8,   0, 13,   3,  4,  14,  7,   5, 11 },
            { 10, 15,   4,  2,   7, 12,   9,  5,   6,  1,  13, 14,   0, 11,   3,  8 },
            {  9, 14,  15,  5,   2,  8,  12,  3,   7,  0,   4, 10,   1, 13,  11,  6 },
            {  4,  3,   2, 12,   9,  5,  15, 10,  11, 14,   1,  7,   6,  0,   8, 13 }
        },
        {
            {  4, 11,   2, 14,  15,  0,   8, 13,   3, 12,   9,  7,   5, 10,   6,  1 },
            { 13,  0,  11,  7,   4,  9,   1, 10,  14,  3,   5, 12,   2, 15,   8,  6 },
            {  1,  4,  11, 13,  12,  3,   7, 14,  10, 15,   6,  8,   0,  5,   9,  2 },
            {  6, 11,  13,  8,   1,  4,  10,  7,   9,  5,   0, 15,  14,  2,   3, 12 }
        },
        {
            { 13,  2,   8,  4,   6, 15,  11,  1,  10,  9,   3, 14,   5,  0,  12,  7 },
            {  1, 15,  13,  8,  10,  3,   7,  4,  12,  5,   6, 11,   0, 14,   9,  2 },
            {  7, 11,   4,  1,   9, 12,  14,  2,   0,  6,  10, 13,  15,  3,   5,  8 },
            {  2,  1,  14,  7,   4, 10,   8, 13,  15, 12,   9,  0,   3,  5,   6, 11 }
        }
    };

    std::string output = "";
    std::string outerBits = "";
    std::string innerBits = "";

    // The right half of the plain text is expanded
    for(int i=0, s=0 ; i<48 ; i+=6, s++)
    {
        outerBits += result[i];
        outerBits += result[i+5];

        innerBits += result[i+1];
        innerBits += result[i+2];
        innerBits += result[i+3];
        innerBits += result[i+4];

        int row = std::stoi(outerBits, nullptr, 2);
        int column = std::stoi(innerBits, nullptr, 2);

        int valInSBox = sboxes[s][row][column];

        output += std::bitset<4>(valInSBox).to_string();

        outerBits = "";
        innerBits = "";
    }

    std::string permutedOutput = "";

    int permutations[32] = {
        16,  7, 20, 21,
        29, 12, 28, 17,
         1, 15, 23, 26,
         5, 18, 31, 10,
         2,  8, 24, 14,
        32, 27,  3,  9,
        19, 13, 30,  6,
        22, 11,  4, 25
    };

    for(int i=0; i<32; ++i)
    {
        permutedOutput += output[permutations[i]-1];
    }

    return permutedOutput;
}

//Needs comments
std::string MainWindow::eBit(std::string str)
{
    std::string result = "";

    int ePermutations[48] = {
         32,     1,    2,     3,     4,    5,
          4,     5,    6,     7,     8,    9,
          8,     9,   10,    11,    12,   13,
         12,    13,   14,    15,    16,   17,
         16,    17,   18,    19,    20,   21,
         20,    21,   22,    23,    24,   25,
         24,    25,   26,    27,    28,   29,
         28,    29,   30,    31,    32,    1
    };

    for(int i=0;i<48;++i)
    {
        result += str[ePermutations[i]-1];
    }

    return result;
}


//DES with Text
QString MainWindow::iDESE(QString plainText, std::string key)
{
    std::vector< std::string > keys = keyGeneration(key);
    std::vector< std::string > blocks = BinaryAscii(plainText.toStdString());

    QString encryptedText;

    for(size_t i=0; i<blocks.size(); ++i)
        encryptedText += DESEncryption(blocks[i], keys);

    return encryptedText;
}

QString MainWindow::iDESD(QString encryptedText, std::string key)
{
    std::vector< std::string > keys = keyGeneration(key);
    std::reverse(keys.begin(), keys.end());

    std::string stdPlainText = encryptedText.toStdString();
    std::string allPlainText = "";

    for(int i=0; i<encryptedText.size()/64; ++i)
    {
        allPlainText += DESEncryption(stdPlainText.substr(i*64, 64), keys).toStdString();
    }

    return QString::fromStdString(BinaryAsciiToText(allPlainText));
}

std::vector< std::string > MainWindow::BinaryAscii(std::string str)
{
    std::vector< std::string > blocksOfData;

    for(size_t i=0; i<str.size()/8; ++i)
    {
        std::string blockStr = str.substr(i*8, 8);
        std::string block = "";

        for(int i=0; i<8; ++i)
            block += CharToBinaryAscii(blockStr[i]);

        blocksOfData.push_back(block);
    }

    if(str.size()%8 != 0)
    {
        int start = ((int)str.size()/8)*8;
        int length = (int)str.size()- start;

        std::string blockStr = str.substr(start, length);
        for(int i=0; i<(8-length); ++i)
            blockStr += " ";

        std::string block = "";
        for(int i=0; i<8; ++i)
            block += CharToBinaryAscii(blockStr[i]);
        blocksOfData.push_back(block);
    }

    return blocksOfData;
}

std::string MainWindow::BinaryAsciiToText(std::string str)
{
    std::string blocksOfData = "";

    for(size_t i=0; i<str.size()/64; ++i)
    {
        std::string blockStr = str.substr(i*64, 64);
        std::string block = "";

        for(int i=0; i<8; ++i)
        {
           std::string ascii = blockStr.substr(i*8, 8);
           block += BinaryAsciiToChar(ascii);
        }
        blocksOfData += block;
    }

    return blocksOfData;
}

std::string MainWindow::CharToBinaryAscii(char ch)
{
    return std::bitset<8>(int(ch)).to_string();
}

char MainWindow::BinaryAsciiToChar(std::string binaryAscii)
{
    return char(std::bitset<8>(binaryAscii).to_ulong());
}
