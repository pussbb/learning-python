SET SQL_MODE="NO_AUTO_VALUE_ON_ZERO";
SET time_zone = "+00:00";

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;


CREATE TABLE IF NOT EXISTS `access_rules` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `role_id` int(11) DEFAULT NULL,
  `directory` varchar(255) DEFAULT NULL,
  `controller` varchar(255) DEFAULT NULL,
  `action` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB  DEFAULT CHARSET=utf8 AUTO_INCREMENT=11 ;

INSERT INTO `access_rules` (`id`, `role_id`, `directory`, `controller`, `action`) VALUES
(5, 0, NULL, 'users', 'login'),
(6, 0, NULL, 'users', 'register'),
(7, 1, NULL, 'users', 'logout'),
(8, 1, NULL, 'users', 'account_info'),
(9, 1, NULL, 'users', 'settings'),
(10, 2, 'admin', '*', '*');

CREATE TABLE IF NOT EXISTS `blog_categories` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(255) NOT NULL,
  `description` text NOT NULL,
  `parent_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB  DEFAULT CHARSET=utf8 AUTO_INCREMENT=10 ;

INSERT INTO `blog_categories` (`id`, `name`, `description`, `parent_id`) VALUES
(1, 'asfsf', 'sdfsdfsdf', NULL),
(4, 'dfsd', 'fsdfsdf', NULL),
(5, 'weewr', 'erwer', NULL),
(6, 'sdfsdfsd', 'sdfdf', 4),
(9, 'sreb ere jjjj', 'sdfdf  ere', 4);

CREATE TABLE IF NOT EXISTS `blog_posts` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `created_at` datetime DEFAULT NULL,
  `author_id` int(11) NOT NULL,
  `uri` varchar(255) NOT NULL,
  `category_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `fk_blog_posts_user` (`author_id`),
  KEY `fk_blog_posts_cat` (`category_id`)
) ENGINE=InnoDB  DEFAULT CHARSET=utf8 AUTO_INCREMENT=40 ;

INSERT INTO `blog_posts` (`id`, `created_at`, `author_id`, `uri`, `category_id`) VALUES
(39, '2013-02-16 07:02:38', 2, 'fdsfsdf', 1);

CREATE TABLE IF NOT EXISTS `blog_post_comments` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `post_id` int(11) NOT NULL,
  `content` text NOT NULL,
  `author_id` int(11) NOT NULL,
  `created_at` datetime DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `fk_blog_post_comments_post` (`post_id`),
  KEY `fk_blog_post_comments_authorid` (`author_id`)
) ENGINE=InnoDB  DEFAULT CHARSET=utf8 AUTO_INCREMENT=4 ;

INSERT INTO `blog_post_comments` (`id`, `post_id`, `content`, `author_id`, `created_at`) VALUES
(1, 39, 'fgdfgdfgdf', 1, '2013-02-16 07:02:03'),
(2, 39, 'gdfgdfgd', 1, '2013-02-16 07:02:05'),
(3, 39, 'dgdfgdfg', 1, '2013-02-16 07:02:07');

CREATE TABLE IF NOT EXISTS `blog_post_contents` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `language_id` int(11) NOT NULL,
  `brief` text NOT NULL,
  `content` text NOT NULL,
  `post_id` int(11) NOT NULL,
  `title` varchar(255) NOT NULL,
  `keywords` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `fk_blog_post_contents_language_id` (`language_id`),
  KEY `fk_blog_post_contents_post_id` (`post_id`)
) ENGINE=InnoDB  DEFAULT CHARSET=utf8 AUTO_INCREMENT=35 ;

INSERT INTO `blog_post_contents` (`id`, `language_id`, `brief`, `content`, `post_id`, `title`, `keywords`) VALUES
(34, 1, '<p>sdfsdfsdf</p>\r\n', '<p>sdfsdfsdf</p>\r\n', 39, 'dfsdfsdf', NULL);

CREATE TABLE IF NOT EXISTS `languages` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `code` varchar(3) CHARACTER SET latin1 NOT NULL,
  `locale` varchar(5) CHARACTER SET latin1 NOT NULL,
  `name` varchar(200) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB  DEFAULT CHARSET=utf8 AUTO_INCREMENT=3 ;

