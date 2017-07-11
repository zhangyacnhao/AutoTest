#-------------------------------------------------
#
# Project created by QtCreator 2015-05-04T13:43:46
#
#-------------------------------------------------

QT       += core gui xml

greaterThan(QT_MAJOR_VERSION, 4): QT += widgets

TARGET = VisualConfig
TEMPLATE = app

SOURCES += main.cpp\
        mainwindow.cpp \
    xmlmodifier.cpp \
    helpinfo.cpp

HEADERS  += mainwindow.h \
    xmlmodifier.h \
    helpinfo.h

FORMS    += mainwindow.ui \
    helpinfo.ui

CONFIG+=c++11

RESOURCES += \
    logo.qrc
