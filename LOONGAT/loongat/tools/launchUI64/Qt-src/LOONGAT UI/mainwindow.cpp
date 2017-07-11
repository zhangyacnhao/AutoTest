#include "mainwindow.h"
#include "ui_mainwindow.h"
#include <stdio.h>
#include <string.h>
#include <QtTest/QTest>

MainWindow::MainWindow(QString passwd, QString rootPath, QWidget *parent) :
    QMainWindow(parent),
    ui(new Ui::MainWindow),
    testRootPath(rootPath),
    rootPassWd(passwd)
{
    ui->setupUi(this);
    ChineseCode();
    initializeMenu();
    initializeCaseTree(testRootPath);
    initializeItemCheckState();
    createActions();
}


void MainWindow::ChineseCode(void)
{    //解决中文乱码
    QString myStyle = "color:black; border:1px solid darkkhaki; border-radius:1px;opacity:200; background-color:white; selection-color:white; selection-background-color:darkkhaki;";
    QTextCodec::setCodecForTr(QTextCodec::codecForName("system"));
    QTextCodec::setCodecForCStrings(QTextCodec::codecForName("system"));
    QTextCodec::setCodecForLocale(QTextCodec::codecForName("system"));
   // 添加颜色设置
    ui->typeLabel->setStyleSheet("color:black; border:1px solid darkkhaki; border-radius:1px;opacity:200;");
    ui->configTextEdit->setStyleSheet(myStyle);
    ui->configFilePathBrowser->setStyleSheet(myStyle);
    ui->treeView->setStyleSheet(myStyle);
    ui->centralWidget->setStyleSheet(myStyle);
    ui->menuBar->setStyleSheet(myStyle);
    ui->statusBar->setStyleSheet("color:gray"); //khaki darkkhaki
}

bool MainWindow::inWriting = false;
bool MainWindow::inChecking = false;

//初始化菜单栏
void MainWindow::initializeMenu()
{
    //QFont myFont=QString::fromUtf8("楷体,18,-1,5,50,0,0,0,0,0");
    runAction = new QAction(QString::fromUtf8("运行(&R)"), this);
    runAction->setShortcut(QKeySequence(Qt::CTRL + Qt::Key_R)); // #2015.10.27 modified by vans
    //runAction->setFont(myFont); set font mid
    runAction->setStatusTip(QString::fromUtf8("开始测试:Ctrl+R"));
    //runAction->setIcon(); set ico  lower
    menuBar()->addAction(runAction);

    saveAction = new QAction(QString::fromUtf8("配置保存(&S)"), this);
    saveAction->setShortcut(QKeySequence(Qt::CTRL + Qt::Key_S));
    saveAction->setStatusTip(QString::fromUtf8("保存当前显示的XML配置文件:Ctrl+S "));  //#2015.10.27 modified by vans
    menuBar()->addAction(saveAction);
    saveLogAction = new QAction(QString::fromUtf8("日志处理(&L)"), this);
    saveLogAction->setShortcut(QKeySequence(Qt::CTRL + Qt::Key_L));  //#2015.10.27 modified by vans
    saveLogAction->setStatusTip(QString::fromUtf8("打包日志文件，并清空项目中的日志:Ctrl+L"));
    menuBar()->addAction(saveLogAction);

    //menuBar()->addMenu(QString::fromUtf8("帮助&H"));
    helpAction = new QAction(QString::fromUtf8("帮助(&H)"),this);
    helpAction->setShortcut(QKeySequence(Qt::Key_F1));
    helpAction->setStatusTip(QString::fromUtf8("查看关于LOONGAT帮助:F1"));
    menuBar()->addAction(helpAction);
}