INSERT INTO `languages` (`id`, `code`, `locale`, `name`) VALUES
(1, 'en', 'en-EN', 'English'),
(2, 'ru', 'ru-RU', 'Русский');

CREATE TABLE IF NOT EXISTS `news` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `title` varchar(255) NOT NULL,
  `link` varchar(255) DEFAULT NULL,
  `author_id` bigint(20) NOT NULL,
  `content` text NOT NULL,
  `created_at` datetime NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB  DEFAULT CHARSET=utf8 AUTO_INCREMENT=8 ;

INSERT INTO `news` (`id`, `title`, `link`, `author_id`, `content`, `created_at`) VALUES
(2, 'fdgdf tt', NULL, 1, '<p>dfsdf dfgfdg</p>\r\n', '2013-01-20 06:01:42'),
(3, 'rtretertertertertertret', NULL, 1, '<p>ater this shield staggered up on tripod legs and became the first of the fighting-machines I had seen. The gun he drove had been unlimbered near Horsell, in order to command the sand pits, and its arrival it was that had precipitated the action. As the limber gunners went to the rear, his horse trod in a rabbit hole and came down, throwing him into a depression of the ground. At the same moment the gun exploded behind him.</p>\r\n\r\n<p>The old man peered from under his green leaf at the danger, and stood as quietly as the boy. For a few seconds this mutual scrutinizing went on; then, the bear betraying a growing irritability, the boy, with a movement of his head, indicated that the old man must step aside from the trail and go down the embankment. The boy followed, going backward, still holding the bow taut and ready. They waited till a crashing among the bushes from the opposite side of the embankment told them the bear had gone on. The boy grinned as he led back to the trail.</p>\r\n\r\n<p>ater this shield staggered up on tripod legs and became the first of the fighting-machines I had seen. The gun he drove had been unlimbered near Horsell, in order to command the sand pits, and its arrival it was that had precipitated the action. As the limber gunners went to the rear, his horse trod in a rabbit hole and came down, throwing him into a depression of the ground. At the same moment the gun exploded behind him.</p>\r\n\r\n<p>The old man peered from under his green leaf at the danger, and stood as quietly as the boy. For a few seconds this mutual scrutinizing went on; then, the bear betraying a growing irritability, the boy, with a movement of his head, indicated that the old man must step aside from the trail and go down the embankment. The boy followed, going backward, still holding the bow taut and ready. They waited till a crashing among the bushes from the opposite side of the embankment told them the bear had gone on. The boy grinned as he led back to the trail.</p>\r\n\r\n<p>ater this shield staggered up on tripod legs and became the first of the fighting-machines I had seen. The gun he drove had been unlimbered near Horsell, in order to command the sand pits, and its arrival it was that had precipitated the action. As the limber gunners went to the rear, his horse trod in a rabbit hole and came down, throwing him into a depression of the ground. At the same moment the gun exploded behind him.</p>\r\n\r\n<p>The old man peered from under his green leaf at the danger, and stood as quietly as the boy. For a few seconds this mutual scrutinizing went on; then, the bear betraying a growing irritability, the boy, with a movement of his head, indicated that the old man must step aside from the trail and go down the embankment. The boy followed, going backward, still holding the bow taut and ready. They waited till a crashing among the bushes from the opposite side of the embankment told them the bear had gone on. The boy grinned as he led back to the trail.</p>\r\n\r\n<div id="cke_pastebin" style="position: absolute; top: -343px; width: 1px; height: 625px; overflow: hidden; margin: 0px; padding: 0px; left: -1000px;">ater this shield staggered up on tripod legs and became the first of the fighting-machines I had seen. The gun he drove had been unlimbered near Horsell, in order to command the sand pits, and its arrival it was that had precipitated the action. As the limber gunners went to the rear, his horse trod in a rabbit hole and came down, throwing him into a depression of the ground. At the same moment the gun exploded behind him.</div>\r\n\r\n<div id="cke_pastebin" style="position: absolute; top: -343px; width: 1px; height: 625px; overflow: hidden; margin: 0px; padding: 0px; left: -1000px;">&nbsp;</div>\r\n\r\n<div id="cke_pastebin" style="position: absolute; top: -343px; width: 1px; height: 625px; overflow: hidden; margin: 0px; padding: 0px; left: -1000px;">The old man peered from under his green leaf at the danger, and stood as quietly as the boy. For a few seconds this mutual scrutinizing went on; then, the bear betraying a growing irritability, the boy, with a movement of his head, indicated that the old man must step aside from the trail and go down the embankment. The boy followed, going backward, still holding the bow taut and ready. They waited till a crashing among the bushes from the opposite side of the embankment told them the bear had gone on. The boy grinned as he led back to the trail.</div>\r\n', '2013-01-20 12:01:56'),
(4, 'drdsfdsfsdf', NULL, 1, '<p>sdfsdfsdfsdfsdf</p>\r\n', '2013-01-26 03:01:44'),
(7, 'dfdsf', 'dsfsdfsdf', 1, '<p>sdfsdfsdfsdf</p>\r\n', '2013-02-16 04:02:37');

