# -*- coding:utf-8 -*-
# @FileName  :database_sql.sql.py
# @Time      :2023/2/14 17:00
# @Author    : yuhaiping

create database ssss charset=utf8;CREATE table indo(
    id int unsigned PRIMARY KEY auto_increment not NULL ,
    title varchar(64),
    author varchar(64),
    hits varchar(20),
    state varchar(20),
    introd TEXT,
    url varchar(128),
    c_time DATETIME
)

CREATE TABLE contents(
'id' int(10) NOT NULL,
'indo_id' int(10) NOT NULL,
'title' varchar(64) NULL,
'content' mediumtext NULL,
'order1' varchar(20) NULL,
'c_time' datetime NOT NULL,
'c_url' varchar(128) NULL,
PRIMARY KEY ('id'),
FOREIGN KEY ('indo_id') REFERENCES 'ssss'.'indo' ('id')
);