#ifndef MAINWINDOW_H
#define MAINWINDOW_H

#define nullptr 0
#include <QString>
#include <Q_INT64>
#include <QStringList>

#include <QMap>
#include <QProcess>
#include <QDateTime>
#include <QFileInfoList>
#include <QFile>
#include <QDir>
#include <QDirIterator>
#include <QAction>
#include <QMainWindow>
#include <QStandardItem>
#include <QMessageBox>
#include <QCloseEvent>
#include <QTextCodec>
#include "xmlmodifier.h"
#include <QKeySequence>
#include <QTextEdit>
#include "helpinfo.h"
#include <QTimer>

namespace Ui {
class MainWindow;
}

typedef struct treeNode {
    QString absPath;
    QStandardItem *item;
}TreeNode;

class MainWindow : public QMainWindow
{
    Q_OBJECT

public:
    explicit MainWindow(QString passwd, QString rootPath, QWidget *parent = 0);
    ~MainWindow();

protected:
    void closeEvent(QCloseEvent *event);

private slots:
    void treeItemChanged(QStandardItem *item);
    void treeItemClicked(const QModelIndex &index);
    void openConfigFile(const QModelIndex &index);
    void changeConfigFile(const QModelIndex &index);
    void saveFileProcess(bool checked);
    void runProject(bool checked);
    void outputLogFiles(bool checked);
    void showHelp(bool checked);
    void processError(QProcess::ProcessError error);
    void showHelpNew(bool checked);
    void closeDialog();

private:
    QTimer *timer;
    helpInfo *dialog;
    void createActions();
    void treeItem_checkAllChild(QStandardItem * item, bool check);
    void treeItem_CheckChildChanged(QStandardItem * item);
    void treeItem_checkAllChild_recursion(QStandardItem * item,bool check);

    Qt::CheckState checkSibling(QStandardItem * item);

    void initGlobalLayout();
    void initializeMenu();
    //初始化测试用例树，在rootPath 路径查找case路径，同时会忽略调框架自带的文件夹
    void initializeCaseTree(QString rootPath);
    void ChineseCode();
    void createTreeNode(QString absPath, QStandardItem *item, TreeNode &treeNode);
    void addTreeItemInfo(TreeNode node);

    bool omitDirectory(QString dirname);
    void setItemTypeLabel(const QModelIndex &index);
    //当 tree item的状态发生改变时设置配置文件路径
    void setConfigFilePath(const QModelIndex &index);
    QString getProperty();
    QString getDirname(const QString &path);
    QString getAbsXMLFilePathFromDir(const QString &dirPath);
    //设置check属性是否可以进行编辑
    void initializeItemAttribute(QStandardItem *item);
    void initializeItemCheckState();
    void setItemCheckedStatus(QStandardItem *item, QString cfgDirPath);
    //修改case配置
    void modifyCaseInModelConfigFile(QStandardItem * childItem, bool isAdd);
    //保存配置修改
    bool saveConfigFile(QString filePath, const QString &content);
    //改变passwd 未实现
    void changeRootPasswdInConfigFile(QString rootXMLPath, QString passwd);
    void sortNodeList(QMap<QString, TreeNode> sortInputList, QList<TreeNode> &sortOutputList);
    //等待配置文件写入完毕和item修改完成
    bool waitSymbolCorrect();
    //获取当前系统名称
    QString getOSName();
    //获取操作系统时间戳
    QString getTimeStamp();

private:
    Ui::MainWindow *ui;
    QStandardItemModel * folderModel;
    //用来存储对应item 的路径 如/home/loongson/loongat/04-menu
    QMap<QModelIndex, QString> mTreeInfo;

    QList<TreeNode> folderTreeList;
    QList<TreeNode> breathInfoList;
    QString testRootPath;
    QString rootPassWd;

    QAction *saveAction;
    QAction *runAction;
    QAction *saveLogAction;
    QAction *helpAction;

    static bool inWriting;
    static bool inChecking;
};

#endif