CREATE TABLE IF NOT EXISTS `users` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `role_id` int(11) NOT NULL DEFAULT '1' COMMENT 'role id',
  `email` text NOT NULL,
  `login` text NOT NULL,
  `password` text NOT NULL,
  `api_key` text NOT NULL,
  `meta_data` text NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB  DEFAULT CHARSET=utf8 AUTO_INCREMENT=21 ;

INSERT INTO `users` (`id`, `role_id`, `email`, `login`, `password`, `api_key`, `meta_data`) VALUES
(1, 2, 'pussbb@gmail.com', 'pussbb', 'e10adc3949ba59abbe56e057f20f883e', '50e716241eaca', '[]'),
(2, 1, '_pussbb@mail.ru', '_pussbb', '25d55ad283aa400af464c76d713c07ad', '511f61536a380', '[]'),
(3, 2, 'tytyt@hgghg.com', 'fdsfsdfsdf', 'e10adc3949ba59abbe56e057f20f883e', '88ec6b44e63311e29fbddc85de55a275', '[]'),
(18, 2, 'tytyt@hgghg.com', 'fdsfsdfsdf', 'cfe95b64ac715d64275365ede690ee7c', 'cc9e9bb6e6db11e2bfd8dc85de55a275', '[]'),
(19, 2, 'tytyt@hgghg.com', 'fdsfsdfsdf', 'cfe95b64ac715d64275365ede690ee7c', '0931fcfce6e211e2aa1cdc85de55a275', '[]'),
(20, 2, 'tytyt@hgghg.com', 'fdsfsdfsdf', 'cfe95b64ac715d64275365ede690ee7c', 'cb5d72eae73011e2878ddc85de55a275', '[]');


ALTER TABLE `blog_posts`
  ADD CONSTRAINT `fk_blog_posts_cat` FOREIGN KEY (`category_id`) REFERENCES `blog_categories` (`id`) ON DELETE CASCADE ON UPDATE CASCADE,
  ADD CONSTRAINT `fk_blog_posts_user` FOREIGN KEY (`author_id`) REFERENCES `users` (`id`) ON DELETE CASCADE ON UPDATE CASCADE;

ALTER TABLE `blog_post_comments`
  ADD CONSTRAINT `fk_blog_post_comments_author_id` FOREIGN KEY (`author_id`) REFERENCES `users` (`id`) ON DELETE CASCADE ON UPDATE CASCADE,
  ADD CONSTRAINT `fk_blog_post_comments_post_id` FOREIGN KEY (`post_id`) REFERENCES `blog_posts` (`id`) ON DELETE CASCADE ON UPDATE CASCADE;

ALTER TABLE `blog_post_contents`
  ADD CONSTRAINT `fk_blog_post_contents_language_id` FOREIGN KEY (`language_id`) REFERENCES `languages` (`id`) ON DELETE CASCADE ON UPDATE CASCADE,
  ADD CONSTRAINT `fk_blog_post_contents_post_id` FOREIGN KEY (`post_id`) REFERENCES `blog_posts` (`id`) ON DELETE CASCADE ON UPDATE CASCADE;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
