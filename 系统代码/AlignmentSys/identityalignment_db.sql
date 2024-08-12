/*
 Navicat Premium Data Transfer

 Source Server         : addrs
 Source Server Type    : MySQL
 Source Server Version : 80026
 Source Host           : localhost:3306
 Source Schema         : identityalignment_db

 Target Server Type    : MySQL
 Target Server Version : 80026
 File Encoding         : 65001

 Date: 23/05/2024 06:06:43
*/

SET NAMES utf8mb4;
SET FOREIGN_KEY_CHECKS = 0;

-- ----------------------------
-- Table structure for clientinfo
-- ----------------------------
DROP TABLE IF EXISTS `clientinfo`;
CREATE TABLE `clientinfo`  (
  `client_id` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `client_name` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `client_pwd` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `client_email` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `client_phone` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  PRIMARY KEY (`client_id`) USING BTREE
) ENGINE = InnoDB CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Table structure for entity
-- ----------------------------
DROP TABLE IF EXISTS `entity`;
CREATE TABLE `entity`  (
  `TID` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `track_info` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL,
  PRIMARY KEY (`TID`) USING BTREE
) ENGINE = InnoDB CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Table structure for identityalignment
-- ----------------------------
DROP TABLE IF EXISTS `identityalignment`;
CREATE TABLE `identityalignment`  (
  `AlignmentID` int NOT NULL AUTO_INCREMENT,
  `SourceUserID` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL,
  `TargetUserID` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL,
  `info` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL,
  PRIMARY KEY (`AlignmentID`) USING BTREE,
  UNIQUE INDEX `unique_combination`(`SourceUserID`, `TargetUserID`) USING BTREE,
  INDEX `TargetUserID`(`TargetUserID`) USING BTREE,
  CONSTRAINT `identityalignment_ibfk_1` FOREIGN KEY (`SourceUserID`) REFERENCES `websiteuser` (`webuser_id`) ON DELETE RESTRICT ON UPDATE RESTRICT,
  CONSTRAINT `identityalignment_ibfk_2` FOREIGN KEY (`TargetUserID`) REFERENCES `websiteuser` (`webuser_id`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE = InnoDB AUTO_INCREMENT = 41 CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Table structure for ownerrelation
-- ----------------------------
DROP TABLE IF EXISTS `ownerrelation`;
CREATE TABLE `ownerrelation`  (
  `ORelationID` int NOT NULL AUTO_INCREMENT,
  `OuserID` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL,
  `Oaddr` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL,
  PRIMARY KEY (`ORelationID`) USING BTREE,
  INDEX `Oaddr`(`Oaddr`) USING BTREE,
  INDEX `OuserID`(`OuserID`) USING BTREE,
  CONSTRAINT `ownerrelation_ibfk_1` FOREIGN KEY (`Oaddr`) REFERENCES `suspiciousbitcoinaddress` (`addr`) ON DELETE RESTRICT ON UPDATE RESTRICT,
  CONSTRAINT `ownerrelation_ibfk_2` FOREIGN KEY (`OuserID`) REFERENCES `websiteuser` (`webuser_id`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE = InnoDB AUTO_INCREMENT = 9 CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Table structure for suspiciousbitcoinaddress
-- ----------------------------
DROP TABLE IF EXISTS `suspiciousbitcoinaddress`;
CREATE TABLE `suspiciousbitcoinaddress`  (
  `addr` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `criminal_type` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL,
  `tagsource` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL,
  `addr_type` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL,
  PRIMARY KEY (`addr`) USING BTREE
) ENGINE = InnoDB CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Table structure for trackingdata
-- ----------------------------
DROP TABLE IF EXISTS `trackingdata`;
CREATE TABLE `trackingdata`  (
  `actionid` int NOT NULL AUTO_INCREMENT,
  `actiontime` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL,
  `actiontype` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL,
  `domainid` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL,
  `trackingid` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL,
  PRIMARY KEY (`actionid`) USING BTREE,
  INDEX `domainid`(`domainid`) USING BTREE,
  INDEX `trackingid`(`trackingid`) USING BTREE,
  CONSTRAINT `trackingdata_ibfk_2` FOREIGN KEY (`domainid`) REFERENCES `websiteinfo` (`web_id`) ON DELETE RESTRICT ON UPDATE RESTRICT,
  CONSTRAINT `trackingdata_ibfk_3` FOREIGN KEY (`trackingid`) REFERENCES `entity` (`TID`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE = InnoDB AUTO_INCREMENT = 216689 CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Table structure for websiteinfo
-- ----------------------------
DROP TABLE IF EXISTS `websiteinfo`;
CREATE TABLE `websiteinfo`  (
  `web_id` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `web_name` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL,
  `web_link` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL,
  `web_info` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL,
  PRIMARY KEY (`web_id`) USING BTREE
) ENGINE = InnoDB CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Table structure for websitepostdata
-- ----------------------------
DROP TABLE IF EXISTS `websitepostdata`;
CREATE TABLE `websitepostdata`  (
  `post_id` int NOT NULL AUTO_INCREMENT,
  `user_id` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL,
  `post_time` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL,
  `post_domain` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL,
  PRIMARY KEY (`post_id`) USING BTREE,
  INDEX `post_domain`(`post_domain`) USING BTREE,
  INDEX `fk_user_id`(`user_id`) USING BTREE,
  CONSTRAINT `fk_user_id` FOREIGN KEY (`user_id`) REFERENCES `websiteuser` (`webuser_id`) ON DELETE RESTRICT ON UPDATE RESTRICT,
  CONSTRAINT `websitepostdata_ibfk_2` FOREIGN KEY (`post_domain`) REFERENCES `websiteinfo` (`web_id`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE = InnoDB AUTO_INCREMENT = 416773 CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Table structure for websiteuser
-- ----------------------------
DROP TABLE IF EXISTS `websiteuser`;
CREATE TABLE `websiteuser`  (
  `webuser_id` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `webuser_name` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL,
  `webuser_link` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL,
  `webid` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL,
  PRIMARY KEY (`webuser_id`) USING BTREE,
  INDEX `webid`(`webid`) USING BTREE,
  CONSTRAINT `websiteuser_ibfk_1` FOREIGN KEY (`webid`) REFERENCES `websiteinfo` (`web_id`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE = InnoDB CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = Dynamic;

SET FOREIGN_KEY_CHECKS = 1;
