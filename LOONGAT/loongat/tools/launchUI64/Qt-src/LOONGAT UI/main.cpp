#include "mainwindow.h"
#include <QApplication>


#include <QFileInfo>

int main(int argc, char *argv[])
{

    QApplication app(argc, argv);
    printf("luanchUI begin.\n");
    //初始化环境变量
    QString RootPath = "";
    QString passwd = "";
    if (argc > 2) {
        passwd = argv[1];
        printf("passwd %s\n", passwd.toStdString().c_str());
        RootPath = argv[2]; // ./launchUI [filePath]
        QFileInfo fileInfo(RootPath);
        RootPath = fileInfo.absoluteFilePath();
        printf("RootPath %s\n", RootPath.toStdString().c_str());
    } else {
        printf("Usage: ./launchUI passwd autotestFilePath\n");
        return -1;
    }
    //传递非空的参数 OSPasswd + testRootPath
    MainWindow w(passwd, RootPath);
    w.show();
    return app.exec();
}