//信号和槽的对接
void MainWindow::createActions()
{
   connect(folderModel, SIGNAL(itemChanged(QStandardItem*)), this, SLOT(treeItemChanged(QStandardItem*)));
   connect(ui->treeView,SIGNAL(clicked(const QModelIndex)), this,SLOT(treeItemClicked(const QModelIndex &)));
   connect(saveAction, SIGNAL(triggered(bool)), this, SLOT(saveFileProcess(bool)));
   connect(runAction, SIGNAL(triggered(bool)), this, SLOT(runProject(bool)));
   connect(saveLogAction, SIGNAL(triggered(bool)), this, SLOT(outputLogFiles(bool)));
   connect(helpAction, SIGNAL(triggered(bool)), this, SLOT(showHelpNew(bool)));
   //connect(helpAction, SIGNAL(error(ProcessError)), this, SLOT(processError(ProcessError)));
}
//窗口关闭和撤销
void MainWindow::closeEvent(QCloseEvent *event)
{

      saveFileProcess(true);
      if (!waitSymbolCorrect()) {
          event->ignore();
      } else {
        event->accept();
    }
}

//等待配置文件修改完毕
bool MainWindow::waitSymbolCorrect()
{

    if (XMLModifier::inWriting || inWriting || inChecking) {
        QTime t;
        t.start();
        while(t.elapsed() < 5000) {
            QCoreApplication::processEvents();
         }

        if (XMLModifier::inWriting || inWriting || inChecking) {
             QMessageBox::information(NULL, "运行提示", "配置文件还在写入中，请稍后再点击", QMessageBox::Yes, QMessageBox::Yes);
            printf("Waiting process is not finished, please try again later.\n");
            return false;
        }
    }

    return true;
}

//开始执行程序 RunAction slot function
void MainWindow::runProject(bool checked) //
{
    Q_UNUSED(checked);
    QDir dir(testRootPath);
    QString name = dir.dirName();
    QString totalAutoTestPath = testRootPath + "/" + name + ".py " + rootPassWd + " -r";
    QString cmd = "python " + totalAutoTestPath;

    printf("begin run autotest projects %s\n", cmd.toStdString().c_str());

    //等待配置文件写入完毕
    if (!waitSymbolCorrect()) {
        return;
    }

    this->hide();
    system(cmd.toStdString().c_str());
    //关闭UI 界面后开始测试
    this->close();
}

//获取XML 文件绝对路径
QString MainWindow::getAbsXMLFilePathFromDir(const QString &dirPath)
{
    QString name = getDirname(dirPath);
    QString xmlFilePath = dirPath + "/" + name + ".xml";

    return xmlFilePath;
}

//执行考包日志--日志打包操作
void MainWindow::outputLogFiles(bool checked)
{
    Q_UNUSED(checked);
    //调用tarlog.sh 打包日志
    QString scriptPath = testRootPath + "/tools/scripts/tarlog.sh";
    QFileInfo fileInfo(testRootPath);
    QChar tail = testRootPath.at(testRootPath.length()-1);
    QString chopPath = testRootPath;
    if (tail == '/') {
        chopPath.chop(1);
        fileInfo.setFile(chopPath);
    }
    QString loongatTarFileAbsolutePath = fileInfo.dir().absolutePath();

    QString timeStamp = getTimeStamp();
    QString osName = getOSName();
    QString label = timeStamp + "-" + osName;

    int ret = QMessageBox::information(NULL, "运行提示", "是否需要保存所有的输出文件？", QMessageBox::Yes | QMessageBox::No, QMessageBox::Yes);
    if (ret != QMessageBox::Yes) {
        return;
    }

    QMessageBox::information(NULL, "运行提示", "保存的输出文件位于: " + loongatTarFileAbsolutePath , QMessageBox::Yes);

    QString cmd  = "bash " + scriptPath + " "  + testRootPath + " " + loongatTarFileAbsolutePath + " "  + label + " " + rootPassWd;
    qDebug() <<"Save Log Command ===> " <<  cmd;
    system(cmd.toStdString().c_str());
}

