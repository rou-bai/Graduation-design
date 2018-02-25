/*
 Navicat Premium Data Transfer

 Source Server         : root
 Source Server Type    : MySQL
 Source Server Version : 50721
 Source Host           : localhost:3306
 Source Schema         : bis1

 Target Server Type    : MySQL
 Target Server Version : 50721
 File Encoding         : 65001

 Date: 22/02/2018 15:28:40
*/

SET NAMES utf8mb4;
SET FOREIGN_KEY_CHECKS = 0;

-- ----------------------------
-- Table structure for car
-- ----------------------------
DROP TABLE IF EXISTS `car`;
CREATE TABLE `car`  (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `car_number` varchar(64) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL,
  `car_type` varchar(64) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL,
  `car_subject` varchar(64) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL,
  `car_teacher_id` int(11) NULL DEFAULT NULL,
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 21 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_general_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of car
-- ----------------------------
INSERT INTO `car` VALUES (1, '川BF541D', '大众', '科目二', NULL);
INSERT INTO `car` VALUES (2, '川BA85498', '大众', '科目二', NULL);
INSERT INTO `car` VALUES (3, '川BWD84S', '大众', '科目二', 1);
INSERT INTO `car` VALUES (4, '川B78Q54', '大众', '科目二', 3);
INSERT INTO `car` VALUES (5, '川B86683', '大众', '科目二', NULL);
INSERT INTO `car` VALUES (6, '川B12WS3', '大众', '科目二', NULL);
INSERT INTO `car` VALUES (7, '川B3323W', '大众', '科目二', NULL);
INSERT INTO `car` VALUES (8, '川B6676X', '大众', '科目二', NULL);
INSERT INTO `car` VALUES (9, '川BC512A', '大众', '科目二', NULL);
INSERT INTO `car` VALUES (10, '川B886CC', '大众', '科目二', 2);
INSERT INTO `car` VALUES (11, '川B89SD5', '大众', '科目三', 2);
INSERT INTO `car` VALUES (12, '川B5885A', '大众', '科目三', NULL);
INSERT INTO `car` VALUES (13, '川B1445Y', '大众', '科目三', NULL);
INSERT INTO `car` VALUES (14, '川BD78T7', '大众', '科目三', NULL);
INSERT INTO `car` VALUES (15, '川B111WS', '大众', '科目三', NULL);
INSERT INTO `car` VALUES (16, '川B7767Y', '大众', '科目三', 1);
INSERT INTO `car` VALUES (17, '川B78JG5', '大众', '科目三', NULL);
INSERT INTO `car` VALUES (18, '川BT6544', '大众', '科目三', NULL);
INSERT INTO `car` VALUES (19, '川B54R45', '大众', '科目三', NULL);
INSERT INTO `car` VALUES (20, '川BF99871', '大众', '科目三', NULL);

-- ----------------------------
-- Table structure for class
-- ----------------------------
DROP TABLE IF EXISTS `class`;
CREATE TABLE `class`  (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `class_time` datetime(0) NULL DEFAULT NULL,
  `class_limit_people` int(11) NULL DEFAULT NULL,
  `class_am` varchar(64) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL,
  `class_pm` varchar(64) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL,
  `class_teacher_id` int(11) NULL DEFAULT NULL,
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 45 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_general_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of class
-- ----------------------------
INSERT INTO `class` VALUES (1, '2018-01-29 00:00:00', 8, '科目二', NULL, 2);
INSERT INTO `class` VALUES (2, '2018-01-30 00:00:00', 8, '科目二', NULL, 2);
INSERT INTO `class` VALUES (3, '2018-01-31 00:00:00', 8, '科目二', NULL, 2);
INSERT INTO `class` VALUES (4, '2018-02-01 00:00:00', 8, '科目二', NULL, 2);
INSERT INTO `class` VALUES (5, '2018-02-02 00:00:00', 8, '科目二', NULL, 2);
INSERT INTO `class` VALUES (6, '2018-02-03 00:00:00', 8, '科目二', NULL, 2);
INSERT INTO `class` VALUES (7, '2018-02-04 00:00:00', 8, '科目二', NULL, 2);
INSERT INTO `class` VALUES (8, '2018-02-04 00:00:00', 8, '科目二', NULL, 2);
INSERT INTO `class` VALUES (9, '2018-01-29 00:00:00', 8, NULL, '科目二', 2);
INSERT INTO `class` VALUES (10, '2018-01-30 00:00:00', 8, NULL, '科目二', 2);
INSERT INTO `class` VALUES (11, '2018-01-31 00:00:00', 8, NULL, '科目二', 2);
INSERT INTO `class` VALUES (12, '2018-02-01 00:00:00', 8, NULL, '科目二', 2);
INSERT INTO `class` VALUES (13, '2018-02-02 00:00:00', 8, NULL, '科目二', 2);
INSERT INTO `class` VALUES (14, '2018-02-03 00:00:00', 8, NULL, '科目二', 2);
INSERT INTO `class` VALUES (15, '2018-02-04 00:00:00', 8, NULL, '科目二', 2);
INSERT INTO `class` VALUES (16, '2018-01-29 00:00:00', 8, '科目二', NULL, 1);
INSERT INTO `class` VALUES (17, '2018-01-29 00:00:00', 8, NULL, '科目三', 1);
INSERT INTO `class` VALUES (18, '2018-01-30 00:00:00', 8, '科目二', NULL, 1);
INSERT INTO `class` VALUES (19, '2018-01-30 00:00:00', 8, NULL, '科目三', 1);
INSERT INTO `class` VALUES (20, '2018-01-31 00:00:00', 8, '科目二', NULL, 1);
INSERT INTO `class` VALUES (21, '2018-01-31 00:00:00', 7, NULL, '科目三', 1);
INSERT INTO `class` VALUES (22, '2018-02-01 00:00:00', 8, '科目二', NULL, 1);
INSERT INTO `class` VALUES (23, '2018-02-01 00:00:00', 7, NULL, '科目三', 1);
INSERT INTO `class` VALUES (24, '2018-02-02 00:00:00', 8, '科目二', NULL, 1);
INSERT INTO `class` VALUES (25, '2018-02-02 00:00:00', 7, NULL, '科目三', 1);
INSERT INTO `class` VALUES (26, '2018-02-03 00:00:00', 8, '科目二', NULL, 1);
INSERT INTO `class` VALUES (27, '2018-02-03 00:00:00', 7, NULL, '科目三', 1);
INSERT INTO `class` VALUES (28, '2018-02-04 00:00:00', 8, '科目二', NULL, 1);
INSERT INTO `class` VALUES (29, '2018-02-04 00:00:00', 8, NULL, '科目三', 1);
INSERT INTO `class` VALUES (31, '2018-01-29 00:00:00', 8, '科目三', NULL, 10);
INSERT INTO `class` VALUES (32, '2018-01-29 00:00:00', 8, NULL, '科目三', 10);
INSERT INTO `class` VALUES (33, '2018-01-30 00:00:00', 8, '科目三', NULL, 10);
INSERT INTO `class` VALUES (34, '2018-01-30 00:00:00', 8, NULL, '科目三', 10);
INSERT INTO `class` VALUES (35, '2018-01-31 00:00:00', 8, '科目三', NULL, 10);
INSERT INTO `class` VALUES (36, '2018-01-31 00:00:00', 8, NULL, '科目三', 10);
INSERT INTO `class` VALUES (37, '2018-02-01 00:00:00', 8, '科目三', NULL, 10);
INSERT INTO `class` VALUES (38, '2018-02-01 00:00:00', 8, NULL, '科目三', 10);
INSERT INTO `class` VALUES (39, '2018-02-02 00:00:00', 8, '科目三', NULL, 10);
INSERT INTO `class` VALUES (40, '2018-02-02 00:00:00', 8, NULL, '科目三', 10);
INSERT INTO `class` VALUES (41, '2018-02-03 00:00:00', 8, '科目三', NULL, 10);
INSERT INTO `class` VALUES (42, '2018-02-03 00:00:00', 8, NULL, '科目三', 10);
INSERT INTO `class` VALUES (43, '2018-02-04 00:00:00', 8, '科目三', NULL, 10);
INSERT INTO `class` VALUES (44, '2018-02-04 00:00:00', 8, NULL, '科目三', 10);

-- ----------------------------
-- Table structure for role
-- ----------------------------
DROP TABLE IF EXISTS `role`;
CREATE TABLE `role`  (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(128) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL,
  `description` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  UNIQUE INDEX `name`(`name`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 4 CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of role
-- ----------------------------
INSERT INTO `role` VALUES (1, 'Student', '学员');
INSERT INTO `role` VALUES (2, 'Teacher', '教练');
INSERT INTO `role` VALUES (3, 'Admin', '管理员');

-- ----------------------------
-- Table structure for roles_users
-- ----------------------------
DROP TABLE IF EXISTS `roles_users`;
CREATE TABLE `roles_users`  (
  `user_id` int(11) NULL DEFAULT NULL,
  `role_id` int(11) NULL DEFAULT NULL,
  INDEX `user_id`(`user_id`) USING BTREE,
  INDEX `role_id`(`role_id`) USING BTREE,
  CONSTRAINT `roles_users_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `user` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT,
  CONSTRAINT `roles_users_ibfk_2` FOREIGN KEY (`role_id`) REFERENCES `role` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE = InnoDB CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of roles_users
-- ----------------------------
INSERT INTO `roles_users` VALUES (1, 3);
INSERT INTO `roles_users` VALUES (2, 2);
INSERT INTO `roles_users` VALUES (3, 1);
INSERT INTO `roles_users` VALUES (4, 2);
INSERT INTO `roles_users` VALUES (5, 2);
INSERT INTO `roles_users` VALUES (6, 2);
INSERT INTO `roles_users` VALUES (7, 2);
INSERT INTO `roles_users` VALUES (8, 2);
INSERT INTO `roles_users` VALUES (9, 2);
INSERT INTO `roles_users` VALUES (10, 2);
INSERT INTO `roles_users` VALUES (11, 2);
INSERT INTO `roles_users` VALUES (12, 2);
INSERT INTO `roles_users` VALUES (13, 1);
INSERT INTO `roles_users` VALUES (14, 1);
INSERT INTO `roles_users` VALUES (15, 1);
INSERT INTO `roles_users` VALUES (16, 1);
INSERT INTO `roles_users` VALUES (17, 1);
INSERT INTO `roles_users` VALUES (18, 1);
INSERT INTO `roles_users` VALUES (19, 1);
INSERT INTO `roles_users` VALUES (20, 1);

-- ----------------------------
-- Table structure for student
-- ----------------------------
DROP TABLE IF EXISTS `student`;
CREATE TABLE `student`  (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `s_subject` varchar(128) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL,
  `s_u_id` int(11) NULL DEFAULT NULL,
  `s_teacher_id` int(11) NULL DEFAULT NULL,
  `s_test_2_id` int(11) NULL DEFAULT NULL,
  `s_am_1_id` int(11) NULL DEFAULT NULL,
  `s_am_2_id` int(11) NULL DEFAULT NULL,
  `s_am_3_id` int(11) NULL DEFAULT NULL,
  `s_am_4_id` int(11) NULL DEFAULT NULL,
  `s_am_5_id` int(11) NULL DEFAULT NULL,
  `s_am_6_id` int(11) NULL DEFAULT NULL,
  `s_am_7_id` int(11) NULL DEFAULT NULL,
  `s_pm_1_id` int(11) NULL DEFAULT NULL,
  `s_pm_2_id` int(11) NULL DEFAULT NULL,
  `s_pm_3_id` int(11) NULL DEFAULT NULL,
  `s_pm_4_id` int(11) NULL DEFAULT NULL,
  `s_pm_5_id` int(11) NULL DEFAULT NULL,
  `s_pm_6_id` int(11) NULL DEFAULT NULL,
  `s_pm_7_id` int(11) NULL DEFAULT NULL,
  `s_test_3_id` int(11) NULL DEFAULT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  INDEX `s_u_id`(`s_u_id`) USING BTREE,
  CONSTRAINT `student_ibfk_1` FOREIGN KEY (`s_u_id`) REFERENCES `user` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE = InnoDB AUTO_INCREMENT = 10 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_general_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of student
-- ----------------------------
INSERT INTO `student` VALUES (1, '科目三', 3, 1, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 21, 23, 25, 27, NULL, NULL);
INSERT INTO `student` VALUES (2, NULL, 13, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL);
INSERT INTO `student` VALUES (3, '科目二', 14, 1, 6, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 2);
INSERT INTO `student` VALUES (4, NULL, 15, 2, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL);
INSERT INTO `student` VALUES (5, NULL, 16, 10, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL);
INSERT INTO `student` VALUES (6, NULL, 17, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL);
INSERT INTO `student` VALUES (7, '科目二', 18, 1, 3, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL);
INSERT INTO `student` VALUES (8, '科目二', 19, NULL, 1, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL);
INSERT INTO `student` VALUES (9, '科目三', 20, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL);

-- ----------------------------
-- Table structure for teacher
-- ----------------------------
DROP TABLE IF EXISTS `teacher`;
CREATE TABLE `teacher`  (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `t_work_time` varchar(128) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL,
  `t_u_id` int(11) NULL DEFAULT NULL,
  `t_class_id` int(11) NULL DEFAULT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  INDEX `t_u_id`(`t_u_id`) USING BTREE,
  CONSTRAINT `teacher_ibfk_1` FOREIGN KEY (`t_u_id`) REFERENCES `user` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE = InnoDB AUTO_INCREMENT = 11 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_general_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of teacher
-- ----------------------------
INSERT INTO `teacher` VALUES (1, '五年', 2, NULL);
INSERT INTO `teacher` VALUES (2, '二十年', 4, NULL);
INSERT INTO `teacher` VALUES (3, '十年', 5, NULL);
INSERT INTO `teacher` VALUES (4, '八年', 6, NULL);
INSERT INTO `teacher` VALUES (5, '十五年', 7, NULL);
INSERT INTO `teacher` VALUES (6, '30年', 8, NULL);
INSERT INTO `teacher` VALUES (8, '八年', 10, NULL);
INSERT INTO `teacher` VALUES (9, '二十一年', 11, NULL);
INSERT INTO `teacher` VALUES (10, '六年', 12, NULL);

-- ----------------------------
-- Table structure for test
-- ----------------------------
DROP TABLE IF EXISTS `test`;
CREATE TABLE `test`  (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `test_subject` varchar(128) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL,
  `test_time` date NULL DEFAULT NULL,
  `sign_start_time` date NULL DEFAULT NULL,
  `sign_end_time` date NULL DEFAULT NULL,
  `sign_number` int(11) NULL DEFAULT NULL,
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 8 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_general_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of test
-- ----------------------------
INSERT INTO `test` VALUES (1, '科目二', '2018-02-27', '2018-02-13', '2018-02-20', 1);
INSERT INTO `test` VALUES (2, '科目三', '2018-02-28', '2018-02-14', '2018-02-27', 1);
INSERT INTO `test` VALUES (3, '科目二', '2018-02-26', '2018-02-14', '2018-02-19', 1);
INSERT INTO `test` VALUES (4, '科目二', '2018-03-06', '2018-02-21', '2018-02-28', 0);
INSERT INTO `test` VALUES (5, '科目二', '2018-02-28', '2018-02-22', '2018-02-27', 0);
INSERT INTO `test` VALUES (6, '科目二', '2018-02-21', '2018-02-18', '2018-02-19', 1);
INSERT INTO `test` VALUES (7, '科目三', '2018-02-21', '2018-02-18', '2018-02-19', 0);

-- ----------------------------
-- Table structure for user
-- ----------------------------
DROP TABLE IF EXISTS `user`;
CREATE TABLE `user`  (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `user_number` varchar(64) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL,
  `username` varchar(64) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `password` varchar(128) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `salt` varchar(128) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL,
  `phone` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL,
  `email` varchar(60) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL,
  `real_name` varchar(60) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL,
  `t_gender` varchar(60) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL,
  `identity_number` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL,
  `active` tinyint(1) NULL DEFAULT NULL,
  `confirmed_at` datetime(0) NULL DEFAULT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  UNIQUE INDEX `username`(`username`) USING BTREE,
  UNIQUE INDEX `identity_number`(`identity_number`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 21 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_general_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of user
-- ----------------------------
INSERT INTO `user` VALUES (1, '21232f297a57a5a743894a0e4a801fc3', 'admin', 'e30aa1a9511f916f64784892f7a0120d', '849a9e4d8305f41990c86943f4d39303', NULL, NULL, NULL, NULL, NULL, 1, NULL);
INSERT INTO `user` VALUES (2, 'accc9105df5383111407fd5b41255e23', 'tt', '38dc6c1c81e09bde1263455c8a485889', '0221fb6996a2530122f8d0a7cf9d24f3', '15281158972', '2802607350@qq.com', '吴亦凡', '男', '522556988456998741', 1, NULL);
INSERT INTO `user` VALUES (3, '3691308f2a4c2f6983f2880d32e29c84', 'ss', '6fb40abc2dd03341344cac6c0114cd4c', '4ac9d1bac2fa1539665cce606d248d13', '15378873457', '2802639403@qq.com', '王尼玛', '女', '677887877856332123', 1, NULL);
INSERT INTO `user` VALUES (4, '4124bc0a9335c27f086f24ba207a4912', 'aa', '6caf154240a7c6af45e53f3a88c85e32', 'f2625b8a6cf7cfd96317a34fd581a22b', '15295561485', '856214554@qq.com', '辣手摧花', '女', '566321455695632154', 1, NULL);
INSERT INTO `user` VALUES (5, '21ad0bd836b90d08f4cf640b4c298e7c', 'bb', '30412d74cdc67f05f395c8063f9a3e28', '13e8484f7dcbf4972fad634e50635a31', '15274458621', '1094724855@qq.com', '鹿晗', '男', '511421455856995417', 1, NULL);
INSERT INTO `user` VALUES (6, 'e0323a9039add2978bf5b49550572c7c', 'cc', 'd6801f2a915a862517ea1cd402e79ce2', 'ac842fb00d87ea94fe07aee6a2fa8248', '18308461797', '1524123659@qq.com', '王爱华', '女', '955663255589652156', 1, NULL);
INSERT INTO `user` VALUES (7, '1aabac6d068eef6a7bad3fdf50a05cc8', 'dd', 'b78fa5acbffb2b968fb006578393f2a0', '23cfbc3f6b9d0d035e0507439bb2f22b', '15295561485', '1524123659@qq.com', '宋美丽', '男', '388552599656556585', 1, NULL);
INSERT INTO `user` VALUES (8, '08a4415e9d594ff960030b921d42b91e', 'ee', '5fb57665d0e80691f17875b66829f792', 'c51003bcd66f6fd526d52cee10d09462', '15898845895', '854256985@qq.com', '王思聪', '女', '666332255412114874', 1, NULL);
INSERT INTO `user` VALUES (9, '633de4b0c14ca52ea2432a3c8a5c4c31', 'ff', 'd38caa1dc5afd91076c6004470a7c095', 'd9947eff39b63c4a515eebde319b464d', '15295561485', '232213424@qq.com', '张立新', '男', '855885699696556985', 1, NULL);
INSERT INTO `user` VALUES (10, '25ed1bcb423b0b7200f485fc5ff71c8e', 'zz', '6787a579820c9d7b112f5c4aa9be6399', '4d6eadb20a924d3e035b1e3fcf355e19', '18596585698', '78541254258@qq.com', '周作人', '女', '211445655412336541', 1, NULL);
INSERT INTO `user` VALUES (11, '9336ebf25087d91c818ee6e9ec29f8c1', 'xx', 'c06da35bb247594145dfd02899a83191', 'cc8a40b29614bdedf06856e63c1e0442', '18314474174', '524158962@qq.com', '刘长青', '男', '855998744565441235', 1, NULL);
INSERT INTO `user` VALUES (12, '2fb1c5cf58867b5bbc9a1b145a86f3a0', 'yy', '102a0a9da3ee7e6fa54ab1aef40efc79', '331327c132da15c2724da517d172eb03', '15284475965', '5985642154@qq.com', '梅长苏', '男', '988774566985669874', 1, NULL);
INSERT INTO `user` VALUES (13, '73c18c59a39b18382081ec00bb456d43', 'gg', '702f0f137bf8f7a81dde71719df274f3', 'df57847caf4b27bd6faa5c6ff4eb317e', '23212323432', '2802607350@qq.com', NULL, NULL, NULL, 1, NULL);
INSERT INTO `user` VALUES (14, '627fcdb6cc9a5e16d657ca6cdef0a6bb', 'st', '99108ebe5e6dec70f6e32c8049b95b4a', '35aece5bf4b2a23657666bed24c6839e', '15295561485', '2324222@qq.com', '王晓华', '男', '277889766567552340', 1, NULL);
INSERT INTO `user` VALUES (15, '099b3b060154898840f0ebdfb46ec78f', 'qq', '8ac268f95d9790b9530ceeb0d1c227b0', '8e8f23646fd5a242e6da935bc4390f89', '12345678901', '2802607350@qq.com', NULL, NULL, NULL, 1, NULL);
INSERT INTO `user` VALUES (16, 'd861877da56b8b4ceb35c8cbfdf65bb4', 'big', '32114b97b4851413511bb880afba3cf6', '978517ddb8cd93b2955be85871734827', '15281158972', '2802607350@qq.com', NULL, NULL, NULL, 1, NULL);
INSERT INTO `user` VALUES (17, 'eb5c1399a871211c7e7ed732d15e3a8b', 'small', 'cfd7fcf11beac8c9cbfda26b84bb06ff', 'bd601d0de98dab37b235f53c55bd6b9c', '15281158972', '2802607350@qq.com', NULL, NULL, NULL, 1, NULL);
INSERT INTO `user` VALUES (18, '4e4d6c332b6fe62a63afe56171fd3725', 'haha', '5495fe4030ad6aea1c197cefa2821d02', 'cc9d61f70b30133f7ca02f31793ae978', '15281158972', '2321124@qq.com', '王美丽', '女', '277889766567552322', 1, NULL);
INSERT INTO `user` VALUES (19, 'a3aca2964e72000eea4c56cb341002a4', 'hhh', '091d51cb288e47afe7950ecffc34d941', 'e588e25d3ffb2f054b5228f34e9f5840', '15281158972', '23222224@qq.com', '王晓峰', '男', '277889766567512342', 1, NULL);
INSERT INTO `user` VALUES (20, '22af645d1859cb5ca6da0c484f1f37ea', 'new', 'ece0f37c6515e5fa84c66a308bf84662', '0ff6afcd325f073787b874bb1b1bbf10', '15274458621', '2321114@qq.com', '张新爱', '男', '277889766567552348', 1, NULL);

SET FOREIGN_KEY_CHECKS = 1;
