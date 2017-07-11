#ifndef HELPINFO_H
#define HELPINFO_H

#include <QDialog>

namespace Ui {
class helpInfo;
}

class helpInfo : public QDialog
{
    Q_OBJECT

public:
    explicit helpInfo(QWidget *parent = 0);
    ~helpInfo();

private:
    Ui::helpInfo *ui;
    void setStyle(void); //设置界面样式
};

#endif // HELPINFO_H
