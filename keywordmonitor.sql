-- phpMyAdmin SQL Dump
-- version 3.5.1
-- http://www.phpmyadmin.net
--
-- 主机: localhost
-- 生成日期: 2014 年 07 月 30 日 01:47
-- 服务器版本: 5.0.51a-community-nt-log
-- PHP 版本: 5.2.4

SET SQL_MODE="NO_AUTO_VALUE_ON_ZERO";
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;

--
-- 数据库: `keywordmonitor`
--

-- --------------------------------------------------------

--
-- 表的结构 `keyword`
--

CREATE TABLE IF NOT EXISTS `keyword` (
  `id` int(20) NOT NULL auto_increment,
  `keyword` varchar(200) NOT NULL,
  `hospital` varchar(50) NOT NULL,
  `uptime` varchar(50) NOT NULL,
  PRIMARY KEY  (`id`)
) ENGINE=InnoDB  DEFAULT CHARSET=utf8 AUTO_INCREMENT=421 ;

-- --------------------------------------------------------

--
-- 表的结构 `platform`
--

CREATE TABLE IF NOT EXISTS `platform` (
  `id` int(20) NOT NULL auto_increment,
  `domain` varchar(100) NOT NULL,
  `other` varchar(100) NOT NULL default 'no',
  PRIMARY KEY  (`id`)
) ENGINE=InnoDB  DEFAULT CHARSET=utf8 AUTO_INCREMENT=291 ;

-- --------------------------------------------------------

--
-- 表的结构 `result`
--

CREATE TABLE IF NOT EXISTS `result` (
  `id` int(20) NOT NULL auto_increment,
  `se` varchar(20) NOT NULL,
  `keyword` varchar(100) NOT NULL,
  `domain` varchar(100) NOT NULL,
  `url` text NOT NULL,
  `rank` varchar(10) NOT NULL,
  `snap` varchar(30) NOT NULL,
  `hospital` varchar(40) NOT NULL,
  `uptime` varchar(30) NOT NULL,
  `classes` varchar(40) NOT NULL default 'no',
  `classtime` varchar(30) NOT NULL default '1999-00-00',
  PRIMARY KEY  (`id`)
) ENGINE=InnoDB  DEFAULT CHARSET=utf8 AUTO_INCREMENT=16989 ;

-- --------------------------------------------------------

--
-- 表的结构 `searchresult`
--

CREATE TABLE IF NOT EXISTS `searchresult` (
  `id` int(20) NOT NULL auto_increment,
  `setype` varchar(30) NOT NULL,
  `hospital` varchar(20) NOT NULL,
  `keyword` varchar(200) NOT NULL,
  `ranknum` varchar(10) NOT NULL,
  PRIMARY KEY  (`id`)
) ENGINE=InnoDB  DEFAULT CHARSET=utf8 AUTO_INCREMENT=8899 ;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
