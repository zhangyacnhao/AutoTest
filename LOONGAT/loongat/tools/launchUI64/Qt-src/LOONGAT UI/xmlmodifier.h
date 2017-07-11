#ifndef XMLMODIFIER_H
#define XMLMODIFIER_H

#include <QDebug>

#include <QtXml/QDomDocument>
#include <QFile>
#include <QStringList>

class XMLModifier
{
public:
    XMLModifier();
    bool openXMLFile(const QString &filePath, QDomDocument &dom);
    bool addModelXMLCase(const QString &filePath, const QString &caseName, const QString &casePath);
    bool deleteModelXMLCase(const QString &filePath, const QString &caseName, const QString &casePath);
    bool saveXMLFile(const QString &filePath, const QDomDocument &dom);
    bool checkXMLFormat(const QString &filePath);
    bool findCase(const QDomNodeList &caseList, const QString &caseName,QDomElement &findEle);
    QStringList getCaseNameList(const QString &filePath);
    bool isModuleConfig(const QString &xmlFilePath);
    static bool inWriting;

private:
};

#endif // XMLMODIFIER_H
