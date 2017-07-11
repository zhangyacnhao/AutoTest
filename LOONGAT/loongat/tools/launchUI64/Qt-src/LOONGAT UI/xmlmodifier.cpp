#include "xmlmodifier.h"
#include <QTextStream>

//XMLModifier 构造函数
XMLModifier::XMLModifier()
{

}

bool XMLModifier::inWriting = false;


//打开XML文件做一些检查
bool XMLModifier::openXMLFile(const QString &filePath, QDomDocument &dom)
{
    if (filePath.isEmpty()){
        return false;
    }

    QFile file(filePath);
    if (!file.open(QIODevice::ReadOnly)) {
        qDebug() << "openXMLFile: cannot read xml file" << filePath;
        return false;
    }

    if (!dom.setContent(&file)) {
        file.close();
        qDebug() << "cannot set xml file content" << filePath;
        return false;
    }

    file.close();
    return true;
}

//勾选添加一个case
bool XMLModifier::addModelXMLCase(const QString &filePath, const QString &caseName, const QString &casePath)
{
    QDomDocument dom("mydoc");  

    if (!openXMLFile(filePath, dom)) {
        qDebug() << "addModelXMLCase : cannot open xml file" << filePath;
        return false;
    }

    QDomNodeList dataList = dom.elementsByTagName("data");
    QDomElement dataEle = dataList.at(0).toElement();

    QString caseLabel = "module";
    if (isModuleConfig(filePath) && !isModuleConfig(casePath)) {
        caseLabel = "case";
    }

    QDomNodeList caseList = dom.elementsByTagName(caseLabel);
    QDomElement addChildEle = caseList.at(0).toElement();


    if (findCase(caseList, caseName, addChildEle)) {

        return false;
    }

    QDomElement caseAppend = dom.createElement(caseLabel);
    QDomText text = dom.createTextNode(caseName);
    caseAppend.appendChild(text);
    QDomAttr attr = dom.createAttribute("type");
    attr.setNodeValue("string");
    caseAppend.setAttributeNode(attr);

    dataEle.appendChild(caseAppend);

    return saveXMLFile(filePath, dom);
}


//查找case
bool XMLModifier::findCase(const QDomNodeList &caseList, const QString &caseName,QDomElement &findEle)
{
    bool findFlag = false;
    for (int i = 0; i < caseList.size(); i++) {
        QDomElement caseEle = caseList.at(i).toElement();
        QString caseValue = caseEle.firstChild().nodeValue();
        if (QString::compare(caseValue, caseName) == 0) {
            findEle = caseEle;
            findFlag = true;
            break;
        }
    }

    return findFlag;
}

//从Case树上删除一个节点
bool XMLModifier::deleteModelXMLCase(const QString &filePath, const QString &caseName, const QString &casePath)
{
    //创建根节点
    QDomDocument dom("mydoc");

    if (!openXMLFile(filePath, dom)) {
        qDebug() << "deleteModelXMLCase : cannot open xml file" << filePath;
        return false;
    }

    QDomNodeList dataList = dom.elementsByTagName("data");
    QDomElement dataEle = dataList.at(0).toElement();

    QString caseLabel = "module";
    //检查filePath是否是一个模块
    if (isModuleConfig(filePath) && !isModuleConfig(casePath)) {
        caseLabel = "case";
    }



    QDomNodeList caseList = dom.elementsByTagName(caseLabel);
    QDomElement deleteChildEle = caseList.at(0).toElement();
    
    if (findCase(caseList, caseName, deleteChildEle)) {

        dataEle.removeChild(deleteChildEle);
    } else {
        return false;
    }

    return saveXMLFile(filePath, dom);
}

//保存XML文件的修改
bool XMLModifier::saveXMLFile(const QString &filePath, const QDomDocument &dom)
{
    QFile file(filePath);
    inWriting = true;
    if(!file.open(QIODevice::WriteOnly | QIODevice::Unbuffered)) {
        qDebug() << "open for add error!";
    }

    QTextStream out(&file);

    dom.save(out, 4);
    if (file.flush()) {
        file.close();
    }

    inWriting = false;
    return true;
}

//检查XML文件的格式是否合法
bool XMLModifier::checkXMLFormat(const QString &filePath)
{
    QDomDocument doc("mydoc");

    QFile file(filePath);
    if (!file.open(QIODevice::ReadOnly))
        return false;

    if (!doc.setContent(&file)) {
        file.close();
        return false;
    }

    file.close();
    return true;
}

//获取选中的cse名称列表
QStringList XMLModifier::getCaseNameList(const QString &filePath)
{
    QDomDocument dom("mydoc");
    QStringList caseNameList;
    caseNameList.clear();

    if (!openXMLFile(filePath, dom)) {
        qDebug() << "getCaseNameList : cannot open xml file" << filePath;
        return caseNameList;
    }

    QDomNodeList caseList = dom.elementsByTagName("case");
    if (caseList.size() == 0) {
        caseList = dom.elementsByTagName("module");
    }

    for (int i = 0; i < caseList.size(); ++ i) {
        caseNameList.append(caseList.at(i).toElement().firstChild().nodeValue());
    }

    return caseNameList;
}

//检查xmlFilePath 是否是一个模块
bool XMLModifier::isModuleConfig(const QString &xmlFilePath)
{
    QDomDocument dom("mydoc");
    QStringList caseNameList;
    caseNameList.clear();
    if (!openXMLFile(xmlFilePath, dom)) {
        return false;
    }

    QDomNodeList modulenameList = dom.elementsByTagName("modulename");
    if (modulenameList.size() != 0) {
        return true;
    }

    return false;
}