void MainWindow::showHelp(bool checked)
{
    Q_UNUSED(checked);
    QDir dir;
    QProcess process;
    QString  path=dir.currentPath() + "/helpDialog/helpInfo";

    qDebug() << "Qsting type" << path;
    if (process.isOpen())
    {
        process.close();
    }
    process.start(path);
    process.waitForFinished();
    process.close();
     //home/loongson/visualcfg-proj/build-VisualConfig-desktop-Release/helpDialog
    //system(path.toStdString().c_str());
}


void MainWindow::showHelpNew(bool checked)
{
    Q_UNUSED(checked);
    this->timer= new QTimer;
    this->dialog=new helpInfo;
    this->dialog->show();
    this->timer->start(8000);// 5s
    connect(this->timer,SIGNAL(timeout()),this,SLOT(closeDialog()));
}

void MainWindow::closeDialog()
{
     this->dialog->close();
     this->timer->stop();
}

void MainWindow::processError(QProcess::ProcessError error)
{
    switch(error)
    {
    case QProcess::FailedToStart:
        QMessageBox::information(NULL,"Failed to start","start unsuccessifully");
        break;
    case QProcess::Crashed:
        QMessageBox::information(0,"Failed to start","start crashed");
        break;
    case QProcess::Timedout:
        QMessageBox::information(0,"Failed to start","start timeout");
        break;
    case QProcess::WriteError:
        QMessageBox::information(NULL,"Failed to start","start write error");
        break;
    case QProcess::ReadError:
        QMessageBox::information(0,"Failed to start","start read error");
        break;
    case QProcess::UnknownError:
        QMessageBox::information(0,"Failed to start","start unknown error");
        break;
    default:
        QMessageBox::information(0,"Start finished","Start successifully");
        break;
    }

}
//获取系统时间戳
QString MainWindow::getTimeStamp()
{
    QDateTime time = QDateTime::currentDateTime();
    //设置显示格式
    QString timeStamp = time.toString("yyyy-MM-dd-hh-mm");

    return timeStamp;
}

//获取系统名称
QString MainWindow::getOSName()
{
    QFile file("/etc/issue");
    QString osName = "";
    if (!file.open(QIODevice::ReadOnly)) {
        qDebug() << "cannot read /etc/issue";
        return "";
    }

    QString content = file.readAll();
    if (content.contains("Fedora") || content.contains("21", Qt::CaseInsensitive)){
        osName = "Fedora-21";
    }
    else if (content.contains("Fdeora", Qt::CaseInsensitive)) {
        osName = "Fedora-13";
    }

    file.close();
    return osName;
}

//修改配置文件
void MainWindow::changeConfigFile(const QModelIndex &index)
{
    static QString lastPath = "";
    static QString lastContent = "";
    //获取XML文件路径
    QMap<QModelIndex, QString>::iterator iter = mTreeInfo.find(index);
    QString xmlFilePath = getAbsXMLFilePathFromDir(iter.value());
    XMLModifier modifier;
    bool lastIsModule = modifier.isModuleConfig(lastPath);
    if (QString::compare(lastPath, xmlFilePath) == 0) {
        return;
    } else {
        lastContent = ui->configTextEdit->toPlainText();
        if (!lastIsModule) {
            if (!saveConfigFile(lastPath, lastContent)) {
                qDebug() << "save config file error, cannot change item";
                return;
            }
        }
    }
    lastPath = xmlFilePath;

    if (modifier.checkXMLFormat(xmlFilePath)) {
        QFile file(xmlFilePath);
        if (!file.open(QIODevice::ReadOnly)) {
            qDebug() << "cannot read xml file" << xmlFilePath;
            QString infoStr = xmlFilePath + " config file format error";
            QMessageBox::information(NULL, "changeConfigFile", infoStr, QMessageBox::Yes, QMessageBox::Yes);
            return;
        }

        QString content = file.readAll();
        ui->configTextEdit->setText(content);
        file.close();

        bool curIsModule = modifier.isModuleConfig(xmlFilePath);
        if (curIsModule) {
            ui->configTextEdit->setReadOnly(true);
        } else {
            ui->configTextEdit->setReadOnly(false);
        }
    }
}

