-- MySQL dump 10.13  Distrib 8.0.36, for Win64 (x86_64)
--
-- Host: 127.0.0.1    Database: nba_search
-- ------------------------------------------------------
-- Server version	8.0.37

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `comments`
--

DROP TABLE IF EXISTS `comments`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `comments` (
  `commentId` int NOT NULL AUTO_INCREMENT,
  `postId` int NOT NULL,
  `userId` int NOT NULL,
  `content` longtext NOT NULL,
  `createdAt` datetime NOT NULL,
  `upvote` int(10) unsigned zerofill NOT NULL,
  PRIMARY KEY (`commentId`),
  UNIQUE KEY `commentId_UNIQUE` (`commentId`),
  KEY `fk_comments_user_id` (`userId`),
  KEY `fk_comments_post_id` (`postId`),
  CONSTRAINT `fk_comments_post_id` FOREIGN KEY (`postId`) REFERENCES `posts` (`postId`),
  CONSTRAINT `fk_comments_user_id` FOREIGN KEY (`userId`) REFERENCES `user` (`userId`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `comments`
--

LOCK TABLES `comments` WRITE;
/*!40000 ALTER TABLE `comments` DISABLE KEYS */;
INSERT INTO `comments` VALUES (1,1,1,'xin chao','2025-04-27 14:57:44',0000000001),(2,1,2,'abc','2025-04-27 20:39:28',0000000001);
/*!40000 ALTER TABLE `comments` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `posts`
--

DROP TABLE IF EXISTS `posts`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `posts` (
  `postId` int NOT NULL AUTO_INCREMENT,
  `userId` int NOT NULL,
  `title` varchar(255) NOT NULL,
  `content` longtext NOT NULL,
  `createdAt` datetime NOT NULL,
  
  PRIMARY KEY (`postId`),
  UNIQUE KEY `postId_UNIQUE` (`postId`),
  KEY `fk_user_id` (`userId`),
  CONSTRAINT `fk_user_id` FOREIGN KEY (`userId`) REFERENCES `user` (`userId`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `posts`
--

LOCK TABLES `posts` WRITE;
/*!40000 ALTER TABLE `posts` DISABLE KEYS */;
INSERT INTO `posts` VALUES (1,1,'TITLE','Hello xin chao tat ca anh em, chao mung anh em da den voi channel Tung Vlog.','2025-04-20 16:27:26');
/*!40000 ALTER TABLE `posts` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `images`
--

DROP TABLE IF EXISTS `images`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;

CREATE TABLE `images` (
  `imageId` int NOT NULL AUTO_INCREMENT,
  `postId` int NOT NULL,
  `imagePath` varchar(255) NOT NULL,
  `uploadedAt` datetime NOT NULL,
  
  PRIMARY KEY (`imageId`),
  UNIQUE KEY `imageId_UNIQUE` (`imageId`),
  KEY `fk_post_id` (`postId`),
  CONSTRAINT `fk_post_id` FOREIGN KEY (`postId`) REFERENCES `posts` (`postId`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3;

/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `upvotes`
--

DROP TABLE IF EXISTS `upvotes`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `upvotes` (
  `upvoteId` int NOT NULL AUTO_INCREMENT,
  `commentId` int NOT NULL,
  `userId` int NOT NULL,
  PRIMARY KEY (`upvoteId`),
  UNIQUE KEY `upvoteId_UNIQUE` (`upvoteId`),
  KEY `fk_upvotes_post_id` (`commentId`),
  KEY `fk_upvotes_user_id` (`userId`),
  CONSTRAINT `fk_upvotes_post_id` FOREIGN KEY (`commentId`) REFERENCES `comments` (`commentId`),
  CONSTRAINT `fk_upvotes_user_id` FOREIGN KEY (`userId`) REFERENCES `user` (`userId`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `upvotes`
--

LOCK TABLES `upvotes` WRITE;
/*!40000 ALTER TABLE `upvotes` DISABLE KEYS */;
/*!40000 ALTER TABLE `upvotes` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `user`
--

DROP TABLE IF EXISTS `user`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `user` (
  `userId` int NOT NULL AUTO_INCREMENT,
  `username` varchar(255) NOT NULL,
  `password` varchar(255) NOT NULL,
  `email` varchar(255) NOT NULL,
  `name` varchar(255) NOT NULL,
  PRIMARY KEY (`userId`),
  UNIQUE KEY `userId_UNIQUE` (`userId`),
  UNIQUE KEY `username_UNIQUE` (`username`)
) ENGINE=InnoDB AUTO_INCREMENT=9 DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `user`
--

LOCK TABLES `user` WRITE;
/*!40000 ALTER TABLE `user` DISABLE KEYS */;
INSERT INTO `user` VALUES (1,'hello','scrypt:32768:8:1$IJ8mO53dZ5EhnO1g$97e2c1bd21fbb9afc6418f08841815a872aecfc28c92e4b8f1b2f8235a43dd265c112f9ed322323ed3697866a736ed5839ce2cca60670694fba082a1441f7ba0','hihi123@gmail.com','tung'),(2,'world','scrypt:32768:8:1$LPWIyHlpHbrOOtxI$5d5003ff3765dbd50a5fcf7c00e52a0716bfb52bf47b6fd47ebfa8365cade2b8f4c72efa8460ef1694c247d54f6048938e262c2513bf1bfd95935b55c9b9c549','hihi123@gmail.com','tung'),(3,'hihi','scrypt:32768:8:1$8y8Bqngj5rf3QnRf$6d25c5ae4f3f0da7ec2befbca790f2a95640df97b6bb006ee4ac6897d44fd1a0217be930c6a86f7fec5faa7913d305686892ec44ea52b3142478366c9da02f09','hihi123@gmail.com','tung'),(6,'hihihi','scrypt:32768:8:1$KAyCL4xWEVDSMnhH$d57f2702446f8a13ef4232a5843769565c30d6ca3a9daeac25f7752cd40fac07d30558228bd873f0719f831c83666ff7e33699e34f2dae29891b83e604432986','email','name'),(7,'hihihihi','scrypt:32768:8:1$MDPAD2F2d3UShorO$4f392cbc83db886f231de5b6dafb762c638f16b41dc6dc1e0cd0535a4e1d5ac2fb28a1ddb8278f1439f93a1647752197322b5cedaf971da3f54f135f718b0ae0','mail','ten'),(8,'abcaba','scrypt:32768:8:1$5xQVJEn3oIOQdF6G$3a2cffdd00004717290a875ae209231a9a22d261748918a3b95103a64b573c705dc7e00ad81a9bed019fbaa9f3b968f4a547d91f6497e702341c62308140d36a','tung@gmail.com','tung');
/*!40000 ALTER TABLE `user` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2025-05-04 18:43:03
