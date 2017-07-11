#include "helpinfo.h"
#include "ui_helpinfo.h"

helpInfo::helpInfo(QWidget *parent) :
    QDialog(parent),
    ui(new Ui::helpInfo)
{
    ui->setupUi(this);
    setStyle();
}

/*
 *LOONGAT help show
 */
void helpInfo::setStyle(void)
{
    Qt::WindowFlags flags=0;
    flags |= Qt::WindowMinimizeButtonHint;
    flags |= Qt::WindowMaximizeButtonHint;
    //背景色为白色
    //ui->logoLabel->setStyleSheet("backgroud-color:white");
    ui->authorInfo->setOpenExternalLinks(true);
    ui->homeInfo->setOpenExternalLinks(true);
    //Ok button
    ui->oKButton->setFocus();
    ui->oKButton->setShortcut(Qt::Key_Enter);
    //设置固定大小
    setWindowFlags(flags);
    setFixedSize(417,392);

}


helpInfo::~helpInfo()
{
    delete ui;
}