//保存XML文件的操作
void MainWindow::saveFileProcess(bool checked)
{
    Q_UNUSED(checked);
    QString PyStr = "XML文件路径: ";
    QString tmpFilePath = ui->configFilePathBrowser->toPlainText();
    //返回"xml文件路径: "的索引
    int inx=tmpFilePath.indexOf(PyStr) + 9;
    QString cfgFilePath = tmpFilePath.mid(inx);
    QString content = ui->configTextEdit->toPlainText();
    saveConfigFile(cfgFilePath, content);
}

bool MainWindow::saveConfigFile(QString filePath, const QString &content)
{
    QString tag = "saveConfigFile";
    XMLModifier modifier;
    //不修改模块配置文件
    if (modifier.isModuleConfig(filePath)) {
        return true;
    }
    //初始化变量
    if (filePath.length() == 0 && content.length() == 0) {
        return true;
    } else if (!(filePath.length() > 0 && content.length() > 0)) {
        QString infoStr = filePath + "config file get error";
        QMessageBox::information(NULL, tag, infoStr, QMessageBox::Yes, QMessageBox::Yes);
        return false;
    }

    QDomDocument dom("mydoc");
    if (!dom.setContent(content)) {
        QString infoStr = filePath + " xml format error";
        QMessageBox::information(NULL, tag, infoStr, QMessageBox::Yes, QMessageBox::Yes);
        return false;
    }

    QFile file(filePath);
    inWriting = true;
    if (!file.open( QIODevice::WriteOnly | QIODevice::Unbuffered)) {
        QString infoStr = filePath + "cannot write config file";
        QMessageBox::information(NULL, tag, infoStr, QMessageBox::Yes, QMessageBox::Yes);
        return false;
    }

    file.write(content.toStdString().c_str());
    if (file.flush()) {
        file.close();
        inWriting = false;
    } else {
        printf("ERROR: file %s is writing\n.......", filePath.toStdString().c_str());
    }

    return true;
}

void MainWindow::openConfigFile(const QModelIndex &index)
{
    QMap<QModelIndex, QString>::iterator iter = mTreeInfo.find(index);
    QString xmlFilePath = getAbsXMLFilePathFromDir(iter.value());

    XMLModifier modifier;
    if (modifier.checkXMLFormat(xmlFilePath)) {
        QFile file(xmlFilePath);
        if (!file.open(QIODevice::ReadOnly)) {
            qDebug() << "cannot read xml file" << xmlFilePath;
            return;
        }
        QString content = file.readAll();
        ui->configTextEdit->setText(content);
        file.close();
    }
}

void MainWindow::setConfigFilePath(const QModelIndex &index)
{
    QString xmlFileAtr = "测试模块";
    QMap<QModelIndex, QString>::iterator iter = mTreeInfo.find(index);

    if (iter == mTreeInfo.end() || iter.value().length() == 0) {
        printf("This item has not set config path");
        return;
    }
    //清空历史信息
    ui->configFilePathBrowser->clear();
    QString xmlCfgFilePath = getAbsXMLFilePathFromDir(iter.value());
    //考虑使用其他快速查找函数来替换
    //从xmlCfgFilePath 中解析
    std::string tyStr = xmlCfgFilePath.toStdString();
    if (tyStr.rfind("-F.xml") != std::string::npos)
        xmlFileAtr = "功能测试";
    else if(tyStr.rfind("-P.xml") != std::string::npos)
        xmlFileAtr = "性能测试";
    else if(tyStr.rfind("-S.xml") != std::string::npos)
        xmlFileAtr = "压力测试";
    ui->configFilePathBrowser->append("测试说明: " + xmlFileAtr);
    ui->configFilePathBrowser->append("XML文件路径: " + xmlCfgFilePath);

}

QString MainWindow::getDirname(const QString &path)
{
    QFileInfo fileInfo(path);
    if (!fileInfo.exists()) {
        qDebug() << "file " << path << "not exists";
        return QString("");
    }

    if (fileInfo.isDir()) {
        QDir dir(path);
        return dir.dirName();
    } else if (fileInfo.isFile()) {
        return fileInfo.absoluteDir().dirName();
    }
    return nullptr;
}


void MainWindow::setItemTypeLabel(const QModelIndex &index)
{


    QMap<QModelIndex, QString>::iterator iter = mTreeInfo.find(index);

    XMLModifier modifier;
    QString xmlFilePath = getAbsXMLFilePathFromDir(iter.value());
    //ui->typeLabel->setStyleSheet("QLabel{border:1px;border-radius:3px;}");  //*****************

    if (modifier.isModuleConfig(xmlFilePath)) {
        ui->typeLabel->setText(QString::fromUtf8("测试信息"));
    } else {
        ui->typeLabel->setText(QString::fromUtf8("测试信息"));
    }
}

void MainWindow::treeItemClicked(const QModelIndex &index)
{

    setItemTypeLabel(index);
    setConfigFilePath(index);
    changeConfigFile(index);
}

void MainWindow::treeItemChanged(QStandardItem *item)
{
    inChecking = true;
    if (item == nullptr) {
        return;
    }

    //如果条目是存在复选框的，那么就进行下面的操作
    if(item -> isCheckable()) {
    //获取当前的选择状态
        Qt::CheckState state = item -> checkState ();
    //如果条目是三态的，说明可以对子目录进行全选和全不选的设置
        if(item -> isTristate ()) {
           if(state != Qt::PartiallyChecked) {
    //当前是选中状态，需要对其子项目进行全选
               treeItem_checkAllChild(item, state == Qt::Checked ? true:false);
           }
        }
        else {
           treeItem_CheckChildChanged(item);
        }
    }

    inChecking = false;
}


/***********************************************
// 功能: 递归检查所有子item选择状态
// 参数: item 当前项目
// 参数: check true时为全选，false时全不选
//
************************************************/

void MainWindow::treeItem_checkAllChild(QStandardItem * item, bool check)
{
    if(item == nullptr) {
        return;
    }

    int rowCount = item->rowCount();
    for(int i = 0;i < rowCount; ++ i) {
        QStandardItem* childItems = item->child(i);
        treeItem_checkAllChild_recursion(childItems, check);
    }
}

void MainWindow::modifyCaseInModelConfigFile(QStandardItem * childItem, bool isAdd = true)
{
    QStandardItem *parentItem = childItem->parent();
    if (parentItem == nullptr) {
        return;
    }

    QMap<QModelIndex, QString>::iterator pIter = mTreeInfo.find(parentItem->index());
    QMap<QModelIndex, QString>::iterator cIter = mTreeInfo.find(childItem->index());

    QString xmlFilePath = getAbsXMLFilePathFromDir(pIter.value());
    QString childPath = cIter.value();
    QString childName = getDirname(childPath);
    QString childConfigPath = getAbsXMLFilePathFromDir(childPath);

    XMLModifier modifier;
    if (isAdd) {
        modifier.addModelXMLCase(xmlFilePath, childName, childConfigPath);
    } else {
        modifier.deleteModelXMLCase(xmlFilePath, childName, childConfigPath);
    }
}


void MainWindow::treeItem_CheckChildChanged(QStandardItem * item)
{
    if(nullptr == item) {
        return;
    }

    Qt::CheckState siblingState = checkSibling(item);
    QStandardItem * parentItem = item->parent();
    if(nullptr == parentItem) {
        return;
    }

    if(Qt::PartiallyChecked == siblingState) {
        if(parentItem->isCheckable() && parentItem->isTristate()) {
            parentItem->setCheckState(Qt::PartiallyChecked);
        }
    } else if(Qt::Checked == siblingState) {
        if(parentItem->isCheckable()) {
            parentItem->setCheckState(Qt::Checked);
        }
    } else {
        if(parentItem->isCheckable()) {
            parentItem->setCheckState(Qt::Unchecked);
        }
    }

    bool check = item->checkState() == Qt::Unchecked ? false : true;
    modifyCaseInModelConfigFile(item, check);

    treeItem_CheckChildChanged(parentItem);
}

void MainWindow::treeItem_checkAllChild_recursion(QStandardItem * item, bool check)
{
    if(item == nullptr) {
        return;
    }

    int rowCount = item->rowCount();
    for(int i = 0; i < rowCount; ++ i) {
        QStandardItem* childItems = item->child(i);

        treeItem_checkAllChild_recursion(childItems,check);
    }

    if(item->isCheckable()) {
        item->setCheckState(check ? Qt::Checked : Qt::Unchecked);
    }
    modifyCaseInModelConfigFile(item, check);

}



/***********************************************
//
// 功能: 测量兄弟节点的情况，如果都选中返回Qt::Checked，都不选中Qt::Unchecked,不完全选中返回Qt::PartiallyChecked
// 参数: item
// 返回值: 如果都选中返回Qt::Checked，都不选中Qt::Unchecked,不完全选中返回Qt::PartiallyChecked
//
************************************************/
Qt::CheckState MainWindow::checkSibling(QStandardItem * item)
{
    //先通过父节点获取兄弟节点
    QStandardItem * parent = item->parent();
    if(nullptr == parent)
        return item->checkState();
    int brotherCount = parent->rowCount();
    int checkedCount(0),unCheckedCount(0);
    Qt::CheckState state;
    for(int i=0;i<brotherCount;++i)
    {
        QStandardItem* siblingItem = parent->child(i);
        state = siblingItem->checkState();
        if(Qt::PartiallyChecked == state)
            return Qt::PartiallyChecked;
        else if(Qt::Unchecked == state)
            ++unCheckedCount;
        else
            ++checkedCount;
        if(checkedCount>0 && unCheckedCount>0)
            return Qt::PartiallyChecked;
    }
    if(unCheckedCount>0)
        return Qt::Unchecked;
    return Qt::Checked;
}


//初始化测试用例树
void MainWindow::initializeCaseTree(QString rootPath)
{
    // 创造树头
    folderModel = new QStandardItemModel(ui->treeView);
    folderModel->setHorizontalHeaderLabels(QStringList()<<QString::fromUtf8("测试用例目录"));

    // 测试rootPath 是否存在
    QString rootDirName = getDirname(rootPath);
    if (rootDirName.length() == 0) {
        return;
    }


    QStandardItem *rootItem = new QStandardItem(rootDirName);
    initializeItemAttribute(rootItem);
    folderModel->appendRow(rootItem);

    TreeNode treeNode;
    createTreeNode(rootPath, rootItem, treeNode);
    addTreeItemInfo(treeNode);

    //广度遍历文件夹树
    while(folderTreeList.size() > 0) {
        QList<TreeNode>::iterator treeIter = folderTreeList.begin();

        QStandardItem *parentItem = treeIter->item;
        QString parentDirPath = treeIter->absPath;

        // 追加一个全局的item map
        QDir dir(parentDirPath);
        QFileInfoList dirList = dir.entryInfoList();

        //在父目录下添加子目录
        QMap<QString, TreeNode> inputMap;
        QList<TreeNode> sortedList;
        for(QFileInfoList::iterator iter = dirList.begin(); iter != dirList.end(); ++ iter) {
            if(!iter->isDir()) {
                continue;
            }

            QString dirPath = iter->absoluteFilePath();
            if(QString::compare(dirPath, parentDirPath) == 0 || dirPath.length() < parentDirPath.length()) {
                continue;
            }

            QString dirName = getDirname(dirPath);
            if (omitDirectory(dirName)) {
                continue;
            }

            QStandardItem *childItem = new QStandardItem(dirName);
            initializeItemAttribute(childItem);
            TreeNode node;
            createTreeNode(dirPath, childItem, node);
            inputMap.insert(dirName, node);
        }

        sortNodeList(inputMap, sortedList);

        for (QList<TreeNode>::iterator iter = sortedList.begin(); iter != sortedList.end(); ++ iter) {
            parentItem->appendRow(iter->item);
            addTreeItemInfo(*iter);
        }

        //设置三态 从三态转化为2态
        if (!parentItem->hasChildren()) {
            parentItem->setTristate(false);
        }
        //移除父节点
        folderTreeList.removeFirst();
    }

    ui->treeView->setModel(folderModel);
}

void MainWindow::initializeItemCheckState()
{
    QList<TreeNode>::iterator treeIter =  breathInfoList.end();
    treeIter --;
    for (; ; treeIter --) {
        QString path = treeIter->absPath;
        setItemCheckedStatus(treeIter->item, treeIter->absPath);

        if (treeIter == breathInfoList.begin()) {
            break;
        }
    }
}

void MainWindow::setItemCheckedStatus(QStandardItem *item, QString cfgDirPath)
{
    Q_UNUSED(cfgDirPath)
    XMLModifier modifier;
    if (item->hasChildren()) {
        int uncheckCount = 0;
        int checkCount = 0;
        int childCount = item->rowCount();
        for (int i = 0; i < childCount; ++ i) {
            Qt::CheckState state = item->child(i)->checkState();
            if (state == Qt::Unchecked) {
                ++ uncheckCount;
            } else if (state == Qt::Checked) {
                ++ checkCount;
            }
        }


        if (uncheckCount == childCount) {
            item->setCheckState(Qt::Unchecked);
        } else if (checkCount == childCount) {
            item->setCheckState(Qt::Checked);
        } else {
            item->setCheckState(Qt::PartiallyChecked);
        }
    } else {
        QStandardItem * parentItem = item->parent();
        QMap<QModelIndex, QString>::iterator pIter = mTreeInfo.find(parentItem->index());
        QString parentDirPath = pIter.value();
        QString parentFilePath = getAbsXMLFilePathFromDir(parentDirPath);
        QStringList nameList = modifier.getCaseNameList(parentFilePath);
        if (nameList.contains(item->text())) {
            item->setCheckState(Qt::Checked);
        } else {
            item->setCheckState(Qt::Unchecked);
        }
    }
}

//或略框架自带的文件夹
bool MainWindow::omitDirectory(QString dirname)
{
    QStringList omitDirList;
    omitDirList << ("screenshot")
                << ("resource")
                << ("result")
                << ("log")
                << ("public")
                << ("tools");

    if (omitDirList.contains(dirname)) {
        return true;
    } else {
        return false;
    }
}

void MainWindow::initializeItemAttribute(QStandardItem *item)
{
    item->setCheckable(true);
    item->setTristate(true);
    item->setEditable(false);
}

void MainWindow::createTreeNode(QString absPath, QStandardItem *item, TreeNode &treeNode)
{
    treeNode.absPath = absPath;
    treeNode.item = item;
}

//增加树节点信息--设置基本属性
void MainWindow::addTreeItemInfo(TreeNode node)
{

    folderTreeList.append(node);
    breathInfoList.append(node);
    mTreeInfo.insert(node.item->index(), node.absPath);
}


void MainWindow::sortNodeList(QMap<QString, TreeNode> sortInputList, QList<TreeNode> &sortOutputList)
{

    QMap<int, TreeNode> resultMap;

    for (QMap<QString, TreeNode>::iterator iter = sortInputList.begin(); iter != sortInputList.end(); ++ iter) {
        QString dirName = iter.key();
        //默认情况下只有一个"-"在case 的名称中
        int numEndIndex =  dirName.indexOf("-");
        int numBeginIndex = dirName.lastIndexOf(".", numEndIndex);
        QString numberStr = dirName.mid(numBeginIndex+1, numEndIndex-numBeginIndex-1);

        int number = numberStr.toInt();
        resultMap.insert(number, iter.value());
    }

    for (QMap<int, TreeNode>::iterator iter = resultMap.begin(); iter != resultMap.end(); iter ++) {

            sortOutputList.append(iter.value());
    }
}

MainWindow::~MainWindow()
{
    delete ui;
}
